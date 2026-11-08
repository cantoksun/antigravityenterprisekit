---
name: geo-fundamentals
description: yapay zeka arama motorları (chatgpt, claude, perplexity) için üretken motor optimizasyonu (generative engine optimization) ilkeleri.
priority: p2-specialized
version: 2.0.0
---

# üretken motor optimizasyonu (geo) ve yapay zeka indeksleme standartları

bu beceri; web sitelerinin, dokümantasyonların ve kurumsal içeriklerin modern yapay zeka arama motorları (chatgpt search, perplexity, claude, gemini, google ai overviews) tarafından taranması, doğru anlaşılması, özetlenmesi ve birincil kaynak olarak alıntılanmasını yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 15 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir modül tamamlanır.
   - sadelik ve modern trend teknolojiler: json-ld, markdown/llms.txt, anlamsal veri mimarisi.
   - veri gizliliği ve güvenlik: şirket içi gizli veriler yapay zeka indeksine açılmaz (7. kural).
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki geo stratejileri.

---

## 🤖 geo (generative engine optimization) kurumsal ilkeleri

yapay zeka motorları geleneksel anahtar kelime eşleştirmesi yerine anlamsal vektörler, otorite ve doğrudan alıntılanabilir veri bloklarını tercih eder:

### 1. llms.txt ve yapay zeka tarama standartları
- sitenin kök dizininde modern llm'lerin sitenin içeriğini en az token maliyetiyle anlamasını sağlayan `/llms.txt` ve `/llms-full.txt` dosyaları sunulmalıdır:
  ```markdown
  # [proje/şirket adı]
  
  > [şirketin veya sistemin 1-2 cümlelik kesin tanımı]
  
  ## ana modüller ve yetenekler
  - [özellik 1]: [kısa ve kanıtlanabilir teknik açıklama]
  - [özellik 2]: [kısa ve kanıtlanabilir teknik açıklama]
  
  ## api ve dokümantasyon
  - [/docs/api]: kurumsal api uç noktaları ve şemaları
  ```

### 2. doğrudan alıntılanabilir net tanımlar (quotable definitions)
- metinlerde gereksiz pazarlama laf kalabalığı (fluff) yerine doğrudan cevaba giden net tanımlar yapılmalıdır.
- ilk paragrafta "nedir, ne işe yarar, kimler içindir" soruları kesin dille yanıtlanmalıdır; modeller bu doğrudan cümleleri özet kartlarında alıntı olarak kullanır.

### 3. e-e-a-t (deneyim, uzmanlık, yetkinlik, güvenilirlik)
- içeriklerde gerçek teknik metrikler, kıyaslama tabloları ve somut veri referansları kullanılmalıdır.
- yazar/uzman profili, yayınlanma tarihi ve kaynak referansları açıkça belirtilmelidir.

### 4. zengin yapılandırılmış veri (schema.org json-ld)
- sayfada paylaşılan teknik ve kurumsal bilgiler arama motorlarına json-ld ile anlamsal olarak bildirilmelidir:
  ```html
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "antigravity kit",
    "applicationCategory": "DeveloperApplication",
    "operatingSystem": "All",
    "description": "kurumsal seviyede yüksek standartlı türkçe yapay zeka ajan kiti"
  }
  </script>
  ```
