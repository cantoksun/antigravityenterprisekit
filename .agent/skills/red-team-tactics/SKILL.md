---
name: red-team-tactics
description: mitre att&ck ve owasp api güvenlik çerçevelerine dayalı ofansif denetim, idor/bola tespiti ve yetki analizi uzmanı.
priority: p0-security
version: 2.0.0
---

# ofansif güvenlik ve idor / bola zafiyet tespit standartları

bu beceri, sistemlerde yetkisiz kullanıcıların başkalarına ait verilere veya işlevlere erişmesini (idor / bola / bfla) önceden tespit edip engellemeyi yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 8 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir modül tamamlanır.
   - **sadelik ve trend teknolojiler:** sade ve modern savunma mimarileri.
   - **yalın veritabanı:** tutarlı yetkilendirme modelleri.
   - **katı api güvenliği & hassas veri koruması:** sırlar açıkta bırakılmaz.
   - **8. kural (idor ve bola önleme):** nesne ve fonksiyon bazlı yetki açıkları kodlama anında tespit edilir ve engellenir.
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki tespit ve denetim kalıpları.

---

## 🎯 8. kural: idor ve bola tespiti ve savunma ilkeleri

### 1. idor (broken object level authorization) nedir ve nasıl önlenir?
idor, kullanıcının istekteki bir id parametresini (örneğin `/api/invoices/1052`) değiştirerek başka bir müşteriye ait faturayı görebilmesi veya değiştirebilmesidir.

- **hatalı kodlama (güvensiz):**
  ```typescript
  // zafiyetli: kullanıcı giriş yapmış ama bu fatura ona mı ait kontrol edilmiyor!
  export async function getInvoice(req, res) {
    const invoice = await db.invoice.findUnique({
      where: { id: req.params.id }
    });
    return res.json({ data: invoice });
  }
  ```

- **kurumsal ve güvenli kodlama (8. kural uyumu):**
  ```typescript
  // güvenli: sahiplik veritabanı sorgusu seviyesinde kısıtlanır
  export async function getInvoice(req, res) {
    const user = req.user; // kimliği doğrulanmış kullanıcı
    const invoice = await db.invoice.findFirst({
      where: { 
        id: req.params.id,
        tenant_id: user.tenant_id, // organizasyon/kiracı izolasyonu
        owner_id: user.id          // nesne sahipliği doğrulaması
      }
    });

    if (!invoice) {
      // 404 dönülerek kaynağın varlığı bile yetkisiz kişiye ifşa edilmez
      return res.status(404).json({ error: { code: "not_found", message: "kayıt bulunamadı" } });
    }

    return res.json({ data: invoice });
  }
  ```

### 2. bola / bfla (broken function level authorization) tespiti
- yönetimsel veya hassas fonksiyonların yalnızca url gizliliğine (`/api/admin/users/export`) güvenilerek bırakılması engellenir.
- her fonksiyon çağrısında kullanıcının rolü (`user.role === 'admin'`) ara yazılım (middleware) veya koruyucu (guard) seviyesinde zorunlu kılınmalıdır.

---

## 🔍 otomatik idor/bola denetim kontrol listesi

her geliştirme ve kod incelemesinde şu 4 soru kontrol edilir:
1. uç nokta bir id parametresi alıyor mu (`params.id`, `body.resourceId`)?
2. sorguda `userId` veya `tenantId` filtresi zorunlu tutulmuş mu?
3. ardışık tam sayılar (1, 2, 3) yerine tahmin edilemez uuid v4 veya cwid kullanılıyor mu?
4. yetkisiz erişim denendiğinde veri veya hata sızıntısı olmadan 403/404 dönülüyor mu?
