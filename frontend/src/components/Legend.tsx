import { Info, Sun, Wind, Zap } from 'lucide-react'
import { useAppStore } from '../store/useAppStore'

export function Legend() {
  const { energyType } = useAppStore()

  const labels = {
    solar: { icon: Sun, text: 'Güneş Potansiyeli', var: 'solar' },
    wind: { icon: Wind, text: 'Rüzgar Potansiyeli', var: 'wind' },
    hybrid: { icon: Zap, text: 'Hibrit Uygunluk', var: 'hybrid' },
  }[energyType] || { icon: Info, text: 'Uygunluk Katmanları', var: 'wind' }

  const Icon = labels.icon

  return (
    <div className="absolute bottom-10 right-10 z-[2000] glass-panel rounded-xl p-4 flex flex-col gap-3 border border-white/10 shadow-2xl">
      <div className="flex items-center gap-2 text-[10px] text-text-muted font-bold uppercase tracking-widest border-b border-white/5 pb-2">
        <Icon size={12} style={{ color: `var(--${labels.var}-high)` }} />
        <span>{labels.text}</span>
      </div>

      <div className={`w-40 h-3 rounded-full bg-gradient-to-r from-[var(--${labels.var}-poor)] via-[var(--${labels.var}-low)] via-[var(--${labels.var}-medium)] to-[var(--${labels.var}-high)] shadow-[0_0_12px_rgba(0,0,0,0.3)]`} />

      <div className="flex items-center justify-between text-[9px] font-mono text-text-muted font-bold px-1">
        <span>0</span>
        <span>35</span>
        <span>55</span>
        <span>75</span>
        <span>100</span>
      </div>

      <div className="flex flex-col gap-2 mt-1">
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full shadow-[0_0_8px_var(--glass-border)]" style={{ backgroundColor: `var(--${labels.var}-high)` }} />
          <span className="text-[11px] text-text-secondary font-medium">Yüksek Verimlilik</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full shadow-[0_0_8px_var(--glass-border)]" style={{ backgroundColor: `var(--${labels.var}-medium)` }} />
          <span className="text-[11px] text-text-secondary font-medium">Orta Seviye</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full shadow-[0_0_8px_var(--glass-border)]" style={{ backgroundColor: `var(--${labels.var}-poor)` }} />
          <span className="text-[11px] text-text-secondary font-medium">Düşük Uygunluk</span>
        </div>
      </div>
    </div>
  )
}
