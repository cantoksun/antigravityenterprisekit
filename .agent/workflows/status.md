---
description: projenin genel sağlık durumunu, kod kalitesini, güvenlik ve mimari uyumunu özetleyin.
priority: p1-workflow
version: 2.0.0
---

# proje durum ve sağlık değerlendirme iş akışı (/status)

bu iş akışı; `orchestrator` ve `security-auditor` liderliğinde projenin 18 temel kurala uyumunu, test durumunu, güvenlik açıklarını ve bellek sağlığını tek bir raporda özetlemeyi yönetir.

---

## 🚨 temel kurallar uyumu (en yüksek öncelik)

1. **türkçe ve küçük harf standardı:** tüm durum raporu küçük harfle ve türkçe karakterlerle (`ç, ğ, ı, ö, ş, ü`) hazırlanır (1. kural).
2. **sorgusuz modüler icra:** kullanıcıya soru sormadan sistem taraması ve checklist çalıştırılarak doğrudan durum raporlanır (2. kural).
3. **adım adım aşamalı yürütme:** denetimler modüler sıra ile taranır (3. kural).
4. **sıfır varsayım (18. kural):** bildirilen tüm metrikler ve dosya durumları gerçek dosya ve komut çıktılarına dayanır.

---

## 📊 kurumsal durum denetim protokolü

durum raporu oluşturulurken şu 4 denetim çalıştırılır:

1. **master checklist denetimi:**
   ```bash
   python .agent/scripts/checklist.py .
   ```
2. **güvenlik ve owasp denetimi (6., 7., 8., 14. kural):**
   - sabit şifre/sır var mı?
   - idor veya rls 42501 açığı var mı?
   - istemcide token depolaması yapılıyor mu?
3. **bellek ve sızıntı denetimi (9., 10., 13. kural):**
   - kapatılmamış dinleyiciler ve limitsiz döngüler var mı?
   - paginasyon veya lazy loading eksikliği var mı?
4. **tasarım ve ux denetimi (15. ve 16. kural):**
   - responsive dialog/drawer ayrımı uygulanmış mı?
   - font sayısı 2-3 (max 4-5) sınırında mı?

---

## 📋 standart durum raporu şablonu

```markdown
📋 **proje genel durum ve sağlık raporu:**

### 🛡️ güvenlik ve mimari uyum (18 kural)
- **api güvenliği & idor denetimi:** [uyumlu / riskler]
- **hassas veri ve oturum koruması:** [uyumlu, sır sızıntısı yok]
- **veritabanı & rls politikaları:** [uyumlu, 42501 ihlali yok]

### ⚡ performans ve bellek
- **bellek sızıntısı analizi:** [sızıntı tespit edilmedi]
- **sayfalama & lazy loading:** [endüstri standartlarında cursor/offset devrede]

### 🎨 arayüz ve deneyim (ux)
- **cihaz ayrımı:** [mobilde alt çekmece, masaüstünde modal devrede]
- **font disiplini:** [toplam [x] font ailesiyle sınırlandırıldı]

### 🧪 test ve doğrulama
- **master checklist:** [6/6 başarılı ✅]
```
