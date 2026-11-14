# iki ajanlı temiz oda hava boşluğu protokolü (two-agent clean-room airgap)

bu tarif, harici kapalı kaynaklı bir sistemin veya tescilli bir ikili dosyanın (binary/apk/electron/.net) telif hakkı ihlali yapmadan ve hukuki clean-room standartlarına %100 uyarak sıfırdan yeniden inşa edilmesini (clean-room rewrite) yönetir.

---

## 🎯 temel prensip: personel ve bağlam ayrımı (personnel separation)

geleneksel yazılım hukukunda ve endüstri standardında tek bir kişinin veya ajanın hem orijinal kaynak kodunu decompile edip hem de yeni kodu yazması "clean-room" sayılmaz (kirlenme riski).

bu nedenle antigravity ai-os içerisinde **hava boşluğu (airgap)** uygulanır:

```
[kirli alan (dirty room)]                   [hava boşluğu (airgap)]                  [temiz oda (clean room)]
┌─────────────────────────┐               ┌────────────────────────┐              ┌─────────────────────────┐
│     kaynak ikili        │               │                        │              │    sıfırdan bağımsız    │
│  (binary / dex / asar)  │               │   SPEC.md / API_DOC    │              │       kaynak kod        │
│            ↓            │  ───────►     │    (yalnızca soyut     │  ───────►    │            ↓            │
│    code-archaeologist   │               │   arayüz ve testler)   │              │    backend-specialist   │
│   (analiz ve decompile) │               │                        │              │   frontend-specialist   │
└─────────────────────────┘               └────────────────────────┘              └─────────────────────────┘
```

---

## 👥 rol ve sorumluluk sınırları

### 1. kirli oda ajanı (dirty room agent) — `code-archaeologist`
- **erişebileceği veriler:** hedef ikili dosya, decompiler çıktıları, ham ağ paketleri.
- **kesinlikle yasak:** yeni projeye kaynak kod yazamaz (`.ts`, `.py`, `.rs` vb. oluşturamaz).
- **tek görevi:** sistemi incelemek, girdi/çıktı davranışlarını belirlemek ve soyut bir `SPEC.md` ile girdi-çıktı json fikstürleri üretmektir.

### 2. hava boşluğu dokümanı (airgap contract) — `SPEC.md`
kirli oda ajanının temiz oda ajanına aktarabileceği **tek yasal köprüdür**:
- **izin verilen içerik:**
  - veri tipleri ve şemalar (alan adları ve tipleri),
  - uç nokta sözleşmeleri (`POST /api/v1/auth`, beklenen gövde ve yanıt formatı),
  - algoritmanın matematiksel veya mantıksal kuralı (örneğin: "tutar * 0.18 kdv eklenir"),
  - girdi -> çıktı test durumları (fixtures).
- **kesinlikle yasaklanan içerik:**
  - orijinal ikiliden kopyalanmış decompile c/c++/c#/js kod parçacıkları,
  - tescilli değişken adları veya orijinal yorum satırları,
  - orijinal telifli görsel, ses veya lisanslı ikili varlıklar.

### 3. temiz oda ajanı (clean room agent) — `backend-specialist` / `frontend-specialist`
- **erişebileceği veriler:** yalnızca `SPEC.md`, test fikstürleri ve kurumsal mimari rehberleri (`clean-code`).
- **kesinlikle yasak:** orijinal ikili dosyayı açamaz, `jadx`, `ilspy`, `ghidra` gibi decompile araçlarını çalıştıramaz.
- **görevi:** `SPEC.md` spesifikasyonunu karşılayan, tdd yaklaşımıyla yazılmış, kurumsal standartlarda yepyeni temiz kodu üretmektir.

---

## 🛡️ doğrulama: `cleanroom_auditor.py`
inşa edilen yeni kodun orijinal ikiliden sızıntı (kirlenme) içerip içermediği sistemimizdeki Clean-Room Denetçisi ile doğrulanır:
```bash
python .agent/skills/reverse-engineering/scripts/cleanroom_auditor.py .
```
denetçi şunları tarar:
- decompiled kod kalıntıları veya decompilation bayrakları,
- yetkisiz ikili varlıkların depoya kopyalanması,
- `SPEC.md` dışındaki doğrudan kaynak kod sızıntıları.
