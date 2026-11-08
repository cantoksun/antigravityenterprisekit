---
name: mobile-design
description: ios ve android uygulamaları için mobil öncelikli tasarım ve karar mekanizmaları. dokunma etkileşimi, performans kalıpları ve platform konvansiyonları.
priority: p1-visual
version: 2.0.0
---

# kurumsal mobil tasarım ve etkileşim standartları

bu beceri; ios, android, react native ve flutter platformlarında mobil öncelikli kullanıcı deneyimi, dokunma ergonomisi, çevrimdışı dayanıklılık ve yerel platform standartlarını yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 14 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir modül tamamlanır.
   - sadelik ve modern trend teknolojiler (react native / expo, flutter vb.).
   - yalın veri modelleme, katı api güvenliği, hassas veri koruması (secure store / keychain).
   - bellek sızıntısı analizi, paginasyon / lazy loading standartları ve owasp oturum denetimi.
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki mobil tasarım ilkeleri.

---

## 📱 kurumsal mobil tasarım ilkeleri

### 1. dokunma ergonomisi ve başparmak bölgesi (thumb zone)
- tüm tıklanabilir veya dokunulabilir bileşenlerin (butonlar, ikonlar, liste öğeleri) dokunma hedefi minimum **48x48dp (ios için 44x44pt)** olmalıdır.
- birincil eylemler (cta butonları, gezinme çubukları) ekranın alt kısmında, tek elle başparmağın rahatça erişebileceği alanda konumlandırılmalıdır.

### 2. platform konvansiyonlarına mutlak uyum
- **ios (human interface guidelines):**
  - alt gezinme çubuğu (tab bar), kaydırarak geri gitme (swipe-to-back) jesti, sf symbols ikonografisi, modal sunum kartları.
- **android (material design 3):**
  - gezinme çekmecesi (navigation drawer) veya alt bar, kayan eylem butonu (fab), ripple dokunma geri bildirimi, donanımsal/sistem geri butonu yönetimi.
- her iki platforma ait gezinme davranışları birbirine karıştırılmamalı, yerel hissiyat korunmalıdır.

### 3. çevrimdışı öncelikli mimari ve ağ toleransı (offline-first)
- zayıf ağlarda veya internet kesintilerinde uygulama donmamalı veya beyaz ekranda kalmamalıdır.
- yerel önbellekleme (sqlite, watermelondb, mmkv, hive) kullanılmalı; çevrimdışıyken yapılan işlemler bir kuyrukta toplanarak bağlantı kurulduğunda senkronize edilmelidir.

### 4. mobil hassas veri depolama (14. kural uyumu)
- mobilde `asyncstorage` veya `sharedpreferences` içinde asla şifre veya düz metin token tutulmaz.
- bunun yerine donanımsal güvenlik modülünü kullanan yerel şifreli depolama tercih edilmelidir:
  - ios: `keychain services`
  - android: `android keystore` / `encryptedsharedpreferences`
  - react native: `expo-secure-store` / `react-native-keychain`

### 5. akıcı performans (60 / 120 fps hedefi)
- liste yapılarında `scrollview` yerine sanallaştırılmış liste bileşenleri (`flatlist`, `flashlist`) kullanılmalıdır (13. kural).
- görsel boyutu ekrana göre optimize edilmeli, gereksiz yüksek çözünürlüklü görseller belleğe alınmamalıdır.
