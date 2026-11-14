# ⚡ .net ve mono derlemeleri tersine mühendislik kılavuzu

bu kılavuz; c# ve .net derlemelerinin (`.dll`, `.exe`), cil (common intermediate language) baytkodunun çözümlenmesi ve iş mantığının haritalandırılmasını yönetir.

---

## 🛠️ araç seti
- **`ilspy` / `ilspycmd`:** açık kaynaklı komut satırı ve arayüz tabanlı .net decompiler.
- **`dnspy`:** .net hata ayıklama (debugging) ve baytkod düzenleme aracı.

---

## 🔍 analiz adımları

### 1. komut satırından kaynak kod çıkarma (`ilspycmd`)
```bash
# ilspycmd kurulu ise tüm projeyi c# dosyalarına dönüştürün
ilspycmd -p -o ./decompiled_dotnet target.dll
```

### 2. hedef algoritmaları ve veri sınıflarını izleme
- `Program.cs` veya `Startup.cs` üzerinden bağımlılık enjeksiyonu (`AddSingleton`, `AddTransient`) yapılarını bulun.
- orm ve veri erişim katmanlarını (`DbContext`, `Dapper` sorguları) tespit ederek veritabanı şemasını soyutlayın.

### 3. temiz oda şartnamesi (clean-room)
- c# sınıflarını doğrudan kopyalamak yerine, veri sözleşmelerini (data contracts) json schema veya typescript interface olarak tanımlayın.
- iş akışı algoritmalarını yalın test senaryoları haline getirip yeniden inşa edin.
