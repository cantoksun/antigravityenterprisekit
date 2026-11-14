---
name: verify-changes
description: kodun çalıştığını sadece varligina bakarak degil, fiilen çalıştırarak kanıtlama. denetim yerine çalıştırma yoluyla doğrulama.
when_to_use: "kod yazıldıktan, bir özellik tamamlandıktan veya hata giderildikten sonra; kullanıcı 'calisiyor mu?', 'test et', 'dogrula' dediğinde kullanılır."
allowed-tools: Read, Bash, Grep, Glob
version: 1.0.0
effort: medium
---

# değişiklikleri doğrula (verify changes) — çalıştırarak kanitlama

> 'var olan kod' ile 'calisan kod' aynı şey değildir. bu beceri, tum değişikliklerin fiilen çalıştırılarak doğrulanmasını zorunlu kılar.

## 🎯 doğrulama hiyerarsisi

1. **derleme ve sozdizimi denetimi:** kodun hatasız derlendiğini ve tip denetiminden geçtiğini doğrulayın.
2. **birim ve entegrasyon testleri:** ilgili testleri koşturun, kırılma olmadığını kanıtlayın.
3. **uctan uca / arayüz denetimi:** servisleri ayağa kaldirarak yerel adresi (localhost:PORT) kontrol edin.
4. **guvenlik ve lint taramasi:** checklist.py çalıştırarak kalite standartlarını onaylayın.

## 🚨 temel kurallar

1. **kullaniciyi yormama (17. kural):** derleme veya test hatalarını kullaniciya sormadan kendi kendine onarin (self-healing).
2. **sifir varsayım (18. kural):** test çıktısını görmeden 'calisiyor' iddiasında bulunmayın.
