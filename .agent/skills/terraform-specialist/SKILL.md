---
name: terraform-specialist
description: terraform iac (kod olarak altyapı), modüler mimari, remote state kilitleme ve güvenli bulut altyapisi yönetimi.
when_to_use: "terraform iac modulleri, bulut altyapisi ve state yonetimi yapilandirilirken kullanilir."
allowed-tools: Read, Write, Edit, Glob, Bash
version: 1.0.0
---

# terraform altyapı uzmanlığı (terraform specialist)

> modüler, sürümlendirilebilir, tekrarlanabilir ve güvenli bulut kaynakları mimarisi.

## 🎯 terraform yonetim prensipleri

1. **durum yönetimi (state management):**
   - yerel state yasaktir; s3/gcs/azure blob üzerinde şifrelenmiş `remote backend`.
   - çakışmaları önlemek için dinamik durum kilidi (`dynamodb_table` veya k8s lock) (33. kural).
2. **moduler mimari:**
   - ağ (vpc), küme (k8s) ve veritabanı (rds) katmanları bağımsız modullere ayrılır.
   - değişkenler tipli ve açıklamalı (`variable "x" { type = string }`) tanımlanır (26. kural).
3. **guvenlik ve sirlar:**
   - tf dosyalarına asla credential gomulmez; ortam değişkenleri veya vault/kms kullanılır (7. kural).

## 🚨 temel kurallar

1. **planlama ve onay disiplini:** `terraform plan` çıktısı doğrulanmadan `apply` yapılmaz.
2. **sifir varsayım (18. kural):** mevcut kaynaklar teyit edilir, `terraform import` dikkatle yönetilir.
