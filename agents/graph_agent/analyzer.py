"""
analyzer.py — Graph analysis algorithms using NetworkX.

Implements structural analyses on the in-memory graph:
- Connected component detection
- Repeated entity detection (shared phones, devices, UPIs, URLs, accounts, identities)
- Degree centrality computation
- Suspicious cluster (fraud ring) detection
- Network risk score estimation
"""

from __future__ import annotations

import networkx as nx
from typing import Any, Dict, List, Set, Tuple
from .logging import get_logger
from .model import get_global_graph
from .schemas import (
    EntityType,
    GraphEvidence,
    SharedEntityFinding,
    SuspiciousCluster,
)

log = get_logger()


def run_graph_analysis(case_id: str) -> GraphEvidence:
    """Analyze the global graph partition relevant to the current case_id."""
    model = get_global_graph()
    G_multi = model.G
    G_simple = model.get_undirected_simple_graph()

    num_nodes = G_simple.number_of_nodes()
    num_edges = G_simple.number_of_edges()

    # 1. Connected components detection
    components_list = [list(c) for c in nx.connected_components(G_simple)]

    # Filter components to only those containing nodes associated with the current case
    case_components: List[List[str]] = []
    for comp in components_list:
        # Check if any node in component has this case_id in its properties or case_ids set
        involved = False
        for node in comp:
            node_data = G_multi.nodes[node]
            if case_id in node_data.get("case_ids", set()) or node_data.get("properties", {}).get("case_id") == case_id:
                involved = True
                break
        if involved:
            case_components.append(comp)

    # 2. Repeated entity detection (general map)
    repeated_entities: Dict[str, List[str]] = {}
    for node, data in G_multi.nodes(data=True):
        node_cases = list(data.get("case_ids", set()))
        if len(node_cases) > 1:
            repeated_entities[node] = node_cases

    # 3. Specific shared entity detections
    shared_phones = _detect_shared_entities_by_type(G_multi, EntityType.PHONE)
    shared_urls = _detect_shared_entities_by_type(G_multi, EntityType.URL)
    shared_upis = _detect_shared_entities_by_type(G_multi, EntityType.UPI)
    shared_accounts = _detect_shared_entities_by_type(G_multi, EntityType.BANK_ACCOUNT)
    shared_devices = _detect_shared_entities_by_type(G_multi, EntityType.DEVICE)
    
    # 4. Repeated identities (Victims or Suspects appearing in multiple cases)
    repeated_victims = _detect_shared_entities_by_type(G_multi, EntityType.VICTIM)
    repeated_suspects = _detect_shared_entities_by_type(G_multi, EntityType.SUSPECT)
    repeated_identities = repeated_victims + repeated_suspects

    # 5. Degree centrality computation (only top centralities in the relevant components)
    degree_centrality: Dict[str, float] = {}
    if num_nodes > 0:
        full_centrality = nx.degree_centrality(G_simple)
        # Filter to nodes in case components
        nodes_in_case_comp = {node for comp in case_components for node in comp}
        # Sort and take top 10
        sorted_centrality = sorted(
            [(node, val) for node, val in full_centrality.items() if node in nodes_in_case_comp],
            key=lambda x: x[1],
            reverse=True
        )[:10]
        degree_centrality = {node: round(val, 4) for node, val in sorted_centrality}

    # 6. Suspicious cluster detection (fraud rings)
    suspicious_clusters = _detect_suspicious_clusters(G_multi, case_components)

    # 7. Network risk score estimation
    risk_score = _estimate_network_risk(
        case_id=case_id,
        case_components=case_components,
        shared_phones=shared_phones,
        shared_devices=shared_devices,
        shared_upis=shared_upis,
        shared_accounts=shared_accounts,
        repeated_suspects=repeated_suspects,
        degree_centrality=degree_centrality
    )

    log.info(
        "[case_id=%s] Analysis complete. Nodes: %d, Edges: %d, Risk Score: %.1f",
        case_id,
        num_nodes,
        num_edges,
        risk_score
    )

    return GraphEvidence(
        num_nodes=num_nodes,
        num_edges=num_edges,
        connected_components=case_components,
        repeated_entities=repeated_entities,
        shared_phones=shared_phones,
        shared_urls=shared_urls,
        shared_upis=shared_upis,
        shared_accounts=shared_accounts,
        shared_devices=shared_devices,
        repeated_identities=repeated_identities,
        degree_centrality=degree_centrality,
        suspicious_clusters=suspicious_clusters,
        network_risk_score=risk_score
    )


def _detect_shared_entities_by_type(G: nx.MultiDiGraph, entity_type: EntityType) -> List[SharedEntityFinding]:
    """Helper to detect entities of a specific type that are linked to multiple cases, victims, or suspects."""
    findings = []
    for node, data in G.nodes(data=True):
        if data.get("type") != entity_type.value:
            continue
        
        node_cases = list(data.get("case_ids", set()))
        if len(node_cases) <= 1:
            continue

        # Trace neighbors to find linked victims and suspects
        connected_victims: Set[str] = set()
        connected_suspects: Set[str] = set()
        
        # Traverse neighbors in undirected view
        for neighbor in G.predecessors(node):
            neigh_type = G.nodes[neighbor].get("type")
            if neigh_type == EntityType.VICTIM.value:
                connected_victims.add(neighbor)
            elif neigh_type == EntityType.SUSPECT.value:
                connected_suspects.add(neighbor)
                
        for neighbor in G.successors(node):
            neigh_type = G.nodes[neighbor].get("type")
            if neigh_type == EntityType.VICTIM.value:
                connected_victims.add(neighbor)
            elif neigh_type == EntityType.SUSPECT.value:
                connected_suspects.add(neighbor)

        findings.append(
            SharedEntityFinding(
                entity_type=entity_type.value,
                entity_id=node,
                connected_cases=node_cases,
                connected_victims=list(connected_victims),
                connected_suspects=list(connected_suspects)
            )
        )
    return findings


def _detect_suspicious_clusters(G: nx.MultiDiGraph, case_components: List[List[str]]) -> List[SuspiciousCluster]:
    """Identify clusters (connected components) that present signs of organized crime or fraud rings."""
    clusters = []
    for idx, comp in enumerate(case_components):
        node_count = len(comp)
        if node_count < 3:
            # Too small to be an organized ring
            continue

        # Count suspects, victims, and unique cases in this component
        case_ids: Set[str] = set()
        suspects: Set[str] = set()
        victims: Set[str] = set()

        for node in comp:
            node_data = G.nodes[node]
            node_type = node_data.get("type")
            
            case_ids.update(node_data.get("case_ids", set()))
            if "case_id" in node_data.get("properties", {}):
                case_ids.add(node_data["properties"]["case_id"])
                
            if node_type == EntityType.SUSPECT.value:
                suspects.add(node)
            elif node_type == EntityType.VICTIM.value:
                victims.add(node)

        suspect_count = len(suspects)
        victim_count = len(victims)
        unique_cases_count = len(case_ids)

        # Suspicious threshold: multiple cases involved, or a suspect exists with multiple victims
        if unique_cases_count > 1 or suspect_count > 0:
            if suspect_count > 0 and unique_cases_count > 1:
                risk_level = "high"
            elif unique_cases_count > 1 or suspect_count > 0 or node_count > 6:
                risk_level = "medium"
            else:
                risk_level = "low"

            clusters.append(
                SuspiciousCluster(
                    cluster_id=idx + 1,
                    nodes=comp,
                    node_count=node_count,
                    case_ids=list(case_ids),
                    suspect_count=suspect_count,
                    victim_count=victim_count,
                    risk_level=risk_level
                )
            )
    return clusters


def _estimate_network_risk(
    case_id: str,
    case_components: List[List[str]],
    shared_phones: List[SharedEntityFinding],
    shared_devices: List[SharedEntityFinding],
    shared_upis: List[SharedEntityFinding],
    shared_accounts: List[SharedEntityFinding],
    repeated_suspects: List[SharedEntityFinding],
    degree_centrality: Dict[str, float]
) -> float:
    """Calculate an overall network risk score in [0.0, 100.0] based on connectivity features."""
    risk = 0.0

    # 1. Base component size risk
    max_comp_size = max([len(c) for c in case_components]) if case_components else 0
    if max_comp_size > 8:
        risk += 15
    elif max_comp_size > 4:
        risk += 10
    elif max_comp_size >= 3:
        risk += 5

    # 2. Risk from shared phone numbers (indicates cross-case link)
    # Check if any shared phone is connected to current case_id
    shared_phone_count = sum(1 for f in shared_phones if case_id in f.connected_cases)
    risk += min(shared_phone_count * 20, 40)

    # 3. Risk from shared devices / UPI / bank accounts
    shared_device_count = sum(1 for f in shared_devices if case_id in f.connected_cases)
    shared_upi_count = sum(1 for f in shared_upis if case_id in f.connected_cases)
    shared_account_count = sum(1 for f in shared_accounts if case_id in f.connected_cases)
    
    risk += min(shared_device_count * 20, 40)
    risk += min(shared_upi_count * 20, 40)
    risk += min(shared_account_count * 20, 40)

    # 4. Repeated suspect involvement
    shared_suspect_count = sum(1 for f in repeated_suspects if case_id in f.connected_cases)
    if shared_suspect_count > 0:
        risk += 30

    # 5. Degree centrality modifier (presence of highly connected hub node)
    max_degree = max(degree_centrality.values()) if degree_centrality else 0.0
    if max_degree > 0.4:
        risk += 15
    elif max_degree > 0.2:
        risk += 10

    # Clamp the risk score to [0.0, 100.0]
    return min(max(risk, 0.0), 100.0)
