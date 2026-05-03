---
title: "Tasarım Sistemi"
tags: [concept, ux, frontend, css]
source: sources/docs/2026-05-02-hackathon-plani.md
date: 2026-05-02
status: active
---

# Tasarım Sistemi

RE-ATLAS'ın UI tasarım dili. [[entities/subagent-mapforge]] bu sisteme uyarak çalışır.

## CSS Değişkenleri

```css
:root {
  --bg-primary:    #0B1220;   /* ana arka plan */
  --bg-secondary:  #111A2E;   /* panel arka planı */
  --bg-elevated:   #1A2540;   /* yükseltilmiş kart */

  --score-high:    #22C55E;   /* ≥70 */
  --score-medium:  #FACC15;   /* 40-69 */
  --score-low:     #EF4444;   /* <40 */

  --solar:         #F59E0B;
  --wind:          #3B82F6;
  --hybrid:        #A855F7;

  --text-primary:  #E5E7EB;
  --text-secondary:#9CA3AF;
  --border:        #1F2937;
  --accent:        #14B8A6;
}
```

## Tipografi

- UI: **Inter** (Google Fonts)
- Sayılar/kodlar: **JetBrains Mono** (Google Fonts)
- Boyutlar: 12(caption) / 14(body) / 16(default) / 20(h3) / 24(h2) / 32(h1) px

## Bileşen Stilleri

- Köşe yuvarlama: `rounded-2xl` (16px)
- Buton hover: `scale(1.02)` + glow efekti
- Geçişler: 200-300ms ease-out
- Gölge: sadece elevated kartlarda

## Harita

- Tile: CartoDB Dark Matter veya Stadia Maps Dark
- Choropleth geçiş animasyonu: 300ms cross-fade

## Performans Hedefleri

- FCP (First Contentful Paint): <1.5s
- TTI (Time to Interactive): <3s
- Harita zoom: 60fps
- API yanıt algısı: <500ms (loading skeleton ile)
- Bundle: <500KB gzipped

## Erişilebilirlik

- Renk körlüğü: yeşil/kırmızı yanına ikon (✓/✗)
- Kontrast: min 4.5:1 (WCAG AA)
- Klavye gezintisi: ESC panel kapatır, ok tuşları harita
- ARIA etiketleri kritik bileşenlerde

## Sources

- [[sources/docs/2026-05-02-hackathon-plani.md]]

## Related

- [[entities/frontend-map]]
- [[entities/subagent-mapforge]]
- [[concepts/choropleth-map]]
