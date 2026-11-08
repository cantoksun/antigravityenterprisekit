---
name: seo-fundamentals
description: teknik seo temelleri, e-e-a-t standartları, core web vitals ve arama motoru indeksleme ilkeleri.
priority: p2-specialized
version: 2.0.0
---

# teknik arama motoru optimizasyonu (seo) kurumsal standartları

bu beceri; web uygulamalarının arama motorları tarafından eksiksiz indekslenmesi, core web vitals performans metrikleri, anlamsal html hiyerarşisi ve meta veri yapılarını yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 15 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir modül tamamlanır.
   - sadelik ve modern trend teknolojiler: next.js metadata api, anlamsal html5, sitemap/robots otomasyonu.
   - bellek, lazy loading ve hız optimizasyonu (9. ve 13. kural ile doğrudan bağlantılıdır).
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki teknik seo yönergeleri.

---

## 🔍 kurumsal teknik seo standartları

### 1. anlamsal html (semantic html) ve başlık hiyerarşisi
- her sayfada mutlaka **yalnızca 1 adet `<h1>`** etiketi bulunmalıdır; sayfanın ana amacını ve odak konusunu içermelidir.
- başlıklar sırasıyla `<h2>`, `<h3>` şeklinde mantıksal bir hiyerarşiyle inmeli; sırf görsel boyutlandırma için başlık etiketi atlanmamalıdır (stil için tailwind sınıfları kullanılmalıdır).
- içerikler `<header>`, `<main>`, `<nav>`, `<article>`, `<section>`, `<footer>` gibi anlamsal etiketlerle ayrılmalıdır.

### 2. meta veriler ve dinamik open graph (og) etiketleri
- arama sonuçlarında ve sosyal paylaşımlarda doğru görünüm için title, description, canonical url ve og etiketleri eksiksiz tanımlanmalıdır:
  ```typescript
  // next.js app router metadata api
  export const metadata: Metadata = {
    title: {
      default: 'antigravity kit - kurumsal yapay zeka ajan kiti',
      template: '%s | antigravity kit',
    },
    description: 'kurumsal seviyede yüksek standartlı türkçe yapay zeka ajan ve beceri kiti.',
    alternates: {
      canonical: 'https://ornek.com/mevcut-sayfa',
    },
    openGraph: {
      title: 'antigravity kit',
      description: 'kurumsal yapay zeka ajan kiti',
      url: 'https://ornek.com',
      siteName: 'antigravity',
      locale: 'tr_TR',
      type: 'website',
    },
  };
  ```

### 3. core web vitals standartları (9. ve 13. kural uyumu)
google sıralama algoritmasında doğrudan yer alan hız metrikleri yeşil bölgede tutulmalıdır:
- **lcp (en büyük içerikli boyama - largest contentful paint):** < 2.5 saniye (kritik görsel önceden yüklenmeli - `priority` etiketi).
- **inp (sonraki boyamayla etkileşim - interaction to next paint):** < 200 ms (ana iş parçacığı bloklanmamalı).
- **cls (kümülatif düzen kayması - cumulative layout shift):** < 0.1 (görsellere ve reklamlara sabit `width`/`height` verilmeli, sayfa atlamaları önlenmeli).

### 4. robots.txt ve dinamik sitemap.xml
- `robots.txt` ile api rotaları (`/api/*`) ve yönetim paneli (`/admin/*`) taranmaya kapatılmalı; kamusal sayfalar için sitemap bağlantısı belirtilmelidir:
  ```plaintext
  User-agent: *
  Disallow: /api/
  Disallow: /admin/
  Allow: /
  
  Sitemap: https://ornek.com/sitemap.xml
  ```
