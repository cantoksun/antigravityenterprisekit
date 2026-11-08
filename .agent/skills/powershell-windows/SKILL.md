---
name: powershell-windows
description: powershell windows terminal kalıpları. kritik püf noktaları, işleç sözdizimi ve hata yönetimi.
priority: p1-operations
version: 2.0.0
---

# kurumsal powershell ve windows terminal kalıpları standartları

bu beceri; windows sistemlerinde ve cross-platform powershell (pwsh) ortamlarında güvenli, nesne tabanlı, hata kontrollü ve kaynak dostu betikler çalıştırmayı ve sistem otomasyonunu yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 16 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir betik/komut modülü tamamlanır.
   - sadelik ve modern trend teknolojiler: powershell core (pwsh 7+), modern cmdlet'ler (4. kural).
   - hassas verilerin korunması: şifreler asla düz metin string olarak tutulmaz, `SecureString` / `PSCredential` veya ortam değişkenleri kullanılır (7. kural).
   - bellek ve süreç yönetimi: açık kalan .net nesneleri ve runspace havuzları temizlenir (9. ve 10. kural).
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki powershell yönergeleri.

---

## 🪟 kurumsal powershell betik standartları

### 1. katı hata tercihi ($ErrorActionPreference = 'Stop')
powershell varsayılan olarak kritik olmayan hatalarda çalışmaya devam eder. kurumsal betiklerde sessiz hataları önlemek için hata aksiyonu kesinlikle durdurma moduna alınmalıdır:
```powershell
# betik başına zorunlu tanımlama
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
```

### 2. nesne odaklı boru hattı (pipeline) disiplini
- metin ayrıştırma (`grep`, `awk`, `regex`) yerine powershell'in güçlü nesne yapısı kullanılmalıdır:
  ```powershell
  # yanlış (metin parçalama):
  Get-Process | Out-String | Select-String "node"

  # doğru ve kurumsal (nesne filtreleme):
  Get-Process -Name "node" -ErrorAction SilentlyContinue |
      Where-Object { $_.WorkingSet64 -gt 500MB } |
      Select-Object -Property Id, ProcessName, WorkingSet64
  ```

### 3. hassas veri ve şifre yönetimi (7. kural uyumu)
- parolalar asla kod içine düz metin olarak yazılmaz.
- ortam değişkenlerinden veya güvenli string nesnelerinden okunur:
  ```powershell
  # ortamdan güvenli parola okuma
  $apiKey = $env:API_KEY
  if ([string]::IsNullOrWhiteSpace($apiKey)) {
      throw "api anahtarı ortam değişkeninde tanımlanmamış."
  }
  ```

### 4. kaynak temizliği ve dispose kalıbı (10. kural uyumu)
- dosya akışları, ağ bağlantıları veya .net com nesneleri işlem bittiğinde `try / finally` içinde serbest bırakılmalıdır:
  ```powershell
  $stream = [System.IO.File]::OpenRead($dosyaYolu)
  try {
      # dosya işleme mantığı
  }
  finally {
      $stream.Dispose() # 10. kural: bellek sızıntısını önle
  }
  ```
