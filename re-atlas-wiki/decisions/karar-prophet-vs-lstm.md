---
title: "Karar: Prophet + Fizik Formülü (LSTM Reddedildi)"
tags: [decision, ml, tahmin]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active
---

# Karar: Prophet + Fizik Formülü (LSTM Reddedildi)

**Karar:** Ana tahmin modeli olarak Prophet + fizik formülü seçildi. LSTM kesinlikle kapsam dışı.

## Gerekçe

- 25 saatlik hackathon'da LSTM'i düzgün eğitmek için yeterli süre yok
- 3 model (Claude + GPT + Gemini) oybirliğiyle LSTM'i reddetti
- LSTM "gösterişli ama zayıf" sonuç riski taşır
- Prophet: hızlı, yorumlanabilir, makul doğruluk
- Fizik formülleri: açıklanabilir, data gerektirmez, tutarlı

## Kapsam

- Prophet opsiyonel: sadece zaman kalırsa aktive edilir
- ForecastSage subagentına yazılı kural: LSTM koduna dokunmaz

## Alternatiflerin Değerlendirmesi

| Yaklaşım | Karar | Neden |
|---|---|---|
| LSTM | ❌ Reddedildi | 25 saatte eğitilemez |
| XGBoost | ⚠️ Bahsedildi | Prophet + fizik yeterli |
| Prophet + fizik | ✅ Seçildi | Hızlı, yorumlanabilir |

## Sources

- [[sources/docs/2026-05-02-project-context.md]]

## Related

- [[concepts/physics-based-forecast]]
- [[entities/subagent-forecastsage]]
