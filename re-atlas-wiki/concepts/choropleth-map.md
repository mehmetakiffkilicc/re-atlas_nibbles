---
title: "Choropleth Harita"
tags: [concept, harita, gorsellestirme]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active
---

# Choropleth Harita

Bölgelerin renk yoğunluğuyla veri değerini temsil eden harita türü. RE-ATLAS'ta uygunluk skorunu görselleştirmek için kullanılır.

## RE-ATLAS'ta Kullanım

**Çift seviye gerçek choropleth:**
- Zoom out → 81 il, her il bir renk (skor 0-100)
- Zoom in → ~973 ilçe, daha granüler skor
- Geçiş: 300 ms cross-fade animasyonu
- 3 mod: Solar / Rüzgar / Hibrit (mod değişince harita yeniden renklenir)

## Renk Skalası

- `#22C55E` — Yüksek uygunluk (≥70)
- `#FACC15` — Orta uygunluk (40-69)
- `#EF4444` — Düşük uygunluk (<40)

## Neden Fake Heatmap Reddedildi

GPT uyardı: PNG overlay ile fake heatmap'te kullanıcı kırmızı bölgeye tıklayıp yeşil skor görürse güven kaybı yaşanır. Karar: **sadece gerçek hesaplanmış skorlar gösterilir.**

## Tutarlılık Sorunu

İl genel skoru ile o ildeki belirli bir koordinatın skoru farklı olabilir (mikro-koşullar). Çözüm: detay panelinde zorunlu açıklama cümlesi:
> "İl genel skoru: 72 / Bu nokta: 84 — fark mikro-koşullar ve şebeke yakınlığından kaynaklanıyor."

## Sources

- [[sources/docs/2026-05-02-project-context.md]]

## Related

- [[entities/leaflet-map]]
- [[entities/frontend-map]]
- [[decisions/karar-cift-seviye-choropleth]]
