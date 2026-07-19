# Geo Intelligence Agent

Heuristics-based geographical crime risk mapping and patrol recommendation agent.

---

## Overview

The Geo Intelligence Agent evaluates spatial incident datasets to compute relative crime density, identify local hotspots, cluster incidents geographically, and plan patrol routes or hubs.

It follows the standard **Agent Contract** so it can be queried independently or wired into the gateway and orchestrator.

---

## Module Structure

| Module | Responsibility |
|---|---|
| `__init__.py` | Package entrypoint, exposing public service functions and Pydantic schemas. |
| `main.py` | FastAPI application and router exposing `/geo/analyze` and `/analyze`. |
| `service.py` | Coordinates coordinate checks, calculations, and response packaging. |
| `config.py` | Settings backing settings with the `GEO_` prefix. |
| `logging.py` | Rotating logger tracking `logs/agents/geo_agent.log`. |
| `schemas.py` | Compliant request and response structures. |
| `mapper.py` | Coordinates validation, Haversine formula, and seeded historical location dataset. |
| `analyzer.py` | Density, region aggregating, Leader clustering, and patrol planning algorithms. |

---

## Algorithms Used

1. **Haversine Distance**: Calculates the great-circle distance between two coordinates on a sphere:
   $$\Delta \text{lat} = \text{lat}_2 - \text{lat}_1$$
   $$\Delta \text{lon} = \text{lon}_2 - \text{lon}_1$$
   $$a = \sin^2(\Delta \text{lat}/2) + \cos(\text{lat}_1) \cos(\text{lat}_2) \sin^2(\Delta \text{lon}/2)$$
   $$c = 2 \cdot \text{atan2}(\sqrt{a}, \sqrt{1-a})$$
   $$d = R \cdot c$$
   Where $R \approx 6371.0 \text{ km}$.
2. **Relative Crime Density**:
   $$\text{Density} = \frac{\text{Incident Count}}{\pi \cdot \text{radius}^2} \quad (\text{incidents per sq km})$$
3. **Hotspot Detection**: Evaluates if the incident count within the target area exceeds a threshold of 3 cases within 3 km.
4. **Incident Clustering**: Groups incidents spatially using a simple leader-clustering heuristic where incidents within 3 km of a cluster center join it, and the cluster centroid is dynamically updated.
5. **Patrol Recommendations**: Simple heuristic routing based on risk score, local hotspots, and categories.

---

## API Contract

### Example Request (`POST /geo/analyze`)
```json
{
  "case_id": "c-geo-2026",
  "input_type": "location",
  "payload": {
    "latitude": 12.9716,
    "longitude": 77.5946,
    "radius_km": 5.0
  }
}
```

### Example Response
```json
{
  "agent": "geo_agent",
  "case_id": "c-geo-2026",
  "verdict": "fraud",
  "confidence": 0.9,
  "risk_score": 90,
  "category": "crime_hotspot",
  "explanation": "High-risk crime hotspot detected. Found 4 nearby incidents within a 5.0 km radius (Risk Score: 90/100).",
  "evidence": {
    "input_coords": [12.9716, 77.5946],
    "valid_coords": true,
    "district": "Bengaluru Urban",
    "state": "Karnataka",
    "nearby_incidents_count": 4,
    "nearby_incidents": [
      {
        "id": "inc-blr-001",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "category": "crypto_fraud",
        "timestamp": "2026-07-01T10:00:00Z",
        "distance_km": 0.0
      }
    ],
    "district_aggregation": {
      "Bengaluru Urban": 5,
      "Central Delhi": 4,
      "Mumbai City": 3,
      "Hyderabad": 2
    },
    "state_aggregation": {
      "Karnataka": 5,
      "Delhi": 4,
      "Maharashtra": 3,
      "Telangana": 2
    },
    "relative_crime_density": 0.0509295,
    "hotspots": [
      {
        "center_latitude": 12.9716,
        "center_longitude": 77.5946,
        "incident_count": 4,
        "radius_km": 5.0,
        "risk_level": "medium"
      }
    ],
    "clusters": [
      {
        "cluster_id": 1,
        "center_latitude": 12.97415,
        "center_longitude": 77.59615,
        "node_count": 4,
        "incidents": ["inc-blr-001", "inc-blr-002", "inc-blr-003", "inc-blr-004"],
        "typical_category": "crypto_fraud"
      }
    ],
    "patrol_recommendations": {
      "priority": "high",
      "patrol_frequency": "hourly",
      "suggested_hubs": ["crypto_fraud", "phishing"],
      "narrative": "Critical risk level (90/100) identified. High density crime hotspot. Immediate hourly patrols recommended..."
    }
  },
  "processed_at": "2026-07-20T00:30:00Z"
}
```

---

## Limitations

- **No GIS DB / PostGIS**: Relies strictly on in-memory linear calculations rather than specialized spatial indexes (like R-Trees) or PostGIS databases.
- **Static Seeding**: incident history remains static and mocked inside memory, meaning updates do not persist across server restarts.
- **Simplistic Clustering**: leader-clustering can vary slightly depending on the order of ingested incidents.
