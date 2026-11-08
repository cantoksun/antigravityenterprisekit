---
name: tdd-workflow
description: test güdümlü geliştirme (tdd) iş akışı ilkeleri. kırmızı-yeşil-refactor döngüsü ve tasarım odaklı testler.
priority: p1-quality
version: 2.0.0
---

# test güdümlü geliştirme (tdd) iş akışı standartları

bu beceri; kod yazmadan önce test yazarak tasarımın netleşmesini, gereksiz kodun (yagni) engellenmesini ve sistemin sıfır gerileme (zero-regression) ile gelişmesini sağlayan tdd döngüsünü yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 14 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir tdd aşaması tamamlanır.
   - sadelik ve modern trend teknolojiler: en sade kodla testi geçirmek esastır (4. kural).
   - katı api güvenliği, hassas veri koruması ve idor/bola testleri.
   - bellek sızıntısı ve kaynak temizliği denetimi.
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki tdd metodolojisi.

---

## 🔴🟢🔵 kırmızı - yeşil - refactor döngüsü

```plaintext
  ┌──────────────┐
  │  1. KIRMIZI  │ ──► başarısız olan en küçük testi yaz (özellik henüz yok)
  └──────────────┘
         │
         ▼
  ┌──────────────┐
  │  2. YEŞİL    │ ──► testi geçirecek en yalın ve doğrudan kodu yaz (yagni)
  └──────────────┘
         │
         ▼
  ┌──────────────┐
  │  3. REFACTOR │ ──► tasarımı temizle, tekrarları kaldır, testler yeşil kalsın
  └──────────────┘
         │
         └────────── döngüyü bir sonraki küçük davranış için tekrarla
```

### 1. aşama: kırmızı (red)
- yazılacak özelliğin yalnızca tek bir davranışını hedefleyen, derleme hatası veya assert hatası veren minimal bir test yazın.
- testin gerçekten beklenen gerekçeyle başarısız olduğunu doğrulayın (yanlışlıkla geçen sahte yeşil test yazmayın).

### 2. aşama: yeşil (green)
- 4. kural (en sade yöntem) uyarınca, testi yeşile çevirecek en doğrudan ve en az kod satırını yazın.
- bu aşamada geleceğe yönelik soyutlamalar yapmayın; temel amaç yalnızca mevcut testi başarıyla tamamlamaktır.

### 3. aşama: refactor (mavi)
- testler yeşil olduktan sonra kodu gözden geçirin:
  - tekrarlayan mantıkları (dry) temizleyin.
  - değişken ve fonksiyon adlarını kendini belgeleyen hale getirin.
  - 9. ve 10. kurallar gereğince bellek kullanımını kontrol edin, açık kaynak kalmadığından emin olun.
  - refactor sonrası tüm testlerin hala yeşil olduğunu doğrulayın.

---

## 🎯 tdd kurumsal ilkeleri

1. **bebek adımları (baby steps):** devasa bir özelliği tek bir dev testle yazmayın; küçük, yönetilebilir ve bağımsız adımlarla ilerleyin (3. kural ile tam uyum).
2. **tasarım aracı olarak test:** test yazmak zorsa, sınıfın veya fonksiyonun çok fazla sorumluluğu (srp ihlali) var demektir; test kodun mimarisini sadeleştirmeye zorlar.
3. **güvenlik testleriyle başlama:** yetki gerektiren bir fonksiyonda ilk yazılacak testlerden biri "yetkisiz kullanıcının erişiminin engellenmesi" (8. ve 14. kural) olmalıdır.
