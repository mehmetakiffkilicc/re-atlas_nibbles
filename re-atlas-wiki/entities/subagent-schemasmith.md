---
title: "Subagent: SchemaSmith"
tags: [entity, subagent, multi-agent]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active
---

# Subagent: SchemaSmith

Pydantic v2 ve TypeScript tip sözleşmelerini yazan subagent. **Sadece tip yazar, logic yazmaz.**

## Sorumluluk

- `contracts/schemas.py` — Pydantic v2 modelleri
- `contracts/schemas.ts` — TypeScript tipleri
- Tüm subagentlar için tek tip doğruluk kaynağı

## Başlangıç Saati

0. saat (ilk başlayan subagent)

## Yetki Sınırı

- Sadece `contracts/` klasöründe çalışır
- Business logic, endpoint, formül YAZMAz

## Sources

- [[sources/docs/2026-05-02-project-context.md]]

## Related

- [[concepts/multi-agent-strateji]]
- [[entities/subagent-apiweaver]]
- [[entities/subagent-scoresmith]]
