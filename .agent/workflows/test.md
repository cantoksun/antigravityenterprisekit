---
description: projedeki birim, entegrasyon ve uçtan uca (e2e) testleri kurumsal standartlarda çalıştırın ve doğrulayın.
priority: p1-workflow
version: 2.0.0
---

# kurumsal test çalıştırma ve doğrulama iş akışı (/test)

bu iş akışı; `test-engineer` ve `qa-automation-engineer` liderliğinde sistemin tüm test katmanlarını çalıştırarak gerileme (regression) hatalarını, güvenlik açıklarını ve bellek sızıntılarını doğrulamayı yönetir.

---

## 🚨 temel kurallar uyumu (en yüksek öncelik)

1. **türkçe ve küçük harf standardı:** tüm test raporları ve çıktılar küçük harfle ve türkçe karakterlerle (`ç, ğ, ı, ö, ş, ü`) yazılır (1. kural).
2. **sorgusuz modüler icra:** testler kullanıcıya soru sormadan piramit sırasıyla (birim -> entegrasyon -> e2e) doğrudan icra edilir (2. kural).
3. **adım adım aşamalı yürütme:** önce birim testler geçmeli, ardından entegrasyon ve en son e2e testleri çalıştırılmalıdır (3. kural).
4. **güvenlik ve yetki testleri:** idor koruması (8. kural), rls ihlali (12. kural) ve owasp oturum güvenliği (14. kural) test senaryoları doğrulanır.
5. **bellek ve kaynak temizliği:** testler sonlandığında açık soket veya bağlantı havuzu kalmadığı doğrulanır (10. kural).
6. **sıfır varsayım (18. kural):** test edilecek bileşenlerin ve apilerin varlığı kod tabanında doğrulanır.

---

## 🧪 3 aşamalı test boru hattı

### 1. aşama: birim testleri (unit tests)
- saf fonksiyonlar, veri dönüştürücüler ve iş mantığı doğrulanır:
  ```bash
  npm run test:unit  # veya pytest tests/unit
  ```
- tüm testler aaa (arrange-act-assert) şablonuna uymalıdır.

### 2. aşama: api ve entegrasyon testleri (integration tests)
- veritabanı sorguları, uç nokta şema doğrulamaları (6. kural) ve idor yetki kontrolleri (8. kural) test edilir:
  ```bash
  npm run test:integration
  ```
- test sonrası veritabanı durumu temizlenir.

### 3. aşama: uçtan uca tarayıcı testleri (e2e tests)
- playwright ile kritik kullanıcı yolculukları ve responsive arayüzler test edilir:
  ```bash
  npm run test:e2e
  ```
- mobil çekmece (drawer) ve masaüstü modal (15. kural) davranışları doğrulanır.

---

## 📊 test sonuç raporu formatı

testler tamamlandığında kullanıcıya şu formatta kurumsal özet sunulur:

```markdown
📊 **test çalıştırma ve doğrulama raporu:**
- **birim testleri:** [geçen / toplam] ✅
- **entegrasyon testleri (güvenlik & idor):** [geçen / toplam] ✅
- **e2e testleri (kullanıcı akışları):** [geçen / toplam] ✅
- **bellek ve sızıntı kontrolü:** [açık bağlantı yok, temiz] ✅
```
