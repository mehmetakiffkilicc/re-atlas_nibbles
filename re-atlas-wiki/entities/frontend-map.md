---
title: "Frontend Harita Uygulaması"
tags: [entity, frontend, react, leaflet]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active
---

# Frontend Harita Uygulaması

React 18 + Vite + TypeScript + TailwindCSS + Leaflet ile yazılan web uygulaması.

## Teknoloji

| Araç | Amaç |
|---|---|
| React 18 + Vite | UI framework + build tool |
| TypeScript | Tip güvenliği |
| TailwindCSS | Stil |
| Leaflet + react-leaflet | İnteraktif harita |
| Zustand | State management |
| Recharts | 48 saatlik tahmin grafiği |

## Bileşenler

- `MapCanvas.tsx` — Ana harita kapsayıcısı
- `ProvinceLayer.tsx` — 81 il choropleth katmanı
- `DistrictLayer.tsx` — ~973 ilçe choropleth katmanı
- `FilterPanel.tsx` — Sol filtre paneli
- `DetailPanel.tsx` — Sağ detay paneli (tıklamada açılır)
- `CompareView.tsx` — İki nokta karşılaştırma
- `TopFiveCard.tsx` — En iyi 5 nokta listesi
- `EnergyTypeToggle.tsx` — Solar / Rüzgar / Hibrit düğmesi
- `ForecastChart.tsx` — Belirsizlik bantlı tahmin grafiği
- `Legend.tsx` — Renk skalası açıklaması

## Tasarım Kararları

- Harita teması: CartoDB Dark Matter veya Stadia Maps Dark
- Arkaplan: `#0B1220`, Panel: `#111A2E`
- Yüksek skor: `#22C55E`, Orta: `#FACC15`, Düşük: `#EF4444`
- Tipografi: Inter (UI) + JetBrains Mono (sayılar)
- Layout: sol filtre paneli | merkez harita | sağ detay paneli

## Sources

- [[sources/docs/2026-05-02-project-context.md]]

## Related

- [[entities/backend-api]]
- [[entities/subagent-mapforge]]
- [[concepts/choropleth-map]]
