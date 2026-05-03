# RE-ATLAS — PROJE BAĞLAM DOSYASI

> **Bu dosyanın amacı:** Farklı AI modelleri (Claude, GPT, Gemini, Claude Antigravity vb.) arasında geçiş yaparken **sıfır bağlam kaybı** yaşamamak. Bu dosya tek başına okunduğunda projenin tüm geçmişi, kararları, mimarisi ve kalan işleri net olarak anlaşılır.
>
> **Kullanım:** Yeni bir AI modeline geçtiğinde bu dosyayı baştan sona oku ve "Bu projenin bağlamını anladın mı?" diye sor. Modelden onay aldıktan sonra konuşmaya devam et.
>
> **Son güncelleme:** Hackathon başlangıcı öncesi planlama aşaması tamamlandı.
> **Proje durumu:** Uygulama aşamasına geçilecek (Claude Code + VS Code).

---

## İÇİNDEKİLER

1. [Proje Kimliği](#1-proje-kimliği)
2. [Yarışma Bağlamı](#2-yarışma-bağlamı)
3. [Fikrin Doğuşu ve Evrimi](#3-fikrin-doğuşu-ve-evrimi)
4. [Çoklu Model Tartışması — Kararların Arka Planı](#4-çoklu-model-tartışması--kararların-arka-planı)
5. [6 Personadan Analiz](#5-6-personadan-analiz)
6. [Donmuş Kapsam (Final)](#6-donmuş-kapsam-final)
7. [Skor Motoru ve Formüller](#7-skor-motoru-ve-formüller)
8. [Veri Katmanları](#8-veri-katmanları)
9. [Teknoloji Yığını](#9-teknoloji-yığını)
10. [Mimari ve Dosya Yapısı](#10-mimari-ve-dosya-yapısı)
11. [Multi-Agent Geliştirme Stratejisi](#11-multi-agent-geliştirme-stratejisi)
12. [25 Saatlik Çalışma Planı](#12-25-saatlik-çalışma-planı)
13. [UX ve Tasarım Kararları](#13-ux-ve-tasarım-kararları)
14. [Demo Akışı](#14-demo-akışı)
15. [Risk Yönetimi](#15-risk-yönetimi)
16. [Açık Sorular ve Bilinen Belirsizlikler](#16-açık-sorular-ve-bilinen-belirsizlikler)
17. [Yeni Modelle Konuşma Başlatma Şablonu](#17-yeni-modelle-konuşma-başlatma-şablonu)

---

## 1. PROJE KİMLİĞİ

| Alan | Değer |
|------|-------|
| **Proje adı** | RE-Atlas |
| **Tek cümle** | Türkiye'nin tamamı için yenilenebilir enerji yatırım uygunluğunu haritada gösteren ve 48 saatlik üretim tahmini sunan karar destek aracı. |
| **Hedef kullanıcı** | Enerji yatırımcısı / saha geliştirme uzmanı (B2B) |
| **Yarışma süresi** | 25 saat |
| **Ekip büyüklüğü** | 4 kişi |
| **Geliştirme ortamı** | VS Code + Claude Code (lokal) |
| **Yardımcı AI modeller** | Claude, GPT, Gemini, Claude Antigravity |

---

## 2. YARIŞMA BAĞLAMI

### 2.1. Seçilen Konu
Yarışmada sunulan birden fazla konu arasından **"Yenilenebilir Enerji Tahmini ve Analizi"** (2 numaralı konu) seçildi.

### 2.2. Yarışmanın Tanımladığı Problem
Türkiye'nin kurulu güneş enerjisi kapasitesi hızla artıyor ancak güneş ve rüzgâr üretimi hava koşullarına bağlı sürekli değişiyor. Bu üretim belirsizliği üç somut sorun yaratıyor:

1. **Bireysel üretici sorunu:** Düzce'nin dağlık bir köyündeki çatı paneli sahibi çiftçi sabah uyandığında bulutlu hava görür, bugün yeterince üretim yapacak mı, satabilir mi bilemez.
2. **Sistem operatörü sorunu:** Enerji şirketleri tahmin yapamadığı için aşırı rezerv tutmak zorunda kalır — hem maliyet hem kaynak israfı.
3. **Bakım planlama sorunu:** Rüzgâr çiftliklerinde bakım ekipleri rüzgârın düşük olduğu saatleri önceden bilebilseydi verimli planlama yapardı.

### 2.3. Yarışmanın Önerdiği Etiketler ve Yaklaşımlar
- **Etiketler:** ML, Time Series, Data Science, LSTM, Prophet, Forecasting
- **Veri & analiz:** Hava durumu API entegrasyonu, zaman serisi tahmini, geçmiş üretim verisi analizi
- **AI/ML:** LSTM ve Prophet, regresyon tabanlı tahmin, ensemble yöntemler
- **Uygulama:** Web uygulaması, API servisi, interaktif harita arayüzü
- **Tasarım:** Sade tahmin arayüzleri, veri görselleştirme

### 2.4. Yarışmanın Önerdiği Veri Kaynakları
- Open-Meteo (ücretsiz hava API)
- PVGIS (Avrupa Güneş Enerjisi Atlası)
- EMRA/EPDK açık verileri
- NREL açık enerji veri setleri

### 2.5. Yarışmanın Önerdiği Örnek Çözüm Fikirleri
*(yarışma sayfasında "ilham için" denen fikirler — birebir uygulanması beklenmiyor)*
- 24-48 saat üretim tahmin sistemi
- Küçük üreticiye "bugün sat mı, depola mı?" karar destek aracı
- Türkiye il bazında karşılaştırmalı potansiyel haritası
- "Çatıma panel kursam ne kadar tasarruf ederim?" hesaplayıcı
- Üretim anomalisi tespit sistemi

---

## 3. FİKRİN DOĞUŞU VE EVRİMİ

### 3.1. İlk Yön (Gemini Önerisi)
İlk olarak Gemini ile konuşuldu. Gemini, fikri genel hatlarıyla onayladı ve dört yardım alanı önerdi: konsept geliştirme, veri pipeline, ML modelleme, UI/UX. Üç alternatif persona sundu (Düzceli bireysel, büyük enerji şirketi, bakım ekibi).

### 3.2. İkinci Adım (Kullanıcının Yön Verişi)
Kullanıcı üç fikri **birleştirme kararı** aldı: "Haritalar üzerinden bölge uygunluğuna bağlı olarak kurulabilecek sistem önerisi + kurulu bölgeler için hava durumuna bağlı tahmin sistemi + bakım ekibi yönlendirmesi." Google Maps API'yi tercih ettiğini belirtti.

### 3.3. Eleştirel Değerlendirme (Claude — Jeopolitik & AI Analisti Rolü)
Claude, fikrin DNA'sının sağlam ama aşağıdaki noktalarda eksik olduğunu söyledi:

- **Kapsam fazla geniş:** Üç farklı problem (site selection, forecasting, route optimization) tek projede yapılmaya çalışılıyor. Birini omurga seçilmeli.
- **Google Maps yanlış araç:** Faturalandırma riski, choropleth zayıf, demo gecesi kota dolar. **Leaflet + OSM** önerildi.
- **Veri katmanı eksik:** Sadece hava verisi yetmez. Türkiye için kritik katmanlar: **YEKA, REPA/GEPA, TEİAŞ trafo merkezleri, OSM landuse, AFAD fay hatları, EPDK lisanssız üretim eşiği, net mahsuplaşma rejimi**.
- **LSTM tuzağı:** 25 saatte düzgün eğitim çok zor. **Prophet + XGBoost + fizik formülü** önerildi.
- **Demo riskleri:** Canlı API kotası, harita yavaşlığı, persona dağınıklığı.

### 3.4. Kapsamı Daraltma Kararı
Kullanıcı şu kararı verdi:
> *"Ana odağım Bölge uygunluk haritası olacak. Üretim tahmini ve bakım yönlendirmesi yan ürün olacak."*

Coğrafi kapsam kararı: **Düzce odaklı DEĞİL, tüm Türkiye haritası.**

### 3.5. Çoklu Persona Analizi
Kullanıcı projeyi 6 farklı kullanıcı gözünden analiz etmeyi istedi. (Detay [Bölüm 5](#5-6-personadan-analiz)'te.) Bu analiz, projenin **tek mod ile çoklu personaya hizmet etmesi** kararını doğurdu — ayrı modlar yerine filtre ve görünüm parametreleriyle özelleşme.

### 3.6. Tüm Türkiye Kapsamına Geçiş ve Çözünürlük Tartışması
Kullanıcı tüm Türkiye dedikten sonra üç çözünürlük yaklaşımı tartışıldı:
- **(A)** Sadece il bazlı choropleth — basit, garantili
- **(B)** Grid heatmap (5km × 5km hücreler) — ~30.000 hücre, ağır
- **(C)** Hibrit (il/ilçe choropleth + tıklamada canlı API) — etkileyici

Kullanıcı **(C) hibrit yaklaşımı** seçti. Ancak GPT ve Gemini'nin uyarısıyla "fake heatmap" fikrinden vazgeçildi. Final çözüm: **çift seviye gerçek choropleth (zoom out → 81 il, zoom in → ~973 ilçe)**, tıklamada koordinat-spesifik canlı API çağrısı.

### 3.7. LSTM'den Vazgeçiş (3 Model Hemfikir)
Üç model de aynı uyarıyı verdi: 25 saatte LSTM düzgün çalışmaz, "gösterişli ama zayıf" sonuç çıkar. Karar: **LSTM iptal, ana model Prophet + fizik formülü.**

### 3.8. Mod Sayısı Kararı
GPT iki mod (Bireysel + Kurumsal), Gemini ve Claude tek mod önerdi. Kullanıcı **tek mod, yatırımcı persona ana hedef** kararını verdi. Diğer personalar sunumda bahsedilecek ama UI'de ayrı ekran almayacak.

---

## 4. ÇOKLU MODEL TARTIŞMASI — KARARLARIN ARKA PLANI

### 4.1. Üç Modelin Hemfikir Olduğu Konular

| Konu | Final Karar | Gerekçe |
|------|-------------|---------|
| LSTM | İptal | 25 saatte düzgün eğitilemez |
| Ana model | Prophet + fizik formülü | Hızlı, yorumlanabilir |
| Harita kütüphanesi | Leaflet + OSM | Ücretsiz, kotasız, choropleth dostu |
| Ana ürün | Bölge uygunluk skoru | Tek net değer önerisi |
| Tahmin modülü | Yan özellik | Ana hikayeyi sulandırmaz |
| Bakım modülü | Tek satır metin | Gerçek route optimization yok |
| Cache stratejisi | Demo modu zorunlu | API çökerse demo kurtarılır |
| Feature freeze | 12. saat | Entegrasyon için yeterli pay |

### 4.2. Modeller Arası Görüş Ayrılığı ve Çözüm

**GPT:** Hibrit çözünürlükteki "fake heatmap" tehlikeli — kullanıcı kırmızı yere tıklayıp yeşil skor görürse güven kaybı.
**Gemini:** Sadece il bazlı choropleth, fake'le uğraşma.
**Claude:** İkisini birleştirelim — il+ilçe çift seviye gerçek choropleth, fake yok.

→ **Final:** Claude'un sentez önerisi kabul edildi.

**GPT:** İki mod (Bireysel + Kurumsal) gerekli.
**Gemini:** Tek mod yeterli, filtreler özelleşmeyi sağlar.
**Claude:** 4 kişi 25 saatte iki UI akışı yetiştiremez, tek mod doğru.

→ **Final:** Tek mod, yatırımcı persona.

### 4.3. Tutarlılık Çözümü
Çift seviye choropleth'te il skoru ile koordinat skoru farklı olabilir. Bu çelişkiyi engellemek için **detay panel başlığında zorunlu açıklama cümlesi** eklendi:

> *"İl genel skoru: 72 / Bu nokta: 84 — fark mikro-koşullar ve şebeke yakınlığından kaynaklanıyor."*

---

## 5. 6 PERSONADAN ANALİZ

### 5.1. Bireysel Kullanıcı (Çiftçi / Ev / Arsa Sahibi)
- **İhtiyacı:** Sayı söyle bana — geri ödeme süresi, yıllık kazanç, hangi sistem.
- **Göremediği:** Çatı yönü/eğimi, gölgeleme, gürültü regülasyonu, lisanssız üretim sınırı.
- **Sistem kararı:** Demo'da bahsedilecek ama UI'de ayrı mod yok.

### 5.2. Enerji Şirketi / Yatırımcı (ANA PERSONA)
- **İhtiyacı:** İl/ilçe sıralaması, top 10 liste, dışlama filtreleri, finansal kart.
- **Bilmesi gerekenler:** Capacity factor, LCOE, en yakın trafo, türbülans, wind rose.
- **Sistem kararı:** **Ürünün ana yüzü bu personadır.** B2B konumlandırma kapısı, ödeme yapan müşteri.

### 5.3. Bakım Ekibi Yöneticisi
- **İhtiyacı:** 7 günlük tahmin, "yarın 14:00-17:00 bakım uygun" önerisi.
- **Sistem kararı:** Sadece **tek satır metin** olarak detay panelinde. Ayrı modül YOK.

### 5.4. Jeopolitik Veri Analisti
- **İhtiyacı:** Bölgesel eşitsizlik, stratejik koridor, iklim projeksiyonu.
- **Sistem kararı:** **Demoda gösterilmeyecek.** Sadece sunumda "altyapı buna da hizmet edebilir" diye bahsedilir.

### 5.5. AI/ML Analisti (Teknik Jüri)
- **İhtiyacı:** MAE/RMSE/MAPE, baseline karşılaştırması, feature importance, belirsizlik.
- **Sistem kararı:** README'ye **Model Card** eklenecek. Test coverage minimum %70 hedefli.

### 5.6. Maliyet Koordinatörü / Finans Modelcisi
- **İhtiyacı:** CAPEX, OPEX, NPV, IRR, geri ödeme, LCOE.
- **Sistem kararı:** Detay panelinde **Finansal Görünüm Kartı** + "ön değerlendirme amaçlıdır" disclaimer'ı.

---

## 6. DONMUŞ KAPSAM (FİNAL)

### 6.1. KAPSAM İÇİ (yapılacak)

**Ana ürün — Bölge Uygunluk Haritası:**
- ✅ Türkiye haritası (Leaflet + OSM dark theme)
- ✅ Çift seviye choropleth: zoom out → 81 il, zoom in → ~973 ilçe
- ✅ 3 mod düğmesi: Güneş / Rüzgâr / Hibrit
- ✅ Tıklamada koordinat-spesifik canlı API çağrısı + sağ panel
- ✅ "En iyi 5 nokta" özelliği
- ✅ İki nokta karşılaştırma modu
- ✅ Sol filtre paneli: Ormanları gizle, Trafo<10km, vb.
- ✅ Renk kodlu skor görselleştirmesi (yeşil/sarı/kırmızı)

**Yan ürün 1 — 48 Saatlik Tahmin (basit):**
- ✅ Tıklanan noktada Open-Meteo forecast + fizik formülü
- ✅ Tek grafik, ±%15 belirsizlik bandı
- ⚠️ Prophet **opsiyonel**, sadece zaman kalırsa

**Yan ürün 2 — Bakım Penceresi (minimal):**
- ✅ "Yarın 14:00-17:00 düşük üretim — bakım için uygun" tek cümle
- ✅ Detay panelinin altında küçük etiket
- ❌ Ayrı sayfa/modül YOK

### 6.2. KAPSAM DIŞI (kesin yapılmayacak)
- ❌ LSTM (3 model hemfikir)
- ❌ Gerçek route/vehicle optimization
- ❌ Çoklu kullanıcı modu (tek mod kararı)
- ❌ Jeopolitik/politika analiz modülü
- ❌ Grid heatmap fake (PNG overlay)
- ❌ PDF export ana özellik olarak (sadece bonus, son saat)
- ❌ Bulut örtüsü what-if simülasyonu
- ❌ REPA/GEPA overlay (sadece referans değer iç doğrulamada)
- ❌ Anomali tespit modülü (bonus, feature freeze sonrası)

### 6.3. ŞARTLI KAPSAM (3. saat kontrolüyle)
- ⚠️ Tüm Türkiye verisi 3 saat içinde alınamazsa **Marmara + Ege'ye daralt** (16 il)

---

## 7. SKOR MOTORU VE FORMÜLLER

### 7.1. Ana Skor Formülü
```
Uygunluk_Skoru = w1·KaynakPotansiyeli
               + w2·AraziUygunluğu
               + w3·ŞebekeYakınlığı
               + w4·RiskFaktörü     (negatif)
               + w5·EkonomikFizibilite
```

### 7.2. Bileşenler

**KaynakPotansiyeli:**
- Güneş için yıllık GHI (kWh/m²/yıl), Open-Meteo'dan
- Rüzgâr için 50m yükseklikte ortalama hız + capacity factor proxy

**AraziUygunluğu (0-1):**
- Orman / SİT / askeri = 0
- Tarım = 0.3
- Çorak / uygun = 1
- OSM landuse'den

**ŞebekeYakınlığı:**
- En yakın iletim hattına mesafe
- 5 km altı = 1, 50 km üstü = 0, lineer interpolasyon

**RiskFaktörü:**
- Deprem + heyelan + sel
- İlk versiyonda **sabit varsayım**

**EkonomikFizibilite:**
- Bölgesel arazi maliyeti proxy + LCOE
- İlk versiyonda **sabit varsayım**

### 7.3. Ağırlıklar (Persona Bazlı, Filtre ile Değişir)
- **Yatırımcı (varsayılan):** w1=0.4, w2=0.2, w3=0.3, w4=0.05, w5=0.05
- **Bireysel (filtre ile):** w1=0.3, w2=0.1, w3=0.05, w4=0.05, w5=0.5
- **İlk versiyonda yalnızca w1, w2, w3 hesaplanır.** w4, w5 sabit.

### 7.4. Fizik Formülleri

**Rüzgâr gücü (kW):**
```
P_wind = 0.5 × ρ × A × v³ × Cp
```
- ρ = 1.225 kg/m³ (hava yoğunluğu)
- Cp = 0.4 (Betz limiti pratik değeri)
- A = π × r² (rotor süpürme alanı)

**Güneş üretimi (kWh/gün):**
```
E_solar = GHI × panel_area × panel_efficiency × performance_ratio
```
- panel_efficiency ≈ 0.18
- performance_ratio ≈ 0.80

**Capacity factor (rüzgâr):**
```
CF = Σ P(v_t) / (P_rated × n_hours)
```

**Belirsizlik bandı:** ±%15 rule-based.

---

## 8. VERİ KATMANLARI

| Katman | Kaynak | Öncelik |
|--------|--------|---------|
| Hava verisi (canlı + tarihsel) | Open-Meteo API | ZORUNLU |
| İl + ilçe sınırları | GitHub açık GeoJSON (cihadturhan/tr-geojson) | ZORUNLU |
| OSM landuse (orman/tarım/yerleşim) | Overpass API | ZORUNLU |
| OSM power (trafo + iletim hattı) | Overpass API | YÜKSEK |
| AFAD fay hatları | MTA açık veri | OPSİYONEL |
| YEKA bölgeleri (~10 nokta) | Manuel | OPSİYONEL |
| REPA/GEPA | Sadece referans/iç doğrulama | OPSİYONEL |

**Cache stratejisi:**
- 81 il merkezi için son 1 yılın saatlik verisi → SQLite
- OSM verileri → basitleştirilmiş GeoJSON (Mapshaper ile)
- Demo modunda tüm veri local JSON'dan okunur

---

## 9. TEKNOLOJİ YIĞINI

| Katman | Teknoloji |
|--------|-----------|
| Frontend | React 18 + Vite + TypeScript + TailwindCSS |
| Harita | Leaflet + react-leaflet |
| State management | Zustand |
| Grafik | Recharts |
| Backend | Python 3.11 + FastAPI + Pydantic v2 |
| HTTP client (BE) | httpx |
| ML | Prophet (opsiyonel) + NumPy |
| Cache | SQLite |
| Veri formatı | GeoJSON, JSON |
| Geliştirme | VS Code + Claude Code |
| Versiyon kontrol | Git |

---

## 10. MİMARİ VE DOSYA YAPISI

```
re-atlas/
├── README.md
├── docs/
│   ├── PROJECT_CONTEXT.md          ← bu dosya
│   ├── hackathon-proje-plani.md
│   ├── claude-code-master-prompt.md
│   ├── MODEL_CARD.md
│   └── DEMO_SCRIPT.md
│
├── contracts/                      ← Tip sözleşmeleri (single source of truth)
│   ├── schemas.py                  (Pydantic v2)
│   ├── schemas.ts                  (TypeScript)
│   └── README.md
│
├── data-pipeline/
│   └── scripts/
│       ├── fetch_provinces.py
│       ├── fetch_districts.py
│       ├── fetch_osm_landuse.py
│       ├── fetch_osm_power.py
│       ├── precompute_weather_cache.py
│       └── simplify_geojson.py
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── score.py
│   │   │   ├── forecast.py
│   │   │   ├── provinces.py
│   │   │   ├── districts.py
│   │   │   └── top.py
│   │   ├── scoring/
│   │   │   ├── engine.py
│   │   │   ├── physics.py
│   │   │   ├── landuse.py
│   │   │   ├── grid_proximity.py
│   │   │   └── weights.py
│   │   ├── forecast/
│   │   │   ├── physics_forecast.py
│   │   │   ├── prophet_wrapper.py
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
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/
    ├── src/
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
    │   ├── api/client.ts
    │   ├── store/useAppStore.ts
    │   ├── types/                  ← contracts/schemas.ts kopyası
    │   ├── mocks/
    │   └── styles/globals.css
    ├── package.json
    ├── vite.config.ts
    ├── tsconfig.json
    └── tailwind.config.js
```

### Backend Endpoint'leri
```
GET /api/health
GET /api/score?lat={}&lon={}&type={solar|wind|hybrid}
GET /api/provinces
GET /api/districts?province_id={}
GET /api/forecast?lat={}&lon={}&hours=48
GET /api/top?type={}&n=5
GET /api/nearest-substation?lat={}&lon={}
GET /api/landuse?lat={}&lon={}
```

---

## 11. MULTI-AGENT GELİŞTİRME STRATEJİSİ

Claude Code üzerinde 1 orkestratör + 6 subagent yapısı kullanılacak. Detayı `claude-code-master-prompt.md`'de.

### 11.1. Orkestratör: `Architect`
- Subagent'ları sırayla başlatır
- Tip uyumsuzluğunda müdahale eder
- 12. saat feature freeze'i zorlar
- Kapsam dışı taleplere "hayır" der

### 11.2. Subagent'lar

| # | Ad | Sorumluluk | Klasör | Başlangıç |
|---|-----|-----------|--------|-----------|
| 1 | **SchemaSmith** | Pydantic + TS tip sözleşmeleri | `/contracts/` | 0. saat |
| 2 | **DataForager** | Statik veri toplama, GeoJSON temizleme | `/data-pipeline/` | 0. saat (paralel) |
| 3 | **ScoreSmith** | Skor motoru, fizik formülleri | `/backend/app/scoring/` | 2. saat |
| 4 | **APIWeaver** | FastAPI endpoint'leri, Open-Meteo entegrasyonu | `/backend/app/` | 4. saat |
| 5 | **MapForge** | React + Leaflet UI | `/frontend/` | 4. saat (paralel) |
| 6 | **ForecastSage** | 48 saatlik tahmin, bakım penceresi | `/backend/app/forecast/` | 8. saat |

### 11.3. Subagent Çağırma Şablonu
```
Sen [SUBAGENT_ADI] subagent'isin. Görev tanımın aşağıdadır.
Kapsam dışına çıkmak YASAKTIR.
Çalışma klasörün: [KLASÖR]
Bağımlılıkların: [LİSTE]
Çıktı dosyaların: [LİSTE]
Kapatma kriterin: [KRİTER]

Master plan: docs/PROJECT_CONTEXT.md
Şimdi başla. İlk adımın [İLK_DOSYA] yazmak.
```

### 11.4. Subagent Yetki Sınırları
- SchemaSmith **sadece** tip yazar, logic yazmaz
- DataForager veri toplar, skor hesaplamaz
- ScoreSmith saf fonksiyon yazar, endpoint yazmaz
- APIWeaver endpoint yazar, formül değiştirmez
- MapForge UI yazar, hesaplama yapmaz
- ForecastSage tahmin üretir, **LSTM'e DOKUNMAZ**

---

## 12. 25 SAATLİK ÇALIŞMA PLANI

| Saat | Aktif Subagent(lar) | Hedef Çıktı | Sahip |
|------|---------------------|-------------|-------|
| 0-2 | SchemaSmith + DataForager | Tip sözleşmeleri, repo iskeleti, mock data | Herkes |
| 2-4 | + ScoreSmith | FastAPI iskeleti, skor formülü test geçiyor | K2, K3 |
| 4-8 | + APIWeaver + MapForge | Health endpoint + boş Leaflet haritası | K2, K3 |
| 8-12 | + ForecastSage; tüm agent'lar entegre | İlk uçtan uca akış çalışıyor | Hepsi |
| **12** | **🔒 FEATURE FREEZE** | Yeni iş yasak, sadece bug fix | Architect |
| 12-16 | Entegrasyon + bug fix | Demo akışı çalışıyor | Hepsi |
| 16-20 | UX cila, Top 5, karşılaştırma, finansal kart | Demo provası 1 | K3, K4 |
| 20-24 | README, Model Card, demo videosu | Demo provası 2-3 | Herkes |
| 24-25 | Buffer | — | — |

### 12.1. Ekip Rolleri (4 Kişi)

| Kişi | Rol | Subagent'lar | Saat Yükü |
|------|-----|--------------|-----------|
| **K1** | Veri / GIS | DataForager | 0-8 (sonra destek) |
| **K2** | Backend / Skor Motoru | SchemaSmith + ScoreSmith + APIWeaver | 0-16 |
| **K3** | Frontend / Harita | MapForge | 4-24 |
| **K4** | ML / Tahmin + Cila | ForecastSage + UI cila | 8-24 |

---

## 13. UX VE TASARIM KARARLARI

### 13.1. Tasarım Dili

**Renk paleti:**
- Arkaplan: koyu lacivert `#0B1220`
- Panel: `#111A2E`
- Yüksek skor (yeşil): `#22C55E`
- Orta skor (sarı): `#FACC15`
- Düşük skor (kırmızı): `#EF4444`
- Güneş modu: `#F59E0B`
- Rüzgâr modu: `#3B82F6`
- Metin: `#E5E7EB`

**Tipografi:**
- UI: Inter
- Sayılar/kodlar: JetBrains Mono

**Buton stili:**
- `rounded-2xl`, hafif glow, hover'da scale 1.02

**Harita teması:** CartoDB Dark Matter veya Stadia Maps Dark

### 13.2. Layout (1440×900)
```
┌─────────────────────────────────────────────────┐
│ [Logo] RE-Atlas    [Solar][Wind][Hybrid]    ⚙  │
├──────┬──────────────────────────────────┬──────┤
│      │                                  │      │
│ FİLTRE│        TÜRKİYE HARİTASI         │ DETAY│
│ PANEL │   (Leaflet, koyu tema)          │ PANEL│
│      │                                  │      │
│ □ Orman                                 │      │
│ □ Trafo<10km                            │      │
│ □ Sit alanı dışla                       │      │
│      │                                  │      │
│      │  [Top 5 göster]   [Karşılaştır]  │      │
└──────┴──────────────────────────────────┴──────┘
```

### 13.3. Detay Panel İçeriği (Tıklamada Açılır)
1. Konum başlığı (il/ilçe + koordinat)
2. Büyük skor rozeti (84/100, renkli)
3. Skor kırılımı: Kaynak / Arazi / Şebeke (3 mini-bar)
4. Önerilen sistem cümlesi *(örn: "Bu nokta için **rüzgâr enerjisi** önerilir. 50m'de 7,2 m/s ortalama hız, 6 km'de 154 kV trafo.")*
5. 48 saatlik tahmin grafiği (belirsizlik bandlı)
6. Bakım penceresi etiketi
7. Finansal kart (CAPEX, yıllık üretim, geri ödeme)
8. *"Karşılaştırmaya ekle"* butonu
9. **ZORUNLU:** Tutarlılık cümlesi *("İl genel skoru: 72 / Bu nokta: 84 — fark mikro-koşullar ve şebeke yakınlığından")*

### 13.4. UX Kuralları
1. **3 saniye kuralı:** Sayfa açıldıktan sonra kullanıcı ne yapacağını 3 saniyede anlamalı.
2. **Tek tık karar:** Tıklama → 1 saniyede sağ panel.
3. **Şeffaflık:** Her skor "neden böyle?" sorusuna cevap verir.
4. **Tutarlılık:** Aynı koordinat = aynı skor (deterministik).
5. **Kurtarılabilirlik:** API çökerse demo modu devreye girer.
6. **Karanlık tema:** Renkli haritada yüksek kontrast.
7. **Yatırımcı dili:** "MAPE %12" yerine "tipik hata ±%12".

---

## 14. DEMO AKIŞI

90 saniyede tamamlanacak akış:

1. Sayfa açılır → Türkiye haritası dolu, illere göre boyalı.
2. "Rüzgâr" düğmesine basılır → harita 300 ms cross-fade ile yeniden renklenir.
3. "Trafo<10km" filtresi açılır → bazı iller solar, bazıları parlak kalır.
4. "Top 5" düğmesine basılır → 5 nokta vurgulanır + liste.
5. 1. sıradaki noktaya tıklanır → sağ panel açılır (skor 87/100, grafik, bakım penceresi).
6. "Karşılaştırmaya ekle" → ikinci noktaya tıklanır → "Karşılaştır" → yan yana metrikler.
7. Zoom in yapılır → choropleth ilçeye geçer (cross-fade).
8. Bir ilçeye tıklanır → daha keskin koordinat verisi.

---

## 15. RİSK YÖNETİMİ

| Risk | Önlem |
|------|-------|
| LSTM eğitimi başarısız | Prophet + fizik formülü; LSTM yasaklı |
| Google Maps kotası | Leaflet + OSM kullanılıyor |
| Canlı API çöker | `DEMO_MODE=true` ile local JSON |
| Tip uyumsuzluğu (entegrasyon) | İlk 2 saatte ortak şema, SchemaSmith truth source |
| Kapsam genişler | 12. saat feature freeze, Architect zorlar |
| Veri toplama uzar | 3. saat fallback: Marmara + Ege'ye daralt |
| 30.000 grid hücresi yavaşlatır | Grid heatmap iptal, çift seviye choropleth |
| Demo gecesi internet | Demo modu hazır, local JSON |
| Çoklu mod karmaşası | Tek mod kararı, filtrelerle özelleşme |
| Tıklama tutarsızlığı (il vs koordinat) | Detay panelinde zorunlu açıklama cümlesi |

---

## 16. AÇIK SORULAR VE BİLİNEN BELİRSİZLİKLER

### 16.1. Karara Bağlanmış (kapatıldı)
- ✅ Çözünürlük: çift seviye gerçek choropleth
- ✅ Mod sayısı: tek
- ✅ Ana model: Prophet + fizik
- ✅ Harita: Leaflet
- ✅ Coğrafya: tüm Türkiye

### 16.2. Karara Bağlanacak (Uygulama Aşamasında)
- ❓ Frontend için Zustand mı Redux mu? (Önerilen: Zustand — daha hafif)
- ❓ Grafik kütüphanesi: Recharts mı Chart.js mi? (Önerilen: Recharts — React-native)
- ❓ Tailwind config'inde özel renk değişkenleri nasıl tanımlanır? (subagent kararı)
- ❓ Test coverage hedefi: %70 yeterli mi? (subagent kararı)

### 16.3. Bilinen Belirsizlikler
- ⚠️ TEİAŞ trafo verisinin OSM'de ne kadar tam olduğu — yarışma başında kontrol edilecek
- ⚠️ Open-Meteo rate limit'in 25 saat boyunca yeterli olup olmayacağı
- ⚠️ Mapshaper komut satırı Windows'ta sorunsuz mu

---

## 17. YENİ MODELLE KONUŞMA BAŞLATMA ŞABLONU

Yeni bir AI modeline geçtiğinde şu mesajla başla:

```
Merhaba. RE-Atlas adlı bir hackathon projesi üzerinde çalışıyorum.
Aşağıda projenin tüm bağlamı bulunuyor — lütfen baştan sona oku
ve "Anladım" dedikten sonra konuşmaya başlayalım.

[PROJECT_CONTEXT.md içeriğini buraya yapıştır]

---

Onay verir misin? Eğer bir noktada belirsizlik varsa veya
ek soru sorman gerekiyorsa şimdi sor. Sonrasında [şu konuda]
yardım istiyorum: ...
```

### 17.1. Modelin Anladığını Doğrulama Soruları
Yeni modele bağlamı verdikten sonra şu soruları sorarak anlayışını test et:

1. "Projenin ana ürünü nedir, yan ürünler ne?"
2. "LSTM neden iptal edildi?"
3. "Hangi veri kaynaklarını zorunlu kullanacağız?"
4. "Feature freeze ne zaman ve neden?"
5. "Demo modu ne işe yarıyor?"
6. "6 subagent'in sorumluluk alanları nedir?"

Modelin tüm sorulara doğru cevap vermesi gerekir. Yanlış cevap varsa ilgili bölümü tekrar okutturun.

---

## SON SÖZ

Bu doküman projenin **tek doğruluk kaynağıdır**. Herhangi bir karar bu dokümanla çelişiyorsa doküman kazanır. Doküman güncellenmediği sürece kararlar değişmemiştir.

Projenin başarısı 25 saatte yapılan kod miktarına değil, **kapsam disiplinine, subagent koordinasyonuna ve demo gecesi çalışan bir ürüne** bağlıdır.

Bol şans.

---

**Doküman versiyonu:** 1.0 (planlama tamamlandı, uygulama başlıyor)
**Son güncelleyen:** Architect (Claude)
**İlgili dosyalar:**
- `docs/hackathon-proje-plani.md` (detaylı proje planı)
- `docs/claude-code-master-prompt.md` (Claude Code orkestrasyon promptu)
- `contracts/schemas.{py,ts}` (tip sözleşmeleri — uygulama başında oluşturulacak)
