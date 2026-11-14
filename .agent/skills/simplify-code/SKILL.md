---
name: simplify-code
description: asiri mühendislik yapılmış kodun karmaşıklığını azaltma. gereksiz soyutlamaları kaldırma, ölü kod temizliği ve mantığı yalınlaştırma.
when_to_use: "kod asiri karmaşık, derin ic ice geçmiş veya gereksiz soyutlamalarla şişmiş oldugunda; kullanıcı 'sadelestir', 'temizle' dediğinde kullanılır."
allowed-tools: Read, Write, Edit, Grep, Glob
version: 1.0.0
effort: medium
---

# kodu sadeleştirme (simplify code) — asiri mühendisliği engelleme

> en iyi kod, yazılması gerekmeyen koddur. ikinci en iyi kod ise herkesin kolayca anlayabildiği koddur.

## 🎯 sadeleştirme prensipleri

1. **erken dönüş (early return):** derin ic ice if/else bloklarını düzleştirin, okunabilirliği artırın.
2. **gereksiz katmanları kaldirma:** tek bir yerde kullanılan ve deger katmayan mikro yardımcıları doğrudan çağrı yerine taşıyın.
3. **olu kod temizligi:** kullanılmayan fonksiyonları, importlari ve gecici yorumları temizleyin.

## 🚨 temel kurallar

1. **sadelik ve modern trend teknolojiler (4. kural):** her zaman en sade ve anlaşılır yöntemi tercih edin.
2. **kesin varlik doğrulaması (18. kural):** sadeleştirme yaparken mevcut işlevselliği bozmayın, testlerle doğrulayın.
