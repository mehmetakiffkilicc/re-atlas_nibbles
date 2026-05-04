import { useRef } from 'react'
import { ErrorBoundary } from './components/ErrorBoundary'
import { LayoutGrid, ArrowLeftRight, Settings } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { MapCanvas } from './components/MapCanvas'
import { FilterPanel } from './components/FilterPanel'
import { DetailPanel } from './components/DetailPanel'
import { EnergyTypeToggle } from './components/EnergyTypeToggle'
import { ViewModeToggle } from './components/ViewModeToggle'
import { TopFiveCard } from './components/TopFiveCard'
import { CompareView } from './components/CompareView'
import { LiveWeatherBadge } from './components/LiveWeatherBadge'
import { GridLoadingIndicator } from './components/GridLoadingIndicator'
import { Legend } from './components/Legend'
import { useAppStore } from './store/useAppStore'
import type { MapCanvasHandle } from './components/MapCanvas'
import './styles/globals.css'

const ENERGY_GLOW: Record<string, string> = {
  solar: '0 0 60px 20px rgba(251,191,36,0.08)',
  wind: '0 0 60px 20px rgba(59,130,246,0.08)',
  hybrid: '0 0 60px 20px rgba(139,92,246,0.08)',
}

export default function App() {
  const mapRef = useRef<MapCanvasHandle>(null)
  const { isCompareMode, toggleCompareMode, detailScore, isLoading, energyType } = useAppStore()

  return (
    <div className="h-screen flex flex-col bg-bg-primary text-text-primary font-sans relative overflow-hidden">
      <div className="absolute inset-0 bg-noise z-0 opacity-10 pointer-events-none" />

      <header
        className="flex items-center justify-between px-6 py-3 bg-bg-secondary/40 backdrop-blur-xl border-b border-glass-border flex-shrink-0 z-50 relative"
        style={{ boxShadow: ENERGY_GLOW[energyType] }}
      >
        <motion.div
          initial={{ x: -20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.4 }}
          className="flex items-center gap-4"
        >
          <motion.div
            whileHover={{ scale: 1.05, rotate: 5 }}
            whileTap={{ scale: 0.95 }}
            className="bg-accent-wind p-2 rounded-xl shadow-lg shadow-accent-wind/30 animate-pulse-glow"
          >
            <LayoutGrid className="text-white" size={20} />
          </motion.div>
          <div>
            <h1 className="text-xl font-bold tracking-tight bg-gradient-to-r from-white via-white to-text-muted bg-clip-text text-transparent">
              RE-Atlas
            </h1>
            <p className="text-[10px] uppercase tracking-[0.2em] text-accent-wind font-bold opacity-80">
              Energy Intelligence
            </p>
          </div>
        </motion.div>

        <motion.div
          initial={{ x: 20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="flex items-center gap-3"
        >
          <EnergyTypeToggle />
          <div className="h-8 w-[1px] bg-glass-border" />
          <ViewModeToggle />
          <div className="h-8 w-[1px] bg-glass-border" />
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={toggleCompareMode}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl border text-sm font-bold transition-all duration-300 ${
              isCompareMode
                ? 'border-accent-hybrid text-accent-hybrid bg-accent-hybrid/10 shadow-[0_0_20px_rgba(139,92,246,0.3)]'
                : 'border-glass-border text-text-muted hover:border-text-secondary hover:text-text-primary'
            }`}
          >
            <ArrowLeftRight size={16} />
            <span className="hidden sm:inline">Karşılaştır</span>
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.1, rotate: 30 }}
            whileTap={{ scale: 0.9 }}
            className="p-2 text-text-muted hover:text-text-primary transition-colors"
          >
            <Settings size={20} />
          </motion.button>
        </motion.div>
      </header>

      <main className="flex-1 flex overflow-hidden relative z-10">
        <motion.div
          initial={{ x: -300, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ type: 'spring', damping: 20, stiffness: 100, delay: 0.15 }}
        >
          <FilterPanel />
        </motion.div>

        <div className="flex-1 relative overflow-hidden">
          <ErrorBoundary>
            <MapCanvas ref={mapRef} />
          </ErrorBoundary>
          <TopFiveCard mapRef={mapRef as React.RefObject<{ flyTo: (lat: number, lon: number) => void }>} />
          <LiveWeatherBadge />
          <GridLoadingIndicator />
        </div>

        <AnimatePresence>
          {(detailScore || isLoading) && (
            <motion.div
              initial={{ x: 400, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: 400, opacity: 0 }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="z-50"
            >
              <DetailPanel />
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {isCompareMode && <CompareView />}

      <motion.div
        initial={{ y: 30, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.6, duration: 0.5 }}
        className="absolute bottom-6 left-1/2 -translate-x-1/2 px-5 py-2.5 glass-panel rounded-full flex items-center gap-3 text-xs text-text-secondary pointer-events-none z-40"
      >
        <div className="w-2 h-2 rounded-full bg-accent-wind animate-pulse" />
        <span className="font-medium tracking-wide">Türkiye Yenilenebilir Enerji Analitik Atlası v1.0</span>
      </motion.div>
      <Legend />
    </div>
  )
}
