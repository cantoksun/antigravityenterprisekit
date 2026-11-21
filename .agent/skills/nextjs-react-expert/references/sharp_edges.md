# ⚠️ nextjs-react-expert: kritik tuzaklar ve keskin kenarlar (sharp edges)

bu doküman; react 19 ve next.js app router mimarilerinde en sık yapılan performans, render ve hydration hatalarını ve bunların kurumsal çözümlerini listeler.

---

### 1. ardışık veri bekleme şelalesi (waterfall await tuzağı)
- **tuzak:** server component içinde bağımsız veri isteklerinin art arda `await` edilmesi:
  ```typescript
  // yavaş: toplam süre = api1 + api2 + api3
  const user = await getUser();
  const posts = await getPosts();
  const metrics = await getMetrics();
  ```
- **çözüm:** bağımsız istekleri paralel başlatın veya streaming `Suspense` ile bölün:
  ```typescript
  // hızlı: paralel yürütme
  const [user, posts, metrics] = await Promise.all([
    getUser(),
    getPosts(),
    getMetrics(),
  ]);
  ```

---

### 2. namlu (barrel) import paket şişmesi tuzağı
- **tuzak:** simge veya ui kütüphanelerinden kök import yapmak (`import { Check } from 'lucide-react'`). derleyicinin yüzlerce kullanılmayan modülü demete dahil etmesine ve cold-start süresinin saniyelerce uzamasına yol açar.
- **çözüm:** doğrudan hedef dosyadan alt import yapın veya `next.config.ts` içinde `optimizePackageImports` tanımlayın:
  ```typescript
  // next.config.ts
  export default {
    experimental: {
      optimizePackageImports: ['lucide-react', '@radix-ui/react-icons'],
    },
  };
  ```

---

### 3. root layout içinde yanlışlıkla dinamik rendere düşme
- **tuzak:** kök `layout.tsx` dosyasında `cookies()` veya `headers()` fonksiyonunu çağırmak, tüm uygulamanın statik önbellekten (ssg/isr) çıkıp tamamen yavaş sunucu renderına (ssr) düşmesine neden olur.
- **çözüm:** dinamik başlık veya çerez okumasını kök layout'ta değil; yalnızca ihtiyaç duyan en derin alt sayfada veya middleware katmanında yapın.

---

### 4. mükerrer sunucu eylemi (server action double-submit)
- **tuzak:** form gönderimlerinde veya buton tıklamalarında `useTransition` / `useActionState` ile bekleme durumu (`isPending`) yönetilmediğinde; kullanıcının iki kez tıklaması çift sipariş veya mükerrer veri üretir.
- **çözüm:** butonları `isPending` durumunda daima devre dışı bırakın ve backend'de `idempotency-key` doğrulayın (20. anayasa kuralı):
  ```typescript
  const [state, formAction, isPending] = useActionState(updateProfile, null);
  return <button disabled={isPending}>{isPending ? 'Kaydediliyor...' : 'Kaydet'}</button>;
  ```
