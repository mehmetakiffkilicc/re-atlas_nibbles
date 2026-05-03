---
title: "Multi-Agent Geliştirme Stratejisi"
tags: [concept, multi-agent, claude-code, proje-yonetim]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active
---

# Multi-Agent Geliştirme Stratejisi

Claude Code üzerinde 1 orkestratör + 6 subagent yapısıyla paralel geliştirme.

## Yapı

**Orkestratör: Architect**
- Subagentları sırayla başlatır
- Tip uyumsuzluğunda müdahale eder
- 12. saatte feature freeze'i zorlar
- Kapsam dışı talepleri reddeder

**Subagentlar:**

| # | Ad | Klasör | Başlangıç |
|---|---|---|---|
| 1 | [[entities/subagent-schemasmith\|SchemaSmith]] | `/contracts/` | 0. saat |
| 2 | [[entities/subagent-dataforager\|DataForager]] | `/data-pipeline/` | 0. saat (paralel) |
| 3 | [[entities/subagent-scoresmith\|ScoreSmith]] | `/backend/app/scoring/` | 2. saat |
| 4 | [[entities/subagent-apiweaver\|APIWeaver]] | `/backend/app/` | 4. saat |
| 5 | [[entities/subagent-mapforge\|MapForge]] | `/frontend/` | 4. saat (paralel) |
| 6 | [[entities/subagent-forecastsage\|ForecastSage]] | `/backend/app/forecast/` | 8. saat |

## Subagent Çağırma Şablonu

```
Sen [SUBAGENT_ADI] subagent'isin. Kapsam dışına çıkmak YASAKTIR.
Çalışma klasörün: [KLASÖR]
Bağımlılıkların: [LİSTE]
Çıktı dosyaların: [LİSTE]
Kapatma kriterin: [KRİTER]
Master plan: docs/PROJECT_CONTEXT.md
```

## Detay

Detaylı orkestrasyon promptu: `raw/docs/master-prompt.md`

## Sources

- [[sources/docs/2026-05-02-project-context.md]]

## Related

- [[concepts/feature-freeze]]
- [[entities/subagent-schemasmith]]
- [[entities/subagent-dataforager]]
- [[entities/subagent-scoresmith]]
- [[entities/subagent-apiweaver]]
- [[entities/subagent-mapforge]]
- [[entities/subagent-forecastsage]]
