---
description: projeyi güvenli, sıfır kesintili ve doğrulanmış biçimde canlı ortama dağıtın.
priority: p1-workflow
version: 2.0.0
---

# kurumsal canlıya alma ve dağıtım iş akışı (/deploy)

bu iş akışı; uygulamanın üretim ortamına taşınması öncesinde güvenlik, kalite, veritabanı ve performans denetimlerini çalıştırarak sıfır kesintili dağıtımı yönetir.

---

## 🚨 temel kurallar uyumu (en yüksek öncelik)

1. **türkçe ve küçük harf standardı:** tüm çıktılar, açıklamalar ve yönlendirmeler küçük harfle ve türkçe karakterlerle (`ç, ğ, ı, ö, ş, ü`) yazılır (1. kural).
2. **sorgusuz modüler icra:** dağıtım adımları kullanıcıya gereksiz sorular sorulmadan standart 5 aşamalı prosedürle doğrudan icra edilir (2. kural).
3. **adım adım aşamalı yürütme:** dağıtım öncesi doğrulama, derleme, migration ve canlıya alma sırayla işletilir (3. kural).
4. **hassas verilerin mutlak korunması:** üretim anahtarları veya veritabanı şifreleri repoya ya da derleme loglarına asla sızdırılmaz (7. kural).
5. **bellek ve sızıntı denetimi:** dağıtılacak yapıda açık kalan soket veya kontrolsüz bellek büyümeleri taranır (9. ve 10. kural).
6. **veritabanı rls uyumu:** migration sonrası satır düzeyi yetkiler (42501) kontrol edilir (12. kural).

---

## 🚀 dağıtım öncesi zorunlu denetim boru hattı

dağıtım komutu tetiklendiğinde `devops-engineer` ve `security-auditor` liderliğinde şu sıra işletilir:

```plaintext
1. statik analiz ──► 2. güvenlik taraması ──► 3. test paketi ──► 4. migration ──► 5. canlıya alma
```

### 1. adım: master checklist denetimi
dağıtım öncesi master denetim betiği çalıştırılır:
```bash
python .agent/scripts/checklist.py .
```
- tüm güvenlik, lint, şema, test, ux ve seo kontrolleri **başarılı (passed)** olmalıdır.
- herhangi bir hata durumunda dağıtım durdurulur ve kritik açık giderilene kadar devam edilmez.

### 2. adım: ortam değişkenleri ve sır doğrulaması (7. kural)
- üretim ortamında `.env` içindeki zorunlu alanların (`DATABASE_URL`, `JWT_SECRET`, `API_KEY`) dolu olduğu ve varsayılan test değerlerinde kalmadığı doğrulanır.

### 3. adım: geriye dönük uyumlu migration (12. kural)
- veritabanı geçişi canlı trafik kesilmeden uygulanır; eski çalışan sürümün çalışmasını bozacak kırıcı şema değişiklikleri engellenir.

### 4. adım: konteyner ve sıfır kesintili geçiş (blue-green)
- yeni sürüm ayağa kaldırılır.
- `/api/health` uç noktası 200 dönene kadar eski sürüme trafik yönlendirilmeye devam edilir.
- doğrulama tamamlandığında yük dengeleyici (load balancer) trafiği yeni sürüme aktarır.

### 5. adım: anında geri alma (rollback) garantisi
- dağıtım sonrası 5xx hata oranları izlenir; beklenmeyen bir çökme anında tek tıkla önceki kararlı sürüme geri dönülür.
