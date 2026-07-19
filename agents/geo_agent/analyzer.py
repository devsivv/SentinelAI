"""
analyzer.py — Analytical core of the Geo Agent.

Implements calculations for density, regional aggregation, hotspots, clustering,
and heuristic patrol recommendations.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Any, Dict, List, Tuple
from .config import settings
from .schemas import Hotspot, IncidentCluster, PatrolRecommendation


def calculate_crime_density(incidents_count: int, radius_km: float) -> float:
    """Calculate the crime density in incidents per square kilometer."""
    if radius_km <= 0.0:
        return 0.0
    area = math.pi * (radius_km ** 2)
    return round(incidents_count / area, 6)


def aggregate_by_region(incidents: List[Dict[str, Any]]) -> Tuple[Dict[str, int], Dict[str, int]]:
    """Aggregate total incidents count by district and state."""
    district_counts: Dict[str, int] = {}
    state_counts: Dict[str, int] = {}
    
    for inc in incidents:
        dist = inc["district"]
        st = inc["state"]
        district_counts[dist] = district_counts.get(dist, 0) + 1
        state_counts[st] = state_counts.get(st, 0) + 1
        
    return district_counts, state_counts


def detect_hotspots(
    center_lat: float, center_lon: float, nearby_incidents: List[Dict[str, Any]], radius_km: float
) -> List[Hotspot]:
    """Detect if the queried area constitutes a crime hotspot based on incident density."""
    count = len(nearby_incidents)
    threshold = settings.hotspot_threshold_cases

    if count >= threshold:
        if count >= 5:
            risk = "high"
        elif count >= 3:
            risk = "medium"
        else:
            risk = "low"
            
        return [
            Hotspot(
                center_latitude=round(center_lat, 6),
                center_longitude=round(center_lon, 6),
                incident_count=count,
                radius_km=radius_km,
                risk_level=risk
            )
        ]
    return []


def cluster_incidents(
    incidents: List[Dict[str, Any]], max_cluster_dist_km: float = 3.0
) -> List[IncidentCluster]:
    """Group nearby incidents spatially using a simple Leader/Radius clustering heuristic."""
    if not incidents:
        return []

    # Format: list of dicts representing clusters:
    # {"center": (lat, lon), "incidents": [inc_dict1, ...]}
    clusters_data: List[Dict[str, Any]] = []

    for inc in incidents:
        lat = inc["latitude"]
        lon = inc["longitude"]
        
        # Try to find a cluster within max_cluster_dist_km
        assigned = False
        for c in clusters_data:
            c_lat, c_lon = c["center"]
            # Simple Haversine calculation inline
            from .mapper import haversine_distance
            dist = haversine_distance(lat, lon, c_lat, c_lon)
            if dist <= max_cluster_dist_km:
                c["incidents"].append(inc)
                # Recalculate centroid center
                all_lats = [x["latitude"] for x in c["incidents"]]
                all_lons = [x["longitude"] for x in c["incidents"]]
                c["center"] = (sum(all_lats) / len(all_lats), sum(all_lons) / len(all_lons))
                assigned = True
                break
                
        if not assigned:
            clusters_data.append({
                "center": (lat, lon),
                "incidents": [inc]
            })

    result_clusters = []
    for idx, c in enumerate(clusters_data):
        c_lat, c_lon = c["center"]
        inc_list = c["incidents"]
        node_count = len(inc_list)
        inc_ids = [x["id"] for x in inc_list]
        
        # Most common crime category in this cluster
        categories = [x["category"] for x in inc_list]
        typical_cat = Counter(categories).most_common(1)[0][0] if categories else "unknown"
        
        result_clusters.append(
            IncidentCluster(
                cluster_id=idx + 1,
                center_latitude=round(c_lat, 6),
                center_longitude=round(c_lon, 6),
                node_count=node_count,
                incidents=inc_ids,
                typical_category=typical_cat
            )
        )
        
    return result_clusters


def recommend_patrols(nearby_incidents: List[Dict[str, Any]], risk_score: int) -> PatrolRecommendation:
    """Heuristic planning of patrol priority, frequency, and hubs based on density analysis."""
    count = len(nearby_incidents)
    
    if count == 0:
        return PatrolRecommendation(
            priority="low",
            patrol_frequency="none",
            suggested_hubs=[],
            narrative="No incidents detected in the immediate vicinity. Maintain baseline observation."
        )

    # Urgent categories
    categories = [x["category"] for x in nearby_incidents]
    most_common_cats = [cat for cat, _ in Counter(categories).most_common(2)]
    
    if risk_score >= settings.risk_high_threshold:
        priority = "high"
        frequency = "hourly"
        narrative = (
            f"Critical risk level ({risk_score}/100) identified. "
            f"High density crime hotspot. Immediate hourly patrols recommended focusing on {', '.join(most_common_cats)}."
        )
    elif risk_score >= settings.risk_medium_threshold:
        priority = "medium"
        frequency = "daily"
        narrative = (
            f"Medium risk level ({risk_score}/100) identified. "
            f"Moderate density hotspot detected. Daily preventive patrols recommended focusing on {', '.join(most_common_cats)}."
        )
    else:
        priority = "low"
        frequency = "weekly"
        narrative = (
            f"Low risk level ({risk_score}/100) identified. "
            f"Weekly standard patrols suggested around hubs of type: {', '.join(most_common_cats)}."
        )

    return PatrolRecommendation(
        priority=priority,
        patrol_frequency=frequency,
        suggested_hubs=most_common_cats,
        narrative=narrative
    )
