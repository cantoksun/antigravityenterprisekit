---
name: bash-linux
description: bash ve linux terminal kalıpları. kritik komutlar, boru hatları (piping), hata yönetimi ve kabuk betikleri.
priority: p1-operations
version: 2.0.0
---

# kurumsal bash ve linux terminal kalıpları standartları

bu beceri; linux ortamlarında güvenli, hata toleranslı, girdi temizliği yapılmış ve sistem kaynaklarını tüketmeyen kabuk (shell) betikleri çalıştırmayı ve otomasyonları yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 16 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir betik/komut modülü tamamlanır.
   - sadelik ve modern trend teknolojiler: modern bash/sh araçları, boru hatları, hafif sistem araçları (4. kural).
   - hassas verilerin korunması: şifreler ve tokenlar betik içine sabit yazılmaz veya `set -x` ile loglarda açığa çıkarılmaz (7. kural).
   - bellek ve kaynak yönetimi: zombi süreçlerin ve arka planda kontrolsüz çalışan alt kabukların önlenmesi (9. ve 10. kural).
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki bash/linux kuralları.

---

## 🐚 kurumsal bash ve linux betik standartları

### 1. katı hata başlığı (strict mode)
tüm bash betikleri istisnasız aşağıdaki başlıkla başlamalıdır:
```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
```
- `-e`: herhangi bir komut başarısız olduğunda (çıkış kodu != 0) betiğin sessizce devam etmesini engeller, anında durdurur.
- `-u`: tanımlanmamış bir değişken kullanıldığında hata fırlatır (örneğin `rm -rf "$DIZIN/*"` komutunda `$DIZIN` boşsa tüm diskin silinmesini önler).
- `-o pipefail`: boru hattında (`cmd1 | cmd2 | cmd3`) ortadaki bir komut hata verirse tüm boru hattının hata koduyla sonlanmasını sağlar.

### 2. değişken tırnaklama ve komut enjeksiyonu koruması
- tüm değişkenler çift tırnak (`"$degisken"`) içinde kullanılmalıdır; aksi halde boşluk içeren dosya yolları bölünür veya enjeksiyona açık hale gelir.
- tehlikeli `eval` komutundan kesinlikle kaçınılmalıdır.

### 3. geçici dosya ve tuzak (trap) ile temizlik (10. kural uyumu)
- betik sonlandığında veya hata aldığında arkasında geçici dosya veya açık kaynak bırakmamalıdır:
  ```bash
  # güvenli geçici dizin
  GECICI_DIZIN="$(mktemp -d)"
  
  # çıkışta veya kesintide otomatik temizle
  trap 'rm -rf "$GECICI_DIZIN"' EXIT INT TERM
  ```

### 4. süreç yönetimi ve arka plan işleri (9. kural)
- döngüler içinde kontrolsüz arka plan işlemleri (`&`) başlatılarak sunucunun işlemci ve bellek limitleri aşılmamalıdır.
- paralel işler gerekiyorsa `xargs -P` veya `parallel` gibi sınırlandırılmış araçlar kullanılmalıdır.
