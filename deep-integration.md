# 🧬 tam yerli derin entegrasyon planı (deep-integration.md)

> bu plan; neural-os'un proje dışında bağımsız bir oyuncak veya ayrı bir sekme gibi durmasını engelleyip; projenin gerçek kodları, ajanları, becerileri ve kurallarıyla doğrudan organik olarak kenetlendiği "tam entegre bir yapay zeka işletim sistemi kokpitine" dönüştürmeyi hedefler.

---

## 1. 🔍 "entegre hissettirmeyen" kök nedenlerin teşhisi

neden yabancı ve kopuk hissettiriyor?
1. **kopuk veri havuzu:** grafikte sadece `.agent/vault/` içindeki 6 tane yapay markdown dosyası var. kullanıcının asıl kiti olan **20 ajan (`agents/`), 60 beceri (`skills/`), 48 kural (`rules/`) ve gerçek sistem mimarisi (`ARCHITECTURE.md`)** grafikte yok!
2. **tek yönlü izleme:** kullanıcı web paneline baktığında sadece notları görüyor; projedeki bir ajanın kim olduğunu, hangi kurala bağlı olduğunu veya hangi beceriyi kullandığını göremiyor.
3. **organik can damarlarının eksikliği:** sistem sadece "not defteri" gibi duruyor, projenin "gerçek dijital ikizi" (digital twin) gibi davranmıyor.

---

## 2. 💎 tam yerel entegrasyon vizyonu: "projenin yaşayan canlı ikizi"

neural-os grafiği doğrudan projenin gerçek omurgasını haritalayacak:
- 🤖 **20 uzman ajan (agents):** `orchestrator`, `backend-specialist`, `security-auditor` vb.
- ⚡ **temel kurumsal beceriler (skills):** `clean-code`, `database-design`, `auth-patterns` vb.
- 📜 **anayasamız (rules):** `GEMINI.md` ve temel kurallar.
- 🏛️ **mimari ve kararlar (architecture & decisions):** `adr-001`, `architecture-overview`.
- 🔗 **gerçek organik bağlar:** örneğin `orchestrator` ajanı `clean-code` ve `parallel-agents` becerilerine bağlanacak; `backend-specialist` `api-patterns` ve `database-design` becerilerine bağlanacak!

kullanıcı grafiği açtığında:
"burası bir not defteri değil, burası benim **antigravity ai-os kitimin yaşayan beyni ve tüm ajanlarımın sinir sistemi!**" hissini %100 yaşayacak.

---

## 3. 📋 aşamalı icra planı

> **kural 2 & kural 3 gereğince:** her aşama adım adım tamamlanacak ve onayınıza sunulacaktır.

### 🔹 modül 1: kitin gerçek varlıklarını (agents, skills, rules) grafiğe bağlayan organik tarayıcı (`graph_engine.py`)
- sadece `vault/` klasörünü değil, doğrudan `.agent/agents/`, `.agent/skills/` ve `.agent/rules/` dizinlerini tarayarak ajandan beceriye uzanan gerçek bağımlılık ağını otonom inşa etme.

### 🔹 modül 2: entegre tip filtreleri ve monokrom siber kokpit rozetleri (`app.js`, `index.html`)
- filtre butonlarına: `🤖 ajanlar (agents)`, `⚡ beceriler (skills)`, `📜 kurallar (rules)`, `⚖️ kararlar (decisions)` eklenmesi.
- bir ajana tıklandığında hangi becerileri ve hangi kuralları kullandığının sağ panelde net bir şekilde listelenmesi.

### 🔹 modül 3: projenin tam dijital ikizi olarak `main` dalına birleştirme ve nihai doğrulama
- projenin yaşayan canlı zihin haritasının tek dosya bağımsız ihracı ve `main` birleştirmesi.
