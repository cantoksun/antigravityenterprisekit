---
name: performance-profiling
description: sistem performans analizi, profil çıkarma, darboğaz tespiti ve kaynak ölçüm ilkeleri.
priority: p0-performance
version: 2.0.0
---

# kurumsal bellek ve performans optimizasyonu standartları

bu beceri, sistemlerde bellek sızıntılarını engellemek, kaynak kullanımını en aza indirmek ve yüksek performanslı çalışma ortamı sağlamak için zorunlu standartları tanımlar.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 9 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir modül tamamlanır.
   - **sadelik ve trend teknolojiler:** yalın ve verimli modern araçlar.
   - **yalın veritabanı:** bayraksız, normalize veri mimarisi.
   - **katı api güvenliği & veri gizliliği:** sırlar ve uç noktalar korunur.
   - **idor/bola önleme:** nesne seviyesinde sahiplik doğrulaması.
   - **9. kural (öncelikli bellek ve performans):** ram ve cpu tüketimi optimize edilir, sızıntılar engellenir.
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki optimizasyon kriterleri.

---

## ⚡ 9. kural: bellek ve performans optimizasyon ilkeleri

### 1. bellek sızıntılarının (memory leak) önlenmesi
- **kaynak temizliği:** açılan dosya tanımlayıcıları (file descriptors), veritabanı bağlantı havuzları ve soketler işlem bitiminde kesinlikle kapatılmalı/serbest bırakılmalıdır.
- **olay dinleyicileri ve abonelikler:** ön yüzde `useEffect` / `addEventListener` yapılarında temizleme fonksiyonları (cleanup / `removeEventListener`) zorunludur.
- **global durum şişkinliği:** modül düzeyinde sınırsız büyüyen harita (`Map`) veya dizi (`Array`) yapıları yerine zayıf referanslar (`WeakMap`, `WeakSet`) veya lru tabanlı sınırlandırılmış önbellekler kullanılmalıdır.

### 2. hesaplama ve cpu verimliliği
- **algoritmik karmaşıklık:** $O(n^2)$ veya daha yüksek karmaşıklıktaki iç içe döngülerden kaçının; indeksleme, harita arama ($O(1)$) veya ikili arama ($O(\log n)$) kalıplarını uygulayın.
- **gereksiz yeniden render (re-render) engelleme:** react/web bileşenlerinde gereksiz renderları önlemek için durumları (state) yerelleştirin, pahalı hesaplamaları memoize edin.

### 3. akış (streaming) ve parça parça işleme (chunking)
- büyük dosyalar, veritabanı dökümleri veya veri dizileri asla tek seferde belleğe yüklenmemelidir (`fs.readFileSync` yerine `stream` / `pipeline`).
- sayfalama ve imleç (cursor-based pagination) kullanılarak ram şişmesi önlenmelidir.

### 4. akıllı önbellekleme (caching)
- sık okunan ve nadir değişen veriler için bellek içi (in-memory) lru cache veya redis kullanılmalı, ttl (yaşam süresi) zorunlu kılınmalıdır.
