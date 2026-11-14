---
name: threat-modeling-expert
description: stride metodolojisi, saldırı agaclari, güvenlik mimarisi incelemesi ve tasarimda güvenlik (secure-by-design) ilkeleri.
when_to_use: "sistem tasarim asamasindayken stride metodolojisiyle tehdit ve risk modellemesi yapilirken kullanilir."
allowed-tools: Read, Write, Grep, Glob
version: 1.0.0
---

# tehdit modelleme uzmanlığı (threat modeling expert)

> sistem inşa edilmeden önce saldırı yüzeylerini, güven sınırlarını ve potansiyel riskleri bilimsel olarak modelleyin.

## 🎯 stride tehdit modeli analizi

1. **spoofing (kimlik taklidi):** güçlü kimlik doğrulama, mfa ve jwt imza denetimi.
2. **tampering (veri değiştirme):** hmac imzaları (35. kural), tls şifreleme, veri tabani bütünlüğü.
3. **repudiation (inkar etme):** değişmez denetim kayıtları (audit logs) (22. kural).
4. **information disclosure (bilgi ifşası):** hassas veri şifreleme (7. kural), güvenli hata mesajları.
5. **denial of service (hizmet engelleme):** hiz sınırlaması (rate limit) (41. kural), devre kesici (28. kural).
6. **elevation of privilege (yetki yükseltme):** nesne ve fonksiyon düzeyi erişim kontrolü (idor/bola) (8. kural).

## 🚨 temel kurallar

1. **sokratik kapi:** mimari riskler tasarim aşamasında sorularla netleştirilir.
2. **delile dayalı tespit:** varsayimsal degil, veri akış şeması (dfd) uzerinden risk çıkartılır.
