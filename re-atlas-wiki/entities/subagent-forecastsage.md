---
title: "Subagent: ForecastSage"
tags: [entity, subagent, multi-agent, tahmin]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active
---

# Subagent: ForecastSage

48 saatlik üretim tahmini ve bakım penceresi öneri modülünü yazan subagent. **LSTM'e kesinlikle dokunmaz.**

## Sorumluluk

- `backend/app/forecast/physics_forecast.py` — fizik tabanlı tahmin
- `backend/app/forecast/prophet_wrapper.py` — Prophet entegrasyonu (opsiyonel)
- `backend/app/forecast/maintenance_window.py` — bakım penceresi önerisi

## Başlangıç Saati

8. saat

## Yetki Sınırı

- LSTM kodu **kesinlikle** yazmaz (3 model hemfikir, kapsam dışı)
- Prophet opsiyonel: sadece zaman kalırsa aktive edilir

## Çıktı

- 48 saatlik üretim tahmini, ±%15 belirsizlik bantlı
- Tek satır bakım penceresi önerisi (örn: "Yarın 14:00-17:00 düşük üretim — bakım için uygun")

## Sources

- [[sources/docs/2026-05-02-project-context.md]]

## Related

- [[concepts/physics-based-forecast]]
- [[decisions/karar-prophet-vs-lstm]]
- [[concepts/multi-agent-strateji]]
