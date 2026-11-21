# 🖤 dünya standartlarında monokrom siber kokpit ux revizyon planı (ux-overhaul.md)

> bu plan; kullanıcının "berbat" olarak nitelendirdiği mevcut arayüzdeki tipografi sıkışıklığını, çiğ ham markdown görünümünü, boşluk hissi eksikliğini ve karmaşık hud elementlerini kaldırıp; linear.app, v0.dev ve raycast kalitesinde, katı iki renk kuralına (saf siyah & koyu gri) sadık kalarak dünya standartlarında bir kullanıcı deneyimi (ux) inşa etmeyi hedefler.

---

## 1. 🔍 mevcut ux problemlerinin dürüst teşhisi

1. **ham markdown kirliliği (raw markdown dumping):** sağ panelde önizleme yerine çiğ `--- frontmatter ---` ve ham `# markdown` kodları düz metin kutusunda gösteriliyor; bu amatör ve okunaksız hissettiriyor.
2. **çiğ emoji yığılması:** düğümlerin içine konulan `🧬, ⚖️, 🧠, 📖` emojileri monokrom ciddiyeti bozuyor ve pikselli/çiğ duruyor; profesyonel siber arayüzlerde emoji yerine vektörel geometrik glifler veya minimal harf kısaltmaları (`C`, `D`, `P`, `E`, `M`) kullanılır.
3. **hud ve buton dağınıklığı:** ekranın dört bir köşesine serpiştirilmiş legend, radar ve butonlar vizör alanını boğuyor; hiyerarşi yok.
4. **arama deneyimi kopukluğu:** arama açılır kutusu arama çubuğunun altında bağımsız yüzen kutu gibi duruyor; raycast / spotlight benzeri akıcı bir klavye odaklı komut paleti (command palette) gibi hissettirmiyor.
5. **statik ve donuk etkileşim:** düğümlere fare geldiğinde (hover) kartlar, bağlantılı hatlar ve komşu düğümler organik olarak parlamıyor veya öne çıkmıyor.

---

## 2. 💎 hedeflenen kurumsal siber ux (linear & raycast kalitesi)

- **saf monokrom tipografi & hiyerarşi:** `Inter / Segoe UI` ile keskin, ferah, yüksek okunabilirlikli başlıklar ve etiketler.
- **zengin ve temiz doküman okuyucu:** frontmatter çiğ olarak gösterilmeyecek; şık meta veri etiketlerine dönüştürülecek, başlıklar temiz h1/h2 olarak hiyerarşik render edilecek.
- **odaklı komşu vurgusu (focus neighbor highlight):** bir düğümün üzerine gelindiğinde diğer tüm ilgisiz düğümler kararacak (%20 opaklık), sadece o düğüm ve doğrudan bağlı olduğu düğümler parlak beyaz/açık gri konturla öne çıkacak.
- **klavye navigasyonu ve akıcı kontroller:** `ESC` ile paneli kapatma, `Cmd/Ctrl + K` veya `/` ile aramaya odaklanma, `Space` ile merkeze dönme.
- **derli toplu hud & şık kontroller:** tek bir alt kontrol çubuğu veya zarif kayan ada (floating dock).

---

## 3. 📋 aşamalı icra planı

> **kural 2 & kural 3 gereğince:** her aşama bağımsız olarak tamamlanacak, test edilecek ve onayınıza sunulacaktır.

### 🔹 modül 1: görsel grafik motoru ve odak etkileşimi revizyonu (`app.js`)
- çiğ emojiler yerine zarif minimal monokrom glifler/tip kısaltmaları.
- dinamik komşu odaklama (hover olan düğümün komşularını parlatıp diğerlerini karartma).
- ipeksi yumuşak kamera süzülmesi (smooth camera transitions).

### 🔹 modül 2: sağ teftiş çekmecesinin profesyonel doküman okuyucuya dönüştürülmesi (`app.js`, `styles.css`)
- çiğ frontmatter kodlarını gizleme; temiz etiketler, tarihler ve yapısal içerik hiyerarşisi oluşturma.
- temiz okunabilir tipografi ve çift yönlü geri bağlantı haplarının modern tasarımı.

### 🔹 modül 3: linear/raycast tarzı komut paleti, kısayollar ve `main` birleştirmesi
- `Ctrl+K` destekli şık monokrom arama/komut paleti.
- derli toplu alt kontrol adası (floating dock).
- `main` dalına nihai birleştirme.
