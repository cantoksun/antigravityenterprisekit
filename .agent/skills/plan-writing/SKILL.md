---
name: plan-writing
description: açık kırılımlar, bağımlılıklar ve doğrulama kriterleri içeren yapılandırılmış görev planlaması.
priority: p1-structural
version: 2.0.0
---

# kurumsal yapılandırılmış planlama ve görev kırılım standartları

bu beceri; karmaşık yazılım geliştirme süreçlerini mantıksal, bağımsız, ölçülebilir ve adım adım (3. kural) ilerleyen kurumsal planlara dönüştürmeyi yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 16 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır (1. kural).
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz (2. kural).
   - adım adım aşamalı yürütülür; her turda tek bir bağımsız modül/aşama tamamlanır (3. kural).
   - sadelik ve modern trend teknolojiler (4. kural).
   - veri mimarisi (5. kural), katı api güvenliği (6. kural), hassas veri koruması (7. kural) ve idor önleme (8. kural) plan aşamasında netleştirilir.
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki planlama standartları.

---

## 📋 kurumsal plan dokümanı şablonu (`{gorev-kodu}.md`)

karmaşık bir geliştirme veya dönüşüm planlanırken şu standart yapı kullanılır:

```markdown
# [görev başlığı]

> [görevin tek cümlelik kurumsal hedefi]

---

## 1. mimari genel bakış ve kapsam
- **kapsam:** [geliştirilecek veya dönüştürülecek modüller]
- **kapsam dışı:** [bu aşamada yapılmayacak işler]
- **teknoloji yığını:** [kullanılacak modern ve sade teknolojiler - 4. kural]

---

## 2. bağımlılıklar ve risk analizi
- **önkoşul bağımlılıkları:** [önceden tamamlanması gereken servisler veya şemalar]
- **güvenlik ve hassas veri kontrolü:** [6. ve 7. kural uyumu]
- **idor/yetki kontrolü:** [8. kural uyumu]

---

## 3. aşamalı modüler görev kırılımı (3. kural uyumu)

### aşama 1: [ilk bağımsız modül adı]
- [ ] görev 1.1: [yapılacak somut işlem]
- [ ] görev 1.2: [yapılacak somut işlem]
- **doğrulama kriteri:** [bu aşamanın bittiğini kanıtlayan birim test veya linter komutu]

### aşama 2: [ikinci bağımsız modül adı]
- [ ] görev 2.1: [yapılacak somut işlem]
- **doğrulama kriteri:** [entegrasyon testi veya kontrol komutu]

### aşama 3: [üçüncü bağımsız modül adı]
- [ ] görev 3.1: [yapılacak somut işlem]
- **doğrulama kriteri:** [e2e testi veya nihai kontrol listesi]
```

---

## 🎯 planlama altın kuralları

1. **ölçülebilir doğrulama:** bir görev maddesi "tamamlandı" sayılabilmek için mutlaka çalıştırılabilir bir test veya kontrol komutuna (`test_runner.py`, `vitest`, `tsc`) dayanmalıdır.
2. **bağımsızlık:** her aşama kendi içinde tamamlanabilir ve test edilebilir olmalıdır; aşamalar arasında gereksiz kilitlenmeler önlenmelidir.
3. **üslup disiplini:** plandaki tüm başlıklar, açıklamalar ve maddeler istisnasız küçük harflerle ve türkçe karakterlerle yazılmalıdır.
