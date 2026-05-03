import { Filter, Trees, MapPin, AlertTriangle, ShieldCheck, Star, ChevronDown, Radio } from 'lucide-react'
import { motion } from 'framer-motion'
import { useAppStore } from '../store/useAppStore'

export function FilterPanel() {
  const { filterState, setFilterState, showTopFive, setShowTopFive } = useAppStore()

  const toggle = (key: keyof typeof filterState) =>
    setFilterState({ ...filterState, [key]: !filterState[key] })

  return (
    <div className="w-72 flex-shrink-0 glass-panel m-4 rounded-2xl p-5 flex flex-col gap-6 overflow-y-auto z-40">
      <div className="flex items-center gap-2 text-text-primary mb-2">
        <Filter size={18} className="text-accent-wind" />
        <h2 className="font-bold tracking-tight">Analiz Paneli</h2>
      </div>

      <div className="space-y-6">
        <div>
          <div className="flex items-center justify-between text-[10px] text-text-muted uppercase tracking-[0.2em] mb-4 font-bold">
            <span>Kısıtlamalar</span>
            <ChevronDown size={12} />
          </div>

          <div className="space-y-3">
            {[
              { key: 'hide_forest' as const, label: 'Ormanlık Alanlar', icon: Trees },
              { key: 'show_yeka' as const, label: 'YEKA Sahaları', icon: ShieldCheck },
              { key: 'exclude_high_risk' as const, label: 'Yüksek Riskli Bölgeler', icon: AlertTriangle },
            ].map(({ key, label, icon: Icon }) => (
              <label
                key={key}
                className="flex items-center justify-between group cursor-pointer p-2 rounded-lg hover:bg-white/5 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className={`p-1.5 rounded-md transition-all duration-200 ${filterState[key] ? 'bg-accent-wind/20 text-accent-wind' : 'bg-white/5 text-text-muted group-hover:text-text-secondary'}`}>
                    <Icon size={16} />
                  </div>
                  <span className={`text-sm transition-colors ${filterState[key] ? 'text-text-primary' : 'text-text-muted group-hover:text-text-secondary'}`}>
                    {label}
                  </span>
                </div>
                <div className={`w-8 h-4 rounded-full relative transition-all duration-300 ${filterState[key] ? 'bg-accent-wind' : 'bg-white/10'}`}>
                  <motion.div
                    className="absolute top-1 w-2 h-2 rounded-full bg-white"
                    animate={{ left: filterState[key] ? 20 : 4 }}
                    transition={{ type: 'spring', damping: 20, stiffness: 300 }}
                  />
                </div>
                <input
                  type="checkbox"
                  checked={!!filterState[key]}
                  onChange={() => toggle(key)}
                  className="hidden"
                />
              </label>
            ))}
          </div>
        </div>

        <div>
          <div className="flex items-center justify-between text-[10px] text-text-muted uppercase tracking-[0.2em] mb-4 font-bold">
            <span>Şebeke Altyapısı</span>
            <ChevronDown size={12} />
          </div>

          <div className="p-3 bg-white/5 rounded-xl border border-glass-border">
            <div className="flex items-center gap-2 mb-3">
              <Radio size={14} className="text-accent-wind" />
              <span className="text-xs text-text-secondary font-medium">Max Trafo Mesafesi</span>
            </div>
            <div className="flex items-center gap-3">
              <input
                type="range"
                min={1} max={100}
                value={filterState.grid_max_km ?? 50}
                onChange={(e) => setFilterState({
                  ...filterState,
                  grid_max_km: Number(e.target.value),
                })}
                className="flex-1 accent-accent-wind h-1 bg-white/10 rounded-lg cursor-pointer"
              />
              <span className="text-sm font-mono text-accent-wind w-10 text-right">
                {filterState.grid_max_km ?? 50}
                <span className="text-[10px] ml-0.5">km</span>
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-auto pt-4 border-t border-glass-border">
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => setShowTopFive(!showTopFive)}
          className={`w-full flex items-center justify-center gap-2 py-3 rounded-xl text-sm font-bold transition-all duration-300 ${
            showTopFive
              ? 'bg-accent-wind text-white shadow-lg shadow-accent-wind/40'
              : 'glass-panel text-text-muted hover:text-text-primary hover:border-text-muted'
          }`}
        >
          <Star size={16} fill={showTopFive ? 'currentColor' : 'none'} />
          En İyi 5 Bölge
        </motion.button>
      </div>
    </div>
  )
}
