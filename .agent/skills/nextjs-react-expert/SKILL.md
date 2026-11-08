---
name: nextjs-react-expert
description: react ve next.js performans optimizasyonu, sunucu bileşenleri, veri getirme mimarileri ve demet küçültme.
priority: p1-visual
version: 2.0.0
---

# modern react ve next.js kurumsal performans ve mimari standartları

bu beceri; react 19, next.js (app router), sunucu bileşenleri (rsc), sıfır şelale (zero-waterfall) veri getirme, bellek yönetimi ve güvenlik standartlarını yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 14 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir modül tamamlanır.
   - sadelik ve modern trend teknolojiler: react 19, next.js app router, server actions (4. kural).
   - katı api ve sunucu eylemi güvenliği (6. kural), idor önleme (8. kural).
   - bellek sızıntısı analizi (10. kural), paginasyon / lazy loading (13. kural) ve owasp oturum denetimi (14. kural).
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki react/next.js yönergeleri.

---

## ⚡ modern react ve next.js standartları

### 1. sunucu bileşenleri (rsc) ve istemci ayrımı
- varsayılan olarak tüm bileşenler sunucu bileşeni (`server component`) kalmalıdır.
- yalnızca kullanıcı etkileşimi (tıklama, form durumu, `useState`, `useEffect`) gerektiren yaprak (leaf) bileşenlerin başına `'use client'` direktifi eklenmelidir.
- bu yaklaşım istemciye giden javascript paket boyutunu (bundle size) minimumda tutar.

### 2. veri getirme şelalelerini engelleme (zero waterfall)
- sıralı `await` çağrıları yerine paralel veri getirme veya sunucu akışı (streaming) kullanılmalıdır:
  ```tsx
  // iyi: bağımsız verileri paralel getir
  const [userData, ordersData] = await Promise.all([
    getUser(userId),
    getUserOrders(userId)
  ]);
  ```
- yavaş yüklenen bileşenler `<Suspense fallback={<Skeleton />}>` içine alınarak sayfanın diğer kısımlarının hızlı render edilmesi sağlanmalıdır.

### 3. server actions güvenliği ve idor koruması (6., 8. ve 14. kural)
- sunucu eylemleri (server actions) kamusal bir post uç noktası gibi davranır; gizli kabul edilemez.
- her server action içinde oturum doğrulaması ve kaynak sahipliği mutlak surette yapılmalıdır:
  ```tsx
  'use server';

  import { auth } from '@/lib/auth'; // güvenli httponly oturum (14. kural)
  import { db } from '@/lib/db';

  export async function updatePost(postId: string, content: string) {
    const session = await auth();
    if (!session?.user) {
      throw new Error('yetkisiz erişim');
    }

    // 8. kural: kullanıcının sadece kendi gönderisini güncellemesine izin ver (idor koruması)
    const updated = await db.post.updateMany({
      where: { id: postId, authorId: session.user.id },
      data: { content }
    });

    if (updated.count === 0) {
      throw new Error('kayıt bulunamadı veya güncelleme yetkiniz yok');
    }
  }
  ```

### 4. istemci bellek sızıntılarını önleme (10. kural uyumu)
- `'use client'` bileşenlerinde `useEffect` içinde tanımlanan tüm abonelikler, event listener'lar ve sayaçlar temizleme (cleanup) fonksiyonu ile sonlandırılmalıdır:
  ```tsx
  useEffect(() => {
    const handleResize = () => setWidth(window.innerWidth);
    window.addEventListener('resize', handleResize);
    
    // temizleme zorunludur: bellek sızıntısını önler
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  ```

### 5. resim ve medya optimizasyonu (13. kural)
- standart `<img>` yerine her zaman `next/image` kullanılmalı; boyutlar (`width`, `height`), otomatik webp/avif dönüşümü ve tembel yükleme (`loading="lazy"`) sağlanmalıdır.
