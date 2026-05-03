import { MapPin, Zap, TrendingUp, AlertCircle, Info, ShieldCheck, Factory, Wallet, Plus, Activity, Flame, ArrowUpRight, ArrowDownRight } from 'lucide-react'
import { motion } from 'framer-motion'
import { useAppStore } from '../store/useAppStore'
import { ForecastChart } from './ForecastChart'

function ScoreBar({ label, value, icon: Icon }: { label: string; value: number; icon: any }) {
  const pct = Math.round(value * 100)
  const colorClass = pct >= 70 ? 'text-score-high' : pct >= 40 ? 'text-score-medium' : 'text-score-low'
  const bgClass = pct >= 70 ? 'bg-score-high' : pct >= 40 ? 'bg-score-medium' : 'bg-score-low'

  return (
    <div className="space-y-1.5">
      <div className="flex justify-between items-center text-[11px]">
        <div className="flex items-center gap-2 text-text-secondary">
          <Icon size={12} className="opacity-70" />
          <span>{label}</span>
        </div>
        <span className={`font-mono font-bold ${colorClass}`}>{pct}%</span>
      </div>
      <div className="h-1.5 bg-white/5 rounded-full overflow-hidden border border-white/5">
        <div className={`h-full rounded-full transition-all duration-1000 ease-out ${bgClass}`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  )
}

function CircularScore({ score }: { score: number }) {
  const color = score >= 70 ? '#22C55E' : score >= 40 ? '#FACC15' : '#EF4444'
  const radius = 30
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (score / 100) * circumference

  return (
    <div className="relative w-20 h-20 flex items-center justify-center">
      <svg className="w-full h-full -rotate-90">
        <circle
          cx="40" cy="40" r={radius}
          fill="transparent" stroke="currentColor" strokeWidth="4"
          className="text-white/5"
        />
        <circle
          cx="40" cy="40" r={radius}
          fill="transparent" stroke={color} strokeWidth="4"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="transition-all duration-1000 ease-out"
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-xl font-bold font-mono" style={{ color }}>{Math.round(score)}</span>
        <span className="text-[8px] text-text-muted font-bold uppercase tracking-tighter">Skor</span>
      </div>
    </div>
  )
}

function DynamicAnalysisHint({ score, breakdown, energyType }: { score: number; breakdown: any; energyType: string }) {
  const energyLabel = energyType === 'solar' ? 'Güneş' : energyType === 'wind' ? 'Rüzgar' : 'Hibrit'
  const entries = Object.entries(breakdown) as [string, number][]
  const strongest = entries.reduce<[string, number]>((a, b) => b[1] > a[1] ? b : a, ['', 0])
  const weakest = entries.reduce<[string, number]>((a, b) => b[1] < a[1] ? b : a, ['', 0])

  const labelMap: Record<string, string> = {
    resource_potential: 'kaynak potansiyeli',
    land_use: 'arazi verimliliği',
    grid_proximity: 'şebeke yakınlığı',
    economic_feasibility: 'finansal fizibilite',
  }

  const strengthLabel = labelMap[strongest[0]] || strongest[0]
  const weaknessLabel = labelMap[weakest[0]] || weakest[0]

  return (
    <div className="p-3 bg-accent-wind/5 rounded-xl border border-accent-wind/15 flex gap-3 items-start">
      <Zap size={14} className="text-accent-wind mt-0.5 flex-shrink-0" />
      <div className="space-y-1">
        <p className="text-[11px] leading-relaxed text-text-secondary">
          Bu bölgenin <span className="text-text-primary font-semibold">{energyLabel}</span> uygunluk skoru{' '}
          <span className="text-text-primary font-bold">{Math.round(score)}</span> puan.
        </p>
        <p className="text-[10px] text-text-muted">
          <span className="text-score-high font-semibold">En güçlü:</span> {strengthLabel} ({Math.round(strongest[1] * 100)}%){' '}
          <span className="mx-1">|</span>{' '}
          <span className="text-score-low font-semibold">Zayıf nokta:</span> {weaknessLabel} ({Math.round(weakest[1] * 100)}%)
        </p>
      </div>
    </div>
  )
}

export function DetailPanel() {
  const { detailScore, energyType, isLoading, isCompareMode, addComparePoint, viewMode, previousEnergyType } = useAppStore()

  if (!detailScore && !isLoading) {
    if (viewMode === 'heatmap') {
      return (
        <div className="w-80 flex-shrink-0 glass-panel m-4 rounded-2xl flex flex-col items-center justify-center gap-4 text-center p-8">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', damping: 15 }}
            className="p-4 rounded-2xl bg-accent-solar/10 border border-accent-solar/20"
          >
            <Flame size={28} className="text-accent-solar" />
          </motion.div>
          <div>
            <p className="text-sm font-semibold text-text-primary">Isı Haritası Modu</p>
            <p className="text-xs text-text-muted mt-1 leading-relaxed">
              Haritada herhangi bir noktaya tıklayarak o koordinatın detaylı uygunluk analizini görün.
            </p>
          </div>
        </div>
      )
    }
    return null
  }

  if (isLoading) {
    return (
      <div className="w-80 flex-shrink-0 glass-panel m-4 rounded-2xl overflow-hidden animate-pulse">
        <div className="p-5 space-y-6">
          <div className="flex justify-between">
            <div className="space-y-2 w-1/2">
              <div className="h-4 bg-white/5 rounded w-full" />
              <div className="h-3 bg-white/5 rounded w-2/3" />
            </div>
            <div className="w-16 h-16 rounded-full bg-white/5" />
          </div>
          <div className="h-24 bg-white/5 rounded-xl" />
          <div className="space-y-3">
            <div className="h-4 bg-white/5 rounded w-1/3" />
            <div className="h-2 bg-white/5 rounded" />
            <div className="h-2 bg-white/5 rounded" />
          </div>
        </div>
      </div>
    )
  }

  if (!detailScore) return null

  const { score, breakdown, explanation, nearest_substation, yeka_zone, financials, province_name, province_avg_score, lat, lon } = detailScore

  return (
    <div className="w-80 flex-shrink-0 glass-panel m-4 rounded-2xl flex flex-col overflow-hidden z-40 shadow-2xl">
      <div className="p-5 flex-1 overflow-y-auto space-y-5 scrollbar-hide">
        <div className="flex items-start justify-between">
          <div className="space-y-1">
            <div className="flex items-center gap-2 text-accent-wind">
              <MapPin size={14} />
              <h3 className="text-sm font-bold text-text-primary tracking-tight">
                {province_name || 'Seçili Nokta'}
              </h3>
            </div>
            <p className="text-[10px] font-mono text-text-muted tracking-wider">
              {lat.toFixed(4)}, {lon.toFixed(4)}
            </p>
          </div>
          <CircularScore score={score} />
        </div>

        <DynamicAnalysisHint score={score} breakdown={breakdown} energyType={energyType} />

        {province_avg_score != null && (
          <div className="p-3 bg-white/5 rounded-xl border border-glass-border flex gap-3 items-start">
            <Info size={14} className="text-accent-wind mt-0.5 flex-shrink-0" />
            <div className="space-y-0.5">
              <p className="text-[10px] leading-relaxed text-text-secondary">
                İl ortalaması <span className="text-text-primary font-bold">{Math.round(province_avg_score)}</span> iken bu koordinat <span className="text-text-primary font-bold">{Math.round(score)}</span> puan.
              </p>
              {score !== province_avg_score && (
                <div className="flex items-center gap-1 mt-1">
                  {score > province_avg_score ? (
                    <>
                      <ArrowUpRight size={12} className="text-score-high" />
                      <span className="text-[9px] text-score-high font-semibold">
                        Ortalamanın %{Math.round(((score - province_avg_score) / province_avg_score) * 100)} üzerinde
                      </span>
                    </>
                  ) : (
                    <>
                      <ArrowDownRight size={12} className="text-score-low" />
                      <span className="text-[9px] text-score-low font-semibold">
                        Ortalamanın %{Math.round(((province_avg_score - score) / province_avg_score) * 100)} altında
                      </span>
                    </>
                  )}
                </div>
              )}
            </div>
          </div>
        )}

        <div className="space-y-2">
          {explanation.highlights.map((h, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.1 }}
              className="flex items-center gap-2 text-[11px] text-score-high bg-score-high/5 p-2 rounded-lg border border-score-high/10"
            >
              <ShieldCheck size={14} />
              <span>{h}</span>
            </motion.div>
          ))}
          {explanation.warnings.map((w, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.1 + 0.2 }}
              className="flex items-center gap-2 text-[11px] text-score-low bg-score-low/5 p-2 rounded-lg border border-score-low/10"
            >
              <AlertCircle size={14} />
              <span>{w}</span>
            </motion.div>
          ))}
        </div>

        <div className="space-y-4">
          <div className="flex items-center gap-2 text-[10px] text-text-muted font-bold uppercase tracking-widest">
            <TrendingUp size={12} />
            <span>Parametre Analizi</span>
          </div>
          <div className="space-y-4">
            <ScoreBar label="Kaynak Potansiyeli" value={breakdown.resource_potential} icon={Zap} />
            <ScoreBar label="Arazi Verimliliği" value={breakdown.land_use} icon={Factory} />
            <ScoreBar label="Şebeke Yakınlığı" value={breakdown.grid_proximity} icon={Activity} />
            <ScoreBar label="Finansal Fizibilite" value={breakdown.economic_feasibility} icon={Wallet} />
            {breakdown.risk_factor != null && (
              <ScoreBar label="Risk Faktörü" value={1 - breakdown.risk_factor} icon={ShieldCheck} />
            )}
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex items-center justify-between text-[10px] text-text-muted font-bold uppercase tracking-widest">
            <span>48 Saatlik Tahmin</span>
            <div className="flex items-center gap-1 text-[8px] text-text-muted">
              <div className="w-2 h-2 rounded-full bg-accent-wind" />
              <span>MW</span>
            </div>
          </div>
          <div className="h-32 -mx-2">
            <ForecastChart key={`${lat},${lon}`} lat={lat} lon={lon} energyType={energyType} />
          </div>
        </div>

        {financials && (
          <div className="bg-bg-secondary border border-glass-border rounded-xl p-4 space-y-3 shadow-inner">
            <div className="flex items-center gap-2 text-[10px] text-text-muted font-bold uppercase tracking-widest mb-1">
              <Wallet size={12} className="text-accent-solar" />
              <span>Yatırım Öngörüsü</span>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-[9px] text-text-muted uppercase">CAPEX</p>
                <p className="text-sm font-mono font-bold text-text-primary">
                  {(financials.capex_tl / 1_000_000).toFixed(1)}<span className="text-[10px] ml-0.5">M TL</span>
                </p>
              </div>
              <div>
                <p className="text-[9px] text-text-muted uppercase">Geri Ödeme</p>
                <p className="text-sm font-mono font-bold text-accent-solar">
                  {financials.payback_years.toFixed(1)}<span className="text-[10px] ml-0.5">Yıl</span>
                </p>
              </div>
            </div>
            <p className="text-[9px] text-text-muted italic border-t border-glass-border pt-2 leading-tight">
              {financials.disclaimer}
            </p>
          </div>
        )}
      </div>

      {isCompareMode && (
        <div className="p-4 bg-bg-secondary border-t border-glass-border">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => addComparePoint({ lat, lon })}
            className="w-full flex items-center justify-center gap-2 py-3 bg-accent-hybrid text-white rounded-xl text-sm font-bold shadow-lg shadow-accent-hybrid/20 hover:scale-[1.02] active:scale-[0.98] transition-all"
          >
            <Plus size={18} />
            Karşılaştırmaya Ekle
          </motion.button>
        </div>
      )}
    </div>
  )
}
