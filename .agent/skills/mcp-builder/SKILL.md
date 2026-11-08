---
name: mcp-builder
description: mcp (model context protocol) sunucu geliştirme ilkeleri. araç tasarımı, kaynak kalıpları ve kurumsal entegrasyonlar.
priority: p2-specialized
version: 2.0.0
---

# model bağlam protokolü (mcp) sunucu ve araç geliştirme standartları

bu beceri; yapay zeka modellerinin veritabanlarına, kurumsal api'lere, dosya sistemlerine ve dış servislere güvenli biçimde erişmesini sağlayan mcp (model context protocol) sunucuları tasarlamayı yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 16 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir mcp modülü tamamlanır.
   - sadelik ve modern trend teknolojiler: `@modelcontextprotocol/sdk`, typescript, stdio ve sse taşıyıcıları.
   - katı güvenlik, girdi doğrulama (6. kural), hassas veri koruması (7. kural) ve yetkisiz işlem engelleme (8. kural).
   - bellek sızıntısı analizi (10. kural) ve sayfalama sınırları (11. kural).
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki mcp geliştirme ilkeleri.

---

## 🔌 kurumsal mcp mimarisi ve araç standartları

mcp sunucuları yapay zeka modelleri ile sistemler arasında köprü kurar. kurumsal düzeyde bir mcp sunucusu üç temel yapı taşından oluşur:

### 1. araçlar (tools): eylemler ve fonksiyonlar
modellerin çağırabileceği fonksiyonlardır. her aracın parametreleri katı zod şemalarıyla doğrulanmalıdır:
```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';

const server = new McpServer({
  name: "kurumsal-veritabani-mcp",
  version: "1.0.0"
});

// güvenli araç tanımı:
server.tool(
  "kullanici-siparislerini-getir",
  "belirli bir kullanıcının geçmiş siparişlerini getirir.",
  {
    userId: z.string().uuid("geçerli bir uuid girilmelidir"),
    limit: z.number().int().min(1).max(50).default(20), // 11. kural: sayfalama tavanı
    cursor: z.string().optional()
  },
  async ({ userId, limit, cursor }) => {
    // 8. kural: idor ve yetki kontrolü
    const orders = await fetchUserOrders({ userId, limit, cursor });
    
    return {
      content: [{ type: "text", text: JSON.stringify(orders, null, 2) }]
    };
  }
);
```

### 2. kaynaklar (resources): salt okunur veri kaynakları
modellerin bağlam olarak doğrudan okuyabileceği statik veya dinamik veri dökümleridir (örneğin veritabanı şemaları, sistem logları, dokümanlar):
- uri şeması açık ve standart olmalıdır: `postgres://analytics/schemas/users`.
- dönen içerik modellerin kolay ayrıştırabileceği yapılandırılmış json veya yalın metin formatında olmalıdır.

### 3. hata ve zafiyet yönetimi (6., 7. ve 10. kural uyumu)
- **en az ayrıcalık ilkesi:** mcp sunucusu yalnızca ihtiyaç duyduğu veritabanı tablolarına salt okunur (read-only) veya kısıtlı yazma izinleriyle bağlanmalıdır.
- **gizli bilgi sızıntısı engeli:** api anahtarları veya bağlantı şifreleri mcp araç çıktılarında modele açık metin olarak dönülmez (7. kural).
- **akış ve bellek temizliği:** büyük kaynaklar okunurken `stream` kullanılmalı ve stdio/sse bağlantıları kapandığında tüm havuzlar serbest bırakılmalıdır (9. ve 10. kural).
