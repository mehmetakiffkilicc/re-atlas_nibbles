import { useEffect, useRef } from 'react'
import { useMap } from 'react-leaflet'
import * as L from 'leaflet'
import { useAppStore } from '../store/useAppStore'

function getHeatColor(score: number, opacity: number = 1): string {
  if (score >= 80) return `rgba(34, 197, 94, ${opacity})`
  if (score >= 65) return `rgba(163, 230, 53, ${opacity})`
  if (score >= 50) return `rgba(250, 204, 21, ${opacity})`
  if (score >= 35) return `rgba(249, 115, 22, ${opacity})`
  return `rgba(239, 68, 68, ${opacity})`
}

class HeatCanvasLayer extends L.Layer {
  private _canvas: HTMLCanvasElement | null = null
  private _data: { lat: number; lon: number; score: number }[] = []
  private _radius = 60
  private _animFrame: number = 0
  private _isDirty = false
  private _offscreen: HTMLCanvasElement | null = null

  setData(data: { lat: number; lon: number; score: number }[]) {
    this._data = data
    this._scheduleRedraw()
  }

  onAdd(map: L.Map): this {
    const pane = map.getPane('overlayPane')!
    this._canvas = L.DomUtil.create('canvas', 'leaflet-heatmap-canvas') as HTMLCanvasElement
    this._canvas.style.position = 'absolute'
    this._canvas.style.pointerEvents = 'none'
    this._canvas.style.willChange = 'transform'
    pane.appendChild(this._canvas)

    this._offscreen = document.createElement('canvas')
    this._offscreen.style.display = 'none'
    document.body.appendChild(this._offscreen)

    map.on('move', this._onMove, this)
    map.on('resize', this._reset, this)

    this._reset()
    return this
  }

  onRemove(map: L.Map): this {
    if (this._canvas) {
      this._canvas.remove()
      this._canvas = null
    }
    if (this._offscreen) {
      this._offscreen.remove()
      this._offscreen = null
    }
    map.off('move', this._onMove, this)
    map.off('resize', this._reset, this)
    if (this._animFrame) cancelAnimationFrame(this._animFrame)
    return this
  }

  private _onMove = () => {
    if ((this._map as any)?._zooming) return
    this._scheduleRedraw()
  }

  private _scheduleRedraw = () => {
    this._isDirty = true
    if (this._animFrame) return
    this._animFrame = requestAnimationFrame(() => {
      this._animFrame = 0
      if (!this._isDirty) return
      this._isDirty = false
      this._redraw()
    })
  }

  private _reset = () => {
    if (!this._canvas || !this._map) return
    const size = this._map.getSize()
    this._canvas.width = size.x
    this._canvas.height = size.y
    if (this._offscreen) {
      this._offscreen.width = size.x
      this._offscreen.height = size.y
    }
    this._redraw()
  }

  private _redraw = () => {
    const map = this._map
    if (!map || !this._canvas || !this._data.length || !this._offscreen) return

    const size = map.getSize()
    const zoom = map.getZoom()
    const r = Math.max(25, (this._radius * (zoom / 6)) * 1.5)

    const offCtx = this._offscreen.getContext('2d')!
    this._offscreen.width = size.x
    this._offscreen.height = size.y
    offCtx.clearRect(0, 0, size.x, size.y)

    const center = map.getCenter()

    const visible = this._data.filter(pt => {
      const px = map.latLngToContainerPoint([pt.lat, pt.lon])
      return px.x > -r * 2 && px.x < size.x + r * 2 && px.y > -r * 2 && px.y < size.y + r * 2
    })

    offCtx.globalAlpha = 0.6
    for (const pt of visible) {
      const px = map.latLngToContainerPoint([pt.lat, pt.lon])
      offCtx.beginPath()
      offCtx.arc(px.x, px.y, r * 0.8, 0, Math.PI * 2)
      offCtx.shadowBlur = r * 1.2
      offCtx.shadowColor = getHeatColor(pt.score, 0.8)
      offCtx.fillStyle = getHeatColor(pt.score, 0.4)
      offCtx.fill()
    }

    offCtx.shadowBlur = 0
    offCtx.globalAlpha = 0.3
    for (const pt of visible) {
      const px = map.latLngToContainerPoint([pt.lat, pt.lon])
      const grad = offCtx.createRadialGradient(px.x, px.y, 0, px.x, px.y, r)
      grad.addColorStop(0, getHeatColor(pt.score, 0.8))
      grad.addColorStop(1, getHeatColor(pt.score, 0))
      offCtx.fillStyle = grad
      offCtx.fillRect(px.x - r, px.y - r, r * 2, r * 2)
    }

    const ctx = this._canvas.getContext('2d')!
    ctx.clearRect(0, 0, size.x, size.y)
    ctx.drawImage(this._offscreen, 0, 0)
  }
}

export function HeatmapLayer() {
  const map = useMap()
  const { provinceScores, viewMode } = useAppStore()
  const layerRef = useRef<HeatCanvasLayer | null>(null)

  useEffect(() => {
    if (viewMode !== 'heatmap') {
      if (layerRef.current) {
        map.removeLayer(layerRef.current)
        layerRef.current = null
      }
      return
    }

    if (!provinceScores.length) return

    if (!layerRef.current) {
      layerRef.current = new HeatCanvasLayer()
      layerRef.current.addTo(map)
    }

    layerRef.current.setData(
      provinceScores.map((p) => ({ lat: p.centroid_lat, lon: p.centroid_lon, score: p.score }))
    )

    return () => {
      if (layerRef.current) {
        map.removeLayer(layerRef.current)
        layerRef.current = null
      }
    }
  }, [map, provinceScores, viewMode])

  return null
}
