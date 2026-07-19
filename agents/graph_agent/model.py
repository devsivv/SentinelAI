"""
model.py — Singleton holding the global, in-memory NetworkX intelligence graph.

Ensures that all cases analyzed by the Graph Agent contribute to a shared network,
allowing correlation and detection of shared/repeated entities across distinct case records.
"""

from __future__ import annotations

import threading
import networkx as nx
from typing import Any, Dict, Set
from .logging import get_logger

log = get_logger()


class InMemoryGraphModel:
    """Singleton wrapper around the networkx MultiDiGraph."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls) -> InMemoryGraphModel:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(InMemoryGraphModel, cls).__new__(cls)
                    cls._instance.G = nx.MultiDiGraph()
                    log.info("Initialized global in-memory NetworkX intelligence graph.")
        return cls._instance

    def add_entity_node(self, node_id: str, node_type: str, properties: Dict[str, Any] | None = None) -> None:
        """Add or update a node in the graph thread-safely."""
        with self._lock:
            props = properties or {}
            if self.G.has_node(node_id):
                # Retrieve current properties and update them
                current_props = self.G.nodes[node_id]
                current_props.update(props)
                # Keep tracking case_ids if this node is linked to multiple cases
                if "case_id" in props:
                    cases: Set[str] = current_props.get("case_ids", set())
                    cases.add(props["case_id"])
                    current_props["case_ids"] = cases
            else:
                cases = set()
                if "case_id" in props:
                    cases.add(props["case_id"])
                
                self.G.add_node(
                    node_id,
                    type=node_type,
                    properties=props,
                    case_ids=cases
                )

    def add_relationship_edge(
        self,
        source_id: str,
        target_id: str,
        rel_type: str,
        properties: Dict[str, Any] | None = None
    ) -> None:
        """Add an edge representing a relationship in the graph thread-safely."""
        with self._lock:
            props = properties or {}
            # MultiDiGraph allows multiple edges between same source & target.
            # We add the edge only if it doesn't already exist with the same relationship type
            # to avoid duplicating identical edges.
            existing_edges = self.G.get_edge_data(source_id, target_id)
            if existing_edges:
                for key, data in existing_edges.items():
                    if data.get("type") == rel_type:
                        # Edge already exists, merge properties
                        data.update(props)
                        return
            
            self.G.add_edge(
                source_id,
                target_id,
                type=rel_type,
                **props
            )

    def get_undirected_simple_graph(self) -> nx.Graph:
        """Convert the MultiDiGraph to an undirected simple Graph for structural analysis.

        This is useful for algorithms like connected components, which expect undirected graphs.
        """
        with self._lock:
            # nx.Graph(MultiDiGraph) automatically collapses multiple directed edges into single undirected ones.
            return nx.Graph(self.G)

    def clear_graph(self) -> None:
        """Reset the graph to empty state (primarily used in tests)."""
        with self._lock:
            self.G.clear()
            log.info("In-memory graph cleared.")


def get_global_graph() -> InMemoryGraphModel:
    """Retrieve the singleton global graph model instance."""
    return InMemoryGraphModel()
