# mcp decompiler ve harici analiz araçları entegrasyonu (mcp decompiler bridges)

bu tarif; ghidra, ida pro/free, radare2/iaito ve craft-anything gibi endüstri standardı statik analiz ve tersine mühendislik araçlarının antigravity ajanları tarafından mcp (model context protocol) veya headless cli üzerinden nasıl orkestre edileceğini tanımlar.

---

## 🎯 temel felsefe ve orkestrasyon modeli
- **araç bağımsızlığı:** ajan tek bir tescilli araca bağımlı kalmaz; açık kaynaklı ve yerel headless araçları (`ghidra analyzeHeadless`, `radare2`, `craft-anything`) önceliklendirir.
- **salt okunur analiz:** mcp sunucuları veya cli araçları ikili dosyayı salt okunur modda inceler; kaynak ortamına asla izinsiz ikili yazma yapmaz.

---

## 🛠️ mcp tersine mühendislik araç ekosistemi

| araç / mcp köprüsü | çalışma şekli | kullanım alanı |
|---|---|---|
| **ghidra headless (`GhidraMCP` / CLI)** | `analyzeHeadless <project_dir> <project_name> -import <binary>` | c/c++ ve yerel ikililerde fonksiyon grafiği, decompile c çıktısı çıkarma |
| **ida mcp (`HexRaysSA/ida-mcp` / `ida-free-mcp`)** | mcp json-rpc soket köprüsü | x86/arm ikililerde etkileşimli kontrol akışı ve xref (çapraz referans) analizi |
| **craft-anything (rust engine)** | cli + mcp: `study`, `check`, `ready` adımları | electron, .net, java, android ve gömülü firmware otomatik incelemesi |
| **radare2 / r2pipe** | `r2 -q -c "aaa; afl; pdf @sym.main" <binary>` | hızlı terminal tabanlı disasm, sembol arama ve string analizi |

---

## 🔬 headless ghidra cli orkestrasyon prosedürü

harici bir mcp sunucusu kurulu olmadığında veya yerel headless analiz gerektiğinde `code-archaeologist` ajanı doğrudan headless ghidra betiğini çalıştırır:

```bash
# 1. ghidra projesi oluştur ve ikiliyi içe aktar
analyzeHeadless /tmp/ghidra_proj temp_project -import ./target_binary -postScript DecompileToJson.py output_functions.json

# 2. üretilen yapısal json analizini oku
cat output_functions.json
```

---

## ⚙️ `mcp_config.json` köprü konfigürasyon şablonu

sisteme bir tersine mühendislik mcp aracı bağlanmak istendiğinde kullanılacak standart konfigürasyon:

```json
{
  "mcpServers": {
    "ghidra": {
      "command": "python",
      "args": ["-m", "ghidra_mcp_bridge", "--headless-path", "/opt/ghidra/support/analyzeHeadless"]
    },
    "craft-anything": {
      "command": "craft-anything",
      "args": ["mcp", "--mode", "clean-room"]
    }
  }
}
```

---

## 📋 mcp sonuçlarını değerlendirme kuralları (43. kural)
1. **decompile çıktısı kanıttır, nihai kod değildir:** mcp aracından dönen c/pseudocode çıktısı tescilli bir yapıdır. doğrudan koda aktarılamaz.
2. **yalnızca davranış ve veri yapıları çıkarılır:** fonksiyonun ne parametre aldığı, ne döndürdüğü ve içindeki matematiksel mantık özetlenerek `SPEC.md` belgesine işlenir.
3. **geçici proje dosyalarının temizlenmesi (45. kural):** ghidra veya r2 tarafından `/tmp` veya çalışma alanında açılan `.gpr`, `.rep` veya dump klasörleri analiz biter bitmez otonom olarak silinir.
