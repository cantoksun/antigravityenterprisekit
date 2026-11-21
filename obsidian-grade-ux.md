# 💎 obsidian kalitesinde profesyonel grafik motoru ve tam siber ux revizyon planı (obsidian-grade-ux.md)

> bu plan; obsidian'ın profesyonel hissettiren temel dinamiklerini (fizik akışkanlığı, etiket yakınlaştırma ölçeği, düğüm sabitleme/pin, arama çubuğu akışkanlığı, sol/sağ katlanabilir yan paneller ve ses/haptik hissi veren görsel tepkiler) analiz edip, antigravity neural-os'u obsidian'dan bile daha akıcı ve kurumsal bir masaüstü kokpitine dönüştürmeyi hedefler.

---

## 1. 🔍 obsidian'ı "profesyonel" hissettiren ama bizde eksik olan 6 kritik dinamik

1. **fizik motorunun sertliği ve titreşimi:**
   - *mevcut durum:* bizim basit kuvvet motorumuz düğümler çok olunca (124 düğüm) titreşiyor veya birbirinin üstüne binebiliyor; obsidian d3-force tabanlı Barnes-Hut quadtree algoritması kullanarak ipeksi bir yerleşim sunar.
2. **dinamik etiket seviyesi (zoom-dependent label culling):**
   - *mevcut durum:* 124 düğümün hepsinin yazısı aynı anda ekranda açık olunca harita boğuluyor ve amatör duruyor.
   - *obsidian kuralı:* uzaklaştıkça sadece büyük merkez düğümlerin (`architecture-overview`, `index`) yazıları görünür; yakınlaştıkça (zoom-in) alt becerilerin yazıları yavaşça belirir (fade-in).
3. **düğüm sabitleme (pin / drag & lock):**
   - *obsidian kuralı:* bir düğümü tutup bir köşeye çektiğinizde orada sabitlenir, tekrar sürükleyene kadar fizik motoru onu fırlatmaz.
4. **katlanabilir sol/sağ çift panel (collapsible dual-sidebars):**
   - *obsidian kuralı:* sol tarafta dosya/katman gezgini, sağ tarafta doküman teftiş çekmecesi bulunur ve istenirse tek tıkla gizlenip grafik tam ekran yapılabilir.
5. **grafik ayar konsolu (live physics tuning hud):**
   - *obsidian kuralı:* sağ üstte/sol üstte minik bir ayar çarkı vardır; kullanıcı yerçekimini (gravity), itme kuvvetini (repulsion) ve bağlantı mesafesini kaydırıcılarla (sliders) anlık değiştirebilir.
6. **ok yönleri (curved directional arrows):**
   - *obsidian kuralı:* bağlar sadece düz çizgi değil, yönlendirilmiş hafif kavisli oklar taşır.

---

## 2. 📋 aşamalı icra planı

> **kural 2 & kural 3 gereğince:** her aşama bağımsız olarak tamamlanacak ve onayınıza sunulacaktır.

### 🔹 modül 1: ipeksi barnes-hut fizik motoru & dinamik etiket ölçekleme (`app.js`)
- düğüm titreşimlerini ve üst üste binmeleri sıfırlayan Barnes-Hut yaklaşımı ve quadtree yerleşimi.
- zoom seviyesine duyarlı etiket gizleme/gösterme (uzakta sadece merkez düğümler, yakında tümü).
- düğümü sürükleyip bırakılan yerde sabitleme (pin node) özelliği.

### 🔹 modül 2: canlı fizik ayar konsolu (gravity, link distance, repulsion sliders)
- sol üstte katlanabilir ayar paneli: kullanıcı yerçekimi ve düğüm mesafesini kaydırıcılarla anlık yönetebilecek.

### 🔹 modül 3: çift yönlü katlanabilir panel mimarisi ve `main` birleştirmesi
- sol gezgin + sağ teftiş çekmecesinin tam obsidian ergonomisinde katlanabilir kılınması.
- `main` dalına nihai aktarım.
