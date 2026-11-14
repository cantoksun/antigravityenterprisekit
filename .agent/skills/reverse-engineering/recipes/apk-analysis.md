# ⚡ android apk ve mobil tersine mühendislik kılavuzu

bu kılavuz; android apk paketlerinin, manifest dosyalarının, api uç noktalarının ve veri modellerinin tersine mühendislikle delillendirilerek çözümlenmesini yönetir.

---

## 🛠️ araç seti ve hazırlık
- **`jadx` / `jadx-gui`:** dex baytkodunu okunabilir java / kotlin kaynak koduna dönüştürmek için birincil araçtır.
- **`apktool`:** kaynakları (`res/`), xml dosyalarını ve `AndroidManifest.xml` dosyasını ham formatta açmak için kullanılır.

---

## 🔍 adım adım inceleme stratejisi

### 1. `AndroidManifest.xml` analizi
apk'nın izinlerini, açık dış bileşenlerini (exported activities, receivers) ve başlangıç noktalarını inceleyin:
```bash
apktool d app.apk -o ./unpacked_apk
```
- kritik izinler: internet, harici depolama, bildirim erişimleri.
- `android:exported="true"` olan bileşenler (güvenlik zafiyetleri ve harici tetikleyiciler için ana hedeftir).

### 2. `jadx` ile api uç noktalarını ve veri modellerini çıkarma
```bash
# komut satırından kaynak kodları çıkarın
jadx -d ./decompiled_src app.apk
```
- **http / api istemcileri:** `retrofit`, `okhttp` veya `httpclient` sınıflarını arayın:
```bash
grep -rn "@GET" ./decompiled_src
grep -rn "@POST" ./decompiled_src
grep -rn "baseUrl" ./decompiled_src
```
- **veri modelleri:** json serileştirme modellerini (`@SerializedName`, `@JsonProperty`) tespit ederek sistemin veri şemasını çıkarın.

### 3. şifreleme ve token depolama analizi
- `SharedPreferences` veya `EncryptedSharedPreferences` kullanımlarını arayın.
- sabit anahtarların (hardcoded keys) olup olmadığını denetleyin.

---

## 📋 temiz oda şartnamesi
tespit edilen api uç noktaları ve veri şemaları için standart bir openapi / swagger veya typescript tipleri oluşturun; orijinal uygulamadaki java sınıflarını kopyalamadan yeniden üretin.
