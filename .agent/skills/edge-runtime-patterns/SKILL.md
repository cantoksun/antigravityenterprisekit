---
name: edge-runtime-patterns
description: cloudflare workers, hono, edge middleware, v8 isolates ve sifir cold-start mimarisi.
priority: standard
version: 1.0.0
when_to_use: "cloudflare workers, hono, edge middleware, v8 isolates ve sifir cold-start mimarisi."
allowed-tools: [Read, Grep, Glob, Bash, Write, Edit]
---

# kurumsal edge runtime ve hono mimari standartları

bu beceri; v8 isolates üzerinde çalışan modern uç bilişim (cloudflare workers, vercel edge, hono, bun) ortamlarında sıfır gecikmeli mikroservis, api ağ geçidi (api gateway) ve küresel önbellek mimarileri geliştirmeyi tanımlar.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (temel anayasa kuralları):**
   - tüm çıktılar ve açıklamalar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır (1. kural).
   - katı api güvenliği, token tavanı ve girdi doğrulaması (6. ve 7. kural).
   - kesin varlık doğrulaması ve sıfır varsayım (18. kural).
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** `backend-specialist` ve `cloud-architect`.
4. **p3 (beceri kuralları):** bu dokümandaki edge standartları.

---

## ⚡ edge runtime çekirdek mimari ilkeleri

1. **v8 isolates vs node.js runtime ayrımı:**
   - edge runtime ortamlarında tam bir node.js sanal makinesi çalışmaz; hafif v8 yalıtımları (isolates) kullanılır.
   - `fs`, `net`, `child_process` gibi yerel os modülleri doğrudan çağrılamaz; standart web standartları (`fetch`, `Request`, `Response`, `WebSockets`, `crypto.subtle`) kullanılmalıdır.
2. **sıfır cold-start (soğuk başlama) disiplini:**
   - edge fonksiyonlarında başlatma süresi (cold start) < 5ms seviyesindedir. ağır harici sdk ve orm yüklemelerinden kaçınılmalı, ultra hafif web çatısı olarak `hono` tercih edilmelidir.
3. **veritabanı erişimi (edge-to-db):**
   - edge ortamlarından doğrudan tcp ile postgresql/mysql bağlanmak bağlantı havuzunu tüketir. daima http/websocket tabanlı serverless sürücüler (`@neondatabase/serverless`, `@libsql/client`, supabase port 6543) kullanılmalıdır.

---

## 🛠️ hono + edge mikroservis standart şablonu

```typescript
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { secureHeaders } from 'hono/secure-headers';

type Bindings = {
  DB: D1Database;
  KV: KVNamespace;
  ENVIRONMENT: string;
};

const app = new Hono<{ Bindings: Bindings }>();

// 1. güvenlik ve başlık middleware'leri
app.use('*', secureHeaders());
app.use('*', cors({
  origin: (origin) => (origin.endsWith('.domain.com') ? origin : null),
  credentials: true,
}));

// 2. hafif uç nokta (edge route)
app.get('/api/health', (c) => {
  return c.json({
    status: 'healthy',
    runtime: 'v8-edge-isolate',
    timestamp: new Date().toISOString(),
  });
});

export default app;
```
