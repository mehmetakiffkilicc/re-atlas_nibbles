---
title: "Feature Freeze"
tags: [concept, proje-yonetim, kapsam]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active
---

# Feature Freeze

Hackathon'un 12. saatinde Architect subagent tarafından zorlanan kural: **yeni özellik eklenmez, sadece bug fix yapılır.**

## Gerekçe

- 25 saatlik hackathon'da entegrasyon ve cila için yeterli süre bırakmak
- Kapsam genişlemesini (scope creep) engellemek
- Demo akışının çalışır hale getirilmesine öncelik vermek

## Takvim

| Saat | Durum |
|---|---|
| 0-12 | Geliştirme serbet |
| **12** | **Feature freeze başlar** |
| 12-24 | Sadece entegrasyon + bug fix + UX cila |
| 24-25 | Buffer |

## Uygulama

Architect subagent 12. saatte tüm subagentlara freeze sinyali verir. Kapsam dışı talepler reddedilir.

## Sources

- [[sources/docs/2026-05-02-project-context.md]]

## Related

- [[decisions/karar-feature-freeze-12saat]]
- [[concepts/multi-agent-strateji]]
