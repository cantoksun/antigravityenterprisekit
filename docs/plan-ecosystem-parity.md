---
title: "antigravity ai-os tam ekosistem paritesi ve pazar liderliği planı"
slug: "plan-ecosystem-parity"
version: "2.0.0"
date: "2026-11-21"
status: "draft"
agent: "project-planner"
rules_applied: [1, 2, 3, 4, 17, 18, 19, 45, 46, 47, 48]
---

# 📋 antigravity ai-os: eksiksiz ekosistem paritesi ve pazar liderliği mimari planı (v2.0)

bu planlama belgesi; internetteki 10 popüler antigravity kitinin (`besync-labs`, `google-antigravity`, `screencut`, `asoji`, `arindam-b`, `omer-metin`, `sickn33`, `rmyndharis` vb.) tüm güçlü özelliklerini ve kitimizin tespit edilen **tüm eksiklerini** (medya/transkript araçları ve açık kaynak beceri içe aktarımı dahil) eksiksiz kapsayacak şekilde güncellenmiştir.

---

## 🎯 1. özet ve iş değeri

- **hedef:** antigravity ai-os kitimizi yalnızca kodlama ve mimari alanında değil; harici beceri içe aktarımı, medya/transkript ayrıştırma, ci/cd otomasyonu, tek komutla kurulum, marketplace eklenti standardı ve otonom github pr botu ile donatarak internetteki tüm açık kaynak repoları tek çatı altında geride bırakan 1 numaralı platform haline getirmek.
- **kapsanan tüm ekosistem eksikleri:**
  1. **ci/cd github actions:** `.github/workflows/verify-kit.yml` (`besync-labs` paritesi).
  2. **otonom kurulum / tek tıkla yükleme:** `install.ps1` ve `install.sh` (`ag-kit` paritesi).
  3. **resmi marketplace eklenti paketi:** `plugin.json` (`asoji` paritesi).
  4. **otonom github pr ve issue botu:** `github_automator.py` (`arindam-b` paritesi).
  5. **tarayıcısız medya & transkript motoru:** `media_extractor.py` (`screencut` paritesi).
  6. **akıllı beceri toplayıcı & niş beceri genişletmesi:** `skill_aggregator.py` (`omer-metin`, `sickn33`, `rmyndharis` paritesi).

---

## 🔍 2. etkilenecek ve oluşturulacak bileşenler (18. kural - kesin varlık teyidi)

### oluşturulacak yeni dosyalar:
1. `.github/workflows/verify-kit.yml` - github actions otomatik doğrulama iş akışı
2. `install.ps1` - windows/powershell tek tıkla kurulum ve projeye enjeksiyon betiği
3. `install.sh` - linux/macos/bash tek tıkla kurulum ve projeye enjeksiyon betiği
4. `plugin.json` - resmi antigravity marketplace eklenti tanım manifestosu
5. `.agent/scripts/github_automator.py` - otonom github pull request ve issue yönetim aracı
6. `.agent/scripts/media_extractor.py` - tarayıcısız youtube/medya transkript ve metadata ayrıştırıcı (screencut paritesi)
7. `.agent/scripts/skill_aggregator.py` - açık kaynak depolardan (sickn33/omer-metin) beceri tarama ve l0/l1 formatında sisteme güvenle dahil etme aracı
8. `.agent/scripts/tests/test_ecosystem_parity.py` - tüm yeni yeteneklerin sözleşme test paketi

### güncellenecek mevcut bileşenler:
1. `.agent/manifest.lock.json` - yeni betiklerin sha-256 kilitleri mühürlenecek
2. `.agent/scripts/verify_kit.py` - yeni testlerin ve fazların master doğrulayıcıya bağlanması
3. `README.md` - ekosistem özellikleri ve rozetlerin güncellenmesi

---

## 🚀 3. aşamalı modüler icra yol haritası (3. kural: tek tur / tek modül)

her turda yalnızca tek bir bağımsız modül inşa edilecek, test edilecek, doğrulanacak ve kullanıcı onayı ile sıradakine geçilecektir:

### 📦 modül 1: github actions ci/cd otomatik doğrulama iş akışı (`besync-labs` paritesi)
- **amaç:** `.github/workflows/verify-kit.yml` tanımlanarak, her commit ve pull request'te ubuntu ve windows üzerinde `verify_kit.py` ve 43 sözleşme testinin otomatik koşması.
- **kapsam:**
  - matrix build: `windows-latest` ve `ubuntu-latest`.
  - python 3.11 ve 3.13 ortam doğrulaması.
  - `verify_kit.py --json` ve `checklist.py .` kalite kapısı yürütmesi.
- **doğrulama:** yaml sözdizim ve şema doğrulaması.

### 📦 modül 2: tek tıkla otonom kurulum ve dışa aktarma betikleri (`install.ps1` & `install.sh`)
- **amaç:** herhangi bir boş veya mevcut react, next.js, python, go, node veya rust projesine bu kiti tek komutla hatasız enjekte eden kurumsal yükleyici.
- **kapsam:**
  - `install.ps1` (powershell 5.1+ & 7+ uyumlu).
  - `install.sh` (posix bash uyumlu, linux & macos).
  - parametreler: `--target-dir`, `--mode` (solo / enterprise++), `--with-vault`.
  - idempotency: mevcut proje dosyalarına zarar vermeden `.agent/` ve kuralları harmanlama.
- **doğrulama:** geçici sanal dizinde test kurulumu.

### 📦 modül 3: resmi antigravity marketplace eklenti manifestosu (`plugin.json`) (`asoji` paritesi)
- **amaç:** kiti resmi `agy` cli ve marketplace platformuna tam uyumlu bir antigravity plugin'i haline getirmek.
- **kapsam:**
  - `plugin.json` oluşturulması (id, version, author, description, skills, agents, rules, configuration).
  - antigravity 2.0 marketplace standartlarına tam uyum.
- **doğrulama:** şema geçerlilik denetimi.

### 📦 modül 4: otonom github pr ve issue yöneticisi (`github_automator.py`) (`arindam-b` paritesi)
- **amaç:** geliştirici veya ajanların terminalden ayrılmadan, yapılan değişiklikleri ve test raporlarını doğrudan github pull request ve issue olarak açabilmesi.
- **kapsam:**
  - sıfır harici bağımlılık (dahili `urllib.request` veya `gh` cli entegrasyonu).
  - otomatik test ve kalite kapısı raporuyla zenginleştirilmiş pr şablonu oluşturma.
  - `--dry-run`, `--title`, `--body`, `--base`, `--head` parametreleri.
- **doğrulama:** kuru çalışma (`--dry-run`) testleri.

### 📦 modül 5: tarayıcısız medya ve transkript ayrıştırıcı (`media_extractor.py`) (`screencut` paritesi)
- **amaç:** `screencut` reposundaki en popüler özellik olan youtube transkript çıkarma, ses/video metadata analizi ve web medya içeriğini tarayıcı açmadan doğrudan CLI/API üzerinden sıfır ek yükle çıkarabilme.
- **kapsam:**
  - `.agent/scripts/media_extractor.py`: youtube video id veya url verildiğinde altyazı/transkript metnini çekme, zaman damgalarını ayıklama ve markdown formatında özet çıkarma.
  - video metadata (başlık, süre, yazar, açıklamalar) çözümleme.
  - agentların araştırma görevlerinde video içeriklerini saniyeler içinde analiz edebilmesini sağlama.
- **doğrulama:** test url'si ve mock transkript simülasyonu.

### 📦 modül 6: akıllı beceri toplayıcı ve kütüphane genişletmesi (`skill_aggregator.py`) (`sickn33` / `omer-metin` paritesi)
- **amaç:** açık kaynak depolardaki (`sickn33`, `omer-metin`, `rmyndharis`) binlerce beceriyi inceleyip filtreleyerek, eksik kurumsal ve niş becerileri bağlam şişkinliği yaratmadan (l0/l1 standartlarında) kütüphanemize güvenle dahil eden toplayıcı motor.
- **kapsam:**
  - `.agent/scripts/skill_aggregator.py`: github veya yerel dizinden `SKILL.md` dosyalarını tarama, yinelenenleri tespit etme, l0/l1 özetlerini çıkarma ve kütüphaneye mühürleme.
  - eksik kalan spesifik niş becerilerin (örneğin gömülü sistemler, mikroservis haberleşmesi vb.) kütüphaneye temiz oda disipliniyle eklenmesi.
- **doğrulama:** beceri tarama, doğrulama ve içe aktarım testleri.

### 📦 modül 7: kapsamlı ekosistem sözleşme testleri ve nihai master doğrulama
- **amaç:** eklenen tüm yeni yeteneklerin (ci/cd, installer, plugin, pr bot, media extractor, skill aggregator) sözleşmelerini doğrulayan test paketi yazmak ve master verifier ile mühürlemek.
- **kapsam:**
  - `.agent/scripts/tests/test_ecosystem_parity.py` oluşturulması.
  - toplam test sayısının 43'ten 50+'ye çıkarılması.
  - `verify_kit.py` ile 4 fazın tamamının (`PASS`) doğrulanması ve uzak depoya (`main`) aktarılması.

---

## 🛡️ 4. kural ve kalite güvencesi

- **kural ve kod kaybı:** sıfır. mevcut 48 kural, 20 ajan, 125 nöral düğüm ve 43 test korunacaktır.
- **token bütçesi:** tüm yeni araçlar bağımsız çalışacak ve `context_budget.py` tavanı (<4,000 token) asla aşılmayacaktır.
