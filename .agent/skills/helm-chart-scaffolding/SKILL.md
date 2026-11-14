---
name: helm-chart-scaffolding
description: kubernetes uygulamalarini paketleme, helm chart sablonlama, values.yaml hiyerarşisi ve coklu ortam yönetimi.
when_to_use: "kubernetes uygulamalarini helm paketlerine donustururken ve coklu ortam degerlerini yonetirken kullanilir."
allowed-tools: Read, Write, Edit, Glob
version: 1.0.0
---

# helm chart yapılandırması (helm chart scaffolding)

> kurumsal kubernetes uygulamalarini yeniden kullanılabilir, sürümlenmiş ve modüler helm paketlerine dönüştürme.

## 🎯 paket mimarisi ve ilkeler

- **values.yaml standardi:** varsayilan güvenli değerler (production-safe defaults).
- **ortam ayriligi:** `values-dev.yaml`, `values-staging.yaml`, `values-prod.yaml` hiyerarşisi.
- **sablonlama disiplini:** `_helpers.tpl` icinde tutarli adlandırma ve etiketleme (labels).
- **bagimlilik yonetimi:** `Chart.yaml` üzerinde net semantik sürümleme (semver).

## 🚨 temel kurallar

1. **sadelik ve modern teknolojiler (4. kural):** gereksiz karmaşık golang sablon fonksiyonlarindan kaçının.
2. **kullaniciyi yormama (17. kural):** chart kurulum komutlarını açık ve dogrulanmis iletin.
