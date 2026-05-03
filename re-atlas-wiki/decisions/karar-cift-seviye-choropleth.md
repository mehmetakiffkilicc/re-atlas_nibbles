---
title: "Karar: Çift Seviye Gerçek Choropleth (Fake Heatmap Yasak)"
tags: [decision, harita, veri-kalitesi]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active
---

# Karar: Çift Seviye Gerçek Choropleth (Fake Heatmap Yasak)

**Karar:** Zoom out → 81 il choropleth, zoom in → ~973 ilçe choropleth. PNG overlay/fake heatmap kesinlikle yasak.

## Alternatiflerin Değerlendirmesi

| Yaklaşım | Karar | Neden |
|---|---|---|
| (A) Sadece il bazlı | ❌ | Yetersiz granülarite |
| (B) Grid heatmap (5×5km) | ❌ | ~30.000 hücre, performans sorunu |
| (C) Çift seviye gerçek choropleth | ✅ | Etkileyici + güvenilir |
| Fake heatmap (PNG overlay) | ❌ | Güven kaybı riski |

## Fake Heatmap Neden Reddedildi

GPT uyardı: Kullanıcı kırmızı bölgeye tıklayıp yeşil skor görürse güven kaybı yaşanır. Gerçek hesaplanmış veri dışında hiçbir görsel kullanılmaz.

## Tutarlılık Çözümü

İl genel skoru ile koordinat skoru arasındaki fark için detay panelinde zorunlu açıklama cümlesi:
> "İl genel skoru: 72 / Bu nokta: 84 — fark mikro-koşullar ve şebeke yakınlığından kaynaklanıyor."

## Sources

- [[sources/docs/2026-05-02-project-context.md]]

## Related

- [[concepts/choropleth-map]]
- [[entities/leaflet-map]]
