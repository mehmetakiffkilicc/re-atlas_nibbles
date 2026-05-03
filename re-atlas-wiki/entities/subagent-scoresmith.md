---
title: "Subagent: ScoreSmith"
tags: [entity, subagent, multi-agent, skor]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active
---

# Subagent: ScoreSmith

Skor motoru ve fizik formüllerini yazan subagent. **Saf fonksiyon yazar, endpoint yazmaz.**

## Sorumluluk

- `backend/app/scoring/engine.py` — ana skor hesaplama
- `backend/app/scoring/physics.py` — rüzgar/güneş fizik formülleri
- `backend/app/scoring/landuse.py` — arazi uygunluk faktörü
- `backend/app/scoring/grid_proximity.py` — şebeke yakınlığı
- `backend/app/scoring/weights.py` — persona ağırlıkları

## Başlangıç Saati

2. saat

## Yetki Sınırı

- `backend/app/scoring/` klasöründe çalışır
- API endpoint yazmaz, formülleri UIWeaver'a bırakır

## Sources

- [[sources/docs/2026-05-02-project-context.md]]

## Related

- [[concepts/skor-motoru]]
- [[concepts/multi-agent-strateji]]
- [[entities/subagent-apiweaver]]
