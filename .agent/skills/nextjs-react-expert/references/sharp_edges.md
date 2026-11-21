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

---

### 5. url parametresiyle açılışta useEffect içi kontrolsüz mutasyon ve mükerrer kayıt tuzağı
- **tuzak:** `?userId=usr_123` gibi bir url parametresiyle sayfaya girildiğinde, `useEffect` içinde kontrolsüz şekilde `startConversation(userId)` gibi bir mutasyon çağırmak. konuşma listesi henüz yüklenirken veya liste durumu güncellenip referansı değiştiğinde effect tekrar tetiklenir ve veritabanında aynı iki kullanıcı arasında mükerrer kopya kayıtlar oluşturur.
- **çözüm (çift katmanlı koruma):**
  1. **ön yüz (ref guard & loading check):** liste henüz yüklenirken mutasyon tetiklenmez, aynı parametre için tek seferlik `useRef` kilidi (`initiatedUserRef.current`) ve mevcut kayıt kontrolü uygulanır:
     ```typescript
     const initiatedUserRef = useRef<string | null>(null);

     useEffect(() => {
       if (!targetUserId || isLoadingConversations) return;
       // mevcut konuşma varsa seç, yeniden oluşturma
       const existing = conversations.find(c => c.participantId === targetUserId);
       if (existing) {
         setSelectedChatId(existing.id);
         return;
       }
       // mükerrer tetiklemeyi ref kilidiyle engelle
       if (initiatedUserRef.current === targetUserId) return;
       initiatedUserRef.current = targetUserId;
       startConversation(targetUserId);
     }, [targetUserId, isLoadingConversations, conversations]);
     ```
  2. **arka yüz ve veritabanı (20. ve 33. anayasa kuralı):** backend uç noktası daima `getOrCreateConversation` (upsert / on conflict do nothing) mantığıyla çalışmalıdır. veritabanında `@@unique([user_a_id, user_b_id])` kısıtlaması bulunmalı, ön yüz kaç kez paralel istek atarsa atsın veritabanı asla ikinci bir kopya üretmemeli, mevcut kaydı dönmelidir.
