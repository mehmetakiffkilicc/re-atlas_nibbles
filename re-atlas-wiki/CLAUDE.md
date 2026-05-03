# RE-ATLAS Wiki — Şema ve Anayasa

## Amaç

Bu vault, **RE-ATLAS** (Renewable Energy Decision Support System) projesinin kalıcı bilgi arşividir. RE-ATLAS, Türkiye genelinde yenilenebilir enerji yatırım kararlarını destekleyen bir karar destek sistemidir (solar/rüzgar/hibrit harita, 48 saatlik tahmin, yatırım analizi).

Bu wiki şunları korur:
- Tüm mimari kararlar ve gerekçeleri
- Servis/modül/API varlık bilgisi
- Teknik kavramlar ve terimler
- Geliştirme sorunları ve çözümleri
- Üst düzey sentez ve analiz sayfaları

**Kullanım modeli:** Yeni bir Claude oturumu başladığında ajan önce `index.md`'yi okur, ardından ilgili sayfaları yükleyerek tam bağlamla çalışmaya başlar. Sohbet geçmişine bağımlılık ortadan kalkar.

---

## Dil

Tüm wiki sayfaları **Türkçe** yazılır. Teknik terimler, kod sembolleri (fonksiyon/değişken/dosya adları), kütüphane ve servis isimleri İngilizce kalabilir.

---

## Klasör Yapısı

```
re-atlas-wiki/
├── CLAUDE.md           ← Bu dosya. Şema ve anayasa. Ajan her operasyonda okur.
├── index.md            ← Tüm wiki sayfalarının kataloğu. Query'de ilk okunur.
├── log.md              ← Append-only olay kaydı. Her operasyon buraya yazılır.
├── raw/                ← Ham kaynaklar. ASLA DEĞİŞTİRİLMEZ.
│   ├── docs/           ← Proje dokümanları (PROJECT_CONTEXT, plan, promptlar)
│   ├── sessions/       ← Claude Code oturum notları ve transkriptler
│   └── assets/         ← Resimler, PDF'ler, diyagramlar
├── sources/            ← Her ham kaynak için bir özet sayfası
│   └── docs/           ← raw/docs/ kaynaklarının özetleri
├── entities/           ← Somut varlıklar: servisler, modüller, API endpoint'leri, dosyalar
├── concepts/           ← Soyut kavramlar: mimari desenler, teknik terimler, metodolojiler
├── decisions/          ← Atomik kararlar (her karar = tek sayfa)
├── issues/             ← Sorunlar ve çözümleri (kök neden + fix)
├── syntheses/          ← Üst düzey sentez ve analiz sayfaları
└── archive/            ← Eskimiş sayfalar. Asla silinmez, buraya taşınır.
```

### Klasör kuralları

| Klasör | İçerir | İçermez |
|---|---|---|
| `raw/` | Orijinal, değiştirilmemiş kaynaklar | Ajan tarafından üretilen hiçbir şey |
| `sources/` | Her raw kaynak için 1 özet sayfası | Özgün analiz veya sentez |
| `entities/` | Projede somut olarak var olan şeyler | Soyut kavramlar |
| `concepts/` | Fikirler, desenler, metodolojiler | Tek bir servisi tanımlayan sayfalar |
| `decisions/` | "X yerine Y çünkü Z" kararları | Genel bilgi |
| `issues/` | Yaşanan sorunlar ve nasıl çözüldüğü | Henüz çözülmemiş sorunlar (bunlar `syntheses/` altında açık-konular olarak işaretlenir) |
| `syntheses/` | Birden fazla kaynağı birleştiren üst analiz | Tek kaynaktan gelen bilgi |
| `archive/` | Geçerliliğini yitirmiş sayfalar | Aktif bilgi |

---

## Sayfa Formatı

Her wiki sayfası şu yapıya uyar:

```markdown
---
title: "Sayfa Başlığı"
tags: [kategori, alt-kategori]
source: sources/docs/2026-05-02-project-context.md
date: 2026-05-02
status: active   # active | stale | archived
---

# Sayfa Başlığı

[İçerik — birden fazla paragraf, liste, tablo olabilir]

## Sources

- [[sources/docs/2026-05-02-project-context.md]] — proje bağlamı dokümanı
- [[sources/docs/2026-05-02-hackathon-plani.md]] — hackathon planı

## Related

- [[entities/backend-api]] — bu karardan etkilenen servis
- [[concepts/physics-based-forecast]] — ilgili kavram
```

### Frontmatter alanları

| Alan | Zorunlu | Açıklama |
|---|---|---|
| `title` | Evet | İnsan-okunabilir başlık |
| `tags` | Evet | En az 1 tag. Kategoriler: `entity`, `concept`, `decision`, `issue`, `synthesis`, `source` |
| `source` | Evet | Bu sayfanın dayandığı birincil kaynak(lar) |
| `date` | Evet | Sayfanın oluşturulma tarihi (YYYY-MM-DD) |
| `status` | Evet | `active` / `stale` / `archived` |

---

## Naming Kuralları

- **Dosya adları:** kebab-case, Türkçe karakter yok (`ş→s`, `ı→i`, `ğ→g`, `ü→u`, `ö→o`, `ç→c`)
- **Source sayfaları:** `YYYY-MM-DD-slug.md` (tarih öne, sonra içeriği tanımlayan kısa ad)
- **Karar sayfaları:** `karar-KONU.md` (örn. `karar-prophet-vs-lstm.md`)
- **Varlık sayfaları:** servis/modülün kod adı (örn. `backend-api.md`, `frontend-map.md`)
- **Kavram sayfaları:** kavramın adı (örn. `physics-based-forecast.md`, `choropleth-map.md`)
- **Issue sayfaları:** `issue-KONU.md` (örn. `issue-leaflet-performance.md`)

---

## INGEST Workflow

Yeni bir kaynak `raw/` altına eklendiğinde:

1. **Oku** — Kaynağın tamamını oku. Çıkar: ana konu, anahtar bulgular, bahsedilen varlıklar (servisler, modüller, API'ler, dosyalar), kavramlar, kararlar, sorunlar.
2. **Özet göster** — 5 maddelik özet kullanıcıya sun, onay iste (kontrollü modda).
3. **Source sayfası yaz** — `sources/<kategori>/YYYY-MM-DD-<slug>.md` dosyası oluştur:
   - YAML frontmatter
   - H1 başlık
   - **Amaç:** Kaynak ne hakkında?
   - **Ne yapıldı / Ne anlatılıyor**
   - **Anahtar noktalar** (madde listesi)
   - **Kararlar** (liste)
   - **Açık konular / Sorular** (liste)
   - **## Sources** bölümü
   - **## Related** bölümü
4. **Entity sayfaları** — Bahsedilen her somut varlık için `entities/` altında sayfa oluştur (yoksa) veya güncelle (varsa). Çift yönlü link kur.
5. **Decision sayfaları** — Her karar için `decisions/` altında atomik sayfa. Bir sayfada bir karar.
6. **Issue sayfaları** — Her sorun/öğrenilen ders için `issues/` altında sayfa (kök neden + fix + ilgili dosyalar).
7. **Concept sayfaları** — Her soyut kavram için `concepts/` altında sayfa oluştur veya güncelle.
8. **index.md güncelle** — İlgili kategori bölümlerine yeni sayfaları ekle.
9. **log.md'ye kayıt** — `## [YYYY-MM-DD] ingest | <slug>` + dokunulan dosyaların listesi.

### RE-ATLAS'a özgü INGEST notları

- `raw/docs/` içindeki kaynaklar: markdown dokümanlar (PROJECT_CONTEXT, hackathon planı, promptlar)
- `raw/sessions/` içindeki kaynaklar: Claude Code oturum notları veya JSONL transkriptleri
- Bir ingest 10-15 sayfaya dokunabilir — bu normaldir
- Çelişki tespit edilirse `## ÇELİŞKİ` başlığıyla işaretle, silme

---

## QUERY Workflow

Wiki'ye soru sorulduğunda:

1. `index.md`'yi oku — soruyla ilgili kategorileri belirle
2. İlgili sayfaları bul ve içerikleri oku (sources/, entities/, concepts/, decisions/, syntheses/)
3. Cevabı sentezle — **her önemli iddia için kaynak referansı ver** (hangi wiki sayfası, hangi raw kaynak)
4. Cevap yeni bir analiz/karşılaştırma içeriyorsa `syntheses/` veya `concepts/` altında geri-dosyala (filed-back)
5. Wiki'de cevap bulunamazsa: hangi bilginin eksik olduğunu söyle, hangi kaynak ingest edilmeli öner
6. `log.md`'ye kayıt: `## [YYYY-MM-DD] query | <kısa soru özeti>` — geri-dosyalama yapıldıysa dosya yolunu da belirt
7. Kullanıcıya cevabı ve oluşturulan/güncellenen sayfaları göster

---

## LINT Workflow

Periyodik sağlık kontrolü (haftalık önerilir):

Kontrol edilenler:
1. **Çelişkiler** — iki sayfa aynı konuda zıt iddialar içeriyor mu?
2. **Eskimiş iddialar** — son 30 günde eklenen kaynaklar mevcut sayfaları geçersiz kılmış mı?
3. **Yetim sayfalar** — hiçbir yerden `[[link]]` almayan sayfalar
4. **Eksik kavram sayfaları** — 3+ sayfada geçen ama kendi sayfası olmayan kavramlar
5. **Tek yönlü cross-reference'lar** — A→B var ama B'nin "Related" bölümünde A yok
6. **Zayıf kaynak sayfaları** — sadece tek raw kaynağa dayanan önemli iddialar

Bulgular `lint-report.md` dosyasına yazılır. **Otomatik düzeltme yapılmaz, sadece raporlanır.**

`log.md`'ye kayıt: `## [YYYY-MM-DD] lint | N bulgu (Ç:x E:y Y:z K:k T:t Z:z)`

---

## Hard Rules

1. **`raw/` immutable.** Ajan `raw/` içine asla yazmaz, değiştirmez. Sadece kullanıcı ekler/düzenler.
2. **Kaynaksız iddia yasak.** Her önemli cümle hangi raw dosyadan geldiğini belirtir.
3. **Çelişki silinmez, işaretlenir.** `## ÇELİŞKİ` başlığıyla görünür yere yaz, ileride çöz.
4. **Çift yönlü bağlantı.** Bir sayfayı güncellerken ona link veren diğer sayfaları da kontrol et.
5. **Her operasyon log'lanır.** Ingest, anlamlı query'ler ve lint pass'leri zaman damgalı `log.md`'ye gider.
6. **Sayfa silinmez, archive edilir.** Stale/hatalı sayfa önce `archive/` altına taşınır, sonra index güncellenir.
7. **Filed-back içerik atomik olur.** Query cevabı wiki'ye dosyalanırken tek "session özeti" değil, ayrık atomik sayfalar olarak yazılır (her biri tek bir fikir/sentez).
8. **Şema birlikte evrilir.** Bir kural çalışmıyorsa bu dosyayı güncelle. Sonraki oturumlarda yeni kural geçerli olur.

---

## RE-ATLAS Proje Özeti (hızlı bağlam)

**Proje:** Yenilenebilir enerji yatırım karar destek sistemi  
**Hedef kullanıcı:** Enerji yatırımcısı / saha geliştirme uzmanı (B2B)  
**Stack:** React 18 + Vite + TypeScript + Leaflet + TailwindCSS (frontend) / Python 3.11 + FastAPI + Pydantic v2 (backend) / SQLite (cache) / GeoJSON (statik veri)  
**Temel özellikler:**
- 81 il + ~973 ilçe düzeyinde çift-seviyeli choropleth harita (solar/rüzgar/hibrit)
- Koordinat bazlı anlık API sorgusu
- 48 saatlik üretim tahmini (±%15 belirsizlik bantları, fizik tabanlı + Prophet opsiyonel)
- Top-5 yatırım noktası önerisi
- Yan yana konum karşılaştırması
- Finansal kart (CAPEX, yıllık verim, geri ödeme süresi)

**Kapsam dışı:** LSTM, gerçek rota optimizasyonu, çoklu kullanıcı modu, geopolitik analiz, fake heatmap  
**Geliştirme modeli:** 1 orkestratör + 6 subajan (SchemaSmith, DataForager, ScoreSmith, APIWeaver, MapForge, ForecastSage)

---

## Şema Değişiklik Geçmişi

| Tarih | Değişiklik |
|---|---|
| 2026-05-02 | İlk versiyon oluşturuldu |
