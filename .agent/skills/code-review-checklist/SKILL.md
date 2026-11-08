---
name: code-review-checklist
description: kod kalitesi, güvenlik, performans ve kurumsal en iyi uygulamaları kapsayan kapsamlı kod inceleme kılavuzu.
priority: p0-quality
version: 2.0.0
---

# kurumsal kod inceleme ve bellek sızıntısı denetim standartları

bu beceri, kod değişikliklerinde kalite, mimari uyum, güvenlik ve özellikle bellek sızıntısı risklerini analiz edip raporlamayı yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 10 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir modül tamamlanır.
   - sadelik, modern trend teknolojiler ve yalın veritabanı kuralları.
   - api güvenliği, hassas veri koruması ve idor/bola önleme.
   - öncelikli bellek ve performans optimizasyonu.
   - **10. kural (bellek sızıntısı analizi ve bildirimi):** bellek sızıntısına yol açabilecek riskli yapılar proaktif olarak taranır ve kullanıcıya raporlanır.
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki inceleme standartları.

---

## 🧠 10. kural: bellek sızıntısı (memory leak) analiz protokolü

yazılan veya gözden geçirilen her kod parçasında aşağıdaki 5 potansiyel sızıntı kaynağı taranır ve tespit edilen durumlar kullanıcıya bildirilir:

### 1. olay dinleyicileri (event listeners) ve abonelikler
- `addEventListener`, websocket veya eventemitter dinleyicisi eklenip yaşam döngüsü sonunda (örneğin bileşen unmount olduğunda) kaldırılmamış mı?
- **bildirim örneği:** `"uyarı: pencere dinleyicisi için removeeventlistener temizleme fonksiyonu bulunmuyor, bellek sızıntısı riski tespit edildi."`

### 2. sayaçlar ve zamanlayıcılar (timers)
- `setInterval` veya `setTimeout` çağrıları başlatılıp bir değişkene bağlanarak (`clearInterval` / `clearTimeout`) temizleniyor mu?
- temizlenmeyen sayaçlar arka planda sonsuza kadar referans tutarak bellek tüketir.

### 3. kontrolsüz büyüyen global koleksiyonlar
- sunucu veya istemci seviyesinde global bir `Map`, `Set` veya dizi içine sürekli yeni eleman eklenip hiç silinmiyor mu?
- önbellekler için sınır (lru) veya zayıf referans (`WeakMap`) kullanılmalıdır.

### 4. kapatılmamış kaynaklar ve veri akışları (streams & sockets)
- dosya okuma/yazma akışları, veritabanı bağlantı havuzları veya soketler hata (`catch` / `finally`) bloklarında güvenle kapatılıyor mu?

### 5. kapamalar (closures) ve referans zincirleri
- iç içe fonksiyonlarda büyük veri nesnelerinin gereksiz yere kapsamda (scope) tutulup çöp toplayıcıdan (garbage collection) kaçırılması riski.

---

## 📋 kullanıcı bildirim formatı (zorunlu şablon)

kodda bir sızıntı şüphesi tespit edildiğinde kullanıcıya şu formatta bildirim yapılır:

```markdown
⚠️ **bellek sızıntısı analizi ve uyarısı (10. kural):**
- **tespit edilen yer:** `[dosya_adı]:[satır_no]`
- **risk türü:** [kapatılmamış dinleyici / temizlenmemiş sayaç / kontrolsüz önbellek]
- **neden sızıntı yapar:** [çöp toplayıcının nesneyi temizleyememe gerekçesi]
- **uygulanan / önerilen çözüm:** [temizleme kodu veya lru çözümü]
```
