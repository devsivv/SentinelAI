"""
mapper.py — Coordinates validation, Haversine formula, and seeded historical location database.
"""

from __future__ import annotations

import math
from typing import Dict, List, Any
from .config import settings

# ---------------------------------------------------------------------------
# Seeded historical incident dataset (Representing crime occurrences in India)
# ---------------------------------------------------------------------------
_HISTORICAL_INCIDENTS: List[Dict[str, Any]] = [
    # Bengaluru Urban (Karnataka)
    {
        "id": "inc-blr-001",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "category": "crypto_fraud",
        "timestamp": "2026-07-01T10:00:00Z",
    },
    {
        "id": "inc-blr-002",
        "latitude": 12.9780,
        "longitude": 77.5910,
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "category": "phishing",
        "timestamp": "2026-07-02T14:30:00Z",
    },
    {
        "id": "inc-blr-003",
        "latitude": 12.9650,
        "longitude": 77.6010,
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "category": "crypto_fraud",
        "timestamp": "2026-07-05T18:15:00Z",
    },
    {
        "id": "inc-blr-004",
        "latitude": 12.9820,
        "longitude": 77.6080,
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "category": "theft",
        "timestamp": "2026-07-10T12:00:00Z",
    },
    {
        "id": "inc-blr-005",
        "latitude": 12.9350,
        "longitude": 77.5350,  # Koramangala area / South Blr
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "category": "mule_account",
        "timestamp": "2026-07-12T09:45:00Z",
    },
    # Central Delhi (Delhi)
    {
        "id": "inc-del-001",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "district": "Central Delhi",
        "state": "Delhi",
        "category": "digital_arrest",
        "timestamp": "2026-07-01T11:00:00Z",
    },
    {
        "id": "inc-del-002",
        "latitude": 28.6190,
        "longitude": 77.2050,
        "district": "Central Delhi",
        "state": "Delhi",
        "category": "scam",
        "timestamp": "2026-07-03T16:20:00Z",
    },
    {
        "id": "inc-del-003",
        "latitude": 28.6080,
        "longitude": 77.2150,
        "district": "Central Delhi",
        "state": "Delhi",
        "category": "digital_arrest",
        "timestamp": "2026-07-04T08:00:00Z",
    },
    {
        "id": "inc-del-004",
        "latitude": 28.6250,
        "longitude": 77.2210,
        "district": "Central Delhi",
        "state": "Delhi",
        "category": "theft",
        "timestamp": "2026-07-08T22:30:00Z",
    },
    # Mumbai City (Maharashtra)
    {
        "id": "inc-mum-001",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "district": "Mumbai City",
        "state": "Maharashtra",
        "category": "online_fraud",
        "timestamp": "2026-07-02T13:00:00Z",
    },
    {
        "id": "inc-mum-002",
        "latitude": 19.0820,
        "longitude": 72.8820,
        "district": "Mumbai City",
        "state": "Maharashtra",
        "category": "cyber_crime",
        "timestamp": "2026-07-04T15:45:00Z",
    },
    {
        "id": "inc-mum-003",
        "latitude": 19.0680,
        "longitude": 72.8710,
        "district": "Mumbai City",
        "state": "Maharashtra",
        "category": "online_fraud",
        "timestamp": "2026-07-06T19:00:00Z",
    },
    # Hyderabad (Telangana)
    {
        "id": "inc-hyd-001",
        "latitude": 17.3850,
        "longitude": 78.4867,
        "district": "Hyderabad",
        "state": "Telangana",
        "category": "mule_account",
        "timestamp": "2026-07-03T10:30:00Z",
    },
    {
        "id": "inc-hyd-002",
        "latitude": 17.3910,
        "longitude": 78.4790,
        "district": "Hyderabad",
        "state": "Telangana",
        "category": "scam",
        "timestamp": "2026-07-05T12:00:00Z",
    },
]


def validate_coordinates(latitude: float, longitude: float) -> bool:
    """Validate latitude is in [-90, 90] and longitude is in [-180, 180]."""
    return (-90.0 <= latitude <= 90.0) and (-180.0 <= longitude <= 180.0)


def haversine_distance(
    lat1: float, lon1: float, lat2: float, lon2: float, earth_radius: float | None = None
) -> float:
    """Calculate the great-circle distance between two points on Earth in kilometers."""
    r = earth_radius or settings.earth_radius_km
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    
    return r * c


def get_historical_incidents() -> List[Dict[str, Any]]:
    """Retrieve the seeded list of historical location-crime incidents."""
    return _HISTORICAL_INCIDENTS


def search_incidents_in_radius(
    latitude: float, longitude: float, radius_km: float
) -> List[Dict[str, Any]]:
    """Search for historical incidents within the specified radius in kilometers."""
    results = []
    for inc in _HISTORICAL_INCIDENTS:
        dist = haversine_distance(latitude, longitude, inc["latitude"], inc["longitude"])
        if dist <= radius_km:
            inc_copy = dict(inc)
            inc_copy["distance_km"] = round(dist, 4)
            results.append(inc_copy)
    return sorted(results, key=lambda x: x["distance_km"])
