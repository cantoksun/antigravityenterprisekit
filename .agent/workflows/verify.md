---
name: verify
description: kod değişikliklerinin çalıştığını fiilen çalıştırarak doğrulama. yalnızca denetimle degil, çalıştırarak kanıtlar.
version: 1.0.0
requires_agents: test-engineer
requires_skills: verify-changes, lint-and-validate
artifact_outputs: verification-report
---

# /verify — değişiklikleri çalıştırarak kanitlama

bu iş akışı, yazılan veya düzenlenen kodun sadece var olduğunu degil, gerçekten sorunsuz çalıştığını doğrulamak için test ve derleme ortamlarını işletir.

## 🎯 doğrulanacak modul veya degisiklik
$ARGUMENTS

---

## 🧭 yürütme adimlari

1. **derleme ve tip denetimi (build & typecheck):**
   - projenin derleme komutlari (`npm run build`, `cargo check`, `tsc`) calistirilir.
2. **test kosturucu (test runner):**
   - ilgili birim veya entegrasyon testleri calistirilarak dogrulanir.
3. **otonom onarim (self-healing - 17. kural):**
   - karsilasilan söz dizimi veya lint hataları kullaniciya sorulmadan otomatik düzeltilir.
4. **checklist denetimi:**
   - `checklist.py .` calistirilarak güvenlik, sema ve kalite kontrolleri onaylanir.

---

## 🚨 katı kurallar

- tum raporlar küçük harflerle ve türkçe karakterlerle yazilir (1. kural).
- test ciktisi görülmeden ve kanıtlanmadan başarılı sayılamaz (18. kural).
