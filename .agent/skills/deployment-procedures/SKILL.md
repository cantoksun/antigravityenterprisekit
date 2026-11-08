---
name: deployment-procedures
description: güvenli canlıya alma süreçleri, sıfır kesinti stratejileri ve geri alma (rollback) protokolleri.
priority: p1-operations
version: 2.0.0
---

# kurumsal canlıya alma ve dağıtım standartları

bu beceri; yazılım sistemlerinin üretim ortamına güvenli, sıfır kesintili (zero-downtime), ortam değişkenleri doğrulanmış ve anında geri alınabilir (rollback) biçimde taşınmasını yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 15 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir dağıtım aşaması tamamlanır.
   - sadelik ve modern trend teknolojiler: docker, kubernetes, github actions, vercel, railway, aws/gcp.
   - katı api ve sır güvenliği: üretim sırları asla git veya yapı loglarına sızdırılamaz (7. kural).
   - veritabanı migration güvenliği ve rls 42501 uyumu (12. kural).
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki dağıtım prosedürleri.

---

## 🚀 5 aşamalı kurumsal dağıtım süreci

```plaintext
  ┌───────────┐     ┌───────────┐     ┌───────────┐     ┌───────────┐     ┌───────────┐
  │ 1. STATİK │ ──► │ 2. YAPI & │ ──► │ 3. STAGING│ ──► │ 4. KANARYA│ ──► │ 5. İZLEME │
  │ & TEST    │     │ KONTEYNER │     │ DOĞRULAMA │     │ / BLUE-GRN│     │ & SAĞLIK  │
  └───────────┘     └───────────┘     └───────────┘     └───────────┘     └───────────┘
```

### 1. aşama: statik analiz, güvenlik ve test kontrolü
- tüm birim ve entegrasyon testleri (`vitest`, `pytest`) yeşil olmalıdır.
- tip denetimi (`tsc --noEmit`, `mypy`) ve linter sıfır hatayla geçmelidir.
- sır taraması (secret scan) yapılarak repoda unutulan `.env` veya api anahtarı olmadığı doğrulanmalıdır (7. kural).

### 2. aşama: yapı ve konteyner üretimi
- docker yapıları çok aşamalı (multi-stage build) olmalıdır; kaynak kod ve derleme bağımlılıkları nihai küçük imajda kalmamalıdır.
- `non-root` kullanıcı (`USER node` / `USER app`) zorunlu tutulmalıdır.

### 3. aşama: hazırlık (staging) ve veritabanı geçişi (migration)
- geriye dönük uyumlu migration: yeni sütunlar eklenirken eski kodun çökmemesi için `nullable` veya varsayılan değerli olmalıdır.
- rls ve yetki politikaları veritabanında test edilmelidir (12. kural).

### 4. aşama: sıfır kesintili canlıya alma (blue-green / canary)
- yeni sürüm ayağa kalkmadan ve sağlık kontrolünden (`health check` `/api/health` 200 dönmeden) eski sürüme giden trafik kesilmez.
- trafik aşamalı olarak (%10 -> %50 -> %100) yeni sürüme aktarılır.

### 5. aşama: canlı izleme ve anında geri alma (rollback)
- dağıtım sonrası 5xx hata oranları ve yanıt süreleri izlenir.
- hata oranı %1'i aşarsa sistem tek bir komut veya ci/cd butonuyla anında önceki kararlı sürüme (previous release) geri döner.

---

## 🩺 standart sağlık kontrolü (health check endpoint)

tüm servisler dağıtım yöneticisinin durum sorgulayabileceği hafif bir uç nokta sunmalıdır:

```typescript
// app/api/health/route.ts
export async function GET() {
  const isDbHealthy = await checkDbConnection();
  if (!isDbHealthy) {
    return Response.json({ status: 'unhealthy', database: 'down' }, { status: 503 });
  }
  return Response.json({ status: 'healthy', timestamp: new Date().toISOString() });
}
```
