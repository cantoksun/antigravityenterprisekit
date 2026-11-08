---
name: documentation-templates
description: kurumsal teknik dokümantasyon şablonları. readme, mimari karar kayıtları (adr), api dokümantasyonu ve kod yorum standartları.
priority: p2-specialized
version: 2.0.0
---

# kurumsal teknik dokümantasyon ve standartlar kılavuzu

bu beceri; projelerin kurulum rehberlerini, mimari karar kayıtlarını (adr), api arayüz dokümanlarını ve kurumsal bilgi birikiminin korunmasını yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 15 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir dokümantasyon modülü tamamlanır.
   - sadelik ve modern trend teknolojiler: markdown, mermaid diyagramları, openapi/swagger şablonları.
   - sırların ve hassas verilerin dokümanlarda ifşa edilmemesi (7. kural).
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki dokümantasyon şablonları.

---

## 📚 kurumsal teknik dokümantasyon şablonları

### 1. kurumsal readme.md şablonu
her projenin kök dizininde yer alan, yeni bir geliştiricinin 5 dakikada projeyi ayağa kaldırmasını sağlayan standart yapı:

```markdown
# [proje adı]

> [projenin tek cümlelik net ve kurumsal amacı]

## 🛠️ teknoloji yığını
- **ön yüz:** react / next.js, tailwind css
- **arka yüz:** node.js / typescript, fastapi
- **veritabanı:** postgresql, redis
- **test & ci:** vitest, playwright, github actions

## 🚀 hızlı başlangıç

### gereksinimler
- node.js >= 20.x veya python >= 3.12
- docker & docker compose

### kurulum adımları
1. depoyu klonlayın ve dizine girin:
   ```bash
   git clone [depo_url]
   cd [proje_dizini]
   ```
2. ortam değişkenlerini hazırlayın (7. kural uyumu):
   ```bash
   cp .env.example .env
   ```
3. bağımlılıkları yükleyin ve başlatın:
   ```bash
   npm install
   npm run dev
   ```

## 🧪 testleri çalıştırma
```bash
npm run test        # birim ve entegrasyon testleri
npm run test:e2e    # playwright uçtan uca testleri
```
```

### 2. api uç nokta dokümantasyon şablonu (6. kural uyumu)
herhangi bir api ucu dokümante edilirken şu şablon kullanılır:

```markdown
### `POST /api/v1/orders`

müşterinin sepetindeki ürünlerle yeni bir sipariş kaydı oluşturur.

- **yetkilendirme:** `Bearer <JWT>` (zorunlu - 6. kural)
- **istek gövdesi (request body):**
  ```json
  {
    "items": [
      { "productId": "prod_101", "quantity": 2 }
    ],
    "shippingAddressId": "addr_202"
  }
  ```
- **başarılı yanıt (201 created):**
  ```json
  {
    "data": {
      "orderId": "ord_901",
      "status": "pending",
      "totalAmount": 450.00
    }
  }
  ```
- **hata durumları:**
  - `400 Bad Request`: girdi şeması geçersiz (zod doğrulama hatası)
  - `401 Unauthorized`: oturum açılmamış
  - `404 Not Found`: ürün veya adres bulunamadı (8. kural idor koruması)
```
