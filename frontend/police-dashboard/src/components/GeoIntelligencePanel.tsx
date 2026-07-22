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

function ChangeView({ center }: { center: [number, number] }) {
  const map = useMap();
  map.setView(center, 13);
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

  const centerCoords: [number, number] = useMemo(() => {
    if (geoData?.input_coords && geoData.input_coords.length === 2) {
      return [geoData.input_coords[0], geoData.input_coords[1]];
    }
    return [12.9716, 77.5946];
  }, [geoData]);

  if (isLoading) {
    return (
      <div className="glass-card border border-white/10 rounded-2xl bg-[#111827]/70 p-12 text-center shadow-xl">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-2 border-blue-500 border-t-transparent mb-3"></div>
        <p className="text-sm font-semibold text-white">Loading Geospatial Intelligence Map…</p>
      </div>
    );
  }

  if (!geoData) {
    return (
      <div className="glass-card border border-white/10 rounded-2xl bg-[#111827]/70 p-8 sm:p-10 text-center shadow-xl">
        <div className="mx-auto w-12 h-12 rounded-full bg-slate-900/80 border border-slate-800 flex items-center justify-center text-gray-400 mb-3">
          <Compass className="h-6 w-6" aria-hidden="true" />
        </div>
        <h3 className="text-base font-bold text-white mb-1">Geospatial Intelligence Unavailable</h3>
        <p className="text-sm text-gray-400 max-w-sm mx-auto leading-relaxed">
          No location coordinates were provided with this case evidence payload.
        </p>
      </div>
    );
  }

  const {
    district = 'Bengaluru Urban',
    state = 'Karnataka',
    nearby_incidents_count = 0,
    nearby_incidents = [],
    relative_crime_density = 0.0,
    hotspots = [],
    clusters = [],
    patrol_recommendations = null,
  } = geoData;

  const getRiskBadgeColor = (verdict: string) => {
    switch (verdict.toLowerCase()) {
      case 'critical':
      case 'high':
      case 'fraud':
        return 'bg-red-500/20 text-red-300 border-red-500/30';
      case 'medium':
      case 'suspicious':
        return 'bg-amber-500/20 text-amber-300 border-amber-500/30';
      case 'low':
      case 'clean':
      case 'safe':
        return 'bg-green-500/20 text-green-300 border-green-500/30';
      default:
        return 'bg-gray-800 text-gray-400 border-gray-700';
    }
  };

  return (
    <div className="glass-card border border-white/10 rounded-2xl overflow-hidden bg-[#111827]/70 backdrop-blur-md shadow-xl text-white">
      {/* 1. Header Bar */}
      <div className="px-4 sm:px-6 py-4 border-b border-white/10 bg-[#080E1A] flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-2.5 min-w-0">
          <MapPin className="h-5 w-5 text-blue-400 shrink-0" aria-hidden="true" />
          <h3 className="text-base sm:text-lg font-bold leading-6 text-white break-words">
            Geospatial Threat Map & Crime Density Analysis
          </h3>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          {/* Toggles */}
          <button
            onClick={() => setShowDensityOverlay(!showDensityOverlay)}
            className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold border transition-all cursor-pointer ${
              showDensityOverlay
                ? 'bg-amber-500/20 text-amber-300 border-amber-500/30 shadow-sm'
                : 'bg-[#0F172A] text-gray-400 border-white/10 hover:text-white'
            }`}
          >
            <Flame className="h-3.5 w-3.5" />
            Density Overlay
          </button>

          <button
            onClick={() => setShowClusters(!showClusters)}
            className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold border transition-all cursor-pointer ${
              showClusters
                ? 'bg-blue-500/20 text-blue-300 border-blue-500/30 shadow-sm'
                : 'bg-[#0F172A] text-gray-400 border-white/10 hover:text-white'
            }`}
          >
            <Layers className="h-3.5 w-3.5" />
            Cluster View
          </button>

          <span
            className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-bold uppercase border ${getRiskBadgeColor(
              agentVerdict
            )}`}
          >
            {agentVerdict.toUpperCase()} ({agentRiskScore}/100)
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 divide-y lg:divide-y-0 lg:divide-x divide-white/10">
        {/* 2. Interactive Leaflet Map (2 Cols) */}
        <div className="lg:col-span-2 relative h-64 sm:h-80 md:h-[440px] bg-[#0F172A] flex flex-col">
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
                <Circle
                  center={centerCoords}
                  radius={5000}
                  pathOptions={{
                    color: '#f59e0b',
                    fillColor: '#f59e0b',
                    fillOpacity: 0.08,
                    dashArray: '4, 4',
                  }}
                />
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
          <div className="absolute bottom-3 left-3 z-10 bg-[#0F172A]/90 backdrop-blur-md p-3 rounded-xl shadow-lg border border-white/10 text-xs space-y-1.5 text-white">
            <div className="font-bold text-white mb-1 border-b border-white/10 pb-1">
              Spatial Risk Legend
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-blue-600 border border-white inline-block"></span>
              <span className="text-gray-300">Target Location</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-red-500 border border-white inline-block"></span>
              <span className="text-gray-300">High Risk / Fraud</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-amber-500 border border-white inline-block"></span>
              <span className="text-gray-300">Medium Risk / Scam</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-emerald-500 border border-white inline-block"></span>
              <span className="text-gray-300">Low Risk / Safe</span>
            </div>
          </div>
        </div>

        {/* 3. Metrics & Information Side Column (1 Col) */}
        <div className="lg:col-span-1 p-4 sm:p-6 space-y-6 overflow-y-auto lg:max-h-[440px]">
          {/* District Summary Panel */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-gray-400 mb-3 flex items-center gap-1.5">
              <Navigation className="h-4 w-4 text-blue-400" />
              District Overview
            </h4>

            <div className="bg-[#0F172A] p-4 rounded-xl border border-white/10 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-400">District & State</span>
                <span className="text-xs font-bold text-white">
                  {district}, {state}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-400">Nearby Incidents</span>
                <span className="text-xs font-bold text-white bg-blue-600/20 px-2 py-0.5 rounded border border-blue-500/30">
                  {nearby_incidents_count}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-400">Crime Density</span>
                <span className="text-xs font-mono font-bold text-white">
                  {relative_crime_density.toFixed(4)} / km²
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-400">Hotspot Status</span>
                <span
                  className={`text-xs font-bold px-2.5 py-0.5 rounded-full border ${
                    hotspots.length > 0
                      ? 'bg-red-500/20 text-red-300 border-red-500/30'
                      : 'bg-green-500/20 text-green-300 border-green-500/30'
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
              <h4 className="text-xs font-bold uppercase tracking-wider text-gray-400 mb-3 flex items-center gap-1.5">
                <ShieldAlert className="h-4 w-4 text-amber-400" />
                Patrol Recommendation
              </h4>

              <div className="bg-gradient-to-br from-amber-950/30 to-slate-900/60 p-4 rounded-xl border border-amber-500/30 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-amber-200">Patrol Priority</span>
                  <span
                    className={`text-xs font-bold uppercase px-2.5 py-0.5 rounded-full border ${getRiskBadgeColor(
                      patrol_recommendations.priority
                    )}`}
                  >
                    {patrol_recommendations.priority}
                  </span>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-amber-200">Suggested Frequency</span>
                  <span className="text-xs font-bold text-amber-300 bg-[#0F172A] px-2 py-0.5 rounded-md border border-amber-500/30 capitalize">
                    {patrol_recommendations.patrol_frequency}
                  </span>
                </div>

                {patrol_recommendations.suggested_hubs?.length > 0 && (
                  <div>
                    <span className="text-xs font-semibold text-amber-200 block mb-1.5">
                      Suggested Focus Hubs
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {patrol_recommendations.suggested_hubs.map((hub, i) => (
                        <span
                          key={i}
                          className="text-[11px] font-mono bg-[#0F172A] text-amber-300 px-2 py-0.5 rounded-md border border-amber-500/30"
                        >
                          {hub}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <p className="text-xs text-amber-200 leading-relaxed bg-[#0F172A]/80 p-3 rounded-xl border border-amber-500/20 mt-1">
                  {patrol_recommendations.narrative}
                </p>
              </div>
            </div>
          )}

          {/* Nearby Incidents List */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-gray-400 mb-3 flex items-center justify-between">
              <span>Nearby Historical Incidents</span>
              <span className="text-[11px] font-normal text-gray-500">Sorted by distance</span>
            </h4>

            {nearby_incidents.length === 0 ? (
              <div className="text-xs text-gray-400 p-3.5 bg-[#0F172A] rounded-xl border border-white/10 text-center">
                No incidents recorded within search radius.
              </div>
            ) : (
              <div className="space-y-2">
                {nearby_incidents.map((inc) => (
                  <div
                    key={inc.id}
                    onClick={() => setSelectedIncident(inc)}
                    className={`p-3 rounded-xl border text-xs cursor-pointer transition-colors ${
                      selectedIncident?.id === inc.id
                        ? 'bg-blue-600/20 border-blue-500/50 ring-1 ring-blue-500/50'
                        : 'bg-[#0F172A] hover:bg-blue-600/10 border-white/10'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-bold text-white">{inc.id}</span>
                      <span className="font-mono text-[11px] text-blue-300 font-bold bg-blue-600/20 px-1.5 py-0.5 rounded border border-blue-500/30">
                        {inc.distance_km != null ? `${inc.distance_km.toFixed(2)} km` : 'N/A'}
                      </span>
                    </div>
                    <div className="text-gray-400 flex items-center justify-between">
                      <span className="capitalize">{inc.category.replace('_', ' ')}</span>
                      <span className="text-[10px] text-gray-500">
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
