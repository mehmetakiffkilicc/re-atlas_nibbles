import { Map, Flame, MapPin } from 'lucide-react'
import { motion } from 'framer-motion'
import { useAppStore, type ViewMode } from '../store/useAppStore'

const MODES: { id: ViewMode; label: string; Icon: any }[] = [
  { id: 'choropleth', label: 'İl Görünümü', Icon: Map },
  { id: 'heatmap', label: 'Isı Haritası', Icon: Flame },
  { id: 'point', label: 'Nokta Seçim', Icon: MapPin },
]

export function ViewModeToggle() {
  const { viewMode, setViewMode } = useAppStore()

  return (
    <div className="flex items-center gap-1 bg-bg-primary/60 border border-glass-border rounded-xl p-1">
      {MODES.map(({ id, label, Icon }) => {
        const active = viewMode === id
        return (
          <motion.button
            key={id}
            onClick={() => setViewMode(id)}
            title={label}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className={`relative flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
              active
                ? 'text-accent-solar'
                : 'text-text-muted hover:text-text-primary hover:bg-white/5'
            }`}
          >
            {active && (
              <motion.div
                layoutId="viewModeBg"
                className="absolute inset-0 bg-accent-solar/15 border border-accent-solar/30 rounded-lg"
                transition={{ type: 'spring', duration: 0.4 }}
              />
            )}
            <span className="relative z-10 flex items-center gap-1.5">
              <Icon size={13} />
              <span className="hidden md:inline">{label}</span>
            </span>
          </motion.button>
        )
      })}
    </div>
  )
}
