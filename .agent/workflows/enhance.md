---
description: mevcut bir özelliği, bileşeni veya kod modülünü kurumsal standartlara göre iyileştirin ve refactor edin.
priority: p1-workflow
version: 2.0.0
---

# kod iyileştirme ve refactor iş akışı (/enhance)

bu iş akışı; mevcut bir kod bloğunu veya modülü 18 temel kural çerçevesinde inceleyip, gereksiz karmaşıklıktan arındırarak performans, güvenlik ve mimari açıdan mükemmelleştirmeyi yönetir.

---

## 🚨 temel kurallar uyumu (en yüksek öncelik)

1. **türkçe ve küçük harf standardı:** tüm açıklamalar ve raporlar küçük harfle ve türkçe karakterlerle (`ç, ğ, ı, ö, ş, ü`) yazılır (1. kural).
2. **sorgusuz modüler icra:** iyileştirme planı doğrudan mantıklı modüllere ayrılarak soru sormadan uygulanır (2. kural).
3. **adım adım aşamalı yürütme:** tek seferde tüm kod tabanı değiştirilmez; her turda tek bir dosya veya modül iyileştirilir (3. kural).
4. **sadelik ve yagni:** aşırı soyutlamalar ve gereksiz yorum satırları kaldırılır (4. kural).
5. **bellek ve sızıntı analizi:** açık kalan dinleyiciler ve kontrolsüz yapılar temizlenir (9. ve 10. kural).
6. **paginasyon ve lazy loading:** eksik veri sınırları ve tembel yüklemeler eklenir (11. ve 13. kural).
7. **cihaz odaklı ux & font disiplini:** masaüstü modal / mobil drawer ayrımı (15. kural) ve 2-3 font sınırı (16. kural) korunur.
8. **kullanıcıyı yormama ve sıfır varsayım:** env/migration doğrudan icra edilir (17. kural) ve tüm değişkenlerin varlığı kod tabanında doğrulanır (18. kural).

---

## 🔧 4 aşamalı refactor protokolü

### 1. aşama: mevcut durum analizi ve varlık doğrulaması (18. kural)
- `code-archaeologist` ve `explorer-agent` mevcut dosyayı ve bağımlılıklarını okur.
- kodda çağrılan değişkenlerin, veritabanı sütunlarının ve prop'ların gerçekten var olduğu teyit edilir.

### 2. aşama: güvenlik ve owasp denetimi (6., 7., 8., 14. kural)
- idor zafiyeti var mı (`owner_id` kontrolü eksik mi)?
- client-side'da token veya hassas veri tutuluyor mu?
- sabit şifre veya açıkta kalan sır var mı?

### 3. aşama: performans ve bellek optimizasyonu (9., 10., 13. kural)
- bellek sızıntısı yapabilecek temizlenmemiş listener/timer var mı?
- liste renderlarında sayfalama veya lazy loading eksik mi?
- aşırı re-render veya gereksiz derin bağımlılıklar giderilir.

### 4. aşama: yalınlaştırma ve test doğrulaması (clean code)
- gereksiz `if-else` karmaşıklığı erken dönüşlerle (early return) sadeleştirilir.
- mevcut birim ve entegrasyon testleri çalıştırılarak hiçbir işlevin bozulmadığı teyit edilir.
