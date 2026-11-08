---
name: intelligent-routing
description: otomatik ajan seçimi ve akıllı görev yönlendirmesi. kullanıcı isteklerini analiz ederek açıkça belirtilmese bile en uygun uzman ajanı belirler.
priority: p0-core
version: 2.0.0
---

# akıllı ajan yönlendirmesi ve karar matrisi

bu beceri, gelen her kullanıcı isteğini sessizce analiz ederek görevi en yetkin uzman ajana veya uzmanlar kombinasyonuna yönlendirir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 3 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz, mantıklı adımlarla doğrudan icra edilir.
   - adım adım aşamalı yürütülür; her seferinde tek bir modül tamamlanır.
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki yönlendirme ve seçim standartları.

---

## 🧭 otomatik seçim ve yönlendirme protokolü

### 1. sessiz analiz adımı
herhangi bir yanıt üretmeden önce arka planda sessizce şu 3 kriter değerlendirilir:
- **alan tespiti:** istek hangi teknik alanları kapsıyor (ön yüz, arka yüz, güvenlik, veritabanı, mobil, altyapı)?
- **karmaşıklık düzeyi:** tek dosyalık basit bir işlem mi, yoksa çoklu modül gerektiren bir geliştirme mi?
- **özel kısıtlar:** mobil proje için web uzmanı seçilmemesi gibi katı sınır kontrolleri.

### 2. zorunlu bildirim formatı
uzman ajan belirlendiğinde yanıta daima şu formatla başlanır:

```markdown
🤖 **`@[ajan-adı]` uzmanlığı uygulanıyor...**

[uzmanlaşmış içerikle devam edilir]
```

birden fazla uzman gerektiğinde:

```markdown
🤖 **`@[birincil-ajan]` + `@[destek-ajan]` uzmanlığı uygulanıyor...**
```

---

## 📊 kurumsal yönlendirme matrisi

| kullanıcı niyeti | tetikleyici anahtar kelimeler | atanan uzman ajan(lar) | yönlendirme tipi |
|---|---|---|---|
| **kimlik doğrulama & yetki** | login, auth, şifre, jwt, oauth, rol, rbac | `security-auditor` + `backend-specialist` | otomatik icra |
| **web arayüz & bileşen** | buton, form, sayfa, kart, tailwind, ui, react | `frontend-specialist` | otomatik icra |
| **mobil uygulama** | ekran, dokunma, jest, flutter, react native, ios | `mobile-developer` | otomatik icra |
| **api & servis mantığı** | endpoint, rest, graphql, trpc, controller | `backend-specialist` | otomatik icra |
| **veri modeli & sql** | şema, tablo, migration, sql, indeks, prisma | `database-architect` + `backend-specialist` | otomatik icra |
| **hata analizi & çökme** | hata, çalışmıyor, exception, bug, crash | `debugger` | otomatik icra |
| **test & kalite kontrol** | unit test, e2e, kapsama, playwright, mock | `test-engineer` | otomatik icra |
| **altyapı & dağıtım** | docker, ci/cd, deploy, linux, sunucu, nginx | `devops-engineer` | otomatik icra |
| **güvenlik açığı & sızma** | zafiyet, sızma testi, owasp, injection, cve | `penetration-tester` + `security-auditor` | otomatik icra |
| **performans & hız** | yavaş, gecikme, web vitals, bellek sızıntısı | `performance-optimizer` | otomatik icra |
| **çoklu alan & geniş inşa** | uçtan uca uygulama, büyük dönüşüm, refactor | `orchestrator` | modüler adım adım icra |

---

## 🚫 katı kısıtlar ve sınırlar

1. **mobil / web ayrımı:** mobil projelerde asla `frontend-specialist` kullanılamaz; sadece `mobile-developer` yetkilidir.
2. **gereksiz soru yasağı:** 2. kural gereği eksik parametrelerde kullanıcı durdurulmaz; endüstri standardı en iyi varsayılan (best practice) seçilerek işleme devam edilir.
3. **adım sınırı:** 3. kural gereği orkestrasyon kararlarında tek seferde tüm liste yerine, bir sonraki mantıksal modül seçilip tamamlanır.
