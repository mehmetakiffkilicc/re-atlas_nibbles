import { Info } from 'lucide-react'

export function Legend() {
  return (
    <div className="absolute bottom-6 right-6 z-[1000] glass-panel rounded-xl p-4 flex flex-col gap-3 border border-white/10 shadow-2xl">
      <div className="flex items-center gap-2 text-[10px] text-text-muted font-bold uppercase tracking-widest border-b border-white/5 pb-2">
        <Info size={12} />
        <span>Uygunluk Katmanları</span>
      </div>

      <div className="w-40 h-3 rounded-full bg-gradient-to-r from-score-low via-score-medium to-score-high shadow-[0_0_12px_rgba(0,0,0,0.3)]" />

      <div className="flex items-center justify-between text-[9px] font-mono text-text-muted font-bold">
        <span>0</span>
        <span>35</span>
        <span>55</span>
        <span>75</span>
        <span>100</span>
      </div>

      <div className="flex flex-col gap-2 mt-1">
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full bg-score-high shadow-[0_0_6px_rgba(34,197,94,0.4)]" />
          <span className="text-[11px] text-text-secondary font-medium">Yüksek Verimlilik</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full bg-score-medium shadow-[0_0_6px_rgba(250,204,21,0.4)]" />
          <span className="text-[11px] text-text-secondary font-medium">Orta Seviye</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full bg-score-low shadow-[0_0_6px_rgba(239,68,68,0.4)]" />
          <span className="text-[11px] text-text-secondary font-medium">Düşük Uygunluk</span>
        </div>
      </div>
    </div>
  )
}
