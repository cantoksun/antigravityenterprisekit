---
name: frontend-design
description: modern web arayüz tasarım ilkeleri. dinamik renk armonisi, 3 renk kuralı, buton ve modal sadeliği (gereksiz x butonu yasağı), tipografi disiplini ve lazy loading analizleri.
priority: p1-visual
version: 2.5.0
---

# kurumsal ön yüz tasarım, renk dengesi ve etkileşim sadeliği standartları

bu beceri; modern web arayüzlerinde kullanıcı deneyimi, renk disiplini (maksimum 3 ana renk tonu), buton ve modal etkileşim sadeliği (dışa dokunarak kapanan pencerelerde gereksiz x butonunun kaldırılması), cihaz odaklı ux (15. kural) ve tipografi disiplinini (16. kural) yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 18 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır (1. kural).
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz (2. kural).
   - adım adım aşamalı yürütülür; her seferinde tek bir modül tamamlanır (3. kural).
   - sadelik ve modern trend teknolojiler (4. kural).
   - paginasyon/lazy loading analizi (13. kural).
   - masaüstü modal vs mobil alt çekmece ayrımı (15. kural).
   - font sınırlandırması ve tipografi disiplini (16. kural).
   - kullanıcıyı yormama (17. kural) ve kesin varlık doğrulaması (18. kural).
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki tasarım ilkeleri.

---

## 🎯 etkileşim ve buton sadeliği: gereksiz "x" butonlarından kaçınma

modern arayüz tasarımında görsel gürültüyü (visual clutter) azaltmak ve arayüzü ferah tutmak esastır:

### 1. sezgisel kapanma ve gereksiz buton temizliği
- **dışa tıklama / dokunma (backdrop click / tap-outside):** modal veya alt çekmece karartılmış arka plana (overlay/backdrop) tıklandığında veya mobilde aşağı kaydırıldığında (swipe-to-dismiss) zaten sezgisel olarak kapanıyorsa, sağ üst köşeye fazladan ve görsel yük oluşturan bir `X` (kapat) butonu koymayın.
- **temiz başlık alanı:** gereksiz `X` butonu kaldırıldığında modal başlığı ferahlar, kullanıcının dikkati dağılmaz ve arayüz daha modern bir görünüme kavuşur.
- **klavye ve erişilebilirlik:** `esc` tuşuyla kapanma ve ekran okuyucu odak yönetimi korunduğu sürece görsel `X` ikonuna ihtiyaç yoktur.

### 2. istisnai durumlar (ne zaman kapatma butonu gerekir?)
- yalnızca form veri kaybı riski olan, dışa tıklamanın kazara kapanmayı önlemek için kasıtlı olarak devreden çıkarıldığı (`modal={true}`, `onPointerDownOutside={e => e.preventDefault()}`) kritik onay diyaloglarında açık bir "iptal" veya "vazgeç" butonu konulmalıdır.

---

## 🎨 renk disiplini: maksimum 3 renk tonu ve dinamik genişletme

- **%60 nötr zemin:** arka plan, yüzeyler ve kartlar.
- **%30 yapısal ton:** başlıklar, ana metinler, kenarlıklar.
- **%10 vurgu (accent):** cta butonları ve aktif durumlar.
- kullanıcının isteği doğrultusunda pastel tonlar veya yeni kategori renkleri ahenkle sisteme eklenebilir.

---

## 📱🖥️ 15. kural: masaüstü vs mobil arayüz ayrımı (responsive ux)
- **mobilde:** başparmak erişimli alt çekmeceler (`drawer` / `bottom sheet`), 48x48dp dokunma hedefleri, kaydırma jestleri.
- **masaüstünde:** geniş ekranı verimli kullanan modallar (`dialog`), popover'lar ve klavye kısayolları.

---

## 🔤 16. kural: tipografi disiplini ve font sınırlaması
- projede toplam font ailesi sayısı **maksimum 2-3 (en fazla 4-5)** ile sınırlıdır; sürekli keyfi font eklenmez.
- hiyerarşi aynı fontun ağırlıkları (`font-normal`, `font-semibold`, `font-bold`) ve boyut ölçekleriyle kurulur.
