import { useEffect, useRef } from 'react'
import { useMap } from 'react-leaflet'
import L from 'leaflet'
import { useAppStore } from '../store/useAppStore'
import { getScore } from '../api/client'

function scoreToColor(score: number): string {
  if (score >= 70) return '#22C55E'
  if (score >= 40) return '#FACC15'
  return '#EF4444'
}

export function ProvinceLayer() {
  const map = useMap()
  const { provinceScores, energyType, viewMode, setDetailScore, setSelectedPoint, setLoading, filterState } = useAppStore()
  const layerRef = useRef<L.GeoJSON | null>(null)

  // Remove layer whenever viewMode is not choropleth
  useEffect(() => {
    if (viewMode !== 'choropleth') {
      if (layerRef.current) {
        map.removeLayer(layerRef.current)
        layerRef.current = null
      }
    }
  }, [viewMode, map])

  // Build/rebuild layer when in choropleth mode
  useEffect(() => {
    if (viewMode !== 'choropleth') return

    if (layerRef.current) {
      map.removeLayer(layerRef.current)
      layerRef.current = null
    }

    const filtered = provinceScores.filter((p) => {
      if (!p.geometry) return false
      if (filterState.hide_forest && p.score < 35) return false
      if (filterState.exclude_high_risk && p.score < 45) return false
      return true
    })

    const features = filtered.map((p) => ({
      type: 'Feature' as const,
      properties: { ...p },
      geometry: p.geometry as GeoJSON.Geometry,
    }))

    if (!features.length) return

    const layer = L.geoJSON(
      { type: 'FeatureCollection' as const, features } as GeoJSON.FeatureCollection,
      {
        style: (feature) => {
          const score = feature?.properties?.score ?? 50
          return {
            fillColor: scoreToColor(score),
            fillOpacity: 0.4,
            color: 'rgba(255, 255, 255, 0.1)',
            weight: 1,
          }
        },
        onEachFeature: (feature, featureLayer) => {
          featureLayer.on('click', async (e) => {
            const { lat, lng } = e.latlng
            setSelectedPoint({ lat, lon: lng })
            setLoading(true)
            const result = await getScore(lat, lng, energyType)
            setDetailScore(result)
            setLoading(false)
          })
          featureLayer.on('mouseover', () => {
            (featureLayer as L.Path).setStyle({
              fillOpacity: 0.6,
              weight: 2,
              color: 'rgba(255, 255, 255, 0.4)'
            })
          })
          featureLayer.on('mouseout', () => {
            layer.resetStyle(featureLayer as L.Path)
          })
        },
      }
    )

    layer.addTo(map)
    layerRef.current = layer

    return () => {
      map.removeLayer(layer)
      layerRef.current = null
    }
  }, [provinceScores, energyType, filterState, viewMode, map])

  return null
}
