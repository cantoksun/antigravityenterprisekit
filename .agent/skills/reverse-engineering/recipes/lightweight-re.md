# ⚡ hafif ve token tasarruflu tersine mühendislik (lean-re)

bu kılavuz, `rea-lab` ve `leanrea` araştırmalarında kanıtlanan temel prensibe dayanır: **devasa decompiler ve mcp araçları çalıştırmadan önce, sistem kaynaklarını ve model tokenlarını korumak için hafif cli araçlarıyla keşif yapılmalıdır.**

---

## 🎯 4 kademeli keşif piramidi

```
     ▲
    / \     kademe 4: derin decompile (ghidra / ida pro / jadx) - en son çare
   /   \    kademe 3: sembol ve disassembly (objdump, ilspy, apktool)
  /     \   kademe 2: ağ ve paket izleme (mitmproxy, devtools, tcpdump)
 /       \  kademe 1: hafif metin ve ikili dosya taraması (strings, file, grep) - ilk adım
 ----------
```

---

## 🛠️ kademe 1: hafif araçlarla keşif (sıfır maliyet, yüksek verim)

### 1. `strings` ile gizli ipuçları arama
ikili dosyadaki tüm okunabilir metinleri hızla listeleyin:
```bash
# api uç noktaları, url'ler ve host isimleri
strings target_binary | grep -E "https?://"

# ortam değişkenleri ve yapılandırma anahtarları
strings target_binary | grep -E "(API_KEY|SECRET|TOKEN|AUTH|CONFIG)"

# hata ve log mesajları (iş akışını anlamak için en değerli ipucu)
strings target_binary | grep -iE "(error|failed|invalid|success|auth)"
```

### 2. sembol tablosu ve dışa aktarılan fonksiyonlar (`nm` / `dumpbin`)
```bash
# linux / macos
nm -D target_binary | grep -E " T " # kod bölümündeki fonksiyonlar

# windows (powershell / visual studio tools)
dumpbin /EXPORTS target.dll
```

### 3. başlık ve dosya türü tespiti (`file`)
```bash
file target_file
```

---

## ⚖️ ne zaman ağır araçlara (ghidra / ida) geçilmeli?

1. kademe 1 araçları ile fonksiyon imzası ve akış çözülemediğinde.
2. karmaşık matematiksel algoritmalar, şifreleme rutinleri veya özel sıkıştırma formatları olduğunda.
3. baytkod / asm seviyesinde register durumlarının takibi zorunlu hale geldiğinde.

> **kural:** önce hafif araçlarla keşif yap → yalnızca hedeflenen spesifik fonksiyon için ağır analiz aracını devreye sok. asla tüm ikili dosyayı tek seferde modele veya ghidra'ya yükleme.
