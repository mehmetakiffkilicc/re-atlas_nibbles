---
title: "Subagent: APIWeaver"
tags: [entity, subagent, multi-agent, backend]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active
---

# Subagent: APIWeaver

FastAPI endpoint'leri ve Open-Meteo entegrasyonunu yazan subagent. **Endpoint yazar, formül değiştirmez.**

## Sorumluluk

- `backend/app/routers/` — tüm API endpoint'leri
- `backend/app/services/openmeteo.py` — Open-Meteo API istemcisi
- `backend/app/services/cache.py` — SQLite cache servisi
- `backend/app/services/landuse_lookup.py`
- `backend/app/services/substation_lookup.py`
- `backend/app/main.py` — FastAPI uygulama başlatma

## Başlangıç Saati

4. saat (ScoreSmith kontratları hazır olduktan sonra)

## Yetki Sınırı

- `scoring/` klasöründeki formülleri değiştirmez
- ScoreSmith'in yazdığı fonksiyonları çağırır

## Sources

- [[sources/docs/2026-05-02-project-context.md]]

## Related

- [[entities/backend-api]]
- [[entities/subagent-scoresmith]]
- [[concepts/multi-agent-strateji]]
