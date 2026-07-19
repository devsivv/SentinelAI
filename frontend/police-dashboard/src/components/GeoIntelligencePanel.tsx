import { useState, useMemo } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle, Tooltip, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import {
  MapPin,
  Flame,
  Layers,
  ShieldAlert,
  Navigation,
  Compass,
} from 'lucide-react';
import type { GeoAgentEvidenceData, GeoIncident } from '../types/api';

interface GeoIntelligencePanelProps {
  geoData?: GeoAgentEvidenceData | null;
  agentVerdict?: string;
  agentRiskScore?: number;
  isLoading?: boolean;
}

// Custom Leaflet Icons using DivIcon for pristine styling without asset dependency
const createMarkerIcon = (color: string, label?: string, isTarget = false) => {
  if (isTarget) {
    return L.divIcon({
      className: 'leaflet-target-marker',
      html: `
        <div style="position: relative; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center;">
          <div style="position: absolute; width: 32px; height: 32px; background-color: rgba(37, 99, 235, 0.3); border-radius: 50%; animation: ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite;"></div>
          <div style="position: relative; width: 24px; height: 24px; background-color: #2563eb; border: 2px solid white; border-radius: 50%; box-shadow: 0 4px 10px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center; color: white;">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/>
            </svg>
          </div>
        </div>
      `,
      iconSize: [32, 32],
      iconAnchor: [16, 16],
      popupAnchor: [0, -16],
    });
  }

  return L.divIcon({
    className: 'leaflet-incident-marker',
    html: `
      <div style="width: 24px; height: 24px; background-color: ${color}; border: 2px solid white; border-radius: 50%; box-shadow: 0 2px 6px rgba(0,0,0,0.25); display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 10px;">
        ${label || ''}
      </div>
    `,
    iconSize: [24, 24],
    iconAnchor: [12, 12],
    popupAnchor: [0, -12],
  });
};

const targetIcon = createMarkerIcon('#2563eb', '', true);
const highRiskIcon = createMarkerIcon('#ef4444', '!');
const medRiskIcon = createMarkerIcon('#f59e0b', '•');
const lowRiskIcon = createMarkerIcon('#10b981', '✓');

// Helper component to re-center map dynamically when target changes
function ChangeView({ center }: { center: [number, number] }) {
  const map = useMap();
  map.setView(center, map.getZoom());
  return null;
}

export default function GeoIntelligencePanel({
  geoData,
  agentVerdict = 'safe',
  agentRiskScore = 0,
  isLoading = false,
}: GeoIntelligencePanelProps) {
  const [showDensityOverlay, setShowDensityOverlay] = useState(true);
  const [showClusters, setShowClusters] = useState(false);
  const [selectedIncident, setSelectedIncident] = useState<GeoIncident | null>(null);

  // Extract center coordinates or fallback to Bengaluru center
  const centerCoords: [number, number] = useMemo(() => {
    if (geoData?.input_coords && geoData.input_coords.length === 2) {
      return [geoData.input_coords[0], geoData.input_coords[1]];
    }
    return [12.9716, 77.5946];
  }, [geoData]);

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-600 border-t-transparent mb-3"></div>
        <p className="text-sm font-medium text-gray-600">Loading spatial geographical intelligence...</p>
      </div>
    );
  }

  if (!geoData) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 text-center">
        <MapPin className="h-10 w-10 text-gray-400 mx-auto mb-2" />
        <h4 className="text-base font-semibold text-gray-900 mb-1">No Geographical Evidence</h4>
        <p className="text-sm text-gray-500 max-w-md mx-auto">
          No location coordinates or spatial evidence items were included in this case. Attach a location payload to trigger the Geo Intelligence Agent.
        </p>
      </div>
    );
  }

  const {
    district,
    state,
    nearby_incidents_count,
    nearby_incidents = [],
    relative_crime_density = 0,
    hotspots = [],
    clusters = [],
    patrol_recommendations,
  } = geoData;

  const getRiskBadgeColor = (priority?: string) => {
    switch (priority?.toLowerCase()) {
      case 'high':
      case 'fraud':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'medium':
      case 'suspicious':
        return 'bg-amber-100 text-amber-800 border-amber-200';
      default:
        return 'bg-green-100 text-green-800 border-green-200';
    }
  };

  return (
    <div className="bg-white shadow-sm ring-1 ring-black ring-opacity-5 rounded-lg overflow-hidden space-y-0">
      {/* 1. Header & Controls Bar */}
      <div className="px-6 py-4 bg-gray-50 border-b border-gray-200 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-100 text-blue-700 rounded-lg shrink-0">
            <Compass className="h-5 w-5" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900 leading-tight">
              Geographical Intelligence & Hotspot Analysis
            </h3>
            <p className="text-xs text-gray-500">
              Spatial crime density, spatial clusters, and automated patrol routing heuristics
            </p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {/* Toggles */}
          <button
            onClick={() => setShowDensityOverlay(!showDensityOverlay)}
            className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium border transition-colors cursor-pointer ${
              showDensityOverlay
                ? 'bg-amber-50 text-amber-700 border-amber-300 shadow-sm'
                : 'bg-white text-gray-600 border-gray-300 hover:bg-gray-50'
            }`}
          >
            <Flame className="h-3.5 w-3.5" />
            Density Overlay
          </button>

          <button
            onClick={() => setShowClusters(!showClusters)}
            className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium border transition-colors cursor-pointer ${
              showClusters
                ? 'bg-blue-50 text-blue-700 border-blue-300 shadow-sm'
                : 'bg-white text-gray-600 border-gray-300 hover:bg-gray-50'
            }`}
          >
            <Layers className="h-3.5 w-3.5" />
            Cluster View
          </button>

          <span
            className={`inline-flex items-center rounded-md px-2.5 py-1 text-xs font-semibold border ${getRiskBadgeColor(
              agentVerdict
            )}`}
          >
            {agentVerdict.toUpperCase()} ({agentRiskScore}/100)
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 divide-y lg:divide-y-0 lg:divide-x divide-gray-200">
        {/* 2. Interactive Leaflet Map (2 Cols) */}
        <div className="lg:col-span-2 relative min-h-[420px] h-[480px] bg-gray-100 flex flex-col">
          <MapContainer
            center={centerCoords}
            zoom={13}
            scrollWheelZoom={false}
            className="w-full h-full z-0"
            style={{ minHeight: '100%', width: '100%' }}
          >
            <ChangeView center={centerCoords} />
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {/* Target Location Marker */}
            <Marker position={centerCoords} icon={targetIcon}>
              <Popup>
                <div className="text-xs space-y-1">
                  <div className="font-bold text-blue-700">Target Investigation Point</div>
                  <div>
                    <span className="font-semibold">Coords:</span> {centerCoords[0].toFixed(4)},{' '}
                    {centerCoords[1].toFixed(4)}
                  </div>
                  <div>
                    <span className="font-semibold">District:</span> {district}
                  </div>
                  <div>
                    <span className="font-semibold">State:</span> {state}
                  </div>
                </div>
              </Popup>
            </Marker>

            {/* Hotspot & Density Circles Overlay */}
            {showDensityOverlay && (
              <>
                {/* General density circle around target */}
                <Circle
                  center={centerCoords}
                  radius={5000} // 5 km default radius
                  pathOptions={{
                    color: '#f59e0b',
                    fillColor: '#f59e0b',
                    fillOpacity: 0.08,
                    dashArray: '4, 4',
                  }}
                />
                {/* Specific detected hotspots */}
                {hotspots.map((hs, idx) => (
                  <Circle
                    key={idx}
                    center={[hs.center_latitude, hs.center_longitude]}
                    radius={hs.radius_km * 1000}
                    pathOptions={{
                      color: hs.risk_level === 'high' ? '#ef4444' : '#f59e0b',
                      fillColor: hs.risk_level === 'high' ? '#ef4444' : '#f59e0b',
                      fillOpacity: 0.2,
                    }}
                  >
                    <Tooltip sticky>
                      <span className="text-xs font-semibold">
                        Hotspot ({hs.risk_level.toUpperCase()} RISK) - {hs.incident_count} Incidents
                      </span>
                    </Tooltip>
                  </Circle>
                ))}
              </>
            )}

            {/* Cluster Circles Overlay */}
            {showClusters &&
              clusters.map((cls) => (
                <Circle
                  key={cls.cluster_id}
                  center={[cls.center_latitude, cls.center_longitude]}
                  radius={1200}
                  pathOptions={{
                    color: '#3b82f6',
                    fillColor: '#3b82f6',
                    fillOpacity: 0.25,
                  }}
                >
                  <Tooltip sticky>
                    <div className="text-xs font-semibold">
                      Cluster #{cls.cluster_id}: {cls.node_count} nodes ({cls.typical_category})
                    </div>
                  </Tooltip>
                </Circle>
              ))}

            {/* Nearby Incident Markers */}
            {!showClusters &&
              nearby_incidents.map((inc) => {
                const icon =
                  inc.category.includes('fraud') || inc.category.includes('arrest')
                    ? highRiskIcon
                    : inc.category.includes('scam') || inc.category.includes('mule')
                    ? medRiskIcon
                    : lowRiskIcon;

                return (
                  <Marker
                    key={inc.id}
                    position={[inc.latitude, inc.longitude]}
                    icon={icon}
                    eventHandlers={{
                      click: () => setSelectedIncident(inc),
                    }}
                  >
                    <Popup>
                      <div className="text-xs space-y-1">
                        <div className="font-bold text-gray-900">{inc.id}</div>
                        <div>
                          <span className="font-semibold">Type:</span> {inc.category}
                        </div>
                        <div>
                          <span className="font-semibold">Distance:</span>{' '}
                          {inc.distance_km != null ? `${inc.distance_km.toFixed(2)} km` : 'N/A'}
                        </div>
                        <div>
                          <span className="font-semibold">District:</span> {inc.district}
                        </div>
                        <div className="text-gray-500 text-[10px]">
                          {new Date(inc.timestamp).toLocaleString()}
                        </div>
                      </div>
                    </Popup>
                  </Marker>
                );
              })}
          </MapContainer>

          {/* Map Legend Overlay */}
          <div className="absolute bottom-3 left-3 z-10 bg-white/95 backdrop-blur-sm p-3 rounded-lg shadow-md border border-gray-200 text-xs space-y-1.5">
            <div className="font-semibold text-gray-900 mb-1 border-b border-gray-200 pb-1">
              Spatial Risk Legend
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-blue-600 border border-white inline-block"></span>
              <span className="text-gray-700">Target Location</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-red-500 border border-white inline-block"></span>
              <span className="text-gray-700">High Risk / Fraud</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-amber-500 border border-white inline-block"></span>
              <span className="text-gray-700">Medium Risk / Scam</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-emerald-500 border border-white inline-block"></span>
              <span className="text-gray-700">Low Risk / Safe</span>
            </div>
          </div>
        </div>

        {/* 3. Metrics & Information Side Column (1 Col) */}
        <div className="lg:col-span-1 p-6 space-y-6 overflow-y-auto max-h-[480px]">
          {/* District Summary Panel */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-3 flex items-center gap-1.5">
              <Navigation className="h-4 w-4 text-blue-600" />
              District Overview
            </h4>

            <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-500">District & State</span>
                <span className="text-xs font-semibold text-gray-900">
                  {district}, {state}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-500">Nearby Incidents</span>
                <span className="text-xs font-bold text-gray-900 bg-white px-2 py-0.5 rounded border border-gray-200">
                  {nearby_incidents_count}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-500">Crime Density</span>
                <span className="text-xs font-mono font-medium text-gray-900">
                  {relative_crime_density.toFixed(4)} / km²
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-500">Hotspot Status</span>
                <span
                  className={`text-xs font-semibold px-2 py-0.5 rounded border ${
                    hotspots.length > 0
                      ? 'bg-red-50 text-red-700 border-red-200'
                      : 'bg-green-50 text-green-700 border-green-200'
                  }`}
                >
                  {hotspots.length > 0 ? 'Active Hotspot Zone' : 'Standard Density'}
                </span>
              </div>
            </div>
          </div>

          {/* Patrol Recommendation Card */}
          {patrol_recommendations && (
            <div>
              <h4 className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-3 flex items-center gap-1.5">
                <ShieldAlert className="h-4 w-4 text-amber-600" />
                Patrol Recommendation
              </h4>

              <div className="bg-amber-50/60 p-4 rounded-lg border border-amber-200 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-medium text-amber-900">Patrol Priority</span>
                  <span
                    className={`text-xs font-bold uppercase px-2 py-0.5 rounded border ${getRiskBadgeColor(
                      patrol_recommendations.priority
                    )}`}
                  >
                    {patrol_recommendations.priority}
                  </span>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-xs font-medium text-amber-900">Suggested Frequency</span>
                  <span className="text-xs font-semibold text-amber-950 bg-white px-2 py-0.5 rounded border border-amber-200 capitalize">
                    {patrol_recommendations.patrol_frequency}
                  </span>
                </div>

                {patrol_recommendations.suggested_hubs?.length > 0 && (
                  <div>
                    <span className="text-xs font-medium text-amber-900 block mb-1.5">
                      Suggested Focus Hubs
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {patrol_recommendations.suggested_hubs.map((hub, i) => (
                        <span
                          key={i}
                          className="text-[11px] font-mono bg-white text-amber-900 px-2 py-0.5 rounded border border-amber-300"
                        >
                          {hub}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <p className="text-xs text-amber-900/90 leading-relaxed bg-white/80 p-2.5 rounded border border-amber-200/80 mt-1">
                  {patrol_recommendations.narrative}
                </p>
              </div>
            </div>
          )}

          {/* Nearby Incidents List */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-3 flex items-center justify-between">
              <span>Nearby Historical Incidents</span>
              <span className="text-[11px] font-normal text-gray-400">Sorted by distance</span>
            </h4>

            {nearby_incidents.length === 0 ? (
              <div className="text-xs text-gray-500 p-3 bg-gray-50 rounded border border-gray-200 text-center">
                No incidents recorded within search radius.
              </div>
            ) : (
              <div className="space-y-2">
                {nearby_incidents.map((inc) => (
                  <div
                    key={inc.id}
                    onClick={() => setSelectedIncident(inc)}
                    className={`p-3 rounded-lg border text-xs cursor-pointer transition-colors ${
                      selectedIncident?.id === inc.id
                        ? 'bg-blue-50 border-blue-300 ring-1 ring-blue-300'
                        : 'bg-white hover:bg-gray-50 border-gray-200'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-bold text-gray-900">{inc.id}</span>
                      <span className="font-mono text-[11px] text-blue-600 font-medium bg-blue-50 px-1.5 py-0.5 rounded border border-blue-100">
                        {inc.distance_km != null ? `${inc.distance_km.toFixed(2)} km` : 'N/A'}
                      </span>
                    </div>
                    <div className="text-gray-600 flex items-center justify-between">
                      <span className="capitalize">{inc.category.replace('_', ' ')}</span>
                      <span className="text-[10px] text-gray-400">
                        {new Date(inc.timestamp).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
