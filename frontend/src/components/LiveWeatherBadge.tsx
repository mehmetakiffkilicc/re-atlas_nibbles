import { useEffect, useState } from 'react'
import { Wind, Sun, Thermometer } from 'lucide-react'
import { useAppStore } from '../store/useAppStore'
import { getLiveWeather } from '../api/client'

export function LiveWeatherBadge() {
  const { energyType, liveWeather, setLiveWeather, selectedPoint } = useAppStore()
  const [fetching, setFetching] = useState(false)

  useEffect(() => {
    if (!selectedPoint) return
    let cancelled = false
    setFetching(true)
    getLiveWeather(selectedPoint.lat, selectedPoint.lon, energyType).then((w) => {
      if (!cancelled && w) setLiveWeather(w)
      setFetching(false)
    }).catch(() => { setFetching(false) })
    return () => { cancelled = true }
  }, [selectedPoint, energyType])

  if (!liveWeather && !fetching) return null

  if (fetching) {
    return (
      <div className="absolute top-4 left-1/2 -translate-x-1/2 z-[1000] glass-panel rounded-xl px-4 py-2 flex items-center gap-3">
        <div className="w-3 h-3 rounded-full border-2 border-accent-wind border-t-transparent animate-spin" />
        <span className="text-[11px] text-text-secondary font-medium">Canlı veri alınıyor...</span>
      </div>
    )
  }

  if (!liveWeather) return null

  const { wind_speed_ms, ghi_w_m2, temperature_c } = liveWeather

  return (
    <div className="absolute top-4 left-1/2 -translate-x-1/2 z-[1000] glass-panel rounded-xl px-4 py-2.5 flex items-center gap-4 border border-white/10 shadow-2xl animate-fade-in">
      <div className="flex items-center gap-2">
        <div className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
        <span className="text-[10px] text-green-400 font-bold uppercase tracking-wider">Canlı</span>
      </div>

      {(energyType === 'wind' || energyType === 'hybrid') && (
        <div className="flex items-center gap-1.5">
          <Wind size={12} className="text-accent-wind" />
          <span className="text-xs text-text-primary font-mono">{wind_speed_ms.toFixed(1)}</span>
          <span className="text-[9px] text-text-muted">m/s</span>
        </div>
      )}

      {(energyType === 'solar' || energyType === 'hybrid') && (
        <div className="flex items-center gap-1.5">
          <Sun size={12} className="text-accent-solar" />
          <span className="text-xs text-text-primary font-mono">{ghi_w_m2.toFixed(0)}</span>
          <span className="text-[9px] text-text-muted">W/m²</span>
        </div>
      )}

      <div className="flex items-center gap-1.5">
        <Thermometer size={12} className="text-orange-400" />
        <span className="text-xs text-text-primary font-mono">{temperature_c.toFixed(1)}</span>
        <span className="text-[9px] text-text-muted">°C</span>
      </div>
    </div>
  )
}
