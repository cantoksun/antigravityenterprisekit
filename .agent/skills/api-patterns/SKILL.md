---
name: api-patterns
description: kurumsal api tasarım ilkeleri. rest, graphql ve trpc karşılaştırması, yanıt formatları, versiyonlama ve sayfalandırma.
priority: p1-structural
version: 2.0.0
when_to_use: "kurumsal api tasarım ilkeleri. rest, graphql ve trpc karşılaştırması, yanıt formatları, versiyonlama ve sayfalandırma."
allowed-tools: [Read, Grep, Glob, Bash, Write, Edit]
---

# kurumsal ve güvenli api tasarım standartları

bu beceri, kurumsal düzeyde ölçeklenebilir, tutarlı ve katı güvenlik standartlarına sahip api arayüzleri inşa etmeyi yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 46 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir modül tamamlanır.
   - **sadelik ve trend teknolojiler:** en sade yöntemlerle, modern teknolojilerle devam edilir.
   - **yalın veritabanı:** bayrak kirliliği engellenir, tekil rol ve durum yapıları kullanılır.
   - **6. kural (katı api güvenliği):** her api isteğinde ve uç noktada güvenlik mutlak surette doğrulanır.
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki api ve uç nokta standartları.

---

## 🛡️ 6. kural: katı api güvenliği kontrol listesi

her api isteğinde ve uç noktada şu güvenlik katmanları tavizsiz uygulanmalıdır:

### 1. katı girdi doğrulama (strict input validation)
- tüm gelen istek gövdeleri (body), parametreler (params) ve sorgu dizgileri (query) şema doğrulayıcılar (zod, valibot, pydantic) ile katı tiplere dönüştürülmelidir.
- beklenmeyen veya tanımsız alanlar anında reddedilmeli (`strip` / `strict`), nesne enjeksiyonları önlenmelidir.

### 2. kimlik doğrulama ve rbac (yetkilendirme)
- oturumsuz erişime açık olması amaçlanmayan tüm uç noktalar jwt / api anahtarı / oturum kontrolünden geçmelidir.
- sadece kimlik tespiti yetmez; kullanıcının ilgili kaynağa (`user.id === resource.owner_id` veya `role === 'admin'`) erişim yetkisi kod seviyesinde doğrulanmalıdır (idor / bfla zafiyetlerine karşı koruma).

### 3. hız sınırlaması ve ddos koruması (rate limiting)
- ip ve kullanıcı bazlı istek hız sınırları uygulanmalıdır (örneğin auth isteklerinde katı limit: dakikada max 5 deneme).
- kaba kuvvet (brute-force) saldırıları engellenmelidir.

### 4. hassas veri gizleme ve güvenli yanıt yapısı
- veritabanı nesneleri doğrudan istemciye döndürülmemeli; şifre karmaları (hash), dahili anahtarlar ve hassas loglar kesinlikle filtrelenmelidir.
- tutarlı ve güvenli yanıt formatı:
  ```json
  {
    "data": { ... },
    "meta": { "page": 1, "limit": 20 }
  }
  ```
- hata anında asla sistem çağrı yığını (stack trace) istemciye iletilmemeli, temiz hata nesneleri dönülmelidir:
  ```json
  {
    "error": {
      "code": "unauthorized",
      "message": "bu işlem için yetkiniz bulunmuyor"
    }
  }
  ```

---

## ⚡ protokol seçimi ve modern trendler

1. **rest:** kamusal, genel tüketim veya mikroservis entegrasyonlarında standart.
2. **trpc / server actions:** full-stack typescript projelerinde sıfır api kazası ve uçtan uca tip güvenliği için tercih edilir.
3. **graphql:** karmaşık ilişkisel veri modellerinde istemciye tam kontrol verilmek istendiğinde kullanılır.

---

## 🔍 şema ve kolon uyumu, mapper kayıpları ve sessiz hata engeli

### 1. şema ve kolon farklılıkları (schema drift & column mismatch)
- **18. kural (sıfır varsayım):** api uç noktalarında veritabanı kolonları asla varsayılmaz. daima veritabanı şemasından otomatik türetilen tipler (`prisma.validator`, drizzle `inferred type`, kysely) kullanılır; elle yazılan ve şemayla senkronize olmayan hayali tipler yasaktır.
- **39. kural (expand & contract):** canlı sistemlerde kolon adı değiştirme veya silme işlemleri doğrudan yapılamaz; geriye dönük uyumluluk için üç aşamalı genişlet ve daralt kalıbı uygulanır.
- **statik şema denetimi:** projelerde `schema_validator.py` çalıştırılarak eksik ilişkiler ve tip sapmaları önceden taranır.

### 2. mapper ve filtreleme kayıpları (data truncation & over-stripping)
- **aşırı filtreleme (over-stripping) engeli:** zod gibi şema doğrulayıcılarda güvenlik için `strip` kullanılırken, domain modelinden dto'ya dönüşüm yapılan mapper katmanında zorunlu alanların sessizce düşmesini engellemek için `satisfies DTO` veya tip zorlaması uygulanır.
- **saf dönüşüm fonksiyonları (pure mappers):** her mapper fonksiyonu açık ve öngörülebilir olmalıdır (`toDTO`, `fromPersistence`). sayfalama (`page`, `limit`), toplam kayıt (`totalCount`) ve filtre meta verileri dönüşüm esnasında asla kaybolamaz.
- **kontrat testleri:** mapper katmanı eksik veya null değer senaryolarına karşı `testing-patterns` altında birim testleriyle doğrulanır.

### 3. sessiz api hataları (silent failures & swallowed exceptions)
- **boş catch yasağı (no empty catch):** `try { ... } catch (e) {}` veya hatayı yalnızca `console.log(e)` yapıp `return null` / `{ success: false }` dönerek hatayı yutmak kesinlikle yasaktır.
- **fail-fast ve standart hata nesnesi:** hata anında sistem sessizce kilitlenmek yerine fail-fast prensibiyle açık hata fırlatmalıdır.
- **yapısal izleme (34. kural):** yakalanan her hata benzersiz bir `x-correlation-id` ile merkezi json loglara işlenmeli ve istemciye standart bir `error.code` ile bildirilmelidir.
- **devre kesici ve zaman aşımı (28. kural):** yanıt vermeyen dış apilerin sessizce sistemi tıkaması `5000ms timeout` ve devre kesici (circuit breaker) ile engellenir.
