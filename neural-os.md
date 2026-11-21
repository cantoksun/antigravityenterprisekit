# 🏛️ kurumsal otonom ikinci beyin ve nöral işletim sistemi (neural-os.md)

> bu plan, harici herhangi bir obsidian veya üçüncü parti yazılıma ihtiyaç duymaksızın, antigravity ai-os kitinin tamamen kendi içinde çalışan, web tabanlı interaktif 2d/3d zihin grafiğine, yerel vektör ve çift yönlü semantik arama motoruna sahip kurumsal seviye otonom bir bilgi işletim sistemi inşa etmeyi hedefler.

---

## 1. 🎯 vizyon ve felsefe: harici bağımlılıktan sıfır sürtünmeli yerel güce

klasik obsidian eklentileri veya harici masaüstü uygulamaları kullanıcının ortam değiştirmesini, manuel indeks kurmasını ve dosya gezinmesini gerektirir. 
**antigravity enterprise neural-os** ile:
1. **harici yazılım bağımlılığı sıfırlanır:** obsidian kurulumuna gerek yoktur. sistem doğrudan tek bir komutla (`python .agent/scripts/neural_os.py --serve`) yerel, şık, karanlık temalı ve modern bir web arayüzü sunar (`http://localhost:PORT`).
2. **canlı interaktif güç ve zihin haritası:** force-directed 2d/3d webgl canvas üzerinde tüm kavramlar, mimari kararlar (adr), epizotlar ve kod bağımlılıkları canlı düğüm fizik motoruyla canlandırılır; düğümlere tıklandığında iç doküman, bağlantılı düğümler ve geri linkler (backlinks) anında açılır.
3. **otonom semantik ve bm25 hibrit arama motoru:** harici api gerektirmeyen saf yerel ağırlıklı tf-idf / bm25 ve n-gram semantik benzerlik motoru ile tüm ajan kararları milisaniyeler içinde taranır.
4. **kolektif hafıza havuzu (shared memory pool):** 20 uzman ajanın her biri mimari bir karar aldığında, hata çözdüğünde veya refactor yaptığında bu işletim sistemine otomatik düğüm ekler; grafik kendi kendini besler ve genişletir.
5. **statik html dışa aktarma (offline self-contained export):** internet bağlantısı veya python sunucusu olmadan da tüm grafiği tek bir taşınabilir `.html` dosyası olarak üretip raporlama/sunum için paylaşabilme imkanı sağlanır.

---

## 2. 🏗️ mimari katmanlar ve bileşen haritası

```
.agent/
├── neural_os/                        # kurumsal nöral os çekirdeği
│   ├── ui/                           # modern web arayüzü ve grafik görselleştirici
│   │   ├── index.html                # tek sayfalık responsive zihin ve grafik paneli
│   │   ├── app.js                    # force-directed graph (d3/canvas) ve interaktif yönetim
│   │   └── styles.css                # modern karanlık tema, cam morfolojisi (glassmorphism)
│   ├── engine/                       # analiz ve arama çekirdeği
│   │   ├── graph_engine.py           # çift yönlü bağlar, merkezilik analizi (pagerank/degree)
│   │   ├── semantic_search.py        # saf yerel bm25 ve semantik benzerlik motoru
│   │   └── exporter.py               # tek dosya bağımsız html dışa aktarıcı
│   └── server.py                     # yerel hafif http api sunucusu (sıfır harici paket)
├── scripts/
│   └── neural_os.py                  # ana cli komut arayüzü (--serve, --search, --export, --audit)
└── vault/                            # yaşayan bilgi deposu (markdown + wikilink)
    ├── concepts/                     # mimari kurallar ve temel kavramlar
    ├── decisions/                    # kurumsal adr mimari kayıtları
    ├── playbooks/                    # kurumsal standartlar ve oyun kitapları
    └── episodes/                     # otonom ajan epizotları ve oturum hafızası
```

---

## 3. 🛡️ kurumsal standartlar ve kurallara uyum

- **1. kural (türkçe karakter & küçük harf):** arayüz ve tüm loglar küçük harflerle ve kusursuz türkçe yapılandırılır.
- **4. kural (sadelik & trend teknolojiler):** ağır kütüphane yığınları yerine tarayıcının yerel canvas/svg api'si ve python'ın yerleşik `http.server` modülü modernize edilerek hafif, sıfır kurulumlu mimari oluşturulur.
- **6., 7., 14. kural (güvenlik & veri koruması):** sunucu yalnızca yerel ağda (`127.0.0.1`) çalışır, path traversal açıklarına karşı katı regex beyaz listesi uygulanır.
- **9., 10. kural (performans & bellek optimizasyonu):** grafik verileri istemciye sıkıştırılmış json olarak tek seferde iletilir, dom düğüm şişmesini engellemek için sanallaştırılmış tuval (canvas render) kullanılır.
- **15. kural (responsive ux):** masaüstünde geniş çift panelli çalışma alanı (sol grafik, sağ doküman önizleme); mobilde/tabletlerde alt çekmece (bottom sheet) uyumlu tam responsive tasarım.
- **17. kural (zero friction):** tek tıkla çalışır (`http://localhost:PORT`), kullanıcıyı ek paket yükleme angaryasıyla uğraştırmaz.

---

## 4. 📋 aşamalı ve modüler icra planı

> **kural 2 & kural 3 gereğince:** her aşama bağımsız olarak tamamlanacak, doğrulanacak ve sırayla onayınıza sunulacaktır.

### 🔹 modül 1: yerel grafik analitiği ve pagerank çekirdeği (`graph_engine.py`)
- çift yönlü grafiğin derin analizi (düğüm derecesi, pagerank algoritması, merkezilik puanları, kümeleme).
- kırık bağlantıların otomatik tespiti ve grafik yoğunluk skorlaması.

### 🔹 modül 2: saf yerel hibrit arama motoru (`semantic_search.py`)
- harici yapay zeka apisi veya api anahtarı gerektirmeyen yerel bm25 / tf-idf anahtar kelime ve semantik alaka motoru.
- anında filtreleme, etiket bazlı ağırlıklandırma ve düğüm özetleme.

### 🔹 modül 3: modern yerel web sunucusu ve sıfır bağımlılıklı api (`server.py`)
- python yerleşik modülleriyle çalışan, path-traversal korumalı, rest api uç noktaları (`/api/graph`, `/api/node/{id}`, `/api/search`).
- otonom port seçimi ve çakışma önleyici yapı.

### 🔹 modül 4: enterprise web grafik ve zihin paneli (`ui/index.html`, `ui/app.js`, `ui/styles.css`)
- obsidian'ı aratmayan modern karanlık tema, cam morfolojisi ve modern tipografi (kural 16).
- yerel yüksek performanslı force-directed canvas zihin grafiği, tıklanabilir düğümler, geri bağlantı paneli, markdown önizleme ve arama çubuğu.

### 🔹 modül 5: tek dosya çevrimdışı dışa aktarıcı (`exporter.py`) ve cli orkestrasyonu (`neural_os.py`)
- tüm css, js ve grafik verisini tek bir taşınabilir `.html` dosyasına gömen dışa aktarıcı.
- `neural_os.py` ana cli aracının devreye alınması ve `main` dalına nihai birleştirme.
