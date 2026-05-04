import { useEffect, useRef, useCallback } from 'react'
import { useMap, useMapEvents } from 'react-leaflet'
import * as L from 'leaflet'
import { useAppStore } from '../store/useAppStore'
import { getGrid, getGridHires } from '../api/client'
import type { ProvinceScore, EnergyType } from '../types'

// Pre-baked radial gradient textures — keyed by "mode-score:diameter", reused across frames
const gradientCache = new Map<string, ImageBitmap>()

const PALETTES: Record<EnergyType, Record<string, [number, number, number]>> = {
  solar: {
    high:   [52, 211, 153],  // Emerald 400
    medium: [251, 191, 36],  // Amber 400
    low:    [251, 146, 60],  // Orange 400
    poor:   [248, 113, 113], // Red 400
  },
  wind: {
    high:   [34, 211, 238],  // Cyan 400
    medium: [56, 189, 248],  // Sky 400
    low:    [129, 140, 248], // Indigo 400
    poor:   [167, 139, 250], // Purple 400
  },
  hybrid: {
    high:   [167, 139, 250], // Purple 400
    medium: [139, 92, 246],  // Violet 500
    low:    [109, 40, 217],  // Violet 700
    poor:   [76, 29, 149],   // Purple 900
  }
}

function getScoreKey(s: number): string {
  if (s >= 75) return 'high'
  if (s >= 55) return 'medium'
  if (s >= 35) return 'low'
  return 'poor'
}

// Snap diameter to nearest power-of-2 so adjacent zoom levels share cached bitmaps
function snapDiameter(d: number): number {
  return Math.max(8, 1 << Math.round(Math.log2(Math.max(1, d))))
}

async function getGradientBitmap(type: EnergyType, scoreKey: string, diameter: number): Promise<ImageBitmap | null> {
  const key = `${type}:${scoreKey}:${diameter}`
  if (gradientCache.has(key)) return gradientCache.get(key)!
  
  const palette = PALETTES[type] || PALETTES.wind
  const [r, g, b] = palette[scoreKey] || [128, 128, 128]
  
  const oc = new OffscreenCanvas(diameter, diameter)
  const ctx = oc.getContext('2d')!
  const cx = diameter / 2
  const grad = ctx.createRadialGradient(cx, cx, 0, cx, cx, cx)
  grad.addColorStop(0,    `rgba(${r},${g},${b},0.65)`)
  grad.addColorStop(0.55, `rgba(${r},${g},${b},0.25)`)
  grad.addColorStop(1,    `rgba(${r},${g},${b},0)`)
  ctx.fillStyle = grad
  ctx.fillRect(0, 0, diameter, diameter)
  const bmp = await oc.transferToImageBitmap()
  gradientCache.set(key, bmp)
  return bmp
}

interface CellData { lat: number; lon: number; score: number; cell_km: number }
// Projected cell: [zoom-level pixel X, zoom-level pixel Y, color key]
type ProjCell = [number, number, string]

export function GridLayer() {
  const map = useMap()
  const { energyType, viewMode, provinceScores, setGridFetching } = useAppStore()

  const canvasRef    = useRef<HTMLCanvasElement | null>(null)
  const cellsRef     = useRef<CellData[]>([])
  const animFrameRef = useRef<number>(0)
  const fetchIdRef   = useRef(0)
  const debounceRef  = useRef<ReturnType<typeof setTimeout> | null>(null)
  const lastBoundsRef = useRef<{ s: number; n: number; w: number; e: number } | null>(null)

  // Gradient bitmap cache
  const bitmapsRef     = useRef<Record<string, ImageBitmap | null>>({})
  const bitmapSizeRef  = useRef(0)

  // ── Performance caches (rebuilt on zoom, reused on pan) ──────────────────
  // Path2D province clip — built in pane-local pixel space at a fixed zoom
  const clipPath2DRef   = useRef<Path2D | null>(null)
  // topLeft at the moment the clip path was built; used to compute pan delta
  const clipTopLeftRef  = useRef<L.Point | null>(null)
  // Province array identity at clip-build time (detect data reload)
  const lastProvincesRef = useRef<ProvinceScore[]>([])
  // map.project() pixel coords for every cell — invariant during pan
  const projectedCellsRef = useRef<ProjCell[]>([])
  // Zoom level at which the two caches above were built
  const lastZoomRef = useRef<number>(-1)

  const clearCanvas = useCallback(() => {
    const c = canvasRef.current
    if (!c) return
    c.getContext('2d')?.clearRect(0, 0, c.width, c.height)
    cellsRef.current = []
    projectedCellsRef.current = []
  }, [])

  // Build province clip Path2D in pane-local coords at the given zoom level.
  // This is called at most once per zoom change — O(vertices) but amortized.
  const buildClipPath2D = useCallback((zoom: number, pixelOrigin: L.Point): Path2D => {
    const path = new Path2D()
    for (const p of provinceScores) {
      const geo = p.geometry as any
      if (!geo) continue
      const polys: number[][][][] = geo.type === 'Polygon' ? [geo.coordinates] : geo.coordinates
      for (const poly of polys) {
        const ring = poly[0]
        if (!ring?.length) continue
        let first = true
        for (const coord of ring) {
          const proj = map.project(L.latLng(coord[1], coord[0]), zoom)
          const px = proj.x - pixelOrigin.x
          const py = proj.y - pixelOrigin.y
          if (first) { path.moveTo(px, py); first = false }
          else path.lineTo(px, py)
        }
      }
    }
    return path
  }, [map, provinceScores])

  // Project all cells to zoom-level pixel space — O(n) but called once per zoom.
  const projectCells = useCallback((cells: CellData[], zoom: number): ProjCell[] => {
    return cells.map(c => {
      const proj = map.project(L.latLng(c.lat, c.lon), zoom)
      return [proj.x, proj.y, getScoreKey(c.score)]
    })
  }, [map])

  const draw = useCallback((canvas: HTMLCanvasElement) => {
    const ctx = canvas.getContext('2d')!
    const size = map.getSize()
    if (canvas.width !== size.x || canvas.height !== size.y) {
      canvas.width = size.x
      canvas.height = size.y
    }

    ctx.clearRect(0, 0, size.x, size.y)
    if (!cellsRef.current.length) return

    const zoom     = map.getZoom()
    const bounds   = map.getBounds()
    const topLeft  = map.latLngToLayerPoint(bounds.getNorthWest())
    L.DomUtil.setPosition(canvas, topLeft)

    const pixelOrigin = map.getPixelOrigin()

    // ── Cache invalidation ────────────────────────────────────────────────
    const zoomChanged      = zoom !== lastZoomRef.current
    const provincesChanged = provinceScores !== lastProvincesRef.current

    if (zoomChanged || provincesChanged || !clipPath2DRef.current) {
      if (provinceScores.length > 0) {
        clipPath2DRef.current  = buildClipPath2D(zoom, pixelOrigin)
        clipTopLeftRef.current = L.point(topLeft.x, topLeft.y)
      }
      lastProvincesRef.current = provinceScores
    }

    if (zoomChanged || !projectedCellsRef.current.length) {
      projectedCellsRef.current = projectCells(cellsRef.current, zoom)
      lastZoomRef.current = zoom
    }

    // ── Cell visibility filter — pure arithmetic, no Leaflet calls ────────
    const cells    = projectedCellsRef.current
    const cellKm   = cellsRef.current[0]?.cell_km ?? 2.23
    const isParcel = zoom >= 10

    // Compute cellPx using project() on fixed reference coords (2 calls, not per-cell)
    const refA  = map.project(L.latLng(39, 35), zoom)
    const refB  = map.project(L.latLng(39, 35 + cellKm / 111), zoom)
    const cellPx = Math.max(2, Math.abs(refB.x - refA.x))
    const half   = cellPx / 2
    const R      = isParcel ? 0 : Math.max(8, cellPx * 1.8)
    const margin = Math.max(R, cellPx) * 2
    const sw = size.x, sh = size.y

    const visible: { sx: number; sy: number; key: string }[] = []
    for (const [projX, projY, key] of cells) {
      // Convert zoom-level pixel → canvas-local coords: subtract pixelOrigin then topLeft
      const sx = projX - pixelOrigin.x - topLeft.x
      const sy = projY - pixelOrigin.y - topLeft.y
      if (sx < -margin || sx > sw + margin || sy < -margin || sy > sh + margin) continue
      visible.push({ sx, sy, key })
    }

    if (!visible.length) return

    ctx.save()

    // ── Province clip — O(1) per frame via translate + cached Path2D ──────
    if (clipPath2DRef.current && clipTopLeftRef.current) {
      // Path2D was built when canvas was at clipTopLeftRef. If canvas has moved
      // (pan), apply a translate to align the path with the current canvas position.
      const dx = topLeft.x - clipTopLeftRef.current.x
      const dy = topLeft.y - clipTopLeftRef.current.y
      ctx.translate(-dx, -dy)          // shift into path's coordinate system
      ctx.clip(clipPath2DRef.current, 'evenodd')
      ctx.translate(dx, dy)            // restore — cell drawing uses canvas-local coords
    }

    // ── Draw cells ────────────────────────────────────────────────────────
    if (isParcel) {
      // Solid rects grouped by color
      const grouped: Record<string, { sx: number; sy: number }[]> = {}
      for (const v of visible) {
        if (!grouped[v.key]) grouped[v.key] = []
        grouped[v.key].push(v)
      }
      for (const [key, pts] of Object.entries(grouped)) {
        const palette = PALETTES[energyType] || PALETTES.wind
        const [r, g, b] = palette[key] || [128, 128, 128]
        ctx.fillStyle = `rgba(${r},${g},${b},0.85)`
        for (const p of pts) ctx.fillRect(p.sx - half, p.sy - half, cellPx, cellPx)
      }
    } else {
      const diameter = snapDiameter(Math.round(R * 2))
      const bitmaps  = bitmapsRef.current

      const neededKeys = ['high', 'medium', 'low', 'poor']
      const hasAllBitmaps = neededKeys.every(k => bitmaps[`${energyType}:${k}`])

      if (bitmapSizeRef.current === diameter && hasAllBitmaps) {
        // Fast path: draw pre-baked gradient bitmaps (no gradient creation per cell)
        for (const v of visible) {
          const bmp = bitmaps[`${energyType}:${v.key}`]
          if (bmp) ctx.drawImage(bmp, v.sx - R, v.sy - R, diameter, diameter)
        }
      } else {
        // Fallback: semi-transparent rects while bitmaps load (one frame only)
        const grouped: Record<string, { sx: number; sy: number }[]> = {}
        for (const v of visible) {
          if (!grouped[v.key]) grouped[v.key] = []
          grouped[v.key].push(v)
        }
        for (const [key, pts] of Object.entries(grouped)) {
          const palette = PALETTES[energyType] || PALETTES.wind
          const [r, g, b] = palette[key] || [128, 128, 128]
          ctx.fillStyle = `rgba(${r},${g},${b},0.45)`
          for (const p of pts) ctx.fillRect(p.sx - R, p.sy - R, diameter, diameter)
        }

        // Build bitmaps async for the current snapped diameter
        if (bitmapSizeRef.current !== diameter || !hasAllBitmaps) {
          bitmapSizeRef.current = diameter
          bitmapsRef.current = {}
          Promise.all(
            neededKeys.map(key =>
              getGradientBitmap(energyType, key, diameter).then(bmp => { 
                bitmapsRef.current[`${energyType}:${key}`] = bmp 
              })
            )
          ).then(() => {
            if (canvasRef.current && cellsRef.current.length) draw(canvasRef.current)
          })
        }
      }

      // Subtle ring on high-score clusters
      if (zoom >= 6) {
        const high = visible.filter(v => v.key === 'high')
        if (high.length >= 5) {
          const palette = PALETTES[energyType] || PALETTES.wind
          const [r, g, b] = palette['high']
          ctx.strokeStyle = `rgba(${r},${g},${b},0.35)`
          ctx.lineWidth = 1.5
          ctx.setLineDash([4, 4])
          for (const c of high) {
            ctx.beginPath()
            ctx.arc(c.sx, c.sy, R * 0.7, 0, Math.PI * 2)
            ctx.stroke()
          }
          ctx.setLineDash([])
        }
      }
    }

    ctx.restore()
  }, [map, provinceScores, buildClipPath2D, projectCells])

  const scheduleDraw = useCallback(() => {
    if (animFrameRef.current) return
    animFrameRef.current = requestAnimationFrame(() => {
      animFrameRef.current = 0
      const canvas = canvasRef.current
      if (canvas && cellsRef.current.length) draw(canvas)
    })
  }, [draw])

  useEffect(() => {
    const pane   = map.getPane('overlayPane')!
    const canvas = L.DomUtil.create('canvas', 'leaflet-grid-canvas') as HTMLCanvasElement
    canvas.style.position      = 'absolute'
    canvas.style.pointerEvents = 'none'
    canvas.style.willChange    = 'transform'
    pane.appendChild(canvas)
    canvasRef.current = canvas

    const size = map.getSize()
    canvas.width  = size.x
    canvas.height = size.y

    const onMove   = () => scheduleDraw()
    const onResize = () => {
      const s = map.getSize()
      canvas.width  = s.x
      canvas.height = s.y
      scheduleDraw()
    }
    // On zoom start: fade out instead of clearing — avoids black flash during animation
    const onZoomStart = () => {
      if (canvas) canvas.style.opacity = '0.35'
      clipPath2DRef.current     = null
      projectedCellsRef.current = []
      lastZoomRef.current       = -1
    }
    const onZoomEnd = () => {
      if (canvas) canvas.style.opacity = '1'
    }

    map.on('move',      onMove)
    map.on('resize',    onResize)
    map.on('zoomstart', onZoomStart)
    map.on('zoomend',   onZoomEnd)

    return () => {
      map.off('move',      onMove)
      map.off('resize',    onResize)
      map.off('zoomstart', onZoomStart)
      map.off('zoomend',   onZoomEnd)
      canvas.remove()
      if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current)
      if (debounceRef.current)  clearTimeout(debounceRef.current)
    }
  }, [map, scheduleDraw])

  useEffect(() => {
    if (viewMode !== 'heatmap') clearCanvas()
  }, [viewMode, clearCanvas])

  const triggerFetch = useCallback(async () => {
    if (viewMode !== 'heatmap') return

    const bounds = map.getBounds()
    const cur = { s: bounds.getSouth(), n: bounds.getNorth(), w: bounds.getWest(), e: bounds.getEast() }

    // Skip fetch if viewport barely moved (>85% overlap)
    if (lastBoundsRef.current) {
      const last = lastBoundsRef.current
      const overlapLat  = Math.max(0, Math.min(cur.n, last.n) - Math.max(cur.s, last.s))
      const overlapLon  = Math.max(0, Math.min(cur.e, last.e) - Math.max(cur.w, last.w))
      const overlapArea = overlapLat * overlapLon
      const curArea     = (cur.n - cur.s) * (cur.e - cur.w)
      if (curArea > 0 && overlapArea / curArea > 0.85) return
    }
    lastBoundsRef.current = cur

    const zoom     = map.getZoom()
    const bboxArea = (cur.n - cur.s) * (cur.e - cur.w)
    // Use hires (Open-Meteo) only at zoom ≥ 10 with a small bbox (<5 sq°)
    const useHires = zoom >= 10 && bboxArea < 5
    const buffer   = useHires ? 0.01 : 0.3
    const myFetchId = ++fetchIdRef.current
    setGridFetching(true)

    const applyData = (data: { cells: CellData[] }) => {
      if (fetchIdRef.current !== myFetchId) return
      if (!data.cells.length) return
      cellsRef.current = data.cells
      projectedCellsRef.current = projectCells(data.cells, zoom)
      lastZoomRef.current = zoom
      bitmapSizeRef.current = 0
      if (canvasRef.current) canvasRef.current.style.opacity = '1'
      const canvas = canvasRef.current
      if (canvas) draw(canvas)
    }

    try {
      if (useHires) {
        try {
          const data = await getGridHires(
            cur.s - buffer, cur.w - buffer, cur.n + buffer, cur.e + buffer, zoom, energyType,
          )
          if (data.cells.length > 0) { applyData(data); return }
        } catch {
          // hires failed — fall through to grid.db
        }
      }
      // grid.db fallback (always reliable)
      const data = await getGrid(
        cur.s - 0.3, cur.w - 0.3, cur.n + 0.3, cur.e + 0.3, 2.23, energyType,
      )
      applyData(data)
    } catch (e) {
      console.error('Grid fetch error:', e)
    } finally {
      if (fetchIdRef.current === myFetchId) setGridFetching(false)
    }
  }, [viewMode, energyType, map, draw, projectCells, setGridFetching])

  const debouncedFetch = useCallback(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(triggerFetch, 400)
  }, [triggerFetch])

  useMapEvents({
    moveend: debouncedFetch,
    // On zoom end: always force a fresh fetch (different zoom = different data source)
    zoomend: () => {
      lastBoundsRef.current = null
      debouncedFetch()
    },
  })

  useEffect(() => {
    if (viewMode === 'heatmap') {
      lastBoundsRef.current = null
      bitmapSizeRef.current = 0
      clipPath2DRef.current = null
      projectedCellsRef.current = []
      lastZoomRef.current = -1
      triggerFetch()
    }
  }, [viewMode, energyType])

  return null
}
