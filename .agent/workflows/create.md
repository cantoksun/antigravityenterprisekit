---
description: doğal dil talebinden kurumsal standartlarda yeni bir uygulama veya modül inşa edin.
priority: p1-workflow
version: 2.0.0
---

# yeni uygulama ve modül inşa iş akışı (/create)

bu iş akışı; sıfırdan kurumsal düzeyde bir web, mobil veya api projesi başlatırken temel kuralları ve uzman ajan rollerini koordine eder.

---

## 🚨 temel kurallar uyumu (en yüksek öncelik)

1. **türkçe ve küçük harf standardı:** tüm çıktılar, açıklamalar ve yönlendirmeler küçük harfle ve türkçe karakterlerle (`ç, ğ, ı, ö, ş, ü`) yazılır (1. kural).
2. **sorgusuz modüler icra:** kullanıcıya gereksiz sorular sormadan en iyi kurumsal varsayılanlar seçilerek doğrudan modüler inşa başlatılır (2. kural).
3. **adım adım aşamalı yürütme:** tüm sistem tek seferde bitirilmeye çalışılmaz; her turda tek bir modül tamamlanır (3. kural).
4. **sadelik ve modern trend teknolojiler:** aşırı mühendislikten uzak, güncel çatı ve araçlar kullanılır (4. kural).
5. **yalın veritabanı:** bayraksız, sade şemalar tasarlanır (5. kural).
6. **güvenlik ve owasp denetimi:** api güvenliği (6. kural), sır koruması (7. kural), idor önleme (8. kural) ve güvenli çerezler (14. kural) baştan kurulur.
7. **cihaz ayrımı ve tipografi:** masaüstü modal / mobil drawer ayrımı (15. kural) ve maksimum 2-3 font sınırı (16. kural) uygulanır.

---

## 🏗️ 4 aşamalı inşa protokolü

### 1. aşama: proje tipi ve uzman ajan tespiti
- web projesi ise: `frontend-specialist` + `backend-specialist`
- mobil projesi ise: `mobile-developer` (kesinlikle frontend uzmanı atanmaz)
- api/arka yüz ise: `backend-specialist` + `database-architect` + `security-auditor`

### 2. aşama: altyapı ve veri temeli
- veritabanı şeması ve migration dosyaları oluşturulur (5. ve 12. kural).
- `.env.example` ve gizli bilgi yapılandırması tamamlanır (7. kural).

### 3. aşama: çekirdek iş mantığı ve api katmanı
- girdi doğrulama şemaları (zod/pydantic) yazılır (6. kural).
- servisler ve idor korumalı veri erişim fonksiyonları kodlanır (8. kural).
- sayfalama ve sınır limitleri tanımlanır (11. kural).

### 4. aşama: sunum katmanı ve doğrulama
- kullanıcı arayüzü ve duyarlı bileşenler (responsive drawer/dialog) eklenir (15. kural).
- birim ve entegrasyon testleri çalıştırılarak modül doğrulanır.
