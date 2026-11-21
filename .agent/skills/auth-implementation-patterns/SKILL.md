---
name: auth-implementation-patterns
description: kurumsal oauth2, openid connect (oidc), jwt ömür döngüsü, session yönetimi, mfa ve rbac/abac mimarileri.
when_to_use: "oauth2, oidc, mfa, jwt oturum omur dongusu ve rbac yetki mimarisi kurulurken kullanilir."
allowed-tools: [Read, Write, Edit, Grep]
version: 2.0.0
---

# kurumsal kimlik doğrulama, yetkilendirme ve yaşam döngüsü standartları

bu beceri; endüstri standardı oauth2, oidc, güvenli çerez tabanlı oturum yönetimi, rol bazlı erişim denetimi (rbac) ve kimlik verilerinin (kullanıcı adı, e-posta vb.) tüm yaşam döngüsü boyunca (kayıt, oauth provisioning, profil düzenleme) tek doğruluk kaynağından (ssot) yönetilmesini sağlar.

---

## 🚨 temel kurallar ve mimari ilkeler

1. **katı api güvenliği (6. kural):** girdi doğrulama, brute-force engeli ve hız sınırlaması.
2. **hassas veri ve sır koruması (7. kural):** argon2/bcrypt ile parola özetleme, asla düz metin saklamama.
3. **istemci tarafı oturum hijyeni (14. kural):** token'lar asla `localStorage` içinde saklanmaz; `httpOnly, Secure, SameSite=Strict` çerezler zorunludur.
4. **tek doğruluk kaynağı ve yaşam döngüsü senkronizasyonu (18. ve 46. kural):** kullanıcı adı, slug veya kimlik kuralları tek bir ekranda izole kalamaz; kayıt, oauth girişi ve profil düzenleme tek bir merkezi doğrulama motoruna bağlanmalıdır.

---

## 🔑 kimlik ve kullanıcı adı yaşam döngüsü senkronizasyonu (ssot)

bir kimlik alanına (örneğin `username`, `slug`, `handle`) bir kural, kısıtlama veya regex getirildiğinde şu 4 temas noktası proaktif olarak ve aynı anda güncellenmelidir:

### 1. tek doğruluk kaynağı (single source of truth - shared engine)
- doğrulama kuralı asla tek bir api route'unda (`app/api/profile/route.ts`) veya tek bir form bileşeninde kopyalanıp bırakılamaz.
- kural ortak bir kütüphane modülünde (`lib/username.ts` veya `shared/validators/auth.ts`) tekilleştirilmelidir:
  ```typescript
  // lib/username.ts - ortak doğrulama ve sanitizasyon motoru
  export const USERNAME_REGEX = /^(?!.*\.\.)(?!^\.)[a-z0-9_.]{3,30}(?<!\.)$/;

  export function isValidUsername(val: string): boolean {
    return USERNAME_REGEX.test(val);
  }
  ```

### 2. sosyal giriş ve oauth ilk profil oluşturma (provisioning sanitization)
- kullanıcı google, apple, github veya clerk/supabase oauth ile ilk kez giriş yaptığında, e-posta veya sosyal profil adı doğrudan ham olarak kullanıcı adına atanmamalıdır (çünkü boşluk, ardışık nokta `..` veya geçersiz karakterler içerebilir).
- **otomatik sanitizasyon (sanitize) ve benzersizlik (unique) motoru zorunludur:**
  ```typescript
  export function sanitizeUsername(candidate: string): string {
    return candidate
      .toLowerCase()
      .trim()
      .replace(/[\s-]+/g, '_')           // boşluk ve tireleri _ yap
      .replace(/[^a-z0-9_.]/g, '')        // geçersiz karakterleri at
      .replace(/\.{2,}/g, '.')           // ardışık çift noktaları tek noktaya indir
      .replace(/^\.+|\.+$/g, '')         // baştaki ve sondaki noktaları sil
      .slice(0, 30);                      // maksimum uzunluk sınırı
  }

  export async function getUniqueUsername(candidate: string, db: DatabaseClient): Promise<string> {
    let clean = sanitizeUsername(candidate);
    if (clean.length < 3) clean = `user_${clean}`.slice(0, 30);
    
    let username = clean;
    let counter = 1;
    // veritabanında çakışma varsa otomatik ekle (_1, _2)
    while (await db.user.findUnique({ where: { username } })) {
      const suffix = `_${counter}`;
      username = `${clean.slice(0, 30 - suffix.length)}${suffix}`;
      counter++;
    }
    return username;
  }
  ```

### 3. tam yaşam döngüsü denetim matrisi
ajan herhangi bir kimlik kuralı yazdığında veya güncellediğinde şu 4 noktayı eksiksiz kontrol etmek zorundadır:
- [ ] **kayıt formu (sign-up):** klasik e-posta/şifre ile kayıt olurken aynı regex/validator çalışıyor mu?
- [ ] **sosyal giriş / webhook (oauth provisioning):** google/github veya clerk webhook ile ilk kullanıcı kaydolurken `getUniqueUsername` sanitizasyonu devrede mi?
- [ ] **profil düzenleme (settings/profile):** ayarlar ekranında aynı regex ve `isUnique` kontrolü çalışıyor mu?
- [ ] **veritabanı kısıtlaması (db constraint):** tabloda `username UNIQUE` indeksi var mı?

### 4. şeffaf bildirim disiplini (developer ve son kullanıcı ux şeffaflığı)
- **geliştiriciye şeffaf raporlama (19. ve 46. kural):** ajan kimlik ve profil kurallarını güncellediğinde bunu sessizce yapamaz; hangi doğrulama kurallarının değiştiğini, oauth kayıt ve webhook katmanında `sanitizeUsername` ve `getUniqueUsername` fonksiyonlarının nasıl devreye alındığını kullanıcıya açıkça bildirmek zorundadır.
- **son kullanıcıya şeffaf ux bildirimi (zero silent mutation):** 
  sosyal girişle kaydolan bir kullanıcının adı otomatik temizlenip değiştirildiğinde veya çakışma sebebiyle `@can.toksun_1` şeklinde atandığında bu durum kullanıcıdan gizlenemez:
  1. **hoş geldin veya onboarding adımı:** kullanıcıya atanan kullanıcı adı açıkça gösterilmeli ("kullanıcı adınız @can.toksun_1 olarak belirlendi; dilediğiniz zaman profil ayarlarından değiştirebilirsiniz") veya ilk girişte kullanıcı adı onaylama/özelleştirme adımı sunulmalıdır.
  2. **anlaşılır doğrulama mesajları:** geçersiz kullanıcı adı denemelerinde jenerik hata mesajları yerine tam ihlal sebebi (örneğin "kullanıcı adı nokta ile başlayamaz ve ardışık iki nokta içeremez") kullanıcıya gösterilmelidir.

---

## 🛡️ token ve oturum ömür döngüsü

1. **access token:** 5 - 15 dakika ömürlü, ram veya `httpOnly` çerezde saklanır.
2. **refresh token:** dönen belirteç (token rotation). yetkisiz kullanımda tüm oturum ailesini iptal eder.
3. **mfa ve rbac:** kritik yönetim işlemlerinde adım adım yetkilendirme (step-up authentication).
