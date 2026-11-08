# kurumsal yapay zeka ajan mimarisi (architecture)

> gelişmiş yapay zeka ajan kabiliyetlerini genişleten kurumsal araç kiti mimari haritası

---

## 📋 genel bakış

kurumsal yapay zeka ajan kiti modüler, rol tabanlı ve yüksek disiplinli bileşenlerden oluşur:

- **20 uzman ajan** - kurumsal rollere ve 19 katı kurala göre özelleştirilmiş yapay zeka profilleri
- **36 beceri (skill)** - alana özel teknik bilgi, rehber ve denetim modülleri
- **11 iş akışı (workflow)** - slash komutları ve süreç yürütme prosedürleri
- **ana doğrulama betikleri (scripts)** - öncelik bazlı kalite, güvenlik ve performans orkestrasyonu

---

## 🏗️ dizin yapısı

```plaintext
.agent/
├── architecture.md          # sistem mimari haritası ve bileşen kataloğu
├── agents/                  # 20 uzman ajan profili (.md)
├── skills/                  # 36 modüler beceri kütüphanesi
├── workflows/               # 11 iş akışı prosedürü (/komutlar)
├── rules/                   # 19 temel kural hiyerarşisi (gemini.md)
└── scripts/                 # ana orkestrasyon ve doğrulama betikleri (checklist, verify_all)
```

---

## 🤖 20 uzman ajan kataloğu

tüm uzman ajanlar katı küçük harf, eksiksiz türkçe karakter, idor/bola koruması, bellek analizi ve responsive ux ilkeleriyle yapılandırılmıştır.

| ajan | odak alanı | birincil beceriler |
|---|---|---|
| `orchestrator` | çoklu ajan koordinasyonu ve modüler aşama yönetimi | parallel-agents, behavioral-modes, clean-code |
| `project-planner` | keşif, socrata analizi ve mimari planlama | brainstorming, plan-writing, architecture |
| `frontend-specialist` | web kullanıcı arayüzü, responsive ux ve dinamik renkler | frontend-design, nextjs-react-expert, tailwind-patterns |
| `backend-specialist` | kurumsal api, iş mantığı ve nesne seviyesinde sahiplik | api-patterns, nodejs-best-practices, database-design |
| `database-architect` | yalın veritabanı şeması, sql indeksleme ve rls 42501 | database-design, api-patterns, clean-code |
| `mobile-developer` | ios, android, react native, alt çekmece ergonomisi | mobile-design, clean-code |
| `game-developer` | oyun mekanikleri, nesne havuzlama ve kare bütçesi | game-development, clean-code, performance-profiling |
| `devops-engineer` | sıfır kesinti dağıtımı, docker ve sunucu yönetimi | deployment-procedures, server-management |
| `security-auditor` | kurumsal güvenlik uyumluluğu, owasp ve sır koruması | vulnerability-scanner, red-team-tactics |
| `penetration-tester` | ofansif güvenlik, ptes, aktif idor/bola sızma testleri | red-team-tactics, vulnerability-scanner, api-patterns |
| `test-engineer` | test piramidi, birim ve entegrasyon test stratejileri | testing-patterns, tdd-workflow, webapp-testing |
| `debugger` | 4 aşamalı sistematik kök neden analizi | systematic-debugging, clean-code |
| `performance-optimizer` | core web vitals, bellek sızıntısı tespiti ve profil çıkarma | performance-profiling, nextjs-react-expert |
| `seo-specialist` | teknik seo, anlamsal web ve üretken motor optimizasyonu (geo) | seo-fundamentals, geo-fundamentals, clean-code |
| `documentation-writer` | teknik dokümantasyon, openapi, adr ve kurumsal readme | documentation-templates, clean-code |
| `product-manager` | gereksinimler, prd belgeleri ve gherkin kabul kriterleri | plan-writing, brainstorming, clean-code |
| `product-owner` | ürün backlog'u, rice/moscow önceliklendirmesi ve mvp sınırları | plan-writing, brainstorming, clean-code |
| `qa-automation-engineer` | playwright e2e otomasyonu, kaos ve sınır testleri | webapp-testing, testing-patterns, clean-code |
| `code-archaeologist` | miras (legacy) sistem analizi, tersine mühendislik ve refactor | clean-code, architecture, code-review-checklist |
| `explorer-agent` | otonom kod tabanı keşfi, import haritalama ve varlık doğrulaması | clean-code, architecture, systematic-debugging |

---

## 🧩 36 modüler beceri sınıflandırması

beceriler görev bağlamına göre ajanlar tarafından isteğe bağlı ve dinamik olarak yüklenir.

### 🎨 ön yüz ve arayüz tasarımı
- `frontend-design`: modern arayüz kalıpları, 3 renk armonisi, gereksiz x butonu engeli ve tipografi disiplini.
- `nextjs-react-expert`: react 19 ve next.js app router performans kalıpları, rsc ve demet optimizasyonu.
- `tailwind-patterns`: tailwind css v4 utility kalıpları, konteyner sorguları ve modern stil belirteçleri.
- `web-design-guidelines`: 100+ maddelik web arayüz, responsive ux, erişilebilirlik ve performans kuralları.
- `mobile-design`: mobil öncelikli alt çekmece (drawer) ergonomisi ve dokunmatik jestler.

### ⚙️ arka yüz, api ve programlama
- `desktop-rust-patterns`: kurumsal masaüstü rust mimarisi, slint/egui yerel gui ve tauri hafif webview standartları.
- `api-patterns`: rest, graphql ve trpc karşılaştırması, standart yanıt zarfları, cursor sayfalama.
- `nodejs-best-practices`: asenkron akışlar, bellek yönetimi ve event loop optimizasyonu.
- `python-patterns`: kurumsal python, fastapi, tip ipuçları (type hints) ve pydantic şemaları.
- `clean-code`: global temiz kod felsefesi, aşırı mühendislik yasağı ve yalınlık standardı.

### 🗄️ veritabanı ve veri mimarisi
- `database-design`: yalın şema tasarımı, gereksiz bayrak yasağı, b-tree indeksleme, rls 42501 hata analizi ve limitsiz sorgu engeli.

### 🛡️ güvenlik ve savunma
- `vulnerability-scanner`: owasp 2026, tedarik zinciri güvenliği, hassas sır koruması ve istemci çerez/oturum denetimi.
- `red-team-tactics`: ofansif güvenlik, mitre att&ck, idor/bola açıkları tespiti ve yetki yükseltme testleri.

### 🧪 test, kalite ve doğrulama
- `testing-patterns`: aaa deseni, birim ve entegrasyon test stratejileri.
- `tdd-workflow`: test güdümlü geliştirme, kırmızı-yeşil-refactor döngüsü.
- `webapp-testing`: playwright tabanlı e2e test otomasyonu, görsel regresyon ve ağ gecikme testleri.
- `code-review-checklist`: kapsamlı kurumsal kod inceleme ve kalite kriterleri.
- `lint-and-validate`: otomatik sözdizimi, tip kontrolü ve statik kod analizi.
- `systematic-debugging`: 4 aşamalı sistematik hata ayıklama ve kök neden analizi.

### 🚀 altyapı, sunucu ve otomasyon
- `deployment-procedures`: sıfır kesinti dağıtımı, aşamalı geçiş ve geri alma (rollback) protokolleri.
- `server-management`: sunucu süreç yönetimi, sistem kaynak izleme ve yük dengeleme.
- `bash-linux`: linux terminal komutları, boru hatları ve kabuk betikleri.
- `powershell-windows`: windows powershell işleç sözdizimi ve ortam yönetimi.

### 📐 mimari, planlama ve ürün yönetimi
- `architecture`: adr kayıtları, mimari ödünleşimler (trade-offs) ve katmanlı sistem tasarımı.
- `app-builder`: uçtan uca full-stack proje iskelesi kurma ve teknoloji yönlendirmesi.
- `plan-writing`: modüler görev kırılımları, bağımlılıklar ve doğrulama kriterleri.
- `brainstorming`: sokratik analiz ve karar mekanizmaları.
- `behavioral-modes`: ajan davranış modları (araştırma, geliştirme, denetim, dağıtım).
- `parallel-agents`: çoklu ajan orkestrasyonu ve iş bölümü kalıpları.
- `intelligent-routing`: otomatik uzman ajan tespiti ve yönlendirme protokolü.

### 📈 büyüme, keşif ve diğer uzmanlıklar
- `seo-fundamentals`: teknik seo, e-e-a-t, core web vitals ve yapısal veriler.
- `geo-fundamentals`: yapay zeka arama motorları (chatgpt, claude, perplexity) için alıntılanabilir veri kurgusu.
- `game-development`: oyun mekanikleri, delta time, nesne havuzlama ve canvas/webgl optimizasyonu.
- `mcp-builder`: model context protocol sunucuları, araç ve kaynak kalıpları.
- `documentation-templates`: kurumsal teknik doküman, readme ve api şablonları.
- `i18n-localization`: çoklu dil desteği, yerelleştirme ve sabit metin izolasyonu.
- `performance-profiling`: cpu/ram profil çıkarma, alev grafikleri ve bellek sızıntısı analizi.

---

## 🔄 11 kurumsal iş akışı (workflows)

slash komutlarıyla tetiklenen standart süreçler:

| komut | açıklama ve amaç |
|---|---|
| `/orchestrate` | çoklu ajanı bağımsız aşamalara bölerek orkestre eder |
| `/plan` | 4 aşamalı mimari planlama ve görev kırılımı yapar |
| `/create` | yeni bir özellik veya modülü sıfırdan inşa eder |
| `/enhance` | mevcut kodu refactor eder ve modernize eder |
| `/debug` | kök neden analiziyle hataları sistematik giderir |
| `/test` | birim, entegrasyon ve e2e testlerini koşturur |
| `/deploy` | 5 aşamalı güvenli canlıya alma sürecini yürütür |
| `/brainstorm` | sokratik sorularla tasarım kararlarını netleştirir |
| `/status` | projenin genel sağlık ve tamamlanma durumunu raporlar |
| `/preview` | yapılan değişiklikleri canlı önizleme ortamında sınar |
| `/ui-ux-pro-max` | modern tasarım stilleri ve renk armonisiyle arayüz üretir |

---

## 🎯 beceri yükleme protokolü (skill loading protocol)

```plaintext
kullanıcı isteği ──> otomatik alan analizi ──> ilgili uzman ajan seçimi
                                                        │
                                                        ▼
                                       frontmatter "skills:" kontrolü
                                                        │
                                                        ▼
                                               skill.md okunur
                                                        │
                                                        ▼
                                  (gerektiğinde) scripts/ ve references/
```

### beceri dizin mimarisi
```plaintext
skill-klasörü/
├── SKILL.md           # (zorunlu) metadata, prensipler ve talimatlar
├── scripts/           # (isteğe bağlı) python denetim ve analiz betikleri
├── references/        # (isteğe bağlı) şablonlar, rehberler ve dökümler
└── assets/            # (isteğe bağlı) görsel veya şematik varlıklar
```

---

## 🛠️ ana doğrulama ve denetim betikleri (master scripts)

projenin kalitesini ve kurallara uyumunu denetleyen iki ana orkestrasyon betiği:

| betik | amaç ve kapsam | ne zaman çalıştırılır? |
|---|---|---|
| `checklist.py` | öncelik bazlı temel denetimler (güvenlik, lint, şema, test, ux, seo) | geliştirme sırasında, her aşama bitiminde |
| `verify_all.py` | tam kapsamlı paket (checklist + lighthouse + playwright + bundle + mobil) | canlıya alma öncesinde ve majör sürümlerde |

### çalıştırma komutları
```powershell
# geliştirme sırasındaki hızlı denetim
$env:PYTHONIOENCODING="utf-8"; python .agent/scripts/checklist.py .

# canlıya alma öncesi tam paket denetim
$env:PYTHONIOENCODING="utf-8"; python .agent/scripts/verify_all.py . --url http://localhost:3000
```

---

## 📊 mimari istatistikler ve kapsama alanı

| metrik | değer |
|---|---|
| **toplam uzman ajan** | 20 ajan (tamamı kurumsal derinlikte) |
| **toplam modüler beceri** | 36 beceri |
| **toplam iş akışı** | 11 slash komutu |
| **ana orkestrasyon betikleri** | 4 betik (`checklist.py`, `verify_all.py`, `auto_preview.py`, `session_manager.py`) |
| **temel mimari kurallar** | 19 katı p0 kuralı (küçük harf, eksiksiz türkçe karakter, sıfır varsayım, şeffaf aşama taahhüdü) |
| **geliştirme kapsamı** | web, mobil, backend, veritabanı, ofansif/defansif güvenlik, oyun geliştirme, teknik seo ve test otomasyonu (~%95 kapsama) |

---

## 🔗 hızlı başvuru eşleşmeleri

| ihtiyaç / alan | görevli uzman ajan | yüklenen çekirdek beceriler |
|---|---|---|
| **web arayüzü & responsive** | `frontend-specialist` | frontend-design, nextjs-react-expert, tailwind-patterns |
| **api & iş mantığı** | `backend-specialist` | api-patterns, nodejs-best-practices, database-design |
| **veritabanı & rls** | `database-architect` | database-design, api-patterns, clean-code |
| **mobil uygulama** | `mobile-developer` | mobile-design, clean-code |
| **güvenlik & sızma testi** | `security-auditor` / `penetration-tester` | vulnerability-scanner, red-team-tactics |
| **performans & bellek** | `performance-optimizer` | performance-profiling, nextjs-react-expert |
| **test otomasyonu** | `qa-automation-engineer` / `test-engineer` | webapp-testing, testing-patterns, tdd-workflow |
| **hata ayıklama** | `debugger` | systematic-debugging, clean-code |
| **ürün & planlama** | `project-planner` / `product-manager` | plan-writing, brainstorming, architecture |
| **orkestrasyon** | `orchestrator` | parallel-agents, behavioral-modes, clean-code |
