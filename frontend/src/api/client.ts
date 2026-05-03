import type { EnergyType, ScoreResponse, ProvinceScore, ForecastResponse, Substation, FilterState } from '../types'
import mockProvinces from '../mocks/provinces.json'
import mockScore from '../mocks/score_response.json'

const BASE = '/api'
const DEMO = (import.meta as unknown as { env: Record<string, string> }).env?.VITE_DEMO_MODE === 'true'

async function apiFetch<T>(url: string, fallback: T): Promise<T> {
  if (DEMO) return fallback
  try {
    const res = await fetch(url)
    if (!res.ok) {
      console.warn(`[RE-Atlas] API ${url} returned ${res.status}`)
      if (res.status === 503) {
        // Backend not ready — throw so ProvinceLoader can retry
        throw new Error('SERVICE_UNAVAILABLE')
      }
      return fallback
    }
    return await res.json() as T
  } catch (err) {
    if (err instanceof Error && err.message === 'SERVICE_UNAVAILABLE') throw err
    console.error(`[RE-Atlas] API fetch failed: ${url}`, err)
    return fallback
  }
}

export async function getProvinces(type: EnergyType, filters?: FilterState): Promise<ProvinceScore[]> {
  let url = `${BASE}/provinces?type=${type}`
  if (filters?.hide_forest) url += '&hide_forest=true'
  if (filters?.exclude_high_risk) url += '&exclude_high_risk=true'
  if (filters?.grid_max_km != null) url += `&grid_max_km=${filters.grid_max_km}`
  return apiFetch(url, mockProvinces as ProvinceScore[])
}

export interface GridCell { lat: number; lon: number; score: number; cell_km: number }
export interface GridResponse { cells: GridCell[]; cell_km: number; total: number }

export async function getGrid(
  minLat: number, minLon: number, maxLat: number, maxLon: number,
  cellKm: number, type: EnergyType,
): Promise<GridResponse> {
  const url = `${BASE}/grid?min_lat=${minLat}&min_lon=${minLon}&max_lat=${maxLat}&max_lon=${maxLon}&cell_km=${cellKm}&type=${type}`
  return apiFetch(url, { cells: [], cell_km: cellKm, total: 0 })
}

export async function getGridHires(
  minLat: number, minLon: number, maxLat: number, maxLon: number,
  zoom: number, type: EnergyType,
): Promise<GridResponse> {
  const url = `${BASE}/grid/hires?min_lat=${minLat}&min_lon=${minLon}&max_lat=${maxLat}&max_lon=${maxLon}&zoom=${zoom}&type=${type}`
  return apiFetch(url, { cells: [], cell_km: 2.23, total: 0 })
}

export async function getScore(lat: number, lon: number, type: EnergyType): Promise<ScoreResponse> {
  return apiFetch(`${BASE}/score?lat=${lat}&lon=${lon}&type=${type}`, mockScore as ScoreResponse)
}

export async function getForecast(lat: number, lon: number, type: EnergyType): Promise<ForecastResponse> {
  const fallback: ForecastResponse = {
    lat, lon, energy_type: type,
    points: Array.from({ length: 48 }, (_, i) => ({
      timestamp: new Date(Date.now() + i * 3600000).toISOString(),
      expected_kw: Math.max(0, 300 + 200 * Math.sin(Math.PI * ((i % 24) - 6) / 12)),
      lower_kw: Math.max(0, 255 + 170 * Math.sin(Math.PI * ((i % 24) - 6) / 12)),
      upper_kw: Math.max(0, 345 + 230 * Math.sin(Math.PI * ((i % 24) - 6) / 12)),
    })),
  }
  return apiFetch(`${BASE}/forecast?lat=${lat}&lon=${lon}&type=${type}&hours=48`, fallback)
}

export async function getTop(type: EnergyType, n = 5): Promise<ProvinceScore[]> {
  return apiFetch(`${BASE}/top?type=${type}&n=${n}`, (mockProvinces as ProvinceScore[]).slice(0, n))
}

export async function getNearestSubstation(lat: number, lon: number): Promise<Substation | null> {
  return apiFetch(`${BASE}/nearest-substation?lat=${lat}&lon=${lon}`, null)
}

export interface LiveWeather {
  wind_speed_ms: number
  ghi_w_m2: number
  temperature_c: number
  timestamp: string
}

export async function getLiveWeather(lat: number, lon: number, type: EnergyType): Promise<LiveWeather | null> {
  if (DEMO) return null
  try {
    const vars = type === 'solar'
      ? 'shortwave_radiation,temperature_2m'
      : type === 'wind'
        ? 'wind_speed_10m,temperature_2m'
        : 'shortwave_radiation,wind_speed_10m,temperature_2m'
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=${vars}&wind_speed_unit=ms`
    const res = await fetch(url)
    if (!res.ok) return null
    const data = await res.json()
    return {
      wind_speed_ms: data.current?.wind_speed_10m ?? 0,
      ghi_w_m2: data.current?.shortwave_radiation ?? 0,
      temperature_c: data.current?.temperature_2m ?? 0,
      timestamp: data.current?.time ?? new Date().toISOString(),
    }
  } catch {
    return null
  }
}
