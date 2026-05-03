import { useEffect, useState } from 'react'
import { Trophy, X, MapPin, ChevronRight } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { useAppStore } from '../store/useAppStore'
import { getTop } from '../api/client'
import type { ProvinceScore } from '../types'

interface Props { mapRef: React.RefObject<{ flyTo: (lat: number, lon: number) => void }> }

export function TopFiveCard({ mapRef }: Props) {
  const { energyType, showTopFive, setShowTopFive, setDetailScore, setSelectedPoint, setLoading } = useAppStore()
  const [topScores, setTopScores] = useState<ProvinceScore[]>([])

  useEffect(() => {
    if (showTopFive) {
      getTop(energyType, 5).then(setTopScores)
    }
  }, [showTopFive, energyType])

  if (!showTopFive || !topScores.length) return null

  const RANK_COLORS = [
    'bg-accent-solar shadow-accent-solar/40',
    'bg-slate-300 shadow-slate-300/40',
    'bg-orange-600 shadow-orange-600/40',
    'bg-score-high shadow-score-high/40',
    'bg-accent-wind shadow-accent-wind/40',
  ]

  const handleClick = async (p: ProvinceScore) => {
    mapRef.current?.flyTo(p.centroid_lat, p.centroid_lon)
    setSelectedPoint({ lat: p.centroid_lat, lon: p.centroid_lon })
    setLoading(true)
    const { getScore: _gs } = await import('../api/client')
    const score = await _gs(p.centroid_lat, p.centroid_lon, energyType)
    setDetailScore(score)
    setLoading(false)
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: -20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -20, scale: 0.95 }}
      transition={{ type: 'spring', damping: 20 }}
      className="absolute top-6 left-6 z-[1000] w-72 glass-panel rounded-2xl shadow-2xl overflow-hidden border border-white/10"
    >
      <div className="flex items-center justify-between px-5 py-4 border-b border-white/5 bg-white/5">
        <div className="flex items-center gap-2">
          <Trophy size={16} className="text-accent-solar" />
          <span className="text-xs font-bold text-text-primary uppercase tracking-widest">En Verimli 5 Bölge</span>
        </div>
        <motion.button
          whileHover={{ scale: 1.1, rotate: 90 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => setShowTopFive(false)}
          className="p-1 text-text-muted hover:text-text-primary transition-colors hover:bg-white/5 rounded-lg"
        >
          <X size={16} />
        </motion.button>
      </div>

      <div className="p-2 space-y-1">
        <AnimatePresence>
          {topScores.map((p, i) => (
            <motion.button
              key={p.province_id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.08 }}
              onClick={() => handleClick(p)}
              className="group w-full flex items-center gap-4 px-4 py-3 hover:bg-white/5 rounded-xl transition-all duration-300 text-left"
            >
              <motion.div
                whileHover={{ scale: 1.1 }}
                className={`w-6 h-6 rounded-lg flex items-center justify-center text-[10px] font-black flex-shrink-0 text-white shadow-lg ${RANK_COLORS[i]}`}
              >
                {i + 1}
              </motion.div>

              <div className="flex-1 min-w-0">
                <div className="text-sm text-text-primary font-bold tracking-tight group-hover:text-accent-wind transition-colors truncate">
                  {p.province_name}
                </div>
                <div className="flex items-center gap-1 text-[10px] text-text-muted">
                  <MapPin size={8} />
                  <span>Merkez Koordinat</span>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <span className={`text-sm font-mono font-black ${p.score >= 70 ? 'text-score-high' : p.score >= 40 ? 'text-score-medium' : 'text-score-low'}`}>
                  {Math.round(p.score)}
                </span>
                <ChevronRight size={14} className="text-text-muted group-hover:translate-x-1 transition-transform" />
              </div>
            </motion.button>
          ))}
        </AnimatePresence>
      </div>
    </motion.div>
  )
}
