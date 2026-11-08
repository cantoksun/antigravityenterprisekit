---
name: architecture
description: kurumsal mimari karar verme çerçevesi. gereksinim analizi, ödünleşim (trade-off) değerlendirmesi ve adr dokümantasyonu.
priority: p1-structural
version: 2.0.0
---

# kurumsal mimari karar çerçevesi (architecture)

bu beceri, sistem mimarisinin tasarlanması, teknoloji seçimleri, bileşen sınırlarının belirlenmesi ve mimari kararların kayıt altına alınmasını yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 3 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz, mantıklı adımlarla doğrudan icra edilir.
   - adım adım aşamalı yürütülür; her seferinde tek bir mimari modül tamamlanır.
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki mimari tasarım ilkeleri.

---

## 🏛️ kurumsal mimari tasarım ilkeleri

### 1. fonksiyonel ve fonksiyonel olmayan gereksinimler (nfr)
her mimari çözüm şu temel kalite özniteliklerini sağlamalıdır:
- **ölçeklenebilirlik:** sistemin artan yük altında yatay veya dikey genişleyebilmesi.
- **güvenilirlik ve dayanıklılık:** tekil hata noktalarından (single point of failure) arındırılmış tasarım, hata toleransı.
- **güvenlik:** en az ayrıcalık ilkesi (principle of least privilege), veri şifreleme ve ağ izolasyonu.
- **sürdürülebilirlik:** gevşek bağlı (loosely coupled), yüksek uyumlu (high cohesion) modüler yapılar.

### 2. ödünleşim (trade-off) analizi
hiçbir mimari çözüm kusursuz ve bedava değildir. her kararda şu dengeler gözetilir:
- **hız / basitlik vs. esneklik:** erken optimizasyon ve aşırı soyutlama engellenir; sadelik esastır.
- **monolit vs. mikroservis:** zorunlu olmadıkça dağıtık sistem karmaşıklığı yerine modüler monolit tercih edilir.
- **tutarlılık vs. erişilebilirlik (cap teoremi):** veri kritikliği düzeyine göre uygun depolama çözümü seçilir.

---

## 📝 mimari karar kayıtları (adr - architecture decision records)

kritik bir mimari tercih yapıldığında şu standart yapı kullanılır:

```markdown
# adr-[numara]: [alınan kararın kısa başlığı]

## durum
[önerildi / kabul edildi / reddedildi / güncellendi]

## bağlam
[kararın alınmasını gerektiren teknik veya iş ihtiyacı]

## karar
[seçilen mimari yaklaşım, teknoloji veya yöntem]

## değerlendirilen alternatifler
1. [seçenek a]: [artıları ve eksileri]
2. [seçenek b]: [artıları ve eksileri]

## sonuçlar
- **olumlu:** [sağlanan faydalar]
- **olumsuz / ödünleşimler:** [katlanılan karmaşıklık veya maliyet]
```

---

## 🧩 bileşen sınırları ve bağımlılık kuralları

1. **tek yönlü veri ve bağımlılık akışı:** üst katmanlar alt katmanları çağırabilir; alt katmanlar üst katmanlara doğrudan bağımlı olamaz (tersine bağımlılık - dependency inversion).
2. **alan sınırları (bounded context):** her modül kendi veri modeline ve kurallarına sahip olmalı, diğer modüllerin iç yapılarına doğrudan müdahale etmemelidir.
3. **adım kuralı:** mimari dönüşümler tek seferde devasa bir revizyon olarak değil, mantıksal alt adımlarla aşamalı olarak hayata geçirilir.
