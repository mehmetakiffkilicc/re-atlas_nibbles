---
title: "Skor Motoru"
tags: [concept, skor, algoritma, backend]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active
---

# Skor Motoru

RE-ATLAS'ın merkezi hesaplama birimi. Her koordinat için 0-100 uygunluk skoru üretir.

## Ana Formül

```
Uygunluk_Skoru = w1·KaynakPotansiyeli
               + w2·AraziUygunluğu
               + w3·ŞebekeYakınlığı
               + w4·RiskFaktörü     (negatif)
               + w5·EkonomikFizibilite
```

## Bileşenler

| Bileşen | Kaynak | V1 Durumu |
|---|---|---|
| KaynakPotansiyeli | Open-Meteo (GHI / rüzgar hızı) | Hesaplanır |
| AraziUygunluğu | OSM landuse (0=orman/SİT, 0.3=tarım, 1=çorak) | Hesaplanır |
| ŞebekeYakınlığı | OSM power (5km=1, 50km=0, lineer) | Hesaplanır |
| RiskFaktörü | Deprem+heyelan+sel | **Sabit varsayım** |
| EkonomikFizibilite | Arazi maliyeti proxy + LCOE | **Sabit varsayım** |

## Ağırlıklar (Persona Bazlı)

| Persona | w1 | w2 | w3 | w4 | w5 |
|---|---|---|---|---|---|
| Yatırımcı (varsayılan) | 0.4 | 0.2 | 0.3 | 0.05 | 0.05 |
| Bireysel (filtre) | 0.3 | 0.1 | 0.05 | 0.05 | 0.5 |

V1'de yalnızca w1, w2, w3 hesaplanır. w4 ve w5 sabittir.

## Sorumluluk

[[entities/subagent-scoresmith]] tarafından `backend/app/scoring/` altında yazılır.

## Sources

- [[sources/docs/2026-05-02-project-context.md]]

## Related

- [[entities/subagent-scoresmith]]
- [[entities/backend-api]]
- [[concepts/physics-based-forecast]]
