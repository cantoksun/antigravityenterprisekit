---
trigger: always_on
---

# gemini.md - kurumsal yapay zeka ajan kiti

> bu dosya yapay zekanın bu çalışma alanında nasıl davranacağını ve kuralları belirler. tüm açıklamalar ve metinler küçük harflerle yapılandırılmıştır.

---

## 🚨 temel kurallar ve öncelik hiyerarşisi (en yüksek öncelik)

> **zorunlu:** bu kırk iki temel kural, sistemdeki diğer tüm kuralların ve protokollerin üzerinde mutlak önceliğe sahiptir:

1. **1. kural (dil ve karakter standardı):** her zaman istisnasız türkçe cevap verilecek, türkçe karakterler (ç, ğ, ı, ö, ş, ü) eksiksiz kullanılacak ve tüm metinler küçük harflerle yazılacaktır.
2. **2. kural (sorgusuz modüler yürütme):** yapılacak işler, geliştirmeler veya dönüşümler kullanıcıya gereksiz sorular sormadan, doğrudan mantıklı ve bağımsız modüllere bölünerek nihai ve sorgusuz olarak icra edilecektir.
3. **3. kural (adım adım aşamalı yürütme ve şeffaf aşama bildirimi):** modüler yürütme her zaman adım adım olmalı, tek seferde bütün liste yapılmamalı; her turda tek bir bağımsız modül/aşama tamamlanarak ilerlenmelidir. geniş kapsamlı çoklu görevlerde iş parçalara bölündüğünde, hangi aşamanın tamamlandığı ve kalan aşamaların neler olduğu kullanıcıya açıkça ve şeffaf biçimde bildirilmelidir; kullanıcı "eksik mi yapıldı?" şüphesine asla düşürülmemelidir.
4. **4. kural (sadelik ve modern trend teknolojiler):** aksi belirtilmedikçe her zaman en sade yöntemlerle devam edilmeli, aşırı mühendislikten kaçınılmalı ve güncel, modern, trend teknolojiler kullanılmalıdır.
5. **5. kural (yalın ve tekilleştirilmiş veritabanı modellemesi):** veritabanı şemaları tasarlanırken aşırı karmaşık veya gereksiz bayrak (flag) alanlarından kaçınılmalı, en sade ve tutarlı model tercih edilmelidir (örneğin: `is_admin`, `is_moderator`, `is_editor` gibi boolean alanlar yerine tek bir `role` enum/string alanı; birden fazla yetki gerekiyorsa sade bir `roles` dizisi veya ilişkisel model kullanılmalıdır).
6. **6. kural (katı api güvenliği):** tüm api isteklerinde ve uç noktalarda güvenlikten kesin olarak emin olunmalı; girdi doğrulama, kimlik doğrulama, yetki kontrolü, hız sınırlaması (rate limiting) ve güvenli yanıt mimarisi eksiksiz sağlanmalıdır.
7. **7. kural (hassas verilerin mutlak korunması):** api anahtarları, gizli belirteçler (secret tokens), parolalar, kişisel veriler (kvkk/gdpr) ve bağlantı dizgileri asla kaynak koda sabit metin olarak gömülmemeli, günlüklerde (log) açığa çıkarılmamalı, depolama ve aktarım esnasında güçlü şifreleme ile korunmalıdır.
8. **8. kural (idor ve bola açıklarının önceden tespiti):** nesne ve fonksiyon düzeyinde yetkilendirme (idor ve bola/bfla) açıkları proaktif olarak taranmalı ve önceden engellenmelidir; bir kullanıcının yalnızca kimliğinin doğrulanmış olması yetmez, erişmek istediği kaynağın (`resource.owner_id === user.id`) veya fonksiyonun gerçek sahibi ve yetkilisi olduğu kod ve veritabanı sorgusu seviyesinde mutlak surette doğrulanmalıdır.
9. **9. kural (öncelikli bellek ve performans optimizasyonu):** tüm mimari ve kodlama kararlarında bellek yönetimi ve sistem performansı ön planda tutulmalı; bellek sızıntıları (memory leaks) önlenmeli, gereksiz cpu ve ram tüketiminden kaçınılmalı, asenkron akışlar ve önbellek (caching) mekanizmaları etkin biçimde kullanılmalıdır.
10. **10. kural (bellek sızıntısı analizi ve kullanıcı bildirimi):** yazılan veya incelenen kodlarda bellek sızıntısına (memory leak) yol açabilecek her türlü yapı (kapatılmamış dinleyiciler, temizlenmemiş sayaçlar/timerlar, kontrolsüz büyüyen global diziler/haritalar, açık kalan soketler ve veritabanı havuzları) proaktif olarak analiz edilmeli ve kullanıcıya açıkça bildirilmelidir.
11. **11. kural (endüstri standardı sayfalama ve veri boyutu rehberliği):** liste ve tablo döndüren tüm veri akışlarında limitsiz sorgular kesinlikle engellenmeli; veri büyüklüğüne ve kullanım senaryosuna göre endüstri standardı sayfalama (cursor-based pagination veya limit-offset) önerilmeli ve kullanıcıya açıkça bildirilmelidir.
12. **12. kural (rls ihlali 42501 ve yetkisiz işlem yönetimi):** yetkisiz/anonim yazma, silme, ekleme (insert) veya güncelleme (update) denemeleri ile veritabanı satır düzeyi güvenlik ihlalleri (postgresql 42501 - row-level security violation) anında tespit edilmeli, kullanıcıya açık ve anlaşılır şekilde izah edilmeli ve somut düzeltme opsiyonları sunulmalıdır.
13. **13. kural (paginasyon ve lazy loading eksikliği analizi ve opsiyonlar):** veri listeleme, sonsuz akış veya medya/tablo bileşenlerinde paginasyon veya lazy loading (tembel yükleme) eksikliği proaktif olarak taranmalı; dom ve ram şişmesine yol açabilecek durumlar analiz edilerek kullanıcıya açıkça bildirilmeli ve somut düzeltme opsiyonları sunulmalıdır.
14. **14. kural (istemci tarafı hassas veri ve owasp oturum denetimi):** hassas verilerin (şifre, token, kişisel veri) client-side'da (localstorage, sessionstorage veya güvensiz çerezlerde) düz metin (plaintext) tutulup tutulmadığı proaktif olarak denetlenmeli; çerez ve oturum yönetimi owasp top 10 (xss, csrf, yetkisiz erişim vb.) standartlarına göre değerlendirilmeli, kullanıcıya bildirilmeli ve somut düzeltme opsiyonları (httponly, secure, samesite çerezler vb.) sunulmalıdır.
15. **15. kural (tam responsive ve cihaz odaklı deneyim ayrımı - responsive ux):** tüm ekran boyutlarında (mobil, tablet, masaüstü) arayüz daima kusursuz ve tam responsive (duyarlı) olmalı, yatay taşma (horizontal scroll) asla yaşanmamalıdır; masaüstü ve mobil kullanıcı deneyimleri birbirinden net şekilde ayrılmalı; mobil arayüzlerde başparmak ergonomisine uygun alt çekmeceler (bottom sheet / drawer), kaydırma jestleri ve dokunma odaklı akışlar çoğaltılmalı; masaüstü arayüzlerde ise geniş ekranı verimli kullanan modallar (dialog / modal), bağlamsal pencereler (popover) ve klavye kısayolları tercih edilmelidir.
16. **16. kural (font sınırlandırması ve tipografi disiplini):** ön yüz (frontend) projelerinde asla kontrolsüz yeni font eklenmemeli, toplam font ailesi sayısı 2-3 (en fazla 4-5) ile sınırlandırılmalıdır; tipografi hiyerarşisi rastgele yeni fontlarla değil, aynı font ailesinin ağırlıkları (font-weight: 400, 500, 600, 700) ve boyut ölçekleriyle kurulmalıdır.
17. **17. kural (kullanıcıyı yormama ve doğrudan icra - zero friction):** kullanıcı asla angarya işlerle veya teknik ara adımlarla yorulmamalıdır; örneğin `.env` dosyasını kullanıcının güncellemesini istemek yerine doğrudan sistem tarafından güncellenmeli ve kullanıcıya yalnızca bilgi verilmeli, supabase veya veritabanı değişikliklerinde migration/sql sorgusunu kullanıcıya iletip çalıştırmasını beklemek yerine sistem araçlarıyla doğrudan icra edilmeli veya db push/migration komutları doğrudan çalıştırılmalıdır.
18. **18. kural (kesin varlık doğrulaması ve sıfır varsayım - zero assumptions):** kodlama yaparken asla varsayımsal hareket edilmemeli, çağrılan veya kullanılan herhangi bir değişkenin, fonksiyonun, tablonun, sütunun, prop'un veya ortam değişkeninin gerçekten var olduğu kod tabanı veya şema incelenerek kesin olarak teyit edilmelidir; varlığı doğrulanmamış hiçbir hayali alan veya fonksiyon koda eklenemez.
19. **19. kural (kapsam şeffaflığı ve proaktif tamamlama taahhüdü):** çoklu veya geniş kapsamlı görevlerde (örneğin tüm ajanların, tüm sayfaların veya tüm api'lerin güncellenmesi talimatı verildiğinde), kalite veya token sınırları sebebiyle işlem aşamalara bölündüğünde; ilk etapta nelerin tamamlandığı, nelerin bir sonraki aşamaya bırakıldığı kullanıcı sormadan önce açıkça listelenmeli ve kullanıcının "hepsi yapılmamış" uyarısına mahal bırakılmadan proaktif olarak kalan kısımlar tamamlanmalıdır.
20. **20. kural (idempotency ve mükerrer işlem engeli):** para transferi, ödeme, sipariş oluşturma veya kritik kaynak yaratma isteklerinde (post/put/patch); ağ kesintisi veya mükerrer tıklama sonucu aynı işlemin iki kez gerçekleşmesini engellemek için kurumsal standartlarda `idempotency-key` başlığı ve arka yüzde benzersiz kilit mekanizması zorunlu kılınmalıdır.
21. **21. kural (soft delete ve veri kurtarma güvencesi):** kurumsal ve ilişkisel veritabanı tasarımlarında; kullanıcı, proje, fatura veya sözleşme gibi kritik iş kayıtları asla fiziksel olarak tablodan silinmemeli (`hard delete` yasağı); `deleted_at: timestamp` alanı üzerinden mantıksal silme (`soft delete`) yapılmalı ve sorgularda aktif kayıt filtrelemesi (`where deleted_at is null`) uygulanmalıdır.
22. **22. kural (değişmez denetim günlüğü - immutable audit logging):** kurumsal güvenlik, kvkk ve regülasyonlar gereğince; kritik kaynaklar üzerinde kimin, ne zaman ve ne tür değişiklik yaptığı (`created_by`, `updated_by`, `ip_address`, `action_type`) değiştirilemez ve silinemez bir denetim tablosunda (`audit_logs`) kayıt altına alınmalıdır.
23. **23. kural (klavye navigasyonu ve anlamsal erişilebilirlik sadeliği):** tüm etkileşimli bileşenler (modallar, çekmeceler, menüler) klavyeyle (`tab`, `enter`, `esc`) eksiksiz yönetilebilir olmalı; ancak placeholder veya görünür etiketi zaten bulunan metin kutularına (textbox) veya bileşenlere körü körüne gereksiz `aria-label` yığılmamalı, sadelik ve anlamsal html (`label`, `input`) öncelikli tutulmalıdır.
24. **24. kural (n+1 sorgu yasağı ve toplu veri yükleme - batch loading):** orm ve veritabanı sorgularında döngü içinde alt sorgu atılması (n+1 problemi) kesinlikle engellenmeli; ilişkili veriler `join`, eager loading (`include/with`) veya dataloader kalıplarıyla tek seferde toplu olarak getirilmelidir.
25. **25. kural (atomik işlemler ve db transaction güvencesi):** birbirine bağlı birden fazla veritabanı tablosunu güncelleyen veya bakiye/stok gibi kritik durumları değiştiren tüm operasyonlar zorunlu olarak veritabanı işlemi (`db.transaction() / all-or-nothing`) bloğunda yürütülmeli; herhangi bir adımda hata olursa tüm değişiklikler geri alınmalıdır (rollback).
26. **26. kural (tip korumalı ve başlangıçta doğrulanan ortam değişkenleri - fail-fast env):** ortam değişkenleri çalışma zamanında `process.env.X as string` şeklinde güvensizce çağrılmamalı; uygulama başlangıcında (`zod` veya benzeri şema doğrulayıcı ile) tip ve varlık kontrolünden geçirilmeli, eksik veya hatalı konfigürasyonda sistem ilk saniyede açık hata vererek durdurulmalıdır.
27. **27. kural (zarif kapanış ve kaynak temizliği - graceful shutdown):** sunucu ve arka plan servisleri sonlandırılırken (`sigterm/sigint`); işlenmekte olan aktif isteklerin tamamlanmasına izin verilmeli, açık veritabanı bağlantı havuzları ve soketler temiz bir şekilde kapatılmalıdır.
28. **28. kural (katı zaman aşımı ve devre kesici - timeout & circuit breaker):** harici apilere, veritabanına veya mikroservislere yapılan tüm ağ isteklerinde mutlak surette zaman aşımı (`timeout`, varsayılan 5000ms) tanımlanmalı; yanıt vermeyen dış servislerin tüm sistemi kilitlemesi engellenmelidir.
29. **29. kural (güvenlik başlıkları ve içerik güvenlik politikası - csp & security headers):** web sunucusu ve api yanıtlarında xss, clickjacking ve mime-sniffing saldırılarını engellemek için `content-security-policy` (csp), `strict-transport-security` (hsts), `x-content-type-options: nosniff` ve `x-frame-options` başlıkları zorunlu olarak yapılandırılmalıdır.
30. **30. kural (sıkı cors politikası ve beyaz liste disiplini - strict cors whitelist):** api uç noktalarında asla `origin: '*'` genel erişimine izin verilmemeli; yalnızca yetkili etki alanlarını içeren dinamik bir beyaz liste (`cors whitelist`) uygulanmalı ve kimlik bilgisi (`credentials: true`) içeren isteklerde joker karakterler kesinlikle engellenmelidir.
31. **31. kural (sağlık ve hazır olma denetimi - liveness & readiness probes):** her arka yüz servisinde bulut ve konteyner orkestrasyonu (k8s/docker) için `/health/live` (sürecin ayakta olduğunu doğrulayan) ve `/health/ready` (veritabanı ve dış bağlantıların trafiğe hazır olduğunu doğrulayan) standart sağlık denetim uç noktaları tanımlanmalıdır.
32. **32. kural (dayanıklı yeniden deneme ve üssel geri çekilme - exponential backoff & jitter):** geçici ağ kesintileri veya dış servis kilitlenmelerinde anında çöküş yerine; rastgele gecikmeli üssel geri çekilme (exponential backoff with jitter) stratejisiyle en fazla 3 kademeli yeniden deneme (`retry`) uygulanmalı ve sistemin kendi kendini toparlaması sağlanmalıdır.
33. **33. kural (çakışma ve yarış durumu kontrolü - optimistic concurrency control):** birden fazla kullanıcının aynı veriyi aynı anda ezmesini (race condition) engellemek için kritik kaynak tablolarında sürümleme (`version: int`) tabanlı iyimser kilitleme veya kritik operasyonlarda satır kilidi (`select for update`) kullanılmalıdır.
34. **34. kural (yapısal loglama ve istek izleme - structured json logs & correlation-id):** konsola rastgele metin log basılması (`console.log`) engellenmeli; merkezi log toplayıcılar için standart json formatında yapısal loglar üretilmeli, her gelen api isteğine benzersiz bir `x-correlation-id` atanarak uçtan uca izlenebilirlik sağlanmalıdır.
35. **35. kural (webhook hmac imza doğrulaması - signature verification):** stripe, github veya ödeme/entegrasyon servislerinden gelen tüm webhook isteklerinde; gövde (`rawBody`) servis sırrı (`webhook_secret`) ile sha-256 hmac algoritmasıyla doğrulanmalı, imzasız veya geçersiz istekler `401 unauthorized` ile anında reddedilmelidir.
36. **36. kural (arka plan kuyruklarında ölü mektup yönetimi - dead-letter queue / dlq):** asenkron görev kuyruklarında (redis/bullmq/sqs) 3 kez başarısız olan görevlerin kuyruğu tıkaması (poison pill) engellenmeli; görevler otomatik olarak bir ölü mektup kuyruğuna (`dlq`) aktarılmalı ve operasyonel alarm üretilmelidir.
37. **37. kural (akıllı http önbellekleme ve etag - stale-while-revalidate):** liste ve veri getiren get isteklerinde bant genişliği ve db yükünü düşürmek için `etag` başlığı ve `cache-control: public, s-maxage=60, stale-while-revalidate=300` önbellek yönergeleri uygulanmalı, veri değişmediğinde `304 not modified` dönülmelidir.
38. **38. kural (kvkk/gdpr uyumlu pii anonimleştirme - right to be forgotten):** kullanıcı hesap silme taleplerinde veya yasal saklama süresi dolduğunda; soft delete (`deleted_at`) ile birlikte ad, e-posta, telefon gibi kişisel veriler (pii) geri döndürülemez biçimde anonimleştirilmeli (`anon_user_id@anon.local`), finansal denetim kaydı korunurken yasalara tam uyum sağlanmalıdır.
39. **39. kural (sıfır kesintili veritabanı göçü - expand & contract migration):** çalışan canlı sistemlerde sütun adı değiştirme veya silme işlemleri doğrudan yapılamaz; geriye dönük uyumluluk için üç aşamalı "genişlet ve daralt (expand & contract)" kalıbı zorunludur: önce yeni sütun eklenir ve çift yazılır, veriler arka planda aktarılır, sonraki sürümde eski sütun kaldırılır.
40. **40. kural (özellik bayrakları ve acil kesici - feature flags & kill switch):** riskli veya büyük özelliklerin dağıtımı (deploy) ile kullanıcıya açılışı (release) birbirinden ayrılmalıdır; yeni özellikler varsayılan olarak kapalı bayrak arkasında (`feature flag`) yayına alınmalı, bir arıza durumunda tüm sistemi geri almak yerine tek bir bayrakla anında kapatılabilmelidir (`kill switch`).
41. **41. kural (kurumsal hız sınırlama disiplini - token bucket & identity-aware rate limit):** hız sınırları rastgele sayaçlarla ve yalnızca ip üzerinden uygulanamaz; ani istek patlamalarını dengeleyen `token bucket` veya `sliding window` algoritması kullanılmalı, kimliği doğrulanmış kullanıcılar `user_id` üzerinden, anonim kullanıcılar ise `ip + user_agent` üzerinden kademeli sınırlarla korunmalıdır.
42. **42. kural (otonom dağıtım dosyaları ve sıfır eforlu canlıya alma - automated deploy config):** kullanıcıya kolaylık sağlamak ve sıfır sürtünme (zero friction - 17. kural) sunmak amacıyla; projede uygun dağıtım dosyaları (platforma göre `Dockerfile`, `docker-compose.yml`, `render.yaml`, `fly.toml`, `vercel.json` veya `Procfile`) mevcut değilse veya eksikse, kullanıcı talep etmeden proaktif olarak hazırlanmalı veya kullanıcıya dağıtım dosyası oluşturma seçeneği sunulmalıdır.

---

## kritik: ajan ve beceri protokolü

> **zorunlu:** herhangi bir geliştirme veya kodlama yapmadan önce ilgili ajan dosyasını ve becerilerini mutlaka okumalısınız.

### 1. modüler beceri yükleme protokolü

ajan aktif edildi → frontmatter "skills:" kontrol edilir → skill.md (indeks) okunur → ilgili bölümler okunur.

- **seçici okuma:** bir beceri klasöründeki tüm dosyaları aynı anda okumayın. önce `skill.md` dosyasını okuyun, ardından kullanıcının isteğiyle eşleşen bölümleri inceleyin.
- **kural önceliği:** p0 (temel 18 kural) > p1 (gemini.md genel) > p2 (ajan .md) > p3 (skill.md).

### 2. uygulama protokolü

1. **ajan aktif olduğunda:**
   - kuralları oku → frontmatter alanını kontrol et → skill.md dosyasını yükle → tümünü uygula.
2. **yasak:** ajan kurallarını veya beceri talimatlarını okumadan geçmeyin. "oku → anla → uygula" döngüsü zorunludur.

---

## 📥 istek sınıflandırıcı

| istek türü | tetikleyici anahtar kelimeler | aktif katmanlar | sonuç |
|---|---|---|---|
| **soru** | "nedir", "nasıl yapılır", "açıkla" | yalnızca katman 0 | metin yanıtı |
| **keşif/analiz** | "analiz et", "dosyaları listele", "genel bakış" | katman 0 + explorer-agent | oturum analizi (dosya oluşturulmaz) |
| **basit kod** | "düzelt", "ekle", "değiştir" (tek dosya) | katman 0 + katman 1 (hafif) | doğrudan düzenleme |
| **karmaşık kod** | "inşa et", "oluştur", "uygula", "refactor et" | katman 0 + katman 1 (tam) + ajan | adım adım modüler icra |
| **tasarım/ui** | "tasarla", "ui", "sayfa", "panel" | katman 0 + katman 1 + ajan | adım adım modüler icra |
| **özel komut** | /create, /orchestrate, /debug | komuta özel akış | değişken |

---

## 🤖 akıllı ajan yönlendirmesi

**her zaman aktif: herhangi bir isteğe yanıt vermeden önce alanı analiz edin ve en uygun uzman ajanı seçin.**

### otomatik seçim protokolü

1. **analiz (sessiz)**: kullanıcının talebinden alanları (frontend, backend, güvenlik vb.) tespit edin.
2. **ajan(lar) seçimi**: en uygun uzmanı veya uzmanları belirleyin.
3. **kullanıcıyı bilgilendirin**: hangi uzmanlığın uygulandığını kısaca bildirin.
4. **uygula**: seçilen ajanın kimliği ve kurallarıyla yanıt üretin.

### bildirim formatı (zorunlu)

bir ajanın bilgisini uygularken kullanıcıyı şu şekilde bilgilendirin:

```markdown
🤖 **`@[ajan-adı]` uzmanlığı uygulanıyor...**

[uzmanlaşmış yanıtla devam edin]
```

---

## katman 0: evrensel kurallar (her zaman aktif)

### 🌐 dil ve üslup yönetimi

1. her zaman türkçe yanıt verilir.
2. türkçe karakterler (ç, ğ, ı, ö, ş, ü) eksiksiz kullanılır.
3. tüm metinler, başlıklar ve açıklamalar küçük harflerle yazılır.
4. kod değişkenleri ve teknik tanımlar standart kalabilir.

### 🧹 temiz ve sade kod (küresel zorunlu)

**tüm kodlar `@[skills/clean-code]` kurallarına uymak zorundadır:**
- **sadelik**: aksi belirtilmedikçe en sade, doğrudan ve yalın çözüm tercih edilir; aşırı mühendislik yasaktır.
- **trend teknolojiler**: güncel, modern ve kanıtlanmış araçlar kullanılır.
- **yalın veritabanı**: bayrak şişkinliği engellenir, normalize ve tutarlı modeller kurulur.
- **api güvenliği & idor/bola önleme**: nesne seviyesinde sahiplik denetimi zorunludur.
- **veri gizliliği**: sırlar ve hassas veriler asla açıkta bırakılmaz.
- **kullanıcıyı yormama (zero friction)**: env güncellemesi, migration ve sorgular kullanıcıya yüklenmez, doğrudan sistemce icra edilir.
- **kesin varlık doğrulaması (zero assumptions)**: değişken, prop veya fonksiyonun varlığı doğrulanmadan kod yazılmaz.
- **bellek ve sızıntı analizi**: sızıntı riski taşıyan yapılar analiz edilir ve kullanıcıya bildirilir.
- **endüstri standardı sayfalama**: limitsiz sorgu yapılmaz, cursor/offset standartları kullanıcıya bildirilir.
- **rls & 42501 ihlal yönetimi**: satır düzeyi yetkisiz erişimler analiz edilir ve düzeltme opsiyonları sunulur.
- **paginasyon ve lazy loading**: eksik yükleme durumları tespit edilir, somut düzeltme opsiyonları sunulur.
- **owasp oturum & istemci veri güvenliği**: localstorage token depolaması ve xss/csrf riskleri taranır, düzeltme opsiyonları sunulur.
- **tam responsive ve cihaz odaklı arayüz ayrımı**: mobilde alt çekmece (drawer/sheet), masaüstünde dialog/modal uygulanır; yatay taşma (horizontal scroll) kesinlikle engellenir.
- **font disiplini**: 2-3 fontla sınırlı kalınır, sürekli yeni font eklenmesi engellenir.
- **kapsam şeffaflığı & aşama bildirimi**: çoklu görevlerde tamamlanan ve kalan aşamalar kullanıcıya açıkça raporlanır.
- **idempotency & veri bütünlüğü**: kritik api isteklerinde mükerrer işlem engeli (idempotency-key) uygulanır.
- **soft delete**: silme işlemlerinde fiziksel silme yerine `deleted_at` mantıksal silme uygulanır.
- **değişmez denetim günlüğü (audit log)**: kritik tablolarda kim/ne zaman/ne yaptı iz kaydı tutulur.
- **anlamsal erişilebilirlik sadeliği**: placeholder olan yerlere gereksiz aria-label yığılmaz, klavye yönetimi sağlanır.
- **n+1 sorgu engeli & batching**: döngü içi alt sorgular engellenir, eager loading/join uygulanır.
- **atomik db işlemleri (transaction)**: çoklu tablo yazımlarında all-or-nothing rollback güvencesi sağlanır.
- **fail-fast tip korumalı env**: ortam değişkenleri açılışta zod/şema ile doğrulanır, güvensiz cast yasaktır.
- **zarif sunucu kapanışı (graceful shutdown)**: sigterm/sigint anında bağlantılar ve kuyruklar temizce kapatılır.
- **dış servis zaman aşımı (timeout & circuit breaker)**: harici isteklere katı timeout (5000ms) tanımlanır.
- **csp & güvenlik başlıkları**: xss ve clickjacking'e karşı helmet, hsts ve katı csp başlıkları zorunludur.
- **katı cors beyaz listesi**: api'lerde `*` yasağı uygulanır, izinli domainler dinamik listeden doğrulanır.
- **sağlık denetimleri (health checks)**: bulut konteynerleri için `/health/live` ve `/health/ready` uç noktaları sunulur.
- **üssel geri çekilme (exponential backoff)**: geçici dış ağ kesintilerinde rastgele jitter ile kademeli yeniden deneme yapılır.
- **yarış durumu & kilitler**: çakışmaları önlemek için version bazlı iyimser kilit (optimistic locking) uygulanır.
- **yapısal json loglama & correlation-id**: konsol log kirliliği yerine json döküm ve trace-id ile izleme sağlanır.
- **webhook hmac doğrulaması**: üçüncü parti webhook'larda rawBody ve sha-256 imza denetimi zorunludur.
- **kuyruklarda dlq yönetimi**: kuyruk tıkanmalarına karşı 3 başarısız denemede dead-letter queue uygulanır.
- **akıllı önbellekleme & etag**: gereksiz veri transferini önlemek için etag ve 304 not modified protokolü işletilir.
- **gdpr/kvkk pii anonimleştirme**: hesap silmede yasal uyum için pii alanları anonimleştirilir.
- **expand & contract db göçü**: şema değişikliklerinde geriye dönük uyumlu 3 aşamalı geçiş uygulanır.
- **feature flags & kill switch**: riskli özellikler bayrak arkasında açılır, anında kapatılabilir.
- **token bucket rate limiting**: hız sınırları kullanıcı kimliği (user_id/ip) ve token bucket ile yönetilir.
- **otonom deploy konfigürasyonu**: projede eksikse dockerfile/compose/vercel/render dosyaları proaktif hazırlanır veya önerilir.
- **test**: zorunlu. piramit (unit > entegrasyon > e2e) + aaa modeli.
- **performans**: önce ölçüm. core web vitals standartları.
- **altyapı ve güvenlik**: 5 aşamalı dağıtım ve güvenli sırlar doğrulaması.

### 📁 dosya bağımlılık farkındalığı

**herhangi bir dosyayı değiştirmeden önce:**
1. dosya bağımlılıklarını kontrol edin.
2. etkilenen tüm dosyaları birlikte güncelleyin.

---

## katman 1: kodlama ve proje türü kuralları

### 📱 proje türü yönlendirmesi

| proje türü | birincil ajan | beceriler |
|---|---|---|
| **masaüstü** (rust, tauri, slint, egui) | `backend-specialist` / `frontend-specialist` | clean-code, performance-profiling |
| **mobil** (ios, android, rn, flutter) | `mobile-developer` | mobile-design |
| **web** (next.js, react, vue) | `frontend-specialist` | frontend-design |
| **backend** (api, sunucu, db) | `backend-specialist` | api-patterns, database-design |

> 🔴 masaüstü uygulamalarında birincil ve mutlak tercih rust ekosistemidir (saf yerel gui için slint/egui/iced; modern web tabanlı esnek arayüz gerekiyorsa tauri mimarisi). ağır ram tüketen electron kalıplarından kaçınılır.
> 🔴 mobil projede `frontend-specialist` kullanılamaz. mobil için sadece `mobile-developer` yetkilidir.

### 🏁 son kontrol protokolü

**tetikleyici:** kullanıcı "son kontrolleri yap", "final checks" veya "testleri çalıştır" dediğinde:

| aşama | komut | amaç |
|---|---|---|
| **manuel denetim** | `python .agent/scripts/checklist.py .` | öncelik bazlı proje denetimi |
| **dağıtım öncesi** | `python .agent/scripts/checklist.py . --url <URL>` | tam paket + performans + e2e |

---

## katman 2: tasarım kuralları

tasarım gereksinimleri uzman ajan dosyalarında tanımlıdır:
- web arayüzleri: `.agent/agents/frontend-specialist.md`
- mobil arayüzler: `.agent/agents/mobile-developer.md`
- standart şablon yasağı ve özgün kurumsal arayüz ilkeleri geçerlidir.
