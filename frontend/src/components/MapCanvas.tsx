import { useEffect, useRef, useState, forwardRef, useImperativeHandle } from 'react'
import { MapContainer, TileLayer, useMapEvents, useMap } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import { ProvinceLayer } from './ProvinceLayer'
import { GridLayer } from './GridLayer'
import { PointMarker } from './PointMarker'
import { Legend } from './Legend'
import { useAppStore } from '../store/useAppStore'
import { getProvinces, getScore } from '../api/client'
import L from 'leaflet'

function MapClickHandler() {
  const { energyType, setDetailScore, setSelectedPoint, setLoading } = useAppStore()

  useMapEvents({
    click: async (e) => {
      const { lat, lng } = e.latlng
      setSelectedPoint({ lat, lon: lng })
      setLoading(true)
      const result = await getScore(lat, lng, energyType)
      setDetailScore(result)
      setLoading(false)
    },
  })
  return null
}

function ProvinceLoader() {
  const { energyType, filterState, setProvinceScores } = useAppStore()
  const [retryCount, setRetryCount] = useState(0)

  useEffect(() => {
    let cancelled = false
    getProvinces(energyType, filterState)
      .then(scores => {
        if (cancelled) return
        if (scores.length === 0 && retryCount < 4) {
          // Backend may still be computing scores (503 → empty array fallback)
          setTimeout(() => setRetryCount(c => c + 1), 2500)
        } else {
          setProvinceScores(scores)
        }
      })
      .catch(() => {
        if (!cancelled && retryCount < 4) {
          setTimeout(() => setRetryCount(c => c + 1), 2500)
        }
      })
    return () => { cancelled = true }
  }, [energyType, filterState, retryCount])

  return null
}

function CursorController() {
  const map = useMap()
  const { viewMode } = useAppStore()

  useEffect(() => {
    const container = map.getContainer()
    if (viewMode === 'point') {
      container.style.cursor = 'crosshair'
    } else if (viewMode === 'heatmap') {
      container.style.cursor = 'default'
    } else {
      container.style.cursor = 'grab'
    }
    return () => { container.style.cursor = '' }
  }, [map, viewMode])

  return null
}

function ScaleIndicator() {
  useEffect(() => {
    return () => {}
  }, [])

  useEffect(() => {
    const el = document.createElement('div')
    el.className = 'leaflet-control-scale-custom'
    el.style.cssText = 'position:absolute;bottom:6px;left:12px;z-index:1000;font-size:10px;color:rgba(148,163,184,0.7);font-family:JetBrains Mono,monospace;pointer-events:none;'
    document.querySelector('.leaflet-container')?.appendChild(el)
    return () => el.remove()
  }, [])

  return null
}

export interface MapCanvasHandle {
  flyTo: (lat: number, lon: number) => void
}

export const MapCanvas = forwardRef<MapCanvasHandle>((_, ref) => {
  const mapRef = useRef<L.Map | null>(null)
  const { viewMode } = useAppStore()

  useImperativeHandle(ref, () => ({
    flyTo: (lat, lon) => {
      mapRef.current?.flyTo([lat, lon], 10, { duration: 1.2 })
    },
  }))

  return (
    <div className="w-full h-full relative">
      <MapContainer
        center={[39.0, 35.0]}
        zoom={6}
        style={{ width: '100%', height: '100%' }}
        ref={mapRef as React.RefObject<L.Map>}
        zoomControl={false}
      >
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>'
          subdomains="abcd"
          maxZoom={19}
        />
        <MapClickHandler />
        <ProvinceLoader />
        <ProvinceLayer />
        <GridLayer />
        <PointMarker />
        <CursorController />
        <ScaleIndicator />
      </MapContainer>

      <div className="absolute top-4 right-4 z-[1000] flex flex-col gap-1">
        <button
          onClick={() => mapRef.current?.zoomIn()}
          className="glass-panel w-9 h-9 flex items-center justify-center text-text-muted hover:text-text-primary hover:border-accent-wind/40 transition-all rounded-t-xl rounded-b-none border border-white/10"
        >
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M7 3v8M3 7h8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
          </svg>
        </button>
        <button
          onClick={() => mapRef.current?.zoomOut()}
          className="glass-panel w-9 h-9 flex items-center justify-center text-text-muted hover:text-text-primary hover:border-accent-wind/40 transition-all rounded-b-xl rounded-t-none border border-t-0 border-white/10"
        >
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M3 7h8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
          </svg>
        </button>
      </div>

    </div>
  )
})

MapCanvas.displayName = 'MapCanvas'
