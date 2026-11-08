---
name: systematic-debugging
description: kök neden analizi ve kanıta dayalı doğrulama içeren 4 aşamalı sistematik hata ayıklama metodolojisi.
---

# sistematik hata ayıklama ilkeleri

bu beceri, karmaşık sistemlerdeki hataların tahmin yerine bilimsel ve kanıt odaklı bir süreçle çözülmesini sağlar.

## 4 aşamalı metodoloji

1. **aşama 1: belirtiyi anlama ve yeniden üretme**
   - hatayı tetikleyen adımları ve girdi verilerini belirleyin.
   - beklenen davranış ile gerçekleşen davranış arasındaki farkı netleştirin.

2. **aşama 2: kök neden hipotezleri geliştirme**
   - sistem akışını, logları ve çağrı yığınını (stack trace) inceleyerek olası nedenleri sıralayın.

3. **aşama 3: kanıtla doğrulama**
   - loglar, birim testler veya kırılma noktalarıyla hipotezi test edin; tahmin yürütmeyin.

4. **aşama 4: kalıcı çözüm ve regresyon koruması**
   - kök nedeni ortadan kaldırın ve bu hatanın bir daha yaşanmaması için otomatik test ekleyin.

## genel kural
- tüm açıklamalar küçük harflerle ve türkçe karakterler eksiksiz kullanılarak yazılmalıdır.
