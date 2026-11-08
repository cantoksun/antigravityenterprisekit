---
name: clean-code
description: yalın, anlaşılır ve kurumsal standartlarda kodlama ilkeleri. aşırı mühendislik ve gereksiz yorum satırlarını engeller.
priority: p0-core
---

# kurumsal yalın ve sade kod standartları (clean code)

bu beceri, tüm uzman ajanlar ve kodlama süreçleri için temel kurumsal kod, icra, veri bütünlüğü, hata direnci, bulut uyumluluğu, güvenlik, regülasyon ve canlıya alma standartlarını tanımlar. 

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 42 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır (1. kural).
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz (2. kural).
   - adım adım aşamalı yürütülür; her seferinde tek bir modül tamamlanır (3. kural).
   - sadelik ve modern trend teknolojiler (4. kural).
   - yalın veritabanı modellemesi (5. kural).
   - katı api güvenliği (6. kural), hassas veri koruması (7. kural) ve idor/bola önleme (8. kural).
   - bellek yönetimi (9. kural), sızıntı analizi (10. kural), sayfalama (11. kural), rls 42501 (12. kural).
   - paginasyon/lazy loading (13. kural), owasp oturum denetimi (14. kural), responsive ux ayrımı (15. kural), font disiplini (16. kural).
   - kullanıcıyı yormama ve doğrudan icra (17. kural).
   - **18. kural (kesin varlık doğrulaması ve sıfır varsayım - zero assumptions):** çağrılan fonksiyonun, değişkenin, tablonun veya prop'un varlığı kod tabanında doğrulanmadan koda eklenemez.
   - **19. kural (kapsam şeffaflığı ve proaktif tamamlama):** iş bölündüğünde tamamlanan ve kalan aşamalar kullanıcıya açıkça raporlanır.
   - **20. kural (idempotency):** mükerrer api işlemlerini önlemek için `idempotency-key` ve arka yüz kilidi uygulanır.
   - **21. kural (soft delete):** kritik iş verilerinde `hard delete` yerine `deleted_at` mantıksal silme uygulanır.
   - **22. kural (değişmez denetim günlüğü - audit logging):** kim/ne zaman/ne yaptı iz kaydı (`audit_logs`) tutulur.
   - **23. kural (klavye navigasyonu ve anlamsal sadelik):** tüm arayüz klavyeyle yönetilebilir olmalı; ancak placeholder veya etiketi olan alanlara gereksiz `aria-label` yığılmamalıdır.
   - **24. kural (n+1 sorgu yasağı ve batch loading):** döngü içi sorgular yasaktır; eager loading (`include`), join veya dataloader zorunludur.
   - **25. kural (atomik işlemler ve db transaction):** çoklu tablo güncellemeleri `db.transaction()` bloğunda yürütülür.
   - **26. kural (tip korumalı fail-fast env):** ortam değişkenleri açılışta şemayla (`zod`) doğrulanır, güvensiz cast yasaktır.
   - **27. kural (zarif kapanış - graceful shutdown):** `sigterm/sigint` anında açık istekler tamamlanır, db havuzları ve soketler temizce kapatılır.
   - **28. kural (dış servis zaman aşımı - timeout & circuit breaker):** harici isteklere mutlak timeout (5000ms) tanımlanır.
   - **29. kural (csp ve güvenlik başlıkları):** helmet ile hsts, nosniff, x-frame-options ve katı csp başlıkları eklenir.
   - **30. kural (sıkı cors beyaz listesi):** `*` genel erişimi yasaktır; izinli domainler dinamik beyaz listeden doğrulanır.
   - **31. kural (sağlık denetimleri - liveness & readiness):** bulut orkestrasyonu için `/health/live` ve `/health/ready` uç noktaları zorunludur.
   - **32. kural (dayanıklı yeniden deneme - exponential backoff & jitter):** geçici ağ hatalarında rastgele gecikmeli kademeli yeniden deneme yapılır.
   - **33. kural (çakışma ve yarış durumu engeli - optimistic concurrency):** kritik tablolarda `version: int` alanı ile iyimser kilitleme uygulanır.
   - **34. kural (yapısal json loglama & correlation-id):** konsol metin kirliliği yerine json formatında ve `x-correlation-id` ile izlenebilir log üretilir.
   - **35. kural (webhook hmac imza doğrulaması):** stripe, github webhook gövdeleri sha-256 hmac ile doğrulanır.
   - **36. kural (kuyruklarda ölü mektup yönetimi - dlq):** asenkron kuyruklarda 3 kez başarısız olan görevler ölü mektup kuyruğuna aktarılır.
   - **37. kural (akıllı önbellekleme & etag):** get uç noktalarında `etag` ve `stale-while-revalidate` ile `304 not modified` işletilir.
   - **38. kural (kvkk/gdpr pii anonimleştirme):** hesap silmede yasal uyum için kişisel veriler geri döndürülemez biçimde anonimleştirilir.
   - **39. kural (expand & contract db göçü):** şema değişikliklerinde geriye dönük uyumlu üç aşamalı geçiş uygulanır.
   - **40. kural (özellik bayrakları & kill switch):** yeni özellikler varsayılan kapalı feature flag ile yayına alınır.
   - **41. kural (token bucket hız sınırlama):** user_id ve ip bazlı token bucket / sliding window algoritması uygulanır.
   - **42. kural (otonom dağıtım konfigürasyonu - automated deploy config):** projede eksik olan dockerfile/compose/vercel/render dosyaları proaktif olarak hazırlanır veya önerilir.
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümanda yer alan teknik standartlar.

---

## 🔍 18. kural: kesin varlık doğrulama ilkeleri (zero assumptions)

- bir dosyaya yeni bir import veya fonksiyon çağrısı eklemeden önce hedef dosya `read_file` veya `grep` ile kontrol edilmelidir.
- veritabanı sorgusu yazarken tablodaki sütun isimleri varsayılmaz; şema dosyası (`schema.prisma`, sql vb.) incelenerek teyit edilir.
- varlığı doğrulanmamış hayali metot veya prop koda yazılamaz.

---

## 🛡️ 20. kural: idempotency ve mükerrer işlem koruması

- finansal işlemler, ödeme, bakiye transferi veya tekil kaynak oluşturma (post) uç noktalarında `idempotency-key` başlığı (header) denetlenmelidir.
- sunucu, gelen anahtarı redis veya veritabanı kilidiyle (örneğin 120 saniyelik benzersiz anahtar) kontrol eder; mükerrer gelen aynı isteğe aynı önbellek yanıtını döner, işlemi tekrar icra etmez.

---

## 🛑 21. kural: soft delete (mantıksal silme) disiplini

- kullanıcılar, organizasyonlar, projeler, sözleşmeler ve finansal kayıtlarda `DELETE FROM` sorgusu yasaktır.
- tablolara `deleted_at TIMESTAMP WITH TIME ZONE NULL` kolonu eklenir.
- silme işlemi `UPDATE table SET deleted_at = NOW() WHERE id = :id` olarak icra edilir.
- liste ve tekil okuma sorgularında `WHERE deleted_at IS NULL` filtresi zorunludur.

---

## 🔏 22. kural: değişmez denetim günlüğü (audit logging)

- kritik nesneler değiştiğinde veya silindiğinde silinemez bir `audit_logs` tablosuna kayıt atılır:
  - `entity_type`: etkilenen tablo (ör. `invoice`, `user_role`).
  - `entity_id`: ilgili kaydın kimliği.
  - `action`: `insert`, `update`, `soft_delete`.
  - `actor_id`: işlemi yapan `user_id`.
  - `ip_address` & `user_agent`.
  - `diff_payload`: json olarak eski ve yeni değer farkı.

---

## ♿ 23. kural: klavye navigasyonu ve aria sadeliği

- tüm açılır pencereler `esc` tuşuyla kapanmalı, `tab` ile sadece pencere içi elemanlar dolaşılmalı (focus trap).
- placeholder veya görünür etiketi olan `<input>` elemanlarına gereksiz `aria-label` yazılmaz; sadece metinsiz ikon butonlarda kullanılır.

---

## ⚡ 24. kural: n+1 sorgu engeli ve eager loading

- döngü içinde veritabanı sorgusu atılamaz (`for item of list { await db.find() }` yasağı).
- ilişkiler orm'in eager loading yeteneğiyle (`prisma.findMany({ include: { author: true } })`) veya sql `JOIN` ile tek seferde çekilir.

---

## 🗄️ 25. kural: atomik db transaction güvencesi

- para çekip bakiye aktarma, sipariş oluşturup stok düşme gibi çoklu adımlı tüm işlemler atomik blokta yazılır:
```typescript
await db.$transaction(async (tx) => {
  await tx.account.decrement({ where: { id: fromId }, data: { balance: amount } });
  await tx.account.increment({ where: { id: toId }, data: { balance: amount } });
});
```

---

## 🛡️ 26. kural: tip korumalı fail-fast ortam değişkenleri

- kodun ortasında `process.env.DB_URL as string` yazılmaz.
- uygulama giriş noktasında `env.ts` modülü oluşturulur ve zod ile doğrulanır:
```typescript
import { z } from 'zod';
export const env = z.object({
  DATABASE_URL: z.string().url(),
  PORT: z.coerce.number().default(3000),
  NODE_ENV: z.enum(['development', 'production', 'test']),
}).parse(process.env);
```

---

## 🔄 27. kural: zarif sunucu kapanışı (graceful shutdown)

- sunucu kapanış sinyali aldığında yeni istekleri durdurur, aktif istekleri bitirir ve havuzu kapatır:
```typescript
process.on('SIGTERM', async () => {
  server.close(async () => {
    await db.$disconnect();
    process.exit(0);
  });
});
```

---

## ⏳ 28. kural: dış servis zaman aşımı (timeout)

- harici apilere istek atarken zaman aşımı zorunludur:
```typescript
const response = await fetch(externalApiUrl, {
  signal: AbortSignal.timeout(5000), // 5 saniye tavan limit
});
```

---

## 🛡️ 29. kural: güvenlik başlıkları (csp & security headers)

- sunucu yanıtlarında helmet veya benzeri middleware ile katı güvenlik başlıkları zorunludur:
```typescript
import helmet from 'helmet';
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'wasm-unsafe-eval'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", 'data:', 'https:'],
    }
  },
  hsts: { maxAge: 31536000, includeSubDomains: true }
}));
```

---

## 🚦 30. kural: katı cors beyaz listesi

- joker `origin: '*'` yasaktır. izinli alanlar liste üzerinden eşleştirilir:
```typescript
const allowedOrigins = [process.env.APP_URL, 'https://app.alanadi.com'];
const corsOptions = {
  origin: (origin, callback) => {
    if (!origin || allowedOrigins.includes(origin)) callback(null, true);
    else callback(new Error('cors erişim engeli'));
  },
  credentials: true,
};
```

---

## 💓 31. kural: sağlık denetimleri (health checks)

- bulut platformları ve konteynerler için iki standart rota tanımlanmalıdır:
```typescript
app.get('/health/live', (req, res) => res.status(200).json({ status: 'live' }));
app.get('/health/ready', async (req, res) => {
  const dbOk = await checkDbConnection();
  if (dbOk) return res.status(200).json({ status: 'ready', db: 'ok' });
  return res.status(503).json({ status: 'unready', db: 'fail' });
});
```

---

## 🔂 32. kural: üssel geri çekilme ile yeniden deneme (exponential backoff & jitter)

- geçici dış servis kesintilerinde rastgele jitter ile yeniden deneme kalıbı uygulanır:
```typescript
async function fetchWithRetry<T>(fn: () => Promise<T>, retries = 3, delay = 500): Promise<T> {
  try {
    return await fn();
  } catch (err) {
    if (retries <= 0) throw err;
    const jitter = Math.random() * 200;
    await new Promise((r) => setTimeout(r, delay + jitter));
    return fetchWithRetry(fn, retries - 1, delay * 2);
  }
}
```

---

## 🧱 33. kural: yarış durumu ve iyimser kilitleme (optimistic concurrency)

- eşzamanlı çakışmaları engellemek için modelde sürüm (version) kontrol edilir:
```typescript
const updated = await db.project.updateMany({
  where: { id: projectId, version: currentVersion },
  data: { ...newData, version: { increment: 1 } }
});
if (updated.count === 0) throw new ConflictException('kayıt başka bir kullanıcı tarafından güncellenmiş');
```

---

## 🧹 34. kural: yapısal json loglama & correlation-id

- her api isteğine middleware seviyesinde benzersiz id atanır ve loglar json formatında basılır:
```typescript
const requestId = req.headers['x-correlation-id'] || crypto.randomUUID();
logger.info({
  timestamp: new Date().toISOString(),
  requestId,
  method: req.method,
  path: req.path,
  userId: req.user?.id,
  message: 'istek işlendi'
});
```

---

## 🔏 35. kural: webhook hmac imza doğrulaması

- stripe veya üçüncü parti sistemlerden gelen webhook gövdeleri sha-256 hmac ile doğrulanır:
```typescript
import crypto from 'crypto';
function verifyWebhookSignature(payload: string, signature: string, secret: string): boolean {
  const expected = crypto.createHmac('sha256', secret).update(payload).digest('hex');
  return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected));
}
```

---

## 📨 36. kural: arka plan kuyruklarında ölü mektup (dlq) yönetimi

- asenkron worker işlerinde zehirli mesajları izole etmek için dlq tanımlanır:
```typescript
const worker = new Worker('emailQueue', async job => {
  await sendEmail(job.data);
}, {
  attempts: 3,
  backoff: { type: 'exponential', delay: 1000 },
});
worker.on('failed', async (job, err) => {
  if (job && job.attemptsMade >= 3) {
    await deadLetterQueue.add('failedJob', { jobData: job.data, error: err.message });
  }
});
```

---

## 🌐 37. kural: akıllı http önbellekleme ve etag

- veri değişmediğinde veritabanı sorgusunu ve gereksiz aktarımı önlemek için etag kullanılır:
```typescript
import etag from 'etag';
app.get('/api/v1/projects', async (req, res) => {
  const data = await getProjectsCached();
  const hash = etag(JSON.stringify(data));
  if (req.headers['if-none-match'] === hash) return res.status(304).end();
  res.setHeader('ETag', hash);
  res.setHeader('Cache-Control', 'public, s-maxage=60, stale-while-revalidate=300');
  return res.json(data);
});
```

---

## 🗄️ 38. kural: kvkk/gdpr uyumlu pii anonimleştirme

- soft delete yapılırken kişisel veriler geri döndürülemez şekilde temizlenir:
```typescript
await db.user.update({
  where: { id: userId },
  data: {
    deleted_at: new Date(),
    email: `deleted_${userId}_${Date.now()}@anonymized.local`,
    name: 'Anonim Kullanıcı',
    phone: null,
    ip_address: null,
  }
});
```

---

## 🔄 39. kural: sıfır kesintili veritabanı göçü (expand & contract)

- canlı sistemlerde sütun adı değiştirme veya silme işlemleri doğrudan yapılamaz; 3 aşamalı döngü işletilir:
```plaintext
1. expand: yeni sütunu nullable ekle, backend kodunda hem eskiye hem yeniye yaz (dual-write).
2. migrate: arka plan betiği ile eski verileri yeni sütuna doldur (backfill).
3. contract: backend kodunu tamamen yeni sütundan okuyacak şekilde güncelle, sonraki sürümde eski sütunu kaldır.
```

---

## 🚩 40. kural: özellik bayrakları ve acil durum kesicisi (feature flags & kill switch)

- yeni özellikler kodda bayrak arkasına alınır ve dağıtım ile yayın birbirinden ayrılır:
```typescript
if (await featureFlags.isEnabled('ai_search_v2', { userId: user.id })) {
  return executeAiSearchV2();
}
return executeLegacySearch();
```

---

## 🚦 41. kural: kurumsal hız sınırlama (token bucket & identity-aware)

- hız sınırları ani patlamaları dengeleyen redis tabanlı token bucket ve kullanıcı kimliğiyle yönetilir:
```typescript
const key = user ? `rate:${user.id}` : `rate:${req.ip}:${hash(req.headers['user-agent'])}`;
const limit = user ? 600 : 60; // oturum açmış kullanıcıya 10 kat kota
const allowed = await tokenBucket.consume(key, limit, 60);
if (!allowed) throw new TooManyRequestsException('kota aşıldı, lütfen bekleyin');
```

---

## 🚀 42. kural: otonom dağıtım konfigürasyonu (automated deploy config)

- kullanıcıya sıfır efor (zero friction) sağlamak için; projede uygun dağıtım dosyaları eksikse otomatik üretilir veya önerilir:
  - docker tabanlı mimariler için çok aşamalı (multi-stage) hafif `Dockerfile` ve `docker-compose.yml`.
  - serverless / edge için `vercel.json` veya `render.yaml`.
  - ortam değişkenleri için eksiksiz `.env.example` şablonu.
