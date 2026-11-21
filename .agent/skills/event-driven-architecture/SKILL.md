---
name: event-driven-architecture
description: transactional outbox pattern, kafka/redis streams, dlq ve idempotency consumer mimarisi.
priority: standard
version: 1.0.0
when_to_use: "transactional outbox pattern, kafka/redis streams, dlq ve idempotency consumer mimarisi."
allowed-tools: [Read, Grep, Glob, Bash, Write, Edit]
---

# kurumsal olay güdümlü mimari ve dağıtık mesajlaşma (event-driven architecture)

bu beceri; mikroservisler ve asenkron arka plan sistemlerinde veri tutarlılığı (eventual consistency), olay akışı (event streaming), transactional outbox kalıbı ve ölü mektup kuyruğu (dlq) yönetimini kurumsal standartlarda tanımlar.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (temel anayasa kuralları):**
   - tüm çıktılar ve açıklamalar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır (1. kural).
   - **20. kural (idempotency ve mükerrer işlem engeli):** her tüketici (consumer) gelen olayı `message_id` ile doğrulamalıdır.
   - **25. kural (atomik işlemler ve db transaction):** iş verisi ile outbox kaydı aynı veritabanı işleminde yazılmalıdır.
   - **36. kural (arka plan kuyruklarında ölü mektup yönetimi - dlq):** 3 kez başarısız olan mesajlar kuyruğu tıkamadan dlq'ya aktarılmalıdır.
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** `backend-specialist` ve `database-architect`.
4. **p3 (beceri kuralları):** bu dokümandaki dağıtık sistem kuralları.

---

## 📦 transactional outbox kalıbı (çift yazma hatasını önleme)

iki ayrı sisteme (veritabanı + mesaj kuyruğu) aynı anda yazmaya çalışmak (dual-write) ağ kesintilerinde veri tutarsızlığı yaratır.

### standart akış:
1. ana iş verisi (`orders`) güncellenirken, aynı veritabanı işlemi (`db.transaction()`) içinde bir `outbox_events` tablosuna olay kaydı atılır.
2. arka planda çalışan hafif bir aktarıcı (relay worker / cdc / debezium), `outbox_events` tablosundaki işlenmemiş kayıtları okuyup kafka/rabbitmq/redis streams'e yayımlar.
3. yayımlanan kayıtlar `published: true` veya `soft delete` ile işaretlenir.

```sql
create table if not exists outbox_events (
  id uuid primary key default gen_random_uuid(),
  aggregate_type text not null,
  aggregate_id text not null,
  event_type text not null,
  payload jsonb not null,
  created_at timestamp with time zone default now(),
  published_at timestamp with time zone null
);
create index idx_outbox_unpublished on outbox_events (created_at) where published_at is null;
```

---

## 🔁 tüketici idempotency ve dlq protokolü

```typescript
// kurumsal olay tüketicisi (idempotent event consumer)
export async function handleEvent(event: { id: string; type: string; payload: any }) {
  // 1. mükerrer işlem kontrolü (20. kural)
  const isProcessed = await redis.set(`processed_event:${event.id}`, '1', 'EX', 86400, 'NX');
  if (!isProcessed) {
    console.warn(`[UYARI] Mükerrer olay atlandı: ${event.id}`);
    return;
  }

  try {
    // 2. asıl iş mantığı
    await processBusinessLogic(event.payload);
  } catch (err) {
    // 3. başarısızlıkta dlq aktarımı (36. kural)
    await handleFailureWithRetryAndDlq(event, err);
    throw err;
  }
}
```
