# ⚠️ database-design: kritik tuzaklar ve keskin kenarlar (sharp edges)

bu doküman, ilişkisel veritabanları (postgresql, mysql, sqlite) ve orm katmanlarında en sık yapılan, sistemi üretimde kilitleyen ve tespiti zor olan kritik mimari tuzakları ve bunların kesin çözümlerini listeler.

---

### 1. yabancı anahtarlarda (foreign key) indeks unutma tuzağı
- **tuzak:** postgresql ve çoğu rdbms, `foreign key` kısıtlaması eklediğinde otomatik olarak indeks oluşturmaz. ana tablodan (`users`) bir kayıt silindiğinde veya güncellendiğinde, alt tabloda (`orders`) fkey indeksi yoksa **tüm alt tablo tam tablo kilitlenmesine (table-level share lock)** uğrar.
- **çözüm:** tüm yabancı anahtar sütunlarına istisnasız b-tree indeksi ekleyin:
  ```sql
  create index idx_orders_user_id on orders(user_id);
  ```

---

### 2. serverless ve edge ortamında bağlantı havuzu (connection pool) tükenmesi
- **tuzak:** next.js server actions veya lambdalar her çalıştığında yeni bir veritabanı istemcisi (`new Client()`) başlatırsa; ani bir trafik patlamasında veritabanının `max_connections` sınırı (ör. 100) anında tükenir ve `fatal: remaining connection slots are reserved` hatası alınır.
- **çözüm:** doğrudan bağlantı yerine daima bir transaction pooler (pgbouncer veya supabase transaction mode - port 6543) kullanın; singleton orm client örneği uygulayın:
  ```typescript
  // prisma / drizzle singleton kalıbı
  const globalForDb = globalThis as unknown as { db: DatabaseClient };
  export const db = globalForDb.db || createDatabaseClient();
  if (process.env.NODE_ENV !== 'production') globalForDb.db = db;
  ```

---

### 3. rls (row-level security) sorgularında fonksiyon değerlendirme maliyeti
- **tuzak:** rls politikasında `auth.uid()` gibi fonksiyonlar her bir satır için tekrar tekrar çalıştırılırsa, 10.000 satırlık bir sorgu dakikalar sürer ve cpu tavan yapar.
- **çözüm:** rls politikalarında `auth.uid()` çağrısını alt sorgu (`select auth.uid()`) içine alarak postgresql'in fonksiyonu yalnızca bir kez yürütüp önbelleğe almasını sağlayın:
  ```sql
  -- yavaş (her satırda fonksiyon çağrısı)
  create policy "user_data" on documents for select using (user_id = auth.uid());

  -- hızlı (tek seferlik değerlendirme)
  create policy "user_data" on documents for select using (user_id = (select auth.uid()));
  ```

---

### 4. canlı tabloda güvenli migration (lock timeout zorunluluğu)
- **tuzak:** büyük bir tabloya `alter table` ile sütun eklerken veya tip değiştirirken tabloya exclusive kilit konur. çalışan uzun bir sorgu kilidin beklemesine ve arkasındaki tüm api isteklerinin kuyrukta şişerek sunucuyu çökertmesine yol açar.
- **çözüm:** canlı göçlerde her zaman kilit zaman aşımı (`lock_timeout`) belirleyin:
  ```sql
  set lock_timeout = '3s';
  alter table users add column if not exists status text default 'active';
  ```
