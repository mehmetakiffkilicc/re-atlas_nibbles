import { useEffect } from 'react'
import { useAppStore } from '../store/useAppStore'
import { getScore } from '../api/client'
import type { ScoreResponse } from '../types'

function ScoreColumn({ s, label }: { s: ScoreResponse; label: string }) {
  const color = s.score >= 70 ? '#22C55E' : s.score >= 40 ? '#FACC15' : '#EF4444'
  return (
    <div className="flex-1 space-y-2">
      <div className="text-center">
        <div className="text-xs text-text-muted">{label}</div>
        <div className="text-2xl font-bold font-mono" style={{ color }}>{Math.round(s.score)}</div>
        <div className="text-xs text-text-muted">{s.province_name || `${s.lat.toFixed(3)}, ${s.lon.toFixed(3)}`}</div>
      </div>
      {(['resource_potential', 'land_use', 'grid_proximity', 'risk_factor', 'economic_feasibility'] as const).map((k) => {
        const v = Math.round(s.breakdown[k] * 100)
        const barColor = v >= 70 ? '#22C55E' : v >= 40 ? '#FACC15' : '#EF4444'
        return (
          <div key={k} className="space-y-0.5">
            <div className="flex justify-between text-xs">
              <span className="text-text-muted capitalize">{k.replace(/_/g, ' ')}</span>
              <span className="font-mono" style={{ color: barColor }}>{v}</span>
            </div>
            <div className="h-1.5 bg-bg-primary rounded-full">
              <div className="h-full rounded-full" style={{ width: `${v}%`, backgroundColor: barColor }} />
            </div>
          </div>
        )
      })}
    </div>
  )
}

export function CompareView() {
  const { comparePoints, compareResults, setCompareResults, clearCompare, energyType, isCompareMode } = useAppStore()

  useEffect(() => {
    if (comparePoints && isCompareMode) {
      Promise.all([
        getScore(comparePoints[0].lat, comparePoints[0].lon, energyType),
        getScore(comparePoints[1].lat, comparePoints[1].lon, energyType),
      ]).then(([a, b]) => {
        setCompareResults({
          score_a: a,
          score_b: b,
          winner: a.score > b.score ? 'a' : b.score > a.score ? 'b' : 'tie',
          delta: Math.abs(a.score - b.score),
        })
      })
    }
  }, [comparePoints, isCompareMode, energyType])

  if (!compareResults) return null

  const { score_a, score_b, winner, delta } = compareResults
  const winnerLabel = winner === 'a' ? score_a.province_name || 'Nokta A' : winner === 'b' ? score_b.province_name || 'Nokta B' : null

  return (
    <div className="absolute inset-0 z-[2000] flex items-center justify-center bg-black/50">
      <div className="bg-bg-card border border-border-subtle rounded-2xl shadow-2xl w-[560px] max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between px-6 py-4 border-b border-border-subtle">
          <div>
            <div className="text-base font-semibold text-text-primary">Karşılaştırma</div>
            {winnerLabel && (
              <div className="text-xs text-score-high">
                ✓ {winnerLabel} kazanıyor (+{delta.toFixed(1)} puan)
              </div>
            )}
            {winner === 'tie' && <div className="text-xs text-score-medium">Beraberlik</div>}
          </div>
          <button onClick={clearCompare} className="text-text-muted hover:text-text-primary text-2xl leading-none">×</button>
        </div>
        <div className="flex gap-6 px-6 py-4">
          <ScoreColumn s={score_a} label="Nokta A" />
          <div className="w-px bg-border-subtle flex-shrink-0" />
          <ScoreColumn s={score_b} label="Nokta B" />
        </div>
      </div>
    </div>
  )
}
