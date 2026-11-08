---
name: database-design
description: kurumsal veritabanı tasarım ilkeleri. şema tasarımı, indeksleme, orm seçimi, yalın veri modelleme, sayfalama ve rls (42501) hata yönetimi.
priority: p1-structural
version: 2.1.0
---

# yalın ve kurumsal veritabanı tasarım standartları

bu beceri, veritabanı şemalarının kurulması, endüstri standardı sayfalama ve satır düzeyi güvenlik (rls) ihlallerinin (postgresql 42501) analiz edilip çözülmesini yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 12 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir modül tamamlanır.
   - sadelik, modern trend teknolojiler, yalın veri modelleme ve api güvenliği.
   - idor/bola önleme, bellek optimizasyonu, sızıntı analizi ve endüstri standardı sayfalama.
   - **12. kural (rls ihlali 42501 ve yetkisiz işlem yönetimi):** yetkisiz ekleme/silme ve rls ihlalleri anında tespit edilir, kullanıcıya açıklanır ve düzeltme opsiyonları sunulur.
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki veri mimarisi standartları.

---

## 🛡️ 12. kural: rls ihlali (42501) ve yetkisiz işlem protokolü

postgresql / supabase gibi modern veritabanlarında `error: 42501 (insufficient_privilege / new row violates row-level security policy)` hatası veya yetkisiz anonim yazma/silme tespit edildiğinde şu protokol işletilir:

### 1. kök neden analizi
- **anonim istemci çağrısı:** istemci oturum açmadan (anon key ile) `insert`, `update` veya `delete` işlemi yapmaya çalışıyor olabilir.
- **eksik rls politikası (policy):** tabloda `alter table ... enable row level security` yapılmış ancak ilgili operasyon (`for insert`, `for update`) için geçerli bir `create policy` tanımlanmamıştır.
- **jwt / auth bağlamı eksikliği:** kullanıcının `auth.uid()` bilgisi veritabanı oturumuna aktarılmamıştır.

### 2. kullanıcı bildirim formatı (zorunlu şablon)

bir 42501 veya rls ihlali oluştuğunda kullanıcıya şu açıklama ve çözüm opsiyonları sunulur:

```markdown
🚨 **veritabanı satır düzeyi güvenlik ihlali uyarısı (12. kural - hata 42501):**
- **etkilenen tablo ve işlem:** `[tablo_adi]` üzerindeki `[insert / update / delete]` işlemi engellendi.
- **neden oluştu:** kullanıcı oturumu yetkisiz (anonim) veya mevcut rls politikası bu kullanıcının satırı değiştirmesine izin vermiyor.

### 🛠️ çözüm opsiyonları:
1. **opsiyon a (güvenli oturum doğrulama - önerilen):**
   istek öncesinde kullanıcının kimliğini doğrulayın ve kullanıcı kimliğini satır sahipliğiyle eşleştirin:
   ```sql
   create policy "kullanıcılar sadece kendi verilerini ekleyebilir" 
   on [tablo_adi] for insert 
   with check (auth.uid() = user_id);
   ```
2. **opsiyon b (servis rolü / backend yetkisi):**
   eğer işlem sunucu tarafında güvenli bir cron/arka plan göreviyse, istemci anahtarı yerine `service_role` anahtarını veya veritabanı superuser yetkisini kullanın.
3. **opsiyon c (anonim erişime kontrollü izin verme):**
   eğer tablo gerçekten halka açık anonim yazmaya uygunsa (örneğin iletişim formu), açık rls politikası tanımlayın:
   ```sql
   create policy "anonim kayıtlara izin ver" 
   on [tablo_adi] for insert 
   to anon with check (true);
   ```
```
