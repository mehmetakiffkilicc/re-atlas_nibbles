import { useEffect, useState } from 'react'
import { ComposedChart, Area, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import { getForecast } from '../api/client'
import type { EnergyType, ForecastPoint } from '../types'

interface Props { lat: number; lon: number; energyType: EnergyType }

const TYPE_COLOR: Record<EnergyType, string> = {
  solar: '#F59E0B', wind: '#3B82F6', hybrid: '#8B5CF6'
}

export function ForecastChart({ lat, lon, energyType }: Props) {
  const [points, setPoints] = useState<ForecastPoint[]>([])
  const color = TYPE_COLOR[energyType]

  useEffect(() => {
    getForecast(lat, lon, energyType).then((r) => setPoints(r.points.slice(0, 24)))
  }, [lat, lon, energyType])

  if (!points.length) return <div className="h-32 flex items-center justify-center text-text-muted text-sm">Yükleniyor…</div>

  const data = points.map((p) => ({
    time: new Date(p.timestamp).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }),
    expected: Math.round(p.expected_kw),
    lower: Math.round(p.lower_kw),
    upper: Math.round(p.upper_kw),
  }))

  return (
    <ResponsiveContainer width="100%" height={120}>
      <ComposedChart data={data} margin={{ top: 4, right: 4, left: -20, bottom: 0 }}>
        <XAxis dataKey="time" tick={{ fill: '#94A3B8', fontSize: 10 }} tickLine={false} interval={5} />
        <YAxis tick={{ fill: '#94A3B8', fontSize: 10 }} tickLine={false} />
        <Tooltip
          contentStyle={{ background: '#162035', border: '1px solid #1E2D45', borderRadius: 6, fontSize: 12 }}
          labelStyle={{ color: '#94A3B8' }}
          itemStyle={{ color: '#F1F5F9' }}
          formatter={(v: number) => [`${v} kW`, '']}
        />
        <Area
          type="monotone" dataKey="upper" stroke="transparent"
          fill={color} fillOpacity={0.15} name="Üst sınır"
        />
        <Area
          type="monotone" dataKey="lower" stroke="transparent"
          fill={color} fillOpacity={0} name="Alt sınır"
        />
        <Line
          type="monotone" dataKey="expected" stroke={color}
          strokeWidth={2} dot={false} name="Beklenen (kW)"
        />
      </ComposedChart>
    </ResponsiveContainer>
  )
}
