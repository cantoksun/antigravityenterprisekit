---
name: testing-patterns
description: kurumsal test kalıpları ve ilkeleri. birim, entegrasyon ve sahte (mock) nesne stratejileri.
priority: p1-quality
version: 2.0.0
---

# kurumsal test kalıpları ve stratejileri (testing patterns)

bu beceri; sistem güvenilirliğini, gerileme (regression) risklerini önlemeyi, birim, entegrasyon ve uçtan uca test standartlarını yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 14 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir modül tamamlanır.
   - sadelik ve modern trend teknolojiler (vitest, jest, playwright, supertest).
   - katı api güvenliği, yetki ve idor/bola testleri.
   - bellek sızıntısı ve kaynak temizliği denetimi.
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki test kalıpları.

---

## 🧪 kurumsal test piramidi ve oranları

```plaintext
        / \
       /e2e\        %10 - kritik kullanıcı akışları (playwright)
      /=====\
     / enteg \      %20 - api & veritabanı entegrasyonu (supertest)
    /=========\
   /   birim   \    %70 - saf fonksiyonlar ve iş mantığı (vitest)
  /_____________\
```

### 1. birim testleri (unit tests - %70)
- izole edilmiş saf iş mantığını ve hesaplamaları doğrular.
- hızlı çalışmalı (milisaniyeler seviyesinde) ve harici ağ/veritabanı çağrısı yapmamalıdır.
- deterministik olmalı, saat/zaman bağımlılıkları sahte zamanlayıcılar (`vi.useFakeTimers`) ile yönetilmelidir.

### 2. entegrasyon testleri (integration tests - %20)
- api uç noktalarının veritabanı, ara yazılımlar (middleware) ve yetkilendirme kurallarıyla birlikte çalışmasını test eder.
- testler gerçek bir test veritabanında (testcontainers veya hafif sqlite) yürütülmeli ve işlem sonrası temizlenmelidir.
- **güvenlik testleri:** 8. kural (idor) ve 12. kural (rls ihlali) senaryoları entegrasyon seviyesinde özellikle test edilir:
  ```typescript
  test('başka bir kullanıcının kaynağına erişilmeye çalışıldığında 404/403 dönmeli', async () => {
    const res = await request(app)
      .get('/api/orders/order-owned-by-user-b')
      .set('Authorization', `Bearer ${tokenOfUserA}`);
    expect(res.status).toBe(404);
  });
  ```

### 3. uçtan uca testler (e2e tests - %10)
- kritik iş akışlarını (üye olma, sipariş tamamlama, ödeme akışı) tarayıcı ortamında gerçek kullanıcı gibi test eder.
- kararsız (flaky) testlerden kaçınmak için kullanıcı odaklı seçiciler (`getByRole`, `getByLabel`) ve otomatik bekleme kullanılır.

---

## 📐 standart aaa (arrange - act - assert) şablonu

her test senaryosu istisnasız üç aşamalı olarak yapılandırılmalıdır:

```typescript
test('geçerli kupon kodu girildiğinde sepete %20 indirim uygulanmalıdır', () => {
  // 1. arrange (düzenle / hazırla): durum ve girdileri oluştur
  const cart = new ShoppingCart();
  cart.addItem({ id: 'p1', price: 100 });
  const coupon = new Coupon({ code: 'INDIRIM20', discountRate: 0.20 });

  // 2. act (çalıştır): test edilen davranışı tetikle
  cart.applyCoupon(coupon);

  // 3. assert (doğrula): kesin beklentiyi teyit et
  expect(cart.getTotalPrice()).toBe(80);
});
```

---

## 🚫 test anti-kalıpları (kaçınılması gerekenler)

1. **aşırı mocklama (over-mocking):** sistemin gerçek davranışını gizleyecek kadar her şeyi mocklamak; mocklar gerçeği yansıtmaz hale gelir.
2. **paylaşılan durum (shared mutable state):** testler arasında global değişken paylaşmak; bir testin başarısızlığı diğerlerini yanıltıcı biçimde bozar.
3. **uyku fonksiyonları (`sleep(3000)`):** zaman aşımını beklemek yerine olayın tamamlandığını izleyen bildirim veya bekleme (`waitFor`) yapıları kullanılmalıdır.
