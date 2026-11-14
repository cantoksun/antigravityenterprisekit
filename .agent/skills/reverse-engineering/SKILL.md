---
name: reverse-engineering
description: kurumsal tersine mühendislik, ikili dosya ve paket analizi, kanıt tabanlı decompile ve temiz oda (clean-room) yeniden üretim ilkeleri.
version: 1.0.0
when_to_use: "kurumsal tersine mühendislik, ikili dosya ve paket analizi, kanıt tabanlı decompile ve temiz oda (clean-room) yeniden üretim ilkeleri."
allowed-tools: [Read, Grep, Glob, Bash, Write, Edit]
---

# 🔬 tersine mühendislik ve kanıt tabanlı analiz becerisi

bu beceri; kaynak kodu bulunmayan veya eksik belgelenmiş sistemlerin, api'lerin, ikili dosyaların (binary), masaüstü paketlerinin (electron, .net), mobil uygulamaların (apk) ve harici ağ protokollerinin delile dayalı olarak çözümlenmesi ve kurumsal standartlarda yeniden inşa edilmesini (clean-room rewrite) yönetir.

---

## 🎯 temel prensipler

1. **delil önceliği (evidence-first):**
   - sistem hakkında asla tahminde bulunulamaz.
   - her tespit somut bir kanıta (çağrı dökümü, bellek izi, ayrıştırılmış baytkod, ağ trafiği veya api yanıtı) dayanmalıdır.
   - bir işlevin ne yaptığı iddia ediliyorsa, bunu kanıtlayan girdi/çıktı testi veya decompile satırı rapora eklenmelidir.

2. **temiz oda disiplini ve hava boşluğu (two-agent clean-room airgap):**
   - tersine mühendislikle elde edilen tescilli veya telifli kaynak kodlar asla doğrudan projeye yapıştırılamaz.
   - analiz eden ajan (`code-archaeologist`) yalnızca soyut bir `SPEC.md` üretir; yeni kodu yazan ajan (`backend-specialist` / `frontend-specialist`) orijinal ikiliyi hiç görmeden yalnızca bu spesifikasyona bakarak temiz kodu sıfırdan yazar (bkz: `recipes/clean-room-airgap.md`).

3. **yasal ve güvenlik sınırları:**
   - lisans ihlali, telifli varlıkların (görsel, ses, tescilli şifreler) yetkisiz kopyalanması kesinlikle engellenir.
   - oyun ve retro rekonstrüksiyonlarda "bring-your-own-assets (byoa)" kuralı uygulanır; grafik/ses varlıkları depoya konulamaz.
   - yalnızca birlikte çalışabilirlik (interoperability), güvenlik araştırması, arşivleme veya modernizasyon amacıyla analiz yapılır.

4. **güvenli ve izole analiz disiplini (untrusted binary isolation):**
   - analiz edilen üçüncü parti ikili dosyaların (binary), crackme'lerin veya derlenmiş paketlerin zararlı yazılım (malware) veya ajanı ele geçirme tehdidi (agent compromise) taşıyabileceği varsayılır.
   - incelemeler mümkün olduğunca ağ bağlantısız, salt-okunur (read-only) kök dizinli ve izole sanal alanlarda (container/sandbox) icra edilir; asla ana çalışma ortamındaki sırlar (secrets/env) hedef ikili dosyaya açılmaz.

---

## 🛠️ hedef sistem analiz yöntemleri

### 1. electron ve javascript paketleri
- **araçlar:** `asar` extractor, js beautifiers, source-map unpacker.
- **yaklaşım:** 
  - `app.asar` arşivini açarak ana süreç (`main process`) ve render süreçleri (`preload`, `renderer`) arasındaki ipc (`ipcRenderer`, `ipcMain`) köprülerini haritalandırın.
  - clipboard köprüleri, yerel sistem çağrıları ve saklanan yerel durumları analiz edin.

### 2. .net ve c# derlemeleri
- **araçlar:** `ilspy`, `dnspy`, `de4dot`.
- **yaklaşım:** cil (common intermediate language) baytkodundan c# sözdizimine dönüştürün, veri modellerini ve iş akışı algoritmalarını tespit edin.

### 3. android (apk / dex)
- **araçlar:** `jadx`, `apktool`.
- **yaklaşım:** manifest izinleri, http servis uçları, sqlite şemaları ve şifreleme/token saklama mekanizmalarını çözümleyin.

### 4. yerel ikili dosyalar (native binaries - c/c++/rust/go)
- **araçlar:** `ghidra`, `ida pro`, `hopper`, `objdump`, `strings`.
- **yaklaşım:** dışa aktarılan fonksiyon sembolleri (exported symbols), string tabloları ve sistem çağrıları (syscall) üzerinden algoritma mantığını çıkarın.

### 5. ağ ve api tersine mühendisliği
- **araçlar:** mitmproxy, browser devtools ağ sekmesi, curl dökümleri.

### 6. donanım ve tescilli protokol analizi
- **araçlar:** wireshark, usbpcap, bettercap, hidraw, pyserial.
- **yaklaşım:** ham paket yakalama, sihirli bayt (magic byte) tespiti, kontrol toplamı (checksum/crc) formülü çıkarma ve python referans protokol sınıfı oluşturma (bkz: `recipes/protocol-and-hardware.md`).

### 7. mcp decompiler ve harici analiz orkestrasyonu
- **araçlar:** ghidra analyzeheadless, ida-mcp, craft-anything, radare2.
- **yaklaşım:** harici decompiler araçlarını mcp veya headless cli ile bağlayarak kontrol akışı ve fonksiyon grafiğini otomatik çıkarma; çıktıları temiz oda spesifikasyonuna dönüştürme (bkz: `recipes/mcp-decompiler-bridges.md`).
- **yaklaşım:** istek/yanıt başlıkları, gizli parametreler, imzalama (hmac) algoritmaları ve oturum yönetimini belgeleyin.

## 📚 özel platform analiz reçeteleri (recipes)

hedef platforma göre optimize edilmiş kılavuzlar:
- [hafif & token tasarruflu analiz (lean-re)](recipes/lightweight-re.md)
- [electron ve asar paket analizi](recipes/electron-unbundling.md)
- [android apk ve dex çözümleme](recipes/apk-analysis.md)
- [.net ve mono cil analizi](recipes/dotnet-decompilation.md)
- [davranışsal eşdeğerlik ve parity test kalıbı](recipes/parity-testing.md)

---

## 📋 standart tersine mühendislik analiz raporu formatı

tersine mühendislik faaliyeti tamamlandığında şu formatta bir rapor üretilir:

```markdown
# 🔬 tersine mühendislik analiz raporu: [hedef-adı]

## 1. hedef sistem özeti
- **tür:** [electron / .net / apk / native binary / api]
- **kullanılan analiz aracı:** [ghidra / jadx / asar / mitm / ...]
- **lisans durumu:** [mit / apache / tescilli / lisanssız]

## 2. kanıtlanmış bulgular (evidence)
- **fonksiyon / uç nokta:** `ornek_fonksiyon(girdi: string) -> boolean`
- **somut delil:** [decompile satırı / ağ isteği ekran görüntüsü / baytkod offseti]
- **çalışma mantığı:** [tam olarak nasıl çalıştığının kanıtlanmış izahı]

## 3. temiz oda (clean-room) spesifikasyonu
- **arayüz (interface):**
  ```typescript
  interface ornekfonksiyon {
    islem(param: string): Promise<Result>;
  }
  ```
- **beklenen davranış ve sınır durumlar (edge cases):**
  - geçersiz girdide `InvalidInputError` fırlatır.
  - ağ kesintisinde varsayılan yerel önbellekten döner.

## 4. yeniden üretim ve modernizasyon önerisi
- [modern dilde (örn. rust / typescript) nasıl sıfırdan yazılacağı]
```
