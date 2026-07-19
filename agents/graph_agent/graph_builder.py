"""
graph_builder.py — Logic to construct and populate the in-memory NetworkX graph.

Responsible for feeding normalized nodes and relationships into the global model,
ensuring appropriate tracking properties (like case IDs) are attached to each node.
"""

from __future__ import annotations

from typing import List
from .model import get_global_graph
from .schemas import Entity, Relationship


def build_case_graph(entities: List[Entity], relationships: List[Relationship], case_id: str) -> None:
    """Populate the global in-memory graph with entities and relationships associated with a case."""
    model = get_global_graph()

    # 1. Add all entities as nodes
    for entity in entities:
        props = dict(entity.properties)
        props["case_id"] = case_id
        model.add_entity_node(
            node_id=entity.id,
            node_type=entity.type.value,
            properties=props
        )

    # 2. Add all relationships as edges
    for rel in relationships:
        props = dict(rel.properties)
        props["case_id"] = case_id
        model.add_relationship_edge(
            source_id=rel.source_id,
            target_id=rel.target_id,
            rel_type=rel.type.value,
            properties=props
        )
