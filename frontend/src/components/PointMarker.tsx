import { CircleMarker, Tooltip } from 'react-leaflet'
import { useAppStore } from '../store/useAppStore'

export function PointMarker() {
  const { selectedPoint, detailScore } = useAppStore()

  if (!selectedPoint) return null

  const score = detailScore?.score
  const color = score == null ? '#94a3b8' : score >= 70 ? '#22C55E' : score >= 40 ? '#FACC15' : '#EF4444'

  return (
    <>
      {/* Outer pulse ring */}
      <CircleMarker
        center={[selectedPoint.lat, selectedPoint.lon]}
        radius={18}
        pathOptions={{
          color,
          fillColor: color,
          fillOpacity: 0.12,
          weight: 1.5,
          opacity: 0.5,
        }}
      />
      {/* Inner solid dot */}
      <CircleMarker
        center={[selectedPoint.lat, selectedPoint.lon]}
        radius={7}
        pathOptions={{
          color: '#0B1220',
          fillColor: color,
          fillOpacity: 0.95,
          weight: 2,
        }}
      >
        {score != null && (
          <Tooltip permanent={false} direction="top" offset={[0, -10]}>
            <span className="text-xs font-bold">{Math.round(score)}</span>
          </Tooltip>
        )}
      </CircleMarker>
    </>
  )
}
