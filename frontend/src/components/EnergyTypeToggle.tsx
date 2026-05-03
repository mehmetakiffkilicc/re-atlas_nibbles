import { Sun, Wind, Zap } from 'lucide-react'
import { motion } from 'framer-motion'
import { useAppStore } from '../store/useAppStore'
import type { EnergyType } from '../types'

const MODES: { type: EnergyType; label: string; icon: any; color: string; glow: string; bg: string }[] = [
  {
    type: 'solar',
    label: 'Güneş',
    icon: Sun,
    color: 'text-accent-solar',
    glow: 'shadow-[0_0_15px_rgba(245,158,11,0.2)]',
    bg: 'bg-accent-solar/10 border-accent-solar/30',
  },
  {
    type: 'wind',
    label: 'Rüzgar',
    icon: Wind,
    color: 'text-accent-wind',
    glow: 'shadow-[0_0_15px_rgba(59,130,246,0.2)]',
    bg: 'bg-accent-wind/10 border-accent-wind/30',
  },
  {
    type: 'hybrid',
    label: 'Hibrit',
    icon: Zap,
    color: 'text-accent-hybrid',
    glow: 'shadow-[0_0_15px_rgba(139,92,246,0.2)]',
    bg: 'bg-accent-hybrid/10 border-accent-hybrid/30',
  },
]

export function EnergyTypeToggle() {
  const { energyType, setEnergyType } = useAppStore()

  return (
    <div className="flex bg-bg-secondary p-1 rounded-xl border border-glass-border relative">
      {MODES.map(({ type, label, icon: Icon, color, glow, bg }) => {
        const active = energyType === type
        return (
          <motion.button
            key={type}
            onClick={() => setEnergyType(type)}
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
            className={`relative flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${
              active
                ? `${color} ${glow} ${bg} border`
                : 'text-text-muted hover:text-text-primary'
            }`}
          >
            <Icon size={16} strokeWidth={2.5} />
            <span className="hidden md:inline">{label}</span>
          </motion.button>
        )
      })}
    </div>
  )
}
