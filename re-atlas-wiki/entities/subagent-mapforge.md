---
title: "Subagent: MapForge"
tags: [entity, subagent, multi-agent, frontend]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active
---

# Subagent: MapForge

React + Leaflet UI bileşenlerini yazan subagent. **UI yazar, hesaplama yapmaz.**

## Sorumluluk

- `frontend/src/` altındaki tüm bileşenler
- Leaflet choropleth katmanları (il + ilçe)
- Filtre paneli, detay paneli, karşılaştırma görünümü
- Zustand store yapısı
- API istemcisi (`api/client.ts`)
- Mock data yapısı

## Başlangıç Saati

4. saat (APIWeaver ile paralel)

## Yetki Sınırı

- Frontend kodu yazar, backend koda dokunmaz
- Hesaplama mantığı içermez, API'den veri çeker

## Sources

- [[sources/docs/2026-05-02-project-context.md]]

## Related

- [[entities/frontend-map]]
- [[entities/subagent-apiweaver]]
- [[concepts/choropleth-map]]
- [[concepts/multi-agent-strateji]]
