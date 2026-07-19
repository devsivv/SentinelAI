"""
test_geo.py — Comprehensive unit and API integration tests for the Geo Intelligence Agent.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app
from agents.geo_agent.mapper import (
    haversine_distance,
    search_incidents_in_radius,
    validate_coordinates,
)
from agents.geo_agent.analyzer import (
    calculate_crime_density,
    cluster_incidents,
    detect_hotspots,
    recommend_patrols,
)
from agents.geo_agent.schemas import GeoAnalysisRequest, GeoPayload
from agents.geo_agent.service import analyze_location

client = TestClient(app)


def test_coordinate_validation():
    """Verify coordinate bounding checks."""
    assert validate_coordinates(12.9716, 77.5946) is True
    assert validate_coordinates(-90.0, -180.0) is True
    assert validate_coordinates(90.0, 180.0) is True
    
    assert validate_coordinates(90.1, 77.5946) is False
    assert validate_coordinates(-91.0, 77.5946) is False
    assert validate_coordinates(12.9716, 180.5) is False
    assert validate_coordinates(12.9716, -181.0) is False


def test_haversine_distance():
    """Verify distance math correctness between known points."""
    # Bengaluru (12.9716, 77.5946) and Chennai (13.0827, 80.2707) distance is approx 290 km
    dist = haversine_distance(12.9716, 77.5946, 13.0827, 80.2707)
    assert 285.0 <= dist <= 295.0

    # Same coordinates must yield 0 distance
    assert haversine_distance(12.9716, 77.5946, 12.9716, 77.5946) == 0.0


def test_radius_search():
    """Test radius search correctly finds seeded incidents in Bengaluru."""
    # Seeded Bengaluru Center (12.9716, 77.5946) has 4 incidents within 5.0 km
    results = search_incidents_in_radius(12.9716, 77.5946, 5.0)
    assert len(results) >= 4
    # All returned distances must be <= 5.0 km
    for res in results:
        assert res["distance_km"] <= 5.0


def test_crime_density_calculation():
    """Verify math for incidents per square kilometer."""
    # Area of circle with r=5.0 km is approx 78.54 sq km. 4 incidents -> density = 4 / 78.54 = 0.050929
    density = calculate_crime_density(4, 5.0)
    assert 0.0509 <= density <= 0.0510

    # 0 radius should handle divide-by-zero gracefully
    assert calculate_crime_density(5, 0.0) == 0.0


def test_hotspot_detection():
    """Test hotspot logic thresholds."""
    incidents = [
        {"latitude": 12.9716, "longitude": 77.5946},
        {"latitude": 12.9720, "longitude": 77.5950},
        {"latitude": 12.9710, "longitude": 77.5940},
    ]
    # 3 incidents constitutes a hotspot (threshold is 3)
    hotspots = detect_hotspots(12.9716, 77.5946, incidents, 3.0)
    assert len(hotspots) == 1
    assert hotspots[0].risk_level == "medium"

    # Less than 3 incidents should return empty hotspots
    assert len(detect_hotspots(12.9716, 77.5946, incidents[:2], 3.0)) == 0


def test_clustering():
    """Verify Leader-clustering groups nearby incidents correctly."""
    incidents = [
        {"id": "1", "latitude": 12.9716, "longitude": 77.5946, "category": "theft"},
        {"id": "2", "latitude": 12.9720, "longitude": 77.5950, "category": "theft"},
        {"id": "3", "latitude": 19.0760, "longitude": 72.8777, "category": "fraud"},
    ]
    clusters = cluster_incidents(incidents, max_cluster_dist_km=2.0)
    # Incidents 1 & 2 should cluster together, incident 3 is isolated -> 2 clusters total
    assert len(clusters) == 2
    
    c1 = next(c for c in clusters if c.cluster_id == 1 or len(c.incidents) == 2)
    assert len(c1.incidents) == 2
    assert "1" in c1.incidents
    assert "2" in c1.incidents
    assert c1.typical_category == "theft"


def test_patrol_recommendations():
    """Verify patrol planning prioritization based on risk."""
    incidents = [{"category": "theft"}]
    # High risk score
    rec_high = recommend_patrols(incidents, 80)
    assert rec_high.priority == "high"
    assert rec_high.patrol_frequency == "hourly"
    assert "theft" in rec_high.suggested_hubs

    # Low risk score
    rec_low = recommend_patrols(incidents, 20)
    assert rec_low.priority == "low"
    assert rec_low.patrol_frequency == "weekly"


@pytest.mark.asyncio
async def test_empty_datasets(monkeypatch):
    """Test behavior when historical incident dataset is empty."""
    # Override seeded list with an empty one
    monkeypatch.setattr("agents.geo_agent.mapper._HISTORICAL_INCIDENTS", [])
    
    payload = GeoPayload(latitude=12.9716, longitude=77.5946, radius_km=5.0)
    request = GeoAnalysisRequest(case_id="case-empty-geo", payload=payload)
    
    response = await analyze_location(request)
    assert response.verdict == "safe"
    assert response.risk_score == 0
    assert response.evidence.nearby_incidents_count == 0
    assert response.evidence.relative_crime_density == 0.0
    assert not response.evidence.hotspots
    assert response.evidence.patrol_recommendations.patrol_frequency == "none"


@pytest.mark.asyncio
async def test_invalid_coordinates_service():
    """Test that service raises ValueError for invalid coordinate coordinates."""
    payload = GeoPayload(latitude=100.0, longitude=77.5946, radius_km=5.0)
    request = GeoAnalysisRequest(case_id="case-invalid", payload=payload)
    
    with pytest.raises(ValueError, match="Latitude must be in"):
        await analyze_location(request)


def test_api_endpoint_success():
    """Test API endpoint `/geo/analyze` success route."""
    response = client.post(
        "/geo/analyze",
        json={
            "case_id": "c-geo-api",
            "input_type": "location",
            "payload": {
                "latitude": 12.9716,
                "longitude": 77.5946,
                "radius_km": 5.0
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["agent"] == "geo_agent"
    assert data["case_id"] == "c-geo-api"
    assert "verdict" in data
    assert "risk_score" in data
    assert "evidence" in data
    assert data["evidence"]["valid_coords"] is True


def test_api_endpoint_invalid_coordinates():
    """Test API endpoint `/geo/analyze` error handling for invalid coordinates."""
    response = client.post(
        "/geo/analyze",
        json={
            "case_id": "c-geo-api",
            "input_type": "location",
            "payload": {
                "latitude": 95.0,  # Invalid latitude
                "longitude": 77.5946,
                "radius_km": 5.0
            }
        }
    )
    # ValueError triggers 400 Bad Request
    assert response.status_code == 400
    assert "detail" in response.json()


def test_api_endpoint_validation_error():
    """Test API endpoint `/geo/analyze` input type validation."""
    response = client.post(
        "/geo/analyze",
        json={
            "case_id": "c-geo-api",
            "input_type": "invalid_type",  # Should be 'location'
            "payload": {
                "latitude": 12.9716,
                "longitude": 77.5946
            }
        }
    )
    # Validator checks input_type and raises ValueError -> 400 Bad Request or 422
    assert response.status_code in (400, 422)
