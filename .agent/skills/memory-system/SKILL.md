---
name: memory-system
description: obsidian uyumlu otonom nöral bellek ve bilgi ağı yönetimi. kararları, kuralları ve oturum hafızasını çift yönlü wikilink grafiğinde tutar.
when_to_use: "kullanıcı 'bunu unutma', 'hafızaya kaydet', 'hatırla' dediğinde, kritik bir mimari karar (adr) alındığında veya oturum tamamlandığında kullanılır."
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
version: 2.0.0
effort: low
---

# 🧠 nöral bellek sistemi (neural memory system v2.0)

> oturumlar arasında mimari kararları, konseptleri ve tecrübeleri obsidian uyumlu bir nöral bilgi ağında (`.agent/vault/`) çift yönlü bağlantılarla (`[[wikilink]]`) kalıcı tutar.

---

## 🎯 genel bakış ve omurga

bu sistem, klasik pasif metin notlarının ötesine geçerek:
1. **çift yönlü bağlantı ağı (bidirectional graph):** tüm bilgiler `[[kavram]]` veya `[[karar]]` şeklinde birbirine düğümlenir.
2. **obsidian uyumluluğu:** kullanıcı `.agent/vault/` dizinini obsidian'da açtığında renk kodlu interaktif bir bilgi grafiği ile karşılaşır.
3. **otonom python motoru:** `.agent/scripts/neural_memory.py` üzerinden otomatik sorgulama, adr üretimi, epizot kaydı ve grafik bütünlüğü denetimi (`--audit`) sağlar.

---

## 📂 dizin hiyerarşisi (`.agent/vault/`)

- `INDEX.md`: harita ve içerik düğümü (maps of content - MOC).
- `concepts/`: genel mimari ilkeler, güvenlik standartları ve desenler.
- `decisions/`: numaralandırılmış mimari karar kayıtları (`adr-*.md`).
- `playbooks/`: adım adım uygulama ve operasyon rehberleri.
- `episodes/`: oturum özetleri ve epizodik tecrübe kayıtları (`episode-*.md`).
- `.obsidian/`: otomatik grafik renklendirme (`graph.json`) ve arayüz ayarları (`app.json`).

---

## 🤖 ajanlar için kullanım protokolü

tüm uzman ajanlar (`orchestrator`, `project-planner`, `backend-specialist` vb.) kritik mimari adımlarda bu protokolü izler:

### 1. geçmiş kararları ve kavramları sorgulama (token tasarruflu)
```bash
python .agent/scripts/neural_memory.py --query <anahtar_kelime>
# veya etiket/tip bazlı filtreleme:
python .agent/scripts/neural_memory.py --type decision
```

### 2. yeni bir mimari karar (adr) ekleme
yeni bir veritabanı seçimi, kimlik doğrulama mimarisi veya yapısal değişiklik yapıldığında:
```python
from neural_memory import NeuralVault
vault = NeuralVault()
vault.add_decision(
    title="PostgreSQL ve pgvector Geçişi",
    context="Yüksek boyutlu vektör araması gereksinimi doğdu.",
    decision="Harici vektör servisi yerine PostgreSQL + pgvector eklentisi seçildi.",
    consequences="Altyapı maliyeti düşürüldü, tek veritabanı üzerinden ACID güvencesi sağlandı.",
    tags=["database", "pgvector", "architecture"]
)
```

### 3. oturum sonu epizodik kayıt (episodic memory hook)
büyük bir dönüm noktası veya modül tamamlandığında:
```python
from neural_memory import NeuralVault
vault = NeuralVault()
vault.add_episode(
    title="Kimlik Doğrulama Katmanı Entegrasyonu",
    summary="OAuth2 ve katı JWT rotasyonu başarıyla tamamlandı.",
    related_nodes=["clean-code-principles", "architecture-overview"]
)
```

### 4. grafik sağlığı denetimi
```bash
python .agent/scripts/neural_memory.py --audit
```
kırık bağlantı (broken link) veya yetim düğüm (orphan node) bırakılmamalıdır.
