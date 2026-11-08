---
description: yapay zeka destekli tasarım zekası, modern tasarım sistemleri, renk harmonisi, responsive ux ve tipografi yönergeleri prosedürü.
---

# 🎨 ui-ux-pro-max: modern tasarım ve responsive ux iş akışı

bu iş akışı web ve mobil arayüzlerin tasarlanmasında, stil, renk paleti ve tipografi seçiminde kurumsal kaliteyi sağlar.

## 🎯 temel tasarım kuralları ve ilkeleri (15. ve 16. kural)

1. **tam responsive ve cihaz ayrımı (15. kural)**:
   - mobilde başparmak ergonomisine uygun alt çekmeceler (drawer / bottom sheet) ve dokunmatik jestler.
   - masaüstünde geniş ekranı etkin kullanan dialog/modal yapıları.
   - asla yatay kayma (horizontal scroll) olmamalıdır (`overflow-x: hidden`).
2. **tipografi ve font disiplini (16. kural)**:
   - toplam font ailesi sayısı 2-3 ile sınırlandırılmalıdır; rastgele yeni fontlar yüklenemez.
3. **renk dengesi ve 3 ton kuralı**:
   - arayüzde standart olarak %60 arka plan / nötr, %30 yapısal / kart, %10 vurgu rengi kullanılır.
   - kullanıcının betimlemesine uygun pastel tonlar veya uyumlu kontrastlar tercih edilir.
4. **buton ve pencere sadeliği**:
   - dışarı dokunarak kapanan mobil çekmece ve modallarda gereksiz `x` kapatma butonu bulundurulmaz.

---

## 🛠️ tasarım sistemi oluşturma ve arama komutları

tasarım sistemi önerilerini aramak ve üretmek için:

```powershell
# tasarım sistemi ve renk paleti önerisi üretme
$env:PYTHONIOENCODING="utf-8"; python .agent/.shared/ui-ux-pro-max/scripts/search.py "<ürün_türü> <sektör> <anahtar_kelimeler>" --design-system -p "ProjeAdı"

# master tasarım sistemi belgesini kaydetme
$env:PYTHONIOENCODING="utf-8"; python .agent/.shared/ui-ux-pro-max/scripts/search.py "<sorgu>" --design-system --persist -p "ProjeAdı"
```

bu komut şu standartları üretir:
- `design-system/master.md`: global stil, renk ve tipografi kuralları.
- `design-system/pages/`: sayfaya özel geçersiz kılma (override) kuralları.

---

## 🚨 katı kurallar

- tüm açıklamalar ve raporlar istisnasız küçük harflerle ve türkçe karakterler (ç, ğ, ı, ö, ş, ü) eksiksiz kullanılarak yazılmalıdır.
- kullanıcıya gereksiz sorular sormadan doğrudan analiz ve modüler icra (2. kural) uygulanmalıdır.
