---
name: batch-operations
description: birden fazla dosyada eşzamanlı toplu işlem ve kalıp bazli değişiklikler. kod tabanı genelinde arama-degistirme ve tutarlı düzenlemeler.
when_to_use: "kullanıcı aynı kalıpla birden fazla dosyayi değiştirmek istediğinde, genel yeniden adlandirma, çoklu ice aktarma veya sürüm güncelleme durumlarında kullanılır. tek dosya düzenlemeleri için kullanılmaz."
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
version: 1.0.0
effort: medium
---

# toplu işlemler (batch operations) — çoklu dosya degisiklikleri

> cok sayıda dosyada tutarlı değişiklikleri tek seferde uygulayın. tek bir kalıp, birden fazla hedef.

## 🎯 genel bakış ve amac

bu beceri, kod tabaninda birden cok dosyayi etkileyen operasyonlari güvenli, atomik ve tutarlı bir şekilde yurutur:
- kod tabanı genelinde arama ve değiştirme (search & replace)
- import/export yollarını ve paket adlarini toplu guncelleme
- sürüm numaralarini ve bagimlilik sürümlerini senkronize etme
- kurumsal mimari değişikliklerinde çoklu dosya uyarlamalari

## 🚨 temel kurallar ve kisitlar

1. **kesin varlik doğrulaması (18. kural):** degistirmeden once her dosyanin varlığını ve içeriğini teyit edin.
2. **yedekleme ve geri alma guvencesi:** toplu operasyon öncesi git çalışma ağacının temiz olduğundan emin olun.
3. **tam dogrulama:** degisiklik sonrası lint ve test çalıştırarak kırılma olmadığını kanıtlayın.
4. **uslup standardi:** tum açıklamalar ve raporlar küçük harfle, türkçe karakterlerle yapılandırılır.
