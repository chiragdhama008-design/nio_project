/**
 * ZoneMap — stylized city zone visualization.
 * Shows 6 zones with risk-colored indicators, roads, and sensor points.
 */

const ZONE_POSITIONS = {
  'zone-1': { x: 200, y: 150, label: 'Central' },
  'zone-2': { x: 370, y: 80, label: 'Industrial' },
  'zone-3': { x: 80, y: 240, label: 'Residential' },
  'zone-4': { x: 370, y: 260, label: 'Riverside' },
  'zone-5': { x: 200, y: 50, label: 'Transit Hub' },
  'zone-6': { x: 80, y: 80, label: 'Outer Ring' },
};

const ROADS = [
  { from: 'zone-5', to: 'zone-1' },
  { from: 'zone-1', to: 'zone-3' },
  { from: 'zone-1', to: 'zone-2' },
  { from: 'zone-1', to: 'zone-4' },
  { from: 'zone-6', to: 'zone-5' },
  { from: 'zone-6', to: 'zone-3' },
  { from: 'zone-2', to: 'zone-4' },
];

function severityColor(severity) {
  switch (severity) {
    case 'critical': return 'var(--color-critical)';
    case 'high': return 'var(--color-warning)';
    case 'moderate': return 'var(--color-caution)';
    default: return 'var(--color-ok)';
  }
}

export default function ZoneMap({ zones }) {
  const zoneList = zones?.zones ?? [];

  const zoneMap = {};
  zoneList.forEach(z => { zoneMap[z.id] = z; });

  return (
    <div className="panel">
      <h2 className="panel-title">City Zone Map</h2>
      <svg viewBox="0 0 460 320" className="zone-map-svg">
        {/* Roads */}
        {ROADS.map((road, i) => {
          const from = ZONE_POSITIONS[road.from];
          const to = ZONE_POSITIONS[road.to];
          return (
            <line
              key={i}
              x1={from.x} y1={from.y}
              x2={to.x} y2={to.y}
              stroke="var(--color-border)"
              strokeWidth="2"
              strokeDasharray="6,3"
            />
          );
        })}

        {/* Zones */}
        {Object.entries(ZONE_POSITIONS).map(([id, pos]) => {
          const zone = zoneMap[id];
          const severity = zone?.risk_level ?? 'low';
          const score = zone?.risk_score ?? 0;
          const color = severityColor(severity);

          return (
            <g key={id}>
              {/* Zone circle */}
              <circle
                cx={pos.x} cy={pos.y} r={32}
                fill="var(--color-surface)"
                stroke={color}
                strokeWidth="2.5"
              />
              {/* Risk score */}
              <text
                x={pos.x} y={pos.y + 2}
                textAnchor="middle"
                dominantBaseline="middle"
                fontSize="14"
                fontWeight="600"
                fill="var(--color-text)"
              >
                {Math.round(score)}
              </text>
              {/* Label */}
              <text
                x={pos.x} y={pos.y + 50}
                textAnchor="middle"
                fontSize="11"
                fill="var(--color-text-secondary)"
              >
                {pos.label}
              </text>
              {/* Status dot */}
              <circle
                cx={pos.x + 24} cy={pos.y - 24} r={5}
                fill={color}
              />
            </g>
          );
        })}

        {/* River line for Riverside */}
        <path
          d="M 340 230 Q 380 250 420 240 Q 450 235 460 260"
          fill="none"
          stroke="var(--color-info)"
          strokeWidth="3"
          opacity="0.4"
        />
      </svg>
    </div>
  );
}
