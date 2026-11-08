---
name: nodejs-best-practices
description: kurumsal node.js geliştirme ilkeleri. çerçeve seçimi, asenkron desenler, bellek yönetimi ve güvenlik.
priority: p1-structural
version: 2.0.0
---

# kurumsal node.js geliştirme ve mimari standartları

bu beceri; yüksek performanslı, asenkron, bellek dostu ve güvenli node.js / typescript arka yüz sistemleri inşa etmeyi yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 14 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir modül tamamlanır.
   - sadelik ve modern trend teknolojiler: typescript, modern runtime'lar (node.js lts, bun, hono, fastify).
   - katı api güvenliği (6. kural), hassas veri koruması (7. kural) ve idor/bola önleme (8. kural).
   - bellek sızıntısı analizi (10. kural), rls 42501 yönetimi (12. kural) ve owasp oturum güvenliği (14. kural).
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki node.js teknik standartları.

---

## 🚀 kurumsal node.js ilkeleri

### 1. olay döngüsü (event loop) koruması ve cpu yönetimi
- ana iş parçacığını (main thread) asla senkron g/ç veya ağır cpu döngüleriyle bloke etmeyin:
  - `fs.readFileSync`, `crypto.pbkdf2Sync` gibi senkron çağrılar üretim ortamında kesinlikle yasaktır; her zaman asenkron versiyonları (`fs.promises`, `crypto.subtle`) kullanılmalıdır.
  - ağır şifreleme veya veri ayrıştırma için `worker_threads` tercih edilmelidir.

### 2. asenkron akışlar ve bellek sızıntılarını önleme (9. ve 10. kural)
- büyük dosyalar okunurken veya stream edilirken belleğe yığılma (`backpressure`) oluşmaması için `stream.pipeline` kullanılmalıdır:
  ```typescript
  import { pipeline } from 'node:stream/promises';
  import { createReadStream, createWriteStream } from 'node:fs';

  // güvenli akış: bellek şişmesini ve sızıntıyı önler
  await pipeline(
    createReadStream('large-input.csv'),
    transformStream,
    createWriteStream('output.csv')
  );
  ```
- **zamanlayıcı ve kaynak temizliği:** global kapsamda unutulan `setInterval` ve kapatılmayan veritabanı havuzları her zaman düzgün kapanma (graceful shutdown) mekanizmasıyla temizlenmelidir.

### 3. güvenli oturum ve çerez yönetimi (14. kural uyumu)
- istemciye token iletirken localstorage yerine güvenli çerez başlıkları kullanılır:
  ```typescript
  res.cookie('token', jwtToken, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 7 * 24 * 60 * 60 * 1000
  });
  ```

### 4. hatasız asenkron yönetim (unhandled rejection yasağı)
- tüm promise zincirlerinde hatalar yakalanmalı (`try/catch`), merkezi bir hata ara yazılımı (error middleware) üzerinden standart hata yanıtı dönülmelidir:
  ```typescript
  process.on('unhandledRejection', (reason) => {
    logger.error('yakalanmamış promise reddi:', reason);
    process.exit(1); // çökmeye izin ver ve süreç yöneticisinin (pm2/k8s) yeniden başlatmasını sağla
  });
  ```

### 5. zarif kapanma (graceful shutdown)
- sistem `SIGTERM` veya `SIGINT` sinyali aldığında yeni istekleri durdurmalı, mevcut istekleri tamamlamalı, veritabanı bağlantı havuzunu kapatmalı ve öyle çıkmalıdır:
  ```typescript
  async function gracefulShutdown(server, dbPool) {
    server.close(async () => {
      await dbPool.end();
      process.exit(0);
    });
  }
  ```
