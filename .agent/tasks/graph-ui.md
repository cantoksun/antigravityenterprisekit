# 🎨 kurumsal sibernetik nöral grafik görselleştirme planı (graph-ui.md)

> bu plan; kullanıcının canlı olarak izlediği `http://127.0.0.1:8990` arayüzünü sıradan statik dairelerden çıkarıp, siber-uzay estetiğine sahip (canlı parçacıklar, neon enerji akışları, 3d katman derinliği, dinamik nabız atan düğümler ve minimap radarı) birinci sınıf bir bilimkurgu/yapay zeka işletim sistemi kokpitine dönüştürmeyi hedefler.

---

## 1. 🔍 görsel eksiklikler ve yükseltme hedefleri

mevcut ekranda:
- çizgiler düz ve cansız statik gri çizgiler.
- düğümler sadece renkli birer daire ve basit etiket.
- arka plan tekdüze radial gradyan; derinlik hissi zayıf.
- veri transferi ve bilgi akışı hissi yok.

**yeni sibernetik nöral kokpit (cyber-neural cockpit):**
1. **enerji akışı & yönlü parçacıklar (animated energy pulses / data packets):**
   - bağlantı çizgileri boyunca kayan canlı neon foton parçacıkları (bilgi akışını simüle eden animasyonlu veri paketleri).
2. **derinlik & siber ızgara (perspective grid & starfield particles):**
   - arka planda fare hareketine ve zum seviyesine duyarlı parallax siber ızgara (cyber grid) ve süzülen hafif yıldız tozu parçacıkları.
3. **dinamik aura & nabız atan düğümler (pulsing glowing halos):**
   - merkez düğümler (özellikle `INDEX` ve yüksek pagerank otoritesine sahip düğümler) canlı neon aurası ve çift katmanlı dönen holografik halkalarla nabız atacak.
4. **mini-harita (minimap / radar HUD):**
   - sağ altta veya sol altta tüm bilgi ağını kuşbakışı gösteren, kameranın nerede olduğunu gösteren siber radar ekranı.
5. **akıllı tipografi ve simgeler (cyber-hud badges):**
   - düğüm türlerine özel ikonlar (`🧬` kavram, `⚖️` karar, `📖` rehber, `📜` epizot), modern monospace siber fontlar ve net kontrast.

---

## 2. 📋 aşamalı icra planı

> **kural 2 & kural 3 gereğince:** her aşama bağımsız olarak tamamlanacak, doğrulanacak ve sırayla onayınıza sunulacaktır.

### 🔹 modül 1: siber ızgara arka planı ve hareketli veri paketi parçacık motoru (`app.js`)
- bağlantı hatları üzerinden veri aktarımı yapan animasyonlu neon foton parçacıkları (`energy pulses`).
- kamera hareketine duyarlı derinlikli siber ızgara ve süzülen parçacık alanı (starfield canvas).

### 🔹 modül 2: holografik dönen halkalar, tipografi ve düğüm ikonları (`app.js`, `styles.css`)
- pagerank seviyesine göre nabız atan neon halkalar, tip bazlı estetik ikonlar ve şık parıltı (bloom/glow).
- modern hud tipografisi ve siber rozetler.

### 🔹 modül 3: radar minimap'i, cam morfolojisi filtre kontrolleri ve `main` birleştirmesi
- canlı kamera alanını gösteren mini radar haritası.
- filtreleme çubukları (sadece kararları göster, sadece kavramları göster vb.).
- `main` dalına nihai aktarım ve canlı sunucu yenilemesi.
