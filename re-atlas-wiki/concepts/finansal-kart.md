---
title: "Finansal Kart"
tags: [concept, ux, finans, detay-panel]
source: sources/docs/2026-05-02-hackathon-plani.md
date: 2026-05-02
status: active
---

# Finansal Kart

Detay panelinin alt bölümünde gösterilen ön değerlendirme finansal özeti. Maliyet koordinatörü / finans uzmanı personasına hizmet eder.

## İçerik

| Satır | Değer | Açıklama |
|---|---|---|
| CAPEX (tahmini) | ~X TL | `CAPEX_SOLAR = 15.000 TL/kWp`, `CAPEX_WIND = 45.000 TL/kW` |
| Yıllık üretim | ~X GWh | Capacity factor × sistem kapasitesi |
| Geri ödeme | ~X yıl | `capex / (yıllık_gelir - yıllık_opex)` |
| LCOE | X TL/kWh | Basitleştirilmiş formül (25 yıl, %10 iskonto) |

## Sabit Varsayımlar (V1)

```python
CAPEX_SOLAR_TL_PER_KWP = 15_000
CAPEX_WIND_TL_PER_KW   = 45_000
ELECTRICITY_PRICE_TL_KWH = 2.5   # YEKDEM + serbest piyasa ortalaması
ANNUAL_OPEX_RATIO = 0.02          # CAPEX'in %2'si
SYSTEM_LIFETIME_YEARS = 25
DISCOUNT_RATE = 0.10
```

## Zorunlu Disclaimer

> "Ön değerlendirme amaçlıdır. Gerçek yatırım kararları için detaylı fizibilite gereklidir."

## Sorumluluk

[[entities/subagent-scoresmith]] → `economic.py` — hesaplama
[[entities/subagent-mapforge]] → `DetailPanel.tsx` — gösterim

## Sources

- [[sources/docs/2026-05-02-hackathon-plani.md]]

## Related

- [[concepts/skor-motoru]]
- [[entities/frontend-map]]
