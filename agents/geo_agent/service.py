"""
service.py — Public service layer for the Geo Agent.

Handles coordinate validation, calculations, and aggregates the AgentResult.
"""

from __future__ import annotations

import time
from typing import List
from .config import settings
from .logging import get_logger
from .mapper import (
    get_historical_incidents,
    search_incidents_in_radius,
    validate_coordinates,
)
from .analyzer import (
    aggregate_by_region,
    calculate_crime_density,
    cluster_incidents,
    detect_hotspots,
    recommend_patrols,
)
from .schemas import (
    GeoAnalysisRequest,
    GeoAnalysisResponse,
    GeoEvidence,
    Incident,
)

log = get_logger()


async def analyze_location(request: GeoAnalysisRequest) -> GeoAnalysisResponse:
    """Validate coordinates, compute local density, detect hotspots, and generate recommendations."""
    t_start = time.perf_counter()
    case_id = request.case_id
    payload = request.payload

    log.info(
        "[case_id=%s] Starting geographical analysis for lat=%.4f, lon=%.4f.",
        case_id,
        payload.latitude,
        payload.longitude,
    )

    # 1. Coordinate range validation
    if not validate_coordinates(payload.latitude, payload.longitude):
        log.warning(
            "[case_id=%s] Invalid coordinates submitted: lat=%.4f, lon=%.4f.",
            case_id,
            payload.latitude,
            payload.longitude,
        )
        raise ValueError("Latitude must be in [-90, 90] and longitude must be in [-180, 180].")

    # 2. Establish search radius
    radius = payload.radius_km or settings.default_radius_km

    # 3. Fetch nearby incidents
    nearby_raw = search_incidents_in_radius(payload.latitude, payload.longitude, radius)
    nearby_incidents: List[Incident] = [Incident(**inc) for inc in nearby_raw]
    count = len(nearby_incidents)

    # 4. Resolve district and state name
    # Default to payload names if supplied, otherwise infer from closest nearby incident or mark unknown
    district = payload.district or "Unknown"
    state = payload.state or "Unknown"
    if district == "Unknown" or state == "Unknown":
        if nearby_incidents:
            closest = nearby_incidents[0]
            if district == "Unknown":
                district = closest.district
            if state == "Unknown":
                state = closest.state

    # 5. Run structural density & hotspot calculations
    density = calculate_crime_density(count, radius)
    hotspots = detect_hotspots(payload.latitude, payload.longitude, nearby_raw, radius)
    clusters = cluster_incidents(nearby_raw)

    # 6. Global regional aggregations
    all_historical = get_historical_incidents()
    dist_agg, state_agg = aggregate_by_region(all_historical)

    # 7. Heuristic risk calculation
    # Base risk: 25 points per incident (max 70)
    risk_score = min(count * 25, 70)
    # Density modifier: if density > 0.05 incidents/km²
    if density > 0.05:
        risk_score += 15
    # Hotspot modifier
    if hotspots:
        risk_score += 15
    # Clamp to [0, 100]
    risk_score = min(max(risk_score, 0), 100)

    # 8. Verdict matching
    category = "none"
    if risk_score >= settings.risk_high_threshold:
        verdict = "fraud"
        category = "crime_hotspot"
        explanation = (
            f"High-risk crime hotspot detected. Found {count} nearby incidents "
            f"within a {radius:.1f} km radius (Risk Score: {risk_score}/100)."
        )
    elif risk_score >= settings.risk_medium_threshold:
        verdict = "suspicious"
        explanation = (
            f"Elevated geographical risk detected. Found {count} nearby incidents "
            f"within a {radius:.1f} km radius (Risk Score: {risk_score}/100)."
        )
    else:
        verdict = "safe"
        explanation = (
            f"Low geographical risk. Queried location features minimal historical incidents "
            f"within a {radius:.1f} km radius (Risk Score: {risk_score}/100)."
        )

    # 9. Patrol recommendations
    patrol = recommend_patrols(nearby_raw, risk_score)

    evidence = GeoEvidence(
        input_coords=(payload.latitude, payload.longitude),
        valid_coords=True,
        district=district,
        state=state,
        nearby_incidents_count=count,
        nearby_incidents=nearby_incidents,
        district_aggregation=dist_agg,
        state_aggregation=state_agg,
        relative_crime_density=density,
        hotspots=hotspots,
        clusters=clusters,
        patrol_recommendations=patrol
    )

    elapsed_ms = (time.perf_counter() - t_start) * 1000
    log.info(
        "[case_id=%s] Geo analysis complete in %.2f ms — verdict=%s, risk=%d",
        case_id,
        elapsed_ms,
        verdict,
        risk_score,
    )

    # Standard Agent Contract confidence is 0.90 if data is found, else 0.80
    confidence = 0.90 if count > 0 else 0.80

    return GeoAnalysisResponse(
        case_id=case_id,
        verdict=verdict,
        confidence=confidence,
        risk_score=risk_score,
        category=category,
        explanation=explanation,
        evidence=evidence
    )
