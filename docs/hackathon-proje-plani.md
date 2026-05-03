# HACKATHON PROJE PLANI — RE-ATLAS

> **Bu dosyanın amacı:** Projenin detaylı planlama dokümanı. `PROJECT_CONTEXT.md` daha kompakt bir özet sunar; bu dosya **kararların arkasındaki gerekçeleri**, **alternatif değerlendirmeleri** ve **uygulama detaylarını** barındırır.
>
> **Hedef okuyucu:** Ekip üyeleri, jüri (sunum öncesi), gelecekteki bakım yapanlar.
>
> **İlgili dosyalar:**
> - `PROJECT_CONTEXT.md` (kök dizin) — özet bağlam, model değişimi için
> - `claude-code-master-prompt.md` — Claude Code orkestrasyon promptu
> - `MODEL_CARD.md` — ML model dokümantasyonu (uygulama sırasında yazılacak)

---

## İÇİNDEKİLER

1. [Yönetici Özeti](#1-yönetici-özeti)
2. [Yarışma Bağlamı](#2-yarışma-bağlamı)
3. [Problem Tanımı](#3-problem-tanımı)
4. [Çözüm Konsepti](#4-çözüm-konsepti)
5. [Hedef Kullanıcılar ve Personalar](#5-hedef-kullanıcılar-ve-personalar)
6. [Kapsam Yönetimi](#6-kapsam-yönetimi)
7. [Teknik Mimari](#7-teknik-mimari)
8. [Skor Motoru — Detaylı Tasarım](#8-skor-motoru--detaylı-tasarım)
9. [Tahmin Modülü — Detaylı Tasarım](#9-tahmin-modülü--detaylı-tasarım)
10. [Veri Stratejisi](#10-veri-stratejisi)
11. [Frontend ve UX Tasarımı](#11-frontend-ve-ux-tasarımı)
12. [Geliştirme Süreci ve Multi-Agent Yaklaşım](#12-geliştirme-süreci-ve-multi-agent-yaklaşım)
13. [25 Saatlik Zaman Çizelgesi](#13-25-saatlik-zaman-çizelgesi)
14. [Risk Yönetimi](#14-risk-yönetimi)
15. [Demo Stratejisi](#15-demo-stratejisi)
16. [Karar Defteri](#16-karar-defteri)
17. [Ekler](#17-ekler)

---

## 1. YÖNETİCİ ÖZETİ

**RE-Atlas**, Türkiye'nin tamamı için yenilenebilir enerji yatırım uygunluğunu interaktif harita üzerinden gösteren ve 48 saatlik üretim tahmini sunan bir karar destek aracıdır.

### 1.1. Tek Cümleyle Değer Önerisi
> Enerji yatırımcıları artık saha ölçümüne çıkmadan önce, Türkiye'nin herhangi bir noktası için "Hangi yenilenebilir enerji sistemi uygundur, ne kadar uygundur ve neden?" sorusunun cevabını **tek tıkla** alabilir.

### 1.2. Üç Cümleyle Demo
1. Kullanıcı Türkiye haritasında bir bölgeye tıklar.
2. Sistem o bölgenin uygunluk skorunu, en yakın trafoyu, arazi tipini, 48 saatlik üretim tahminini ve geri ödeme süresini gösterir.
3. Kullanıcı iki noktayı yan yana karşılaştırabilir veya "Türkiye'nin en iyi 5 yatırım noktası"nı tek tıkla görebilir.

### 1.3. Teknik Özet
- **Frontend:** React + Vite + TypeScript + Leaflet + TailwindCSS
- **Backend:** Python 3.11 + FastAPI + Pydantic v2
- **ML:** Prophet (opsiyonel) + fizik tabanlı formüller
- **Veri:** Open-Meteo (canlı + cache), OSM (statik), GeoJSON il/ilçe sınırları

### 1.4. Yarışma Kısıtları
- **Süre:** 25 saat
- **Ekip:** 4 kişi
- **Geliştirme:** VS Code + Claude Code (lokal)
- **Multi-agent stratejisi:** 1 orkestratör + 6 subagent

---

## 2. YARIŞMA BAĞLAMI

### 2.1. Seçilen Konu
Yarışmada sunulan konular arasından **2 numaralı konu — "Yenilenebilir Enerji Tahmini ve Analizi"** seçildi.

Yarışmanın bu konuya atadığı etiketler:
`ML` `Time Series` `Data Science` `LSTM` `Prophet` `Forecasting`

### 2.2. Yarışmanın Tanımladığı Problem
Türkiye'nin kurulu güneş enerjisi kapasitesi son yıllarda hızla artmaktadır. Ancak bu büyüme beraberinde ciddi bir sorun getirmektedir: güneş ve rüzgâr enerjisi, hava koşullarına bağlı olarak sürekli değişmektedir.

### 2.3. Yarışmanın Verdiği Üç Senaryo
1. Düzce'nin dağlık köyünde çatısına panel kurmuş çiftçinin "bugün üretim yapabilecek mi, satabilir mi?" sorusu
2. Enerji şirketlerinin tahmin yapamadığı için aşırı rezerv tutması
3. Rüzgâr çiftliklerinde bakım planlamasında düşük rüzgâr saatlerinin önceden bilinememesi

### 2.4. Yarışmanın Önerdiği Veri Kaynakları
- Open-Meteo (ücretsiz hava API)
- PVGIS (Avrupa Güneş Enerjisi Atlası)
- EMRA/EPDK açık verileri
- NREL açık enerji veri setleri

### 2.5. Yarışmanın Önerdiği Örnek Çözümler
*(Sayfada "yalnızca ilham içindir, sınırlama değildir" notuyla verilmiş.)*
- 24-48 saat üretim tahmini
- Bireysel üretici için "sat mı depola mı" karar destek aracı
- İl bazlı karşılaştırmalı potansiyel haritası
- Çatı paneli tasarruf hesaplayıcısı
- Üretim anomalisi tespit sistemi

---

## 3. PROBLEM TANIMI

### 3.1. Sorunun Üç Katmanı

**Katman 1 — Yatırım kararı belirsizliği:**
Türkiye'de yenilenebilir enerji yatırımı yapmak isteyen bir şirket, sahaya çıkmadan önce hangi bölgenin uygun olduğunu bilemez. Saha ölçümü pahalıdır (200-500 bin TL bir mast kurulumu, 12 ay ölçüm). Şirketler kâğıt üstünde ön eleme yapmadan saha ekibi göndermek zorunda kalır.

**Katman 2 — Üretim tahmin belirsizliği:**
Mevcut santraller bile günlük üretimlerini doğru tahmin edemez. Bu, hem dengeleme piyasasında ceza ödemelerine hem de bakım planlamasında verimsizliğe yol açar.

**Katman 3 — Bireysel üretici karar paralizi:**
Çatısına panel taktırmak isteyen bireysel kullanıcı "kaç yılda kendini öder, hangi sistemi seçmeliyim?" sorusunu cevaplayamadığı için karar veremez veya yanlış karar verir.

### 3.2. Bizim Odak Noktamız

Üç katmandan **Katman 1 (yatırım kararı)** ana çözüm hedefimizdir. Katman 2 yan ürün olarak desteklenir. Katman 3 sunumda referans olarak geçer ama UI'de ayrı mod almaz.

**Gerekçe:** B2B yatırımcı ödeme yapan müşteridir, jüri ticari değer arar. Tek mod + filtreler ile diğer personalara da hizmet edebiliriz.

### 3.3. Çözüm Kapsamı Dışındaki Sorunlar
- Şebekeye senkronizasyon ve dengeleme piyasası optimizasyonu
- Sigorta ve finansman ürünleri tasarımı
- Tedarik zinciri (panel/türbin temin) yönetimi
- Enerji depolama (batarya) optimizasyonu
- Politika analizi ve regülasyon tavsiyesi

---

## 4. ÇÖZÜM KONSEPTİ

### 4.1. Ürünün Üç Bileşeni

**Bileşen 1 — Bölge Uygunluk Haritası (ANA ÜRÜN):**
Türkiye'nin tamamı için interaktif choropleth harita. İl seviyesinde başlar, zoom yapıldıkça ilçeye geçer. Tıklamada koordinat-spesifik canlı analiz açılır.

**Bileşen 2 — 48 Saatlik Üretim Tahmini (YAN ÜRÜN):**
Tıklanan noktada Open-Meteo forecast verisi alınır, fizik formülleri ile üretime dönüştürülür, ±%15 belirsizlik bandıyla grafik olarak gösterilir.

**Bileşen 3 — Bakım Penceresi Önerisi (MİNİMAL):**
Tahmin verisinden en düşük üretim penceresi tek satırlık metin olarak detay panelinde gösterilir. Ayrı modül değildir.

### 4.2. Tasarım Felsefesi

**1. "Sayı söyle bana" prensibi:** Soyut "uygundur" yerine somut "84/100 puan, geri ödeme 7,2 yıl" verilir.

**2. Şeffaflık:** Her skor "neden böyle?" sorusuna cevap verir. Skor kırılımı (kaynak/arazi/şebeke) gösterilir.

**3. Kurtarılabilirlik:** İnternet kesintisinde demo modu devreye girer, kullanıcı farkına varmaz.

**4. Tutarlılık:** İl ortalaması ile koordinat skoru farklı olabilir; bu fark **mutlaka açıklanır** ("İl: 72 / Bu nokta: 84 — fark mikro-koşullar ve şebeke yakınlığından").

**5. Yatırımcı dili:** Teknik terimler tooltip'te açıklanır. "MAPE %12" değil "tipik hata ±%12".

### 4.3. Ürün Adı Kararı
**RE-Atlas** (Renewable Energy Atlas)
- Kısa, akılda kalıcı, İngilizce/Türkçe okunuşu aynı
- "Atlas" coğrafya çağrışımı ürünün harita kalbiyle uyumlu
- Domain'i bulunabilir, marka çakışması az

---

## 5. HEDEF KULLANICILAR VE PERSONALAR

### 5.1. Persona Analizi (6 Açıdan)

#### 5.1.1. Bireysel Kullanıcı — Çiftçi / Ev Sahibi / Arsa Sahibi
**Profil:** 45-60 yaş, teknik bilgisi sınırlı, "komşumun paneli var, ben de mi yapsam?" düşüncesinde.

**İhtiyacı:**
- Geri ödeme süresi (yıl)
- Yıllık tahmini kazanç (TL)
- Hangi sistem uygun (güneş/rüzgâr)

**Göremediği:**
- Çatı yönü/eğimi etkisi
- Gölgeleme sorunu
- Gürültü/titreşim regülasyonu (rüzgâr için)
- Lisanssız üretim sınırı (5 MW altı için ayrı rejim)
- Mülkiyet durumu (kira/mülk, apartman onayı)

**Sistem yaklaşımı:** Demo'da sunum açılışında bahsedilir, ürünün ayrı modu OLMAZ. Filtre paneli ile aynı ana arayüz "Bireysel mod"a yaklaştırılabilir.

---

#### 5.1.2. Enerji Şirketi / Yatırımcı (ANA PERSONA)
**Profil:** Yenilenebilir enerji firması geliştirme uzmanı veya yatırım analisti. "Hangi 5 ilçeye saha ekibi göndereyim?" sorusunu soruyor.

**İhtiyacı:**
- İl/ilçe bazında **sıralanabilir liste**
- "Top 10 ilçe" çıktısı
- **Dışlama filtreleri** (orman, SİT, askeri, 1. derece tarım)
- Excel/PDF rapor (B2B sunumlarda kullanmak için)

**Bilmesi gerekenler:**
- Wind rose (rüzgâr yönü ve frekansı)
- Türbülans yoğunluğu
- Capacity factor (rüzgâr için Türkiye ortalaması ~%32, güneş ~%17)
- LCOE (Levelized Cost of Energy)
- En yakın TEİAŞ trafosu mesafesi

**Sistem yaklaşımı:** Bu personaya **birincil olarak hizmet edilir.** Tüm UI tasarımı ve demo akışı bu personanın iş akışına optimize edilir. Top 5 özelliği ve karşılaştırma modu doğrudan bu kişi için tasarlanmıştır.

---

#### 5.1.3. Bakım Ekibi Yöneticisi
**Profil:** Mevcut santralin operasyon müdürü. Bakım planlaması yapıyor.

**İhtiyacı:**
- 7 günlük üretim tahmin grafiği
- "Yarın 14:00-17:00 düşük üretim" gibi pencere önerileri
- Anomali uyarıları

**Bilmesi gerekenler:**
- Tahmin belirsizlik aralığı (önemli! tek sayı yetmez)
- Soğuk başlatma süresi (türbin durdurmak/başlatmak 30-60 dk)
- 50 km/h üstü rüzgârda yüksekte çalışma yasak

**Sistem yaklaşımı:** Detay panelinde **tek satırlık bakım penceresi cümlesi**. Ayrı sayfa/dashboard YOK. Sunumda "aynı altyapı operasyon ekibine de hizmet eder" denilir.

---

#### 5.1.4. Jeopolitik Veri Analisti
**Profil:** Düşünce kuruluşu veya bakanlık danışmanı. "Türkiye'nin enerji bağımsızlığı için kapasite nereye yığılmalı?" sorusunu soruyor.

**İhtiyacı:**
- Bölgesel eşitsizlik analizi
- Komşu ülke kıyaslaması
- İklim değişikliği projeksiyonu (2030-2050)
- Stratejik koridor analizi (boru hattı vs yenilenebilir koridor)

**Sistem yaklaşımı:** **Demo'da gösterilmez.** Sunumda 30 saniye "altyapı politika yapıcılara da hizmet edebilir" denilir. UI'de modül YOK.

---

#### 5.1.5. AI/ML Analisti (Teknik Jüri)
**Profil:** Hackathon jürisinin teknik kanadı. Modelinizi kurcalayacak.

**İhtiyacı:**
- MAE, RMSE, MAPE metrikleri
- Baseline karşılaştırması ("naif tahmin MAPE 18, Prophet MAPE 11")
- Feature importance
- Belirsizlik kuantifikasyonu
- Time-series cross-validation kanıtı

**Sezdikleri:**
- "LSTM kullandık" cümlesini duyduğunda gözlerini kıstırır
- Random split (zaman serisi için sızıntı) gördüğünde puan kırar

**Sistem yaklaşımı:** **MODEL_CARD.md** dosyası hazırlanır: veri kaynakları, train/test periyotları, metrikler, sınırlılıklar, etik notlar. Ablation study yapılır ("LSTM denedik, Prophet seçtik çünkü...").

---

#### 5.1.6. Maliyet Koordinatörü / Finans Modelcisi
**Profil:** Yatırımcının yanındaki finans uzmanı. "Bu sayı ne anlama geliyor?" diye soruyor.

**İhtiyacı:**
- CAPEX (TL/kWp veya TL/kW)
- OPEX (yıllık bakım, sigorta)
- NPV, IRR, geri ödeme süresi
- LCOE
- Hassasiyet analizi

**Bilmesi gerekenler:**
- Döviz riski (ekipman ithal, gelir TL)
- Vergi teşvikleri, KDV istisnası
- Finansman maliyeti (kredi faizi, equity beklentisi)

**Sistem yaklaşımı:** Detay panelinde **Finansal Görünüm Kartı** (kaba sayılar + "ön değerlendirme amaçlıdır" disclaimer'ı). PDF export bonus özellik (zaman kalırsa son saatte).

### 5.2. Persona Önceliklendirmesi

| Persona | Önem | UI'da Yer | Demo'da Yer |
|---------|------|-----------|-------------|
| Yatırımcı | Çok yüksek | Birincil | Ana hikaye |
| Bireysel | Orta-yüksek | Filtre ile | Açılış sahnesi |
| Bakım yöneticisi | Orta | Tek satır | 30 sn bahis |
| Finans uzmanı | Orta-yüksek | Finansal kart | Detay panel |
| AI analisti (jüri) | Yüksek | Model Card | README'de |
| Jeopolitik | Düşük | Yok | Sunumda 1 cümle |

---

## 6. KAPSAM YÖNETİMİ

### 6.1. Kapsam İçi (MUST HAVE)

#### Ana Ürün — Harita
- Türkiye haritası (Leaflet + OSM dark theme)
- Çift seviye choropleth (zoom out → 81 il, zoom in → ilçe)
- 3 mod düğmesi (Güneş / Rüzgâr / Hibrit)
- Tıklamada koordinat-spesifik canlı API
- Renkli skor görselleştirmesi (yeşil/sarı/kırmızı)
- Sol filtre paneli (orman, trafo<10km, sit dışla)
- Sağ detay panel
- Top 5 özelliği
- İki nokta karşılaştırma modu
- Tutarlılık açıklama cümlesi (zorunlu)

#### Yan Ürün — Tahmin
- 48 saatlik forecast grafiği
- Fizik formülü tabanlı dönüşüm
- ±%15 belirsizlik bandı
- Prophet wrapper (OPSİYONEL — zaman kalırsa)

#### Yan Ürün — Bakım
- Tek satırlık öneri metni
- Detay panelinin altında etiket olarak

#### Doküman
- README.md
- MODEL_CARD.md
- DEMO_SCRIPT.md

### 6.2. Kapsam Dışı (KESİN YOK)

- LSTM (3 model hemfikir — 25 saatte düzgün eğitilemez)
- Gerçek route/vehicle optimization
- Çoklu kullanıcı modu (bireysel/kurumsal/operasyon ayrı UI)
- Jeopolitik analiz modülü
- Grid heatmap fake (PNG overlay)
- Bulut örtüsü what-if simülasyonu
- REPA/GEPA overlay (sadece referans değer iç doğrulamada)
- Anomali tespit modülü
- İklim projeksiyonu
- Karbon ayak izi sayfası

### 6.3. Şartlı Kapsam (NICE TO HAVE)

- PDF export (sadece feature freeze sonrası, zaman kalırsa)
- Prophet wrapper (sadece fizik tabanlı tahmin tamamsa)
- Anomali tespit basit hali (sadece feature freeze sonrası)
- "What-if" basit slider (panel verim değiştirme — son saat)

### 6.4. Coğrafi Kapsam Fallback

**3. saat kontrolü:** Tüm Türkiye için OSM landuse + power verisi alınamadıysa **Marmara + Ege bölgesine daralt** (16 il). Bu, hikayeyi bozmaz çünkü Türkiye'nin yenilenebilir enerji yoğunluğu zaten bu bölgelerdedir.

---

## 7. TEKNİK MİMARİ

### 7.1. Yüksek Seviye Mimari

```
┌──────────────────────────────────────────────────┐
│              FRONTEND (React + Vite)             │
│  ┌────────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ MapCanvas  │  │ Filters  │  │ DetailPanel  │  │
│  └────────────┘  └──────────┘  └──────────────┘  │
└─────────────────────┬────────────────────────────┘
                      │ REST (JSON)
                      ▼
┌──────────────────────────────────────────────────┐
│            BACKEND (FastAPI + Pydantic)          │
│  ┌────────────────┐  ┌────────────────────────┐  │
│  │ Score Engine   │  │  Forecast Engine       │  │
│  │ (saf fonksiyon)│  │  (Open-Meteo + fizik)  │  │
│  └────────────────┘  └────────────────────────┘  │
│  ┌────────────────────────────────────────────┐  │
│  │  Cache Layer (SQLite + JSON)               │  │
│  └────────────────────────────────────────────┘  │
└─────────────────────┬────────────────────────────┘
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
   ┌─────────┐   ┌─────────┐   ┌──────────┐
   │ Open-   │   │  OSM    │   │ Static   │
   │ Meteo   │   │ Overpass│   │ GeoJSON  │
   │  API    │   │  API    │   │  Files   │
   └─────────┘   └─────────┘   └──────────┘
```

### 7.2. Teknoloji Yığını Detayı

| Katman | Teknoloji | Versiyon | Gerekçe |
|--------|-----------|----------|---------|
| Frontend framework | React | 18 | Olgun ekosistem, Leaflet entegrasyonu kolay |
| Build tool | Vite | 5+ | Hızlı HMR, basit yapılandırma |
| Dil (FE) | TypeScript | 5+ | Tip güvenliği, contracts/schemas.ts |
| Harita | Leaflet + react-leaflet | 1.9+ / 4+ | Ücretsiz, OSM dostu, plugin ekosistemi |
| State | Zustand | 4+ | Redux'tan hafif, TypeScript dostu |
| Stil | TailwindCSS | 3+ | Hızlı prototipleme, utility-first |
| Grafik | Recharts | 2+ | React-native, SVG tabanlı |
| Backend framework | FastAPI | 0.110+ | Async, Pydantic v2, otomatik OpenAPI |
| Dil (BE) | Python | 3.11 | Olgun, Prophet uyumlu |
| Validation | Pydantic | v2 | TypeScript ile tip eşlemesi |
| HTTP client | httpx | 0.27+ | Async, modern |
| ML | Prophet | 1.1+ | Hızlı, yorumlanabilir |
| Numeric | NumPy | 1.26+ | Fizik formülleri |
| Cache | SQLite | yerleşik | Sıfır konfigürasyon |
| GIS | shapely | 2+ | Poligon işlemleri |

### 7.3. Repo Yapısı

```
re-atlas/
├── PROJECT_CONTEXT.md
├── README.md
├── .gitignore
│
├── docs/
│   ├── hackathon-proje-plani.md     ← bu dosya
│   ├── claude-code-master-prompt.md
│   ├── MODEL_CARD.md
│   └── DEMO_SCRIPT.md
│
├── contracts/
│   ├── schemas.py                    (Pydantic v2)
│   ├── schemas.ts                    (TypeScript)
│   └── README.md
│
├── data-pipeline/
│   ├── scripts/
│   │   ├── fetch_provinces.py
│   │   ├── fetch_districts.py
│   │   ├── fetch_osm_landuse.py
│   │   ├── fetch_osm_power.py
│   │   ├── precompute_weather_cache.py
│   │   └── simplify_geojson.py
│   └── README.md
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   (FastAPI entry)
│   │   ├── config.py
│   │   ├── routers/
│   │   │   ├── score.py
│   │   │   ├── forecast.py
│   │   │   ├── provinces.py
│   │   │   ├── districts.py
│   │   │   └── top.py
│   │   ├── scoring/
│   │   │   ├── engine.py             (ana skor fonksiyonu)
│   │   │   ├── physics.py            (rüzgâr/güneş formülleri)
│   │   │   ├── landuse.py            (arazi skoru)
│   │   │   ├── grid_proximity.py     (şebeke yakınlığı)
│   │   │   └── weights.py            (ağırlık tanımları)
│   │   ├── forecast/
│   │   │   ├── physics_forecast.py   (BİRİNCİL)
│   │   │   ├── prophet_wrapper.py    (OPSİYONEL)
│   │   │   └── maintenance_window.py
│   │   └── services/
│   │       ├── openmeteo.py
│   │       ├── cache.py
│   │       ├── landuse_lookup.py
│   │       └── substation_lookup.py
│   ├── data/
│   │   ├── provinces.geojson
│   │   ├── districts.geojson
│   │   ├── landuse.geojson
│   │   ├── substations.geojson
│   │   ├── transmission_lines.geojson
│   │   └── cache/
│   │       ├── weather_yearly.sqlite
│   │       └── demo_weather.json
│   ├── tests/
│   │   ├── test_scoring.py
│   │   └── test_forecast.py
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/
    ├── src/
    │   ├── main.tsx
    │   ├── App.tsx
    │   ├── components/
    │   │   ├── MapCanvas.tsx
    │   │   ├── ProvinceLayer.tsx
    │   │   ├── DistrictLayer.tsx
    │   │   ├── FilterPanel.tsx
    │   │   ├── DetailPanel.tsx
    │   │   ├── CompareView.tsx
    │   │   ├── TopFiveCard.tsx
    │   │   ├── EnergyTypeToggle.tsx
    │   │   ├── Legend.tsx
    │   │   └── ForecastChart.tsx
    │   ├── api/
    │   │   └── client.ts
    │   ├── store/
    │   │   └── useAppStore.ts
    │   ├── types/                    (contracts/schemas.ts kopyası)
    │   ├── mocks/
    │   └── styles/
    │       └── globals.css
    ├── public/
    ├── package.json
    ├── vite.config.ts
    ├── tsconfig.json
    └── tailwind.config.js
```

### 7.4. Backend Endpoint'leri

| Endpoint | Metod | Açıklama | Yanıt Süresi |
|----------|-------|----------|--------------|
| `/api/health` | GET | Sağlık kontrolü | <50 ms |
| `/api/score?lat={}&lon={}&type={}` | GET | Tek nokta canlı skor | <500 ms |
| `/api/provinces` | GET | 81 il önceden hesaplı | <100 ms |
| `/api/districts?province_id={}` | GET | Bir ilin ilçeleri | <200 ms |
| `/api/forecast?lat={}&lon={}&hours=48` | GET | 48 saat tahmin | <800 ms |
| `/api/top?type={}&n=5` | GET | En iyi N nokta | <300 ms |
| `/api/nearest-substation?lat={}&lon={}` | GET | En yakın trafo | <200 ms |
| `/api/landuse?lat={}&lon={}` | GET | Arazi tipi | <100 ms |

### 7.5. Demo Modu

**Ortam değişkeni:** `DEMO_MODE=true`

Bu mod aktifken:
- Open-Meteo API'sine istek atılmaz, `backend/data/cache/demo_weather.json`'dan okunur
- OSM Overpass API'sine istek atılmaz, statik GeoJSON'lardan okunur
- Tüm yanıtlar deterministiktir

**Sebep:** Demo gecesi internet kesintisi veya rate limit projeyi mahveder. Demo modu hayat sigortasıdır.

---

## 8. SKOR MOTORU — DETAYLI TASARIM

### 8.1. Ana Formül

```
Uygunluk_Skoru = w1·KaynakPotansiyeli
               + w2·AraziUygunluğu
               + w3·ŞebekeYakınlığı
               + w4·RiskFaktörü     (negatif)
               + w5·EkonomikFizibilite

Skor = clamp(Uygunluk_Skoru × 100, 0, 100)
```

### 8.2. Bileşen Hesaplamaları

#### 8.2.1. Kaynak Potansiyeli (0-1)

**Güneş için:**
```python
def solar_resource_score(ghi_annual_kwh_m2: float) -> float:
    """
    GHI (Global Horizontal Irradiance) yıllık değeri.
    Türkiye'de tipik aralık: 1200-2000 kWh/m²/yıl.
    """
    if ghi_annual_kwh_m2 < 1200:
        return 0.0
    if ghi_annual_kwh_m2 > 1900:
        return 1.0
    return (ghi_annual_kwh_m2 - 1200) / 700
```

**Rüzgâr için:**
```python
def wind_resource_score(avg_wind_speed_50m: float) -> float:
    """
    50m yükseklikte yıllık ortalama rüzgâr hızı (m/s).
    Türbin cut-in: ~3 m/s, nominal: ~12 m/s.
    """
    if avg_wind_speed_50m < 4.0:
        return 0.0
    if avg_wind_speed_50m > 9.0:
        return 1.0
    return (avg_wind_speed_50m - 4.0) / 5.0
```

**Hibrit:** `max(solar, wind)` veya ağırlıklı kombinasyon.

#### 8.2.2. Arazi Uygunluğu (0-1)

```python
LANDUSE_SCORES = {
    "forest": 0.0,        # orman → kullanılamaz
    "protected": 0.0,     # SİT, milli park
    "military": 0.0,      # askeri yasak
    "residential": 0.1,   # yerleşim
    "farmland": 0.3,      # tarım (özel izin gerekir)
    "meadow": 0.7,        # çayır
    "barren": 1.0,        # çorak
    "industrial": 0.8,    # endüstriyel
    "default": 0.5,       # bilinmeyen
}
```

#### 8.2.3. Şebeke Yakınlığı (0-1)

```python
def grid_proximity_score(distance_km: float) -> float:
    """
    En yakın iletim hattına mesafe (km).
    """
    if distance_km <= 5:
        return 1.0
    if distance_km >= 50:
        return 0.0
    return 1.0 - (distance_km - 5) / 45
```

#### 8.2.4. Risk Faktörü (0-1, negatif katkı)

İlk versiyonda **sabit 0.1** (varsayılan düşük risk). İleride:
- Deprem bölgesi (1. derece: 0.5, 2. derece: 0.3, ...)
- Heyelan riski
- Sel riski

#### 8.2.5. Ekonomik Fizibilite (0-1)

İlk versiyonda **sabit 0.7** (orta düzey). İleride:
- Bölgesel arazi maliyeti
- LCOE hesabı
- Mesafe bazlı lojistik maliyeti

### 8.3. Ağırlıklar (Mod Bazlı)

```python
WEIGHTS_INVESTOR = {  # Varsayılan
    "resource": 0.40,
    "landuse": 0.20,
    "grid": 0.30,
    "risk": 0.05,
    "economic": 0.05,
}

WEIGHTS_INDIVIDUAL = {  # Filtre ile aktif
    "resource": 0.30,
    "landuse": 0.10,
    "grid": 0.05,    # bireysel için trafo önemsiz
    "risk": 0.05,
    "economic": 0.50,  # bireyselde geri ödeme önemli
}
```

### 8.4. Fizik Formülleri (Üretim Hesabı)

#### 8.4.1. Rüzgâr Türbini Gücü

```python
def wind_power_kw(wind_speed_ms: float, rotor_diameter_m: float = 80,
                  cp: float = 0.4, rho: float = 1.225) -> float:
    """
    P = 0.5 × ρ × A × v³ × Cp

    ρ: hava yoğunluğu (kg/m³)
    A: rotor süpürme alanı (m²)
    v: rüzgâr hızı (m/s)
    Cp: güç katsayısı (Betz limiti = 16/27 ≈ 0.593, pratik ~0.4)

    Cut-in: 3 m/s, cut-out: 25 m/s
    """
    if wind_speed_ms < 3 or wind_speed_ms > 25:
        return 0.0
    area = math.pi * (rotor_diameter_m / 2) ** 2
    return 0.5 * rho * area * (wind_speed_ms ** 3) * cp / 1000
```

#### 8.4.2. Güneş Paneli Üretimi

```python
def solar_power_kw(ghi_w_m2: float, panel_area_m2: float = 50,
                   efficiency: float = 0.18, pr: float = 0.80) -> float:
    """
    P = GHI × A × η × PR

    GHI: anlık global yatay ışınım (W/m²)
    A: panel alanı (m²)
    η: panel verimi
    PR: performance ratio (kayıplar)
    """
    return ghi_w_m2 * panel_area_m2 * efficiency * pr / 1000
```

#### 8.4.3. Capacity Factor

```python
def capacity_factor(hourly_production_kw: list[float],
                     rated_power_kw: float) -> float:
    """
    CF = Σ P(t) / (P_rated × n_hours)

    Türkiye ortalaması:
    - Rüzgâr: ~32%
    - Güneş: ~17%
    """
    if not hourly_production_kw or rated_power_kw == 0:
        return 0.0
    total = sum(hourly_production_kw)
    max_possible = rated_power_kw * len(hourly_production_kw)
    return total / max_possible
```

### 8.5. Skor Açıklayıcılığı

Her skor yanında **insan-okur açıklama** üretilir:

```python
def explain_score(breakdown: ScoreBreakdown) -> str:
    """
    Skor kırılımını cümle halinde açıklar.
    Örnek çıktı:
    'Bu nokta için rüzgâr enerjisi önerilir. 50m yükseklikte
    7,2 m/s ortalama hız (yüksek), arazi tipi çorak (uygun),
    6 km mesafede 154 kV trafo mevcut.'
    """
    ...
```

---

## 9. TAHMİN MODÜLÜ — DETAYLI TASARIM

### 9.1. İki Tabakalı Yaklaşım

**Tabaka 1 — Fizik Tabanlı (BİRİNCİL):**
1. Open-Meteo'dan 48 saatlik forecast çek
2. Her saat için `wind_power_kw()` veya `solar_power_kw()` uygula
3. ±%15 belirsizlik bandı ekle
4. JSON döndür

**Tabaka 2 — Prophet (OPSİYONEL):**
1. 8-12 saat penceresinde fizik tabanlı tamamsa
2. Tarihsel veriyle Prophet eğit
3. Karşılaştırmalı sonuç göster
4. **Eğer Prophet 12. saate kadar tamamlanmazsa İPTAL.**

### 9.2. Open-Meteo Forecast Kullanımı

```python
# Endpoint
"https://api.open-meteo.com/v1/forecast"

# Parametreler
{
    "latitude": 40.85,
    "longitude": 31.16,
    "hourly": [
        "wind_speed_10m",
        "wind_speed_100m",
        "shortwave_radiation",   # GHI proxy
        "direct_normal_irradiance",
        "temperature_2m",
        "cloud_cover",
    ],
    "forecast_days": 2,
    "timezone": "auto",
}
```

### 9.3. Bakım Penceresi Tespiti

```python
def find_maintenance_window(
    forecast: list[ForecastPoint],
    duration_hours: int = 3,
    max_safe_wind_kmh: float = 50
) -> MaintenanceWindow | None:
    """
    En düşük üretim penceresi bul (peş peşe N saat).
    Güvenlik filtresi: rüzgâr 50 km/h üstüyse o pencere reddedilir.
    """
    ...

# Çıktı örneği:
# "Yarın 14:00-17:00 arası beklenen üretim ortalama 0.4 MW
# (profil maksimumunun %22'si). Bakım için uygun pencere."
```

### 9.4. Belirsizlik Bandı

İlk versiyon **rule-based ±%15**. İleride:
- Tarihsel hata dağılımından kalibre edilebilir
- Saatlere göre (gece/gündüz) farklı bantlar
- Quantile regression

### 9.5. LSTM Yasağı

**ForecastSage subagent'i LSTM eğitmeye, Keras/TensorFlow kurmaya, neural network yazmaya YETKİLİ DEĞİLDİR.**

Gerekçe:
- 25 saatte düzgün eğitim çok zor
- Overfit/underfit riski yüksek
- Yorumlanabilirlik düşük
- Jüri "gösterişli ama zayıf" algılar

Eğer demo'da neural network gerektiğine inanılırsa Prophet baseline'ı tercih edilir.

---

## 10. VERİ STRATEJİSİ

### 10.1. Veri Kaynakları

| Kaynak | Tür | Erişim | Boyut Tahmini |
|--------|-----|--------|---------------|
| Open-Meteo | Saatlik hava | API (ücretsiz) | <1 MB cache/il |
| GitHub: tr-geojson | İl/ilçe sınırları | Statik dosya | ~3 MB |
| OSM Overpass | Landuse, power | API (rate limit var) | ~10-20 MB |
| AFAD | Fay hatları | Açık veri | ~1 MB |
| YEKA bölgeleri | Bakanlık duyuruları | Manuel | <1 KB |

### 10.2. Veri Hazırlık Akışı

```
[Yarışma öncesi/ilk 2 saat]
    ↓
fetch_provinces.py     → provinces.geojson
fetch_districts.py     → districts.geojson
fetch_osm_landuse.py   → landuse_raw.geojson
fetch_osm_power.py     → power_raw.geojson
    ↓
simplify_geojson.py (Mapshaper)
    ↓
landuse.geojson (basitleştirilmiş, <5 MB)
substations.geojson
transmission_lines.geojson
    ↓
precompute_weather_cache.py
    ↓
weather_yearly.sqlite (81 il × 8760 saat)
```

### 10.3. Cache Stratejisi

**Tarihsel hava verisi:**
- 81 il merkezi için son 1 yılın saatlik verisi
- SQLite'a yazılır
- Boot zamanında belleğe yüklenir (LRU)

**Forecast cache:**
- Her koordinat için 1 saatlik TTL
- Anahtar: `f"{round(lat, 2)}_{round(lon, 2)}_{type}"`
- SQLite veya basit JSON

**İl/ilçe skorları:**
- Boot zamanında hesaplanır
- Bellekte tutulur
- Dosyaya da yazılır (boot hızı için)

### 10.4. Veri Boyut Optimizasyonu

**Mapshaper komutları:**
```bash
# İl sınırları için %90 basitleştirme
mapshaper provinces_raw.geojson \
  -simplify dp 10% \
  -o provinces.geojson

# OSM landuse için tip filtresi + basitleştirme
mapshaper landuse_raw.geojson \
  -filter '["forest","farmland","residential","industrial"].includes(landuse)' \
  -simplify 5% \
  -o landuse.geojson
```

**Hedef boyutlar:**
- `provinces.geojson`: <500 KB
- `districts.geojson`: <2 MB
- `landuse.geojson`: <5 MB
- `substations.geojson`: <500 KB
- `transmission_lines.geojson`: <2 MB

### 10.5. Veri Darboğazı Önlemi (3. Saat Kontrolü)

3. saat sonunda eğer:
- İl sınırları alınmış ✓
- Open-Meteo cache hazır ✓
- OSM landuse 30 dakikadan uzun sürüyor ✗

→ **Otomatik karar:** Marmara + Ege'ye daralt. 16 il yeterli hikaye verir.

---

## 11. FRONTEND VE UX TASARIMI

### 11.1. Tasarım Sistemi

#### Renk Paleti
```css
:root {
  /* Arkaplan */
  --bg-primary: #0B1220;
  --bg-secondary: #111A2E;
  --bg-elevated: #1A2540;

  /* Skor renkleri */
  --score-high: #22C55E;
  --score-medium: #FACC15;
  --score-low: #EF4444;

  /* Mod renkleri */
  --solar: #F59E0B;
  --wind: #3B82F6;
  --hybrid: #A855F7;

  /* Metin */
  --text-primary: #E5E7EB;
  --text-secondary: #9CA3AF;
  --text-muted: #6B7280;

  /* Kenarlık ve ayırıcı */
  --border: #1F2937;
  --divider: #374151;

  /* Vurgu */
  --accent: #14B8A6;
  --accent-hover: #2DD4BF;
}
```

#### Tipografi
- **UI:** Inter (Google Fonts)
- **Sayılar/kodlar:** JetBrains Mono (Google Fonts)
- **Boyutlar:** 12px (caption), 14px (body), 16px (default), 20px (h3), 24px (h2), 32px (h1)

#### Komponent Stili
- Köşe yuvarlama: `rounded-2xl` (16px)
- Buton hover: `scale(1.02)` + glow
- Geçişler: 200-300 ms ease-out
- Gölge: minimum, sadece elevated kartlarda

### 11.2. Ana Layout

```
┌──────────────────────────────────────────────────────────┐
│ HEADER (h: 64px)                                         │
│ [Logo] RE-Atlas         [Solar][Wind][Hybrid]      [⚙]   │
├──────────┬──────────────────────────────────┬────────────┤
│          │                                  │            │
│ FİLTRE   │                                  │  DETAY     │
│ PANEL    │                                  │  PANEL     │
│ (w:280px │         HARİTA (esnek)           │ (w: 360px, │
│  sol)    │                                  │  sağ,      │
│          │                                  │  açılınca) │
│ □ Orman  │                                  │            │
│ □ Trafo  │                                  │            │
│ □ SİT    │                                  │            │
│          │                                  │            │
│          │                                  │            │
│          │  [Top 5]    [Karşılaştırma]      │            │
└──────────┴──────────────────────────────────┴────────────┘
                                              ↑
                          Tıklamada açılır,
                          ESC veya X ile kapanır
```

### 11.3. Detay Panel İçeriği

```
┌─────────────────────────────────────┐
│ ✕                                   │
│                                     │
│ 📍 BURSA / KARACABEY                │
│ 40.213°N, 28.366°E                  │
│                                     │
│        ┌─────────┐                  │
│        │   84    │                  │
│        │  /100   │                  │
│        └─────────┘                  │
│         YÜKSEK                      │
│                                     │
│ ─── Skor Kırılımı ───               │
│ Kaynak       ████████░░  82         │
│ Arazi        █████████░  91         │
│ Şebeke       ███████░░░  73         │
│                                     │
│ ─── Önerilen Sistem ───             │
│ 💨 Rüzgâr Enerjisi                  │
│                                     │
│ Bu nokta için rüzgâr enerjisi       │
│ önerilir. 50m yükseklikte 7,2 m/s   │
│ ortalama hız, 6 km mesafede         │
│ 154 kV trafo mevcut.                │
│                                     │
│ ⚠ İl genel skoru: 72 / Bu nokta: 84 │
│ Fark mikro-koşullar ve şebeke       │
│ yakınlığından.                      │
│                                     │
│ ─── 48 Saat Tahmin ───              │
│ [Recharts grafiği — belirsizlik     │
│  bandlı çizgi]                      │
│                                     │
│ 🔧 Yarın 14:00-17:00 düşük üretim   │
│ — bakım için uygun pencere.         │
│                                     │
│ ─── Finansal Görünüm ───            │
│ CAPEX (tahmini)    ~12.5M TL        │
│ Yıllık üretim      ~3.2 GWh         │
│ Geri ödeme         ~6.8 yıl         │
│ ⓘ Ön değerlendirme amaçlıdır.       │
│                                     │
│ [+ Karşılaştırmaya Ekle]            │
└─────────────────────────────────────┘
```

### 11.4. UX Kuralları

1. **3 saniye kuralı:** Sayfa açıldıktan sonra kullanıcı ne yapacağını 3 saniyede anlamalı.
2. **Tek tık karar:** Tıklama → 1 saniye içinde sağ panel açılır.
3. **Şeffaflık:** Her skor "neden böyle?" sorusuna cevap verir.
4. **Tutarlılık:** Aynı koordinat = aynı skor (deterministik).
5. **Kurtarılabilirlik:** API çökerse demo modu, kullanıcı farkına varmaz.
6. **Karanlık tema:** Renkli haritada yüksek kontrast.
7. **Yatırımcı dili:** "MAPE %12" yerine "tipik hata ±%12".
8. **Klavye desteği:** ESC ile panel kapama, oklar ile harita gezinme.

### 11.5. Performans Hedefleri

- **First Contentful Paint:** <1.5 sn
- **Time to Interactive:** <3 sn
- **Harita zoom akıcılığı:** 60 fps
- **API yanıtı algı:** <500 ms (loading skeleton ile)
- **Bundle boyutu:** <500 KB gzipped

### 11.6. Erişilebilirlik

- Renk körlüğü: yeşil/kırmızı yanına ikon (✓/✗) eklenir
- Kontrast oranı: minimum 4.5:1 (WCAG AA)
- Klavye gezintisi tüm interaktif elemanlar için
- ARIA etiketleri kritik komponentlerde

---

## 12. GELİŞTİRME SÜRECİ VE MULTI-AGENT YAKLAŞIM

### 12.1. Multi-Agent Mimarisi

Claude Code üzerinde **1 orkestratör + 6 subagent** yapısı kullanılacak.

#### Orkestratör: `Architect`
- Subagent'ları sırayla başlatır
- Tip uyumsuzluğunda müdahale eder
- 12. saat feature freeze'i zorlar
- Kapsam dışı taleplere "hayır" der
- Master plan dokümanını referans alır

#### Subagent'lar

| # | Ad | Sorumluluk | Klasör | Başlangıç |
|---|-----|-----------|--------|-----------|
| 1 | **SchemaSmith** | Pydantic + TS tip sözleşmeleri | `/contracts/` | 0. saat |
| 2 | **DataForager** | Statik veri toplama, GeoJSON | `/data-pipeline/` | 0. saat (paralel) |
| 3 | **ScoreSmith** | Skor motoru, fizik formülleri | `/backend/app/scoring/` | 2. saat |
| 4 | **APIWeaver** | FastAPI + Open-Meteo | `/backend/app/` | 4. saat |
| 5 | **MapForge** | React + Leaflet UI | `/frontend/` | 4. saat (paralel) |
| 6 | **ForecastSage** | 48 saatlik tahmin + bakım | `/backend/app/forecast/` | 8. saat |

### 12.2. Subagent Yetki Sınırları

| Subagent | YAPABİLİR | YAPAMAZ |
|----------|-----------|---------|
| SchemaSmith | Tip yazma | Logic yazma, UI yazma |
| DataForager | Veri toplama, temizleme | Skor hesaplama, endpoint |
| ScoreSmith | Saf fonksiyon | Endpoint, UI, veri toplama |
| APIWeaver | Endpoint, servis | Formül değiştirme, tip yazma |
| MapForge | UI komponentleri | Hesaplama, backend |
| ForecastSage | Tahmin, bakım penceresi | LSTM, endpoint, UI |

### 12.3. Subagent Çağırma Şablonu

```markdown
Sen [SUBAGENT_ADI] subagent'isin. Görev tanımın aşağıdadır.
Kapsam dışına çıkmak YASAKTIR.

Çalışma klasörün: [KLASÖR]
Bağımlılıkların: [LİSTE]
Çıktı dosyaların: [LİSTE]
Kapatma kriterin: [KRİTER]

Master plan: docs/hackathon-proje-plani.md
Bağlam: PROJECT_CONTEXT.md

Şimdi başla. İlk adımın [İLK_DOSYA] yazmak.
Her dosyayı yazmadan önce hangi tipleri kullanacağını
contracts/schemas.{py|ts}'den oku.
Yazdığın her dosya sonunda kısa bir doğrulama mesajı ver.
```

### 12.4. Ekip Rolleri (4 Kişi)

| Kişi | Rol | Yönettiği Subagent'lar | Saat Yükü |
|------|-----|------------------------|-----------|
| **K1** | Veri / GIS Mühendisi | DataForager | 0-8 (sonra destek) |
| **K2** | Backend / Skor Geliştirici | SchemaSmith + ScoreSmith + APIWeaver | 0-16 |
| **K3** | Frontend / Harita Geliştirici | MapForge | 4-24 |
| **K4** | ML / Tahmin + Cila | ForecastSage + UI cila | 8-24 |

### 12.5. İletişim Protokolü

- **Slack/Discord kanalı:** Ekip içi anlık iletişim
- **Tip değişiklikleri:** Her zaman SchemaSmith'i güncelle, sonra haber ver
- **Endpoint değişiklikleri:** APIWeaver duyurur, MapForge günceller
- **Bug raporu:** GitHub Issues yerine Discord thread (hızlı)

### 12.6. Versiyon Kontrol

- **Branch stratejisi:** `main` (canlı) + feature branch'ler
- **Commit mesajı:** İngilizce, conventional commits (`feat:`, `fix:`, `docs:`)
- **Pull request:** Hackathon'da fazla ağır, doğrudan main'e push (küçük ekip)
- **Tag:** `v0.1-mvp` (12. saat), `v1.0-demo` (24. saat)

---

## 13. 25 SAATLİK ZAMAN ÇİZELGESİ

### 13.1. Genel Çizelge

| Saat | Faz | Aktif Subagent(lar) | Hedef Çıktı |
|------|-----|---------------------|-------------|
| 0-2 | Kuruluş | SchemaSmith + DataForager | Tip sözleşmeleri, repo iskeleti, mock data |
| 2-4 | Temel | + ScoreSmith | FastAPI iskeleti, skor formülü test geçiyor |
| 4-8 | Paralel inşa | + APIWeaver + MapForge | Health endpoint + boş Leaflet haritası |
| 8-12 | Entegrasyon | + ForecastSage | İlk uçtan uca akış çalışıyor |
| **12** | **🔒 FREEZE** | — | Yeni iş yasak |
| 12-16 | Stabilizasyon | Hepsi | Demo akışı baştan sona çalışıyor |
| 16-20 | Cila | K3, K4 | Top 5, karşılaştırma, finansal kart |
| 20-24 | Doküman | Herkes | README, Model Card, demo videosu |
| 24-25 | Buffer | — | Son provalar |

### 13.2. Kritik Dönüm Noktaları

| Saat | Dönüm noktası | Kontrol kriteri |
|------|---------------|-----------------|
| 2 | Tip sözleşmeleri kapalı | Pydantic ↔ TypeScript birebir eşleşiyor |
| 3 | Veri darboğazı kontrolü | Tüm Türkiye mi, daraltılmış mı? |
| 6 | Skor motoru çalışıyor | Test koordinat için skor üretiliyor |
| 8 | Frontend backend'e bağlandı | Mock data değil, gerçek API |
| 10 | Tahmin grafiği çalışıyor | Forecast endpoint + Recharts render |
| **12** | **Feature freeze** | Hiçbir yeni özellik kabul edilmiyor |
| 14 | Demo akışı çalışıyor | 90 saniyelik akış başarılı |
| 18 | Cila tamam | Tüm UX detayları yerinde |
| 22 | Doküman tamam | README + Model Card hazır |
| 24 | Demo videosu hazır | <2 dakika, kayıtlı |

### 13.3. Saat Saat Detay

#### Saat 0-2 (Kuruluş)
- Repo oluştur, .gitignore
- `contracts/schemas.py` ve `contracts/schemas.ts` yaz
- `data-pipeline/scripts/` iskeleti
- Boş `frontend/` ve `backend/` klasörleri
- `requirements.txt` ve `package.json`
- Mock data dosyaları

#### Saat 2-4 (Temel)
- `backend/app/main.py` (boş FastAPI)
- `backend/app/scoring/physics.py` (formüller + testler)
- İl sınırları GeoJSON indirildi ve basitleştirildi
- `backend/data/provinces.geojson` hazır

#### Saat 4-8 (Paralel İnşa)
- `backend/app/routers/score.py` (mock yanıt)
- `backend/app/routers/provinces.py` (gerçek veri)
- `backend/app/services/openmeteo.py`
- `frontend/src/App.tsx` (Leaflet boş harita)
- `frontend/src/components/MapCanvas.tsx`
- `frontend/src/components/EnergyTypeToggle.tsx`
- OSM landuse verisi alındı/işlendi

#### Saat 8-12 (Entegrasyon)
- `backend/app/forecast/physics_forecast.py`
- `frontend/src/components/DetailPanel.tsx`
- `frontend/src/components/FilterPanel.tsx`
- `frontend/src/components/ForecastChart.tsx`
- İlk uçtan uca tıklama akışı çalışıyor

#### Saat 12 — FEATURE FREEZE 🔒

#### Saat 12-16 (Stabilizasyon)
- Tüm endpoint'ler 200 dönüyor
- Tüm UI komponentleri render oluyor
- Bug fix
- CORS, error handling
- Demo modu test

#### Saat 16-20 (Cila)
- `frontend/src/components/TopFiveCard.tsx`
- `frontend/src/components/CompareView.tsx`
- Finansal kart komponenti
- Bakım penceresi etiketi
- Animasyonlar, geçişler
- Tutarlılık açıklama cümlesi

#### Saat 20-24 (Doküman + Demo)
- README.md (kurulum, kullanım, API dokümantasyonu)
- MODEL_CARD.md (formüller, sınırlılıklar, metrikler)
- DEMO_SCRIPT.md (90 saniyelik akış)
- Demo videosu (ekran kaydı)
- Sunum slaytları (varsa)
- Demo provası 1, 2, 3

#### Saat 24-25 (Buffer)
- Son test
- Demo modu doğrulama
- Yedek video kaydı
- Teslim

---

## 14. RİSK YÖNETİMİ

### 14.1. Risk Matrisi

| Risk | Olasılık | Etki | Önlem |
|------|----------|------|-------|
| LSTM eğitimi başarısız | Yüksek | Yüksek | Prophet + fizik formülü, LSTM yasaklı |
| Google Maps kotası dolar | Orta | Yüksek | Leaflet + OSM (kotasız) |
| Canlı API çökmesi (demo) | Orta | Kritik | `DEMO_MODE=true` ile local JSON |
| Tip uyumsuzluğu | Yüksek | Orta | İlk 2 saatte ortak şema, SchemaSmith truth |
| Kapsam genişlemesi | Çok yüksek | Yüksek | 12. saat feature freeze, Architect zorlar |
| Veri toplama uzar | Orta | Yüksek | 3. saat fallback (Marmara+Ege) |
| OSM Overpass rate limit | Düşük | Orta | Yarışma öncesi hazırlık, cache |
| Frontend performans | Düşük | Orta | GeoJSON basitleştirme, lazy load |
| Tıklama tutarsızlığı | Yüksek | Orta | Detay panelinde zorunlu açıklama |
| Demo gecesi internet | Düşük | Kritik | Demo modu hazır, local JSON |
| Ekip içi iletişim kopması | Düşük | Yüksek | Saatlik check-in, Discord açık |
| Komitleyemediği değişiklik | Orta | Orta | Saatlik commit zorunluluğu |

### 14.2. Acil Durum Planları

#### Plan A — Veri Pipeline Çökerse
- Mock data ile devam
- Önceden hazırlanmış 5-10 örnek koordinatın sabit yanıtları
- "Demo örnekleri" olarak sun

#### Plan B — Backend Çökerse
- Frontend mock data'ya düşer
- localStorage'da örnek yanıtlar
- Demo akışı bozulmaz

#### Plan C — Frontend Build Patlarsa
- Önceden build edilmiş static dist'i deploy et
- `npm run dev` yerine `npm run preview`

#### Plan D — Ekip Üyesi Düşerse (Hastalık vs.)
- O kişinin subagent'ları diğer üyelere paylaştırılır
- Kapsam tekrar daraltılır
- Architect karar verir

### 14.3. Olası Tıkanma Noktaları

**OSM Overpass API yavaş yanıt veriyorsa:**
- Pre-fetched dosyaları kullan
- Geofabrik download'larından statik dosya al

**Prophet kurulumu Windows'ta sorun çıkarıyorsa:**
- Prophet'i atla, sadece fizik formülü kullan
- Demo'da "Prophet'i denedik, fizik yeterli" de

**Mapshaper komut satırı çalışmıyorsa:**
- mapshaper.org online aracını kullan
- veya turf.js ile programatik basitleştir

---

## 15. DEMO STRATEJİSİ

### 15.1. Demo Hedefleri

1. **30 saniyede ürünü anlat** — ilk hookta kazan
2. **90 saniyede tüm kapasiteyi göster** — etkileyici akış
3. **Kapanışta hatırlatıcı bir an** — jüri akılda kalsın

### 15.2. 90 Saniyelik Demo Akışı

| Sn | Aksiyon | Anlatım |
|----|---------|---------|
| 0-10 | Sayfa açılır | "Türkiye'nin yenilenebilir enerji yatırım haritası." |
| 10-20 | "Rüzgâr" düğmesine bas | "Rüzgâr potansiyeline göre renklendirildi." |
| 20-30 | "Trafo<10km" filtresi | "Şebekeye yakın bölgeler vurgulandı." |
| 30-40 | "Top 5" düğmesi | "Türkiye'nin en uygun 5 noktası." |
| 40-55 | 1. noktaya tıkla | "Skor 87, geri ödeme 6.8 yıl, 154kV trafo 6km'de." |
| 55-65 | Tahmin grafiğini göster | "48 saatlik üretim tahmini, ±15% güven aralığı." |
| 65-75 | "Karşılaştırmaya ekle" → 2. nokta | "İki nokta yan yana." |
| 75-85 | Zoom in → ilçe seviyesi | "İl bazından ilçe bazına otomatik geçiş." |
| 85-90 | Kapanış | "RE-Atlas: Türkiye'nin yenilenebilir enerji atlası." |

### 15.3. Demo Hazırlığı

- Demo modu test edildi (internet kesik test)
- Önceden seçilmiş 3-4 "altın koordinat" (görsel olarak çarpıcı)
- Tarayıcı sekmeleri kapalı, bildirimler kapalı
- Ekran kaydı yedek hazır (canlı demo çökerse)
- Sunum bilgisayarı şarjda, internet kontrolü
- İkincil bilgisayar/yedek demo cihazı hazır

### 15.4. Sunum Sırasında Söylenmemesi Gerekenler

- "Aslında bunu da yapacaktık ama..." (kapsam savunması)
- "Eğer çalışırsa..." (güvensizlik)
- "Bu sadece demo, gerçekte daha iyi olacak..." (özür)
- "LSTM kullansaydık daha iyi olurdu..." (kararı sorgulamak)

### 15.5. Sunum Sırasında Vurgulanacaklar

- "25 saatte ürettiğimiz çalışan ürün"
- "Türkiye'ye özgü veri katmanları" (TEİAŞ, OSM landuse)
- "Şeffaf skor — her sayı açıklanabilir"
- "Demo modu ile her zaman çalışır"
- "Pragmatik model seçimi — Prophet + fizik"

---

## 16. KARAR DEFTERİ

Bu bölüm projedeki kritik kararların tarihçesini tutar. Yeni karar verildiğinde buraya eklenir.

### Karar 001 — Coğrafi Kapsam
- **Tarih:** Planlama aşaması
- **Karar:** Tüm Türkiye (Düzce odaklı değil)
- **Gerekçe:** Sunum etkisi, yatırımcı persona için anlamlı
- **Fallback:** 3. saatte Marmara+Ege'ye daralt

### Karar 002 — Harita Kütüphanesi
- **Tarih:** Planlama aşaması
- **Karar:** Leaflet + OSM (Google Maps değil)
- **Gerekçe:** Ücretsiz, kotasız, choropleth dostu
- **Çağrı:** Faturalandırma riski yok

### Karar 003 — Ana ML Modeli
- **Tarih:** Planlama aşaması (3 model hemfikir)
- **Karar:** Prophet + fizik formülü (LSTM iptal)
- **Gerekçe:** 25 saatte LSTM düzgün çalışmaz, yorumlanabilirlik düşük
- **İstisna:** Prophet de opsiyonel, fizik birincil

### Karar 004 — Çözünürlük Stratejisi
- **Tarih:** Planlama aşaması (GPT + Gemini uyarısı sonrası)
- **Karar:** Çift seviye gerçek choropleth (il + ilçe)
- **Gerekçe:** Fake heatmap çelişki yaratır, gerçek veri tutarlı
- **Tutarlılık:** Detay panelinde açıklama cümlesi zorunlu

### Karar 005 — Kullanıcı Modu
- **Tarih:** Planlama aşaması
- **Karar:** Tek mod, yatırımcı persona ana
- **Gerekçe:** 4 kişi 25 saatte iki UI yetiştiremez, filtreler özelleşme sağlar
- **Etki:** Bireysel ve operasyon personaları sadece sunumda bahsedilir

### Karar 006 — Multi-Agent Yaklaşımı
- **Tarih:** Planlama aşaması
- **Karar:** 1 orkestratör + 6 subagent (Architect, SchemaSmith, DataForager, ScoreSmith, APIWeaver, MapForge, ForecastSage)
- **Gerekçe:** Paralel çalışma, yetki sınırı, kapsam disiplini
- **Risk:** Tip uyumsuzluğu — SchemaSmith truth source

### Karar 007 — Feature Freeze Saati
- **Tarih:** Planlama aşaması
- **Karar:** 12. saatte feature freeze
- **Gerekçe:** 13 saatlik stabilizasyon ve cila penceresi gerekli
- **Zorlama:** Architect tüm yeni iş taleplerini reddeder

---

## 17. EKLER

### Ek A — Faydalı Linkler

**Veri Kaynakları:**
- Open-Meteo API: https://open-meteo.com/en/docs
- OSM Overpass: https://overpass-api.de/
- Türkiye GeoJSON: https://github.com/cihadturhan/tr-geojson
- AFAD açık veri: https://www.afad.gov.tr/
- MTA fay haritaları: https://www.mta.gov.tr/
- REPA Atlas: https://repa.enerji.gov.tr/
- GEPA Atlas: https://gepa.enerji.gov.tr/

**Teknoloji Dokümantasyon:**
- FastAPI: https://fastapi.tiangolo.com/
- Pydantic v2: https://docs.pydantic.dev/
- Leaflet: https://leafletjs.com/
- react-leaflet: https://react-leaflet.js.org/
- Recharts: https://recharts.org/
- Prophet: https://facebook.github.io/prophet/
- Tailwind: https://tailwindcss.com/

### Ek B — Komut Hatırlatıcıları

**Backend kurulum:**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend kurulum:**
```bash
cd frontend
npm install
npm run dev    # Vite dev server, port 5173
```

**Veri pipeline:**
```bash
cd data-pipeline
python scripts/fetch_provinces.py
python scripts/fetch_osm_landuse.py
python scripts/simplify_geojson.py
python scripts/precompute_weather_cache.py
```

**Mapshaper (Node.js global):**
```bash
npm install -g mapshaper
mapshaper input.geojson -simplify 5% -o output.geojson
```

### Ek C — Test Senaryoları

#### Test Koordinatları (Manuel Doğrulama İçin)

| Lokasyon | Koordinat | Beklenti |
|----------|-----------|----------|
| Karacabey/Bursa | 40.213, 28.366 | Yüksek rüzgâr skoru |
| Kayseri merkez | 38.733, 35.485 | Yüksek güneş skoru |
| Çamlıca/İstanbul | 41.025, 29.066 | Düşük (yerleşim) |
| Tuz Gölü kıyısı | 38.737, 33.371 | Hibrit yüksek |
| Çatalca ormanı | 41.218, 28.450 | Düşük (orman) |

### Ek D — Sözlük

| Terim | Açıklama |
|-------|----------|
| GHI | Global Horizontal Irradiance — yatay yüzeye düşen toplam güneş ışınımı (W/m² veya kWh/m²) |
| Cp | Power coefficient — türbinin rüzgâr enerjisini elektriğe dönüştürme verimi (max %59.3, pratik %35-45) |
| Capacity Factor | Bir santralin yıllık ürettiği enerjinin, sürekli nominal güçte çalışsaydı üreteceğine oranı |
| LCOE | Levelized Cost of Energy — bir enerji projesinin ömür boyu maliyetinin üretilen enerjiye bölünmesi |
| YEKA | Yenilenebilir Enerji Kaynak Alanları — Bakanlığın tahsis ettiği özel bölgeler |
| REPA | Türkiye Rüzgâr Enerjisi Potansiyel Atlası |
| GEPA | Türkiye Güneş Enerjisi Potansiyel Atlası |
| TEİAŞ | Türkiye Elektrik İletim A.Ş. — iletim sistemini işletir |
| EPDK | Enerji Piyasası Düzenleme Kurumu |
| Choropleth | Bölgelerin sayısal değere göre renklendirildiği harita türü |
| Cut-in / Cut-out | Türbinin çalışmaya başladığı / güvenlik için durduğu rüzgâr hızı |
| MAPE | Mean Absolute Percentage Error — tahmin hatası ölçütü |

---

## SON SÖZ

Bu doküman projenin **detaylı planlama referansıdır**. Tasarım kararları, gerekçeleri, alternatif değerlendirmeleri burada bulunur. Daha kompakt bir özet `PROJECT_CONTEXT.md`'dedir.

Bir karar değiştiğinde **Karar Defteri** (Bölüm 16) güncellenir. Doküman versiyonu yenilenir.

**Doküman versiyonu:** 1.0
**Durum:** Planlama tamamlandı, uygulama başlıyor
**İlgili dosyalar:**
- `PROJECT_CONTEXT.md` (kompakt bağlam)
- `claude-code-master-prompt.md` (orkestrasyon)
- `MODEL_CARD.md` (uygulama sonrası)
- `DEMO_SCRIPT.md` (uygulama sonrası)

---

*"Hız değil disiplin kazandırır. Asıl zafer 12. saatten sonra başlar."*
