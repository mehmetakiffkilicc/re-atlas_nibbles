---
title: "Fizik Tabanlı Tahmin"
tags: [concept, tahmin, ml, fizik]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active
---

# Fizik Tabanlı Tahmin

LSTM yerine seçilen tahmin yaklaşımı. Fizik formülleri + Prophet (opsiyonel) ile 48 saatlik üretim tahmini üretir.

## Formüller

**Rüzgar gücü (kW):**
```
P_wind = 0.5 × ρ × A × v³ × Cp
```
- ρ = 1.225 kg/m³ (hava yoğunluğu, sabit)
- Cp = 0.4 (Betz limiti pratik değeri)
- A = π × r² (rotor süpürme alanı)
- v = rüzgar hızı (Open-Meteo'dan)

**Güneş üretimi (kWh/gün):**
```
E_solar = GHI × panel_area × panel_efficiency × performance_ratio
```
- panel_efficiency ≈ 0.18
- performance_ratio ≈ 0.80
- GHI = Global Horizontal Irradiance (Open-Meteo'dan)

**Capacity factor (rüzgar):**
```
CF = Σ P(v_t) / (P_rated × n_hours)
```

**Belirsizlik bandı:** ±%15 rule-based (sabit varsayım).

## Prophet Entegrasyonu

Prophet opsiyonel — sadece zaman kalırsa aktive edilir. Ana tahmin fizik formüllerine dayanır.

## Neden LSTM Reddedildi

- 3 model (Claude + GPT + Gemini) oybirliğiyle reddetti
- 25 saatte düzgün eğitim yapılamaz
- "Gösterişli ama zayıf" sonuç riski
- Detay: [[decisions/karar-prophet-vs-lstm]]

## Sources

- [[sources/docs/2026-05-02-project-context.md]]

## Related

- [[entities/subagent-forecastsage]]
- [[entities/open-meteo-service]]
- [[decisions/karar-prophet-vs-lstm]]
