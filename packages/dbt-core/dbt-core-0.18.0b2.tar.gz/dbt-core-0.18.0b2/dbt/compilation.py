import os
from collections import defaultdict
from typing import List, Dict, Any, Tuple, cast

import networkx as nx  # type: ignore

from dbt import flags
from dbt.clients import jinja
from dbt.clients.system import make_directory
from dbt.context.providers import generate_runtime_model
from dbt.contracts.graph.manifest import Manifest
from dbt.contracts.graph.compiled import (
    InjectedCTE,
    COMPILED_TYPES,
    NonSourceNode,
    NonSourceCompiledNode,
    CompiledSchemaTestNode,
)
from dbt.contracts.graph.parsed import ParsedNode
from dbt.exceptions import dependency_not_found, InternalException
from dbt.graph import Graph
from dbt.logger import GLOBAL_LOGGER as logger
from dbt.node_types import NodeType
from dbt.utils import add_ephemeral_model_prefix, pluralize

graph_file_name = 'graph.gpickle'


def _compiled_type_for(model: ParsedNode):
    if type(model) not in COMPILED_TYPES:
        raise InternalException(
            f'Asked to compile {type(model)} node, but it has no compiled form'
        )
    return COMPILED_TYPES[type(model)]


def print_compile_stats(stats):
    names = {
        NodeType.Model: 'model',
        NodeType.Test: 'test',
        NodeType.Snapshot: 'snapshot',
        NodeType.Analysis: 'analysis',
        NodeType.Macro: 'macro',
        NodeType.Operation: 'operation',
        NodeType.Seed: 'seed file',
        NodeType.Source: 'source',
    }

    results = {k: 0 for k in names.keys()}
    results.update(stats)

    stat_line = ", ".join([
        pluralize(ct, names.get(t)) for t, ct in results.items()
        if t in names
    ])

    logger.info("Found {}".format(stat_line))


def _node_enabled(node: NonSourceNode):
    # Disabled models are already excluded from the manifest
    if node.resource_type == NodeType.Test and not node.config.enabled:
        return False
    else:
        return True


def _generate_stats(manifest: Manifest):
    stats: Dict[NodeType, int] = defaultdict(int)
    for node in manifest.nodes.values():
        if _node_enabled(node):
            stats[node.resource_type] += 1

    for source in manifest.sources.values():
        stats[source.resource_type] += 1
    for macro in manifest.macros.values():
        stats[macro.resource_type] += 1
    return stats


def _add_prepended_cte(prepended_ctes, new_cte):
    for cte in prepended_ctes:
        if cte.id == new_cte.id:
            cte.sql = new_cte.sql
            return
    prepended_ctes.append(new_cte)


def _extend_prepended_ctes(prepended_ctes, new_prepended_ctes):
    for new_cte in new_prepended_ctes:
        _add_prepended_cte(prepended_ctes, new_cte)


class Linker:
    def __init__(self, data=None):
        if data is None:
            data = {}
        self.graph = nx.DiGraph(**data)

    def edges(self):
        return self.graph.edges()

    def nodes(self):
        return self.graph.nodes()

    def find_cycles(self):
        try:
            cycle = nx.find_cycle(self.graph)
        except nx.NetworkXNoCycle:
            return None
        else:
            # cycles is a List[Tuple[str, ...]]
            return " --> ".join(c[0] for c in cycle)

    def dependency(self, node1, node2):
        "indicate that node1 depends on node2"
        self.graph.add_node(node1)
        self.graph.add_node(node2)
        self.graph.add_edge(node2, node1)

    def add_node(self, node):
        self.graph.add_node(node)

    def write_graph(self, outfile: str, manifest: Manifest):
        """Write the graph to a gpickle file. Before doing so, serialize and
        include all nodes in their corresponding graph entries.
        """
        out_graph = self.graph.copy()
        for node_id in self.graph.nodes():
            data = manifest.expect(node_id).to_dict()
            out_graph.add_node(node_id, **data)
        nx.write_gpickle(out_graph, outfile)


class Compiler:
    def __init__(self, config):
        self.config = config

    def initialize(self):
        make_directory(self.config.target_path)
        make_directory(self.config.modules_path)

    def _create_node_context(
        self,
        node: NonSourceCompiledNode,
        manifest: Manifest,
        extra_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        context = generate_runtime_model(
            node, self.config, manifest
        )
        context.update(extra_context)
        if isinstance(node, CompiledSchemaTestNode):
            # for test nodes, add a special keyword args value to the context
            jinja.add_rendered_test_kwargs(context, node)

        return context

    def _get_compiled_model(
        self,
        manifest: Manifest,
        cte_id: str,
        extra_context: Dict[str, Any],
    ) -> NonSourceCompiledNode:

        if cte_id not in manifest.nodes:
            raise InternalException(
                f'During compilation, found a cte reference that could not be '
                f'resolved: {cte_id}'
            )
        cte_model = manifest.nodes[cte_id]
        if getattr(cte_model, 'compiled', False):
            assert isinstance(cte_model, tuple(COMPILED_TYPES.values()))
            return cast(NonSourceCompiledNode, cte_model)
        elif cte_model.is_ephemeral_model:
            # this must be some kind of parsed node that we can compile.
            # we know it's not a parsed source definition
            assert isinstance(cte_model, tuple(COMPILED_TYPES))
            # update the node so
            node = self.compile_node(cte_model, manifest, extra_context)
            manifest.sync_update_node(node)
            return node
        else:
            raise InternalException(
                f'During compilation, found an uncompiled cte that '
                f'was not an ephemeral model: {cte_id}'
            )

    def _recursively_prepend_ctes(
        self,
        model: NonSourceCompiledNode,
        manifest: Manifest,
        extra_context: Dict[str, Any],
    ) -> Tuple[NonSourceCompiledNode, List[InjectedCTE]]:
        if model.extra_ctes_injected:
            return (model, model.extra_ctes)

        if flags.STRICT_MODE:
            if not isinstance(model, tuple(COMPILED_TYPES.values())):
                raise InternalException(
                    f'Bad model type: {type(model)}'
                )

        prepended_ctes: List[InjectedCTE] = []

        for cte in model.extra_ctes:
            cte_model = self._get_compiled_model(
                manifest,
                cte.id,
                extra_context,
            )
            cte_model, new_prepended_ctes = self._recursively_prepend_ctes(
                cte_model, manifest, extra_context
            )
            _extend_prepended_ctes(prepended_ctes, new_prepended_ctes)
            new_cte_name = add_ephemeral_model_prefix(cte_model.name)
            sql = f' {new_cte_name} as (\n{cte_model.compiled_sql}\n)'
            _add_prepended_cte(prepended_ctes, InjectedCTE(id=cte.id, sql=sql))

        model.prepend_ctes(prepended_ctes)

        manifest.update_node(model)

        return model, prepended_ctes

    def compile_node(
        self, node: NonSourceNode, manifest, extra_context=None
    ) -> NonSourceCompiledNode:
        if extra_context is None:
            extra_context = {}

        logger.debug("Compiling {}".format(node.unique_id))

        data = node.to_dict()
        data.update({
            'compiled': False,
            'compiled_sql': None,
            'extra_ctes_injected': False,
            'extra_ctes': [],
            'injected_sql': None,
        })
        compiled_node = _compiled_type_for(node).from_dict(data)

        context = self._create_node_context(
            compiled_node, manifest, extra_context
        )

        compiled_node.compiled_sql = jinja.get_rendered(
            node.raw_sql,
            context,
            node)

        compiled_node.compiled = True

        injected_node, _ = self._recursively_prepend_ctes(
            compiled_node, manifest, extra_context
        )

        return injected_node

    def write_graph_file(self, linker: Linker, manifest: Manifest):
        filename = graph_file_name
        graph_path = os.path.join(self.config.target_path, filename)
        if flags.WRITE_JSON:
            linker.write_graph(graph_path, manifest)

    def link_node(
        self, linker: Linker, node: NonSourceNode, manifest: Manifest
    ):
        linker.add_node(node.unique_id)

        for dependency in node.depends_on_nodes:
            if dependency in manifest.nodes:
                linker.dependency(
                    node.unique_id,
                    (manifest.nodes[dependency].unique_id)
                )
            elif dependency in manifest.sources:
                linker.dependency(
                    node.unique_id,
                    (manifest.sources[dependency].unique_id)
                )
            else:
                dependency_not_found(node, dependency)

    def link_graph(self, linker: Linker, manifest: Manifest):
        for source in manifest.sources.values():
            linker.add_node(source.unique_id)
        for node in manifest.nodes.values():
            self.link_node(linker, node, manifest)

        cycle = linker.find_cycles()

        if cycle:
            raise RuntimeError("Found a cycle: {}".format(cycle))

    def compile(self, manifest: Manifest, write=True) -> Graph:
        linker = Linker()

        self.link_graph(linker, manifest)

        stats = _generate_stats(manifest)

        if write:
            self.write_graph_file(linker, manifest)
        print_compile_stats(stats)

        return Graph(linker.graph)


def compile_manifest(config, manifest, write=True) -> Graph:
    compiler = Compiler(config)
    compiler.initialize()
    return compiler.compile(manifest, write=write)


def _is_writable(node):
    if not node.injected_sql:
        return False

    if node.resource_type == NodeType.Snapshot:
        return False

    return True


def compile_node(adapter, config, node, manifest, extra_context, write=True):
    compiler = Compiler(config)
    node = compiler.compile_node(node, manifest, extra_context)

    if write and _is_writable(node):
        logger.debug('Writing injected SQL for node "{}"'.format(
            node.unique_id))

        node.build_path = node.write_node(
            config.target_path,
            'compiled',
            node.injected_sql
        )

    return node
