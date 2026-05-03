---
title: "Demo Koordinatları"
tags: [entity, demo, test]
source: sources/docs/2026-05-02-hackathon-plani.md
date: 2026-05-02
status: active
---

# Demo Koordinatları

Önceden seçilmiş, görsel olarak çarpıcı test ve demo koordinatları.

## Demo için "Altın Koordinatlar"

| Lokasyon | Koordinat | Beklenen Sonuç |
|---|---|---|
| Karacabey / Bursa | 40.213°N, 28.366°E | Yüksek rüzgar skoru |
| Kayseri merkez | 38.733°N, 35.485°E | Yüksek güneş skoru |
| Tuz Gölü kıyısı | 38.737°N, 33.371°E | Hibrit — yüksek |

## Skor Doğrulama Koordinatları

| Lokasyon | Koordinat | Beklenen Sonuç |
|---|---|---|
| Çamlıca / İstanbul | 41.025°N, 29.066°E | Düşük (yerleşim alanı) |
| Çatalca ormanı | 41.218°N, 28.450°E | Düşük (orman) |

## Kullanım

- Unit test için hardcoded input/output validation
- Demo akışında sırayla kullanılır (Karacabey → rüzgar → Top5 → tahmin)
- Demo gecesi önceden bu koordinatlar için yanıtlar `demo_weather.json`'a yazılır

## Sources

- [[sources/docs/2026-05-02-hackathon-plani.md]]

## Related

- [[concepts/demo-mode]]
- [[entities/sqlite-cache]]
