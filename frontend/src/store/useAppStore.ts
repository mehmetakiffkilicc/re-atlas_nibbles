import { create } from 'zustand'
import type { EnergyType, ScoreResponse, FilterState, ProvinceScore, CompareResponse, Coordinate } from '../types'
import type { LiveWeather } from '../api/client'

export type ViewMode = 'choropleth' | 'heatmap' | 'point'

interface AppState {
  energyType: EnergyType
  viewMode: ViewMode
  filterState: FilterState
  selectedPoint: Coordinate | null
  detailScore: ScoreResponse | null
  provinceScores: ProvinceScore[]
  isLoading: boolean
  showTopFive: boolean
  isCompareMode: boolean
  comparePoints: [Coordinate, Coordinate] | null
  compareResults: CompareResponse | null
  liveWeather: LiveWeather | null
  isGridFetching: boolean
  previousEnergyType: EnergyType

  setEnergyType: (t: EnergyType) => void
  setViewMode: (m: ViewMode) => void
  setFilterState: (f: FilterState) => void
  setSelectedPoint: (c: Coordinate | null) => void
  setDetailScore: (s: ScoreResponse | null) => void
  setProvinceScores: (scores: ProvinceScore[]) => void
  setLoading: (v: boolean) => void
  setShowTopFive: (v: boolean) => void
  toggleCompareMode: () => void
  addComparePoint: (c: Coordinate) => void
  clearCompare: () => void
  setCompareResults: (r: CompareResponse | null) => void
  setLiveWeather: (w: LiveWeather | null) => void
  setGridFetching: (v: boolean) => void
}

export const useAppStore = create<AppState>((set) => ({
  energyType: 'wind',
  viewMode: 'choropleth',
  filterState: { hide_forest: false, show_yeka: false, grid_max_km: null, exclude_high_risk: false },
  selectedPoint: null,
  detailScore: null,
  provinceScores: [],
  isLoading: false,
  showTopFive: false,
  isCompareMode: false,
  comparePoints: null,
  compareResults: null,
  liveWeather: null,
  isGridFetching: false,
  previousEnergyType: 'wind',

  setEnergyType: (t) => set((state) => ({ energyType: t, detailScore: null, previousEnergyType: state.energyType })),
  setViewMode: (m) => set({ viewMode: m, selectedPoint: null, detailScore: null }),
  setFilterState: (f) => set({ filterState: f }),
  setSelectedPoint: (c) => set({ selectedPoint: c }),
  setDetailScore: (s) => set({ detailScore: s }),
  setProvinceScores: (scores) => set({ provinceScores: scores }),
  setLoading: (v) => set({ isLoading: v }),
  setShowTopFive: (v) => set({ showTopFive: v }),
  toggleCompareMode: () => set((s) => ({ isCompareMode: !s.isCompareMode, comparePoints: null, compareResults: null })),
  addComparePoint: (c) => set((s) => {
    if (!s.comparePoints) return { comparePoints: [c, c] }
    return { comparePoints: [s.comparePoints[0], c] }
  }),
  clearCompare: () => set({ comparePoints: null, compareResults: null, isCompareMode: false }),
  setCompareResults: (r) => set({ compareResults: r }),
  setLiveWeather: (w) => set({ liveWeather: w }),
  setGridFetching: (v) => set({ isGridFetching: v }),
}))
