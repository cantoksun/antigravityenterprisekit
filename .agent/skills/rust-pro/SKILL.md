---
name: rust-pro
description: modern rust (2024 sürümü) geliştirme standartları. asenkron akışlar (tokio/axum), sistem güvenliği, sıfır maliyetli soyutlama ve masaustu sistemler.
when_to_use: "rust projelerinde, .rs dosyalarında, cargo.toml yönetiminde, axum web servislerinde, tauri veya slint masaustu uygulamalarında kullanılır."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---

# modern rust uzmanlığı (rust-pro) — sistem ve masaustu mimarisi

> modern rust standartları, sıfır maliyetli soyutlama, bellek güvenliği ve yuksek performanslı kurumsal sistemler.

## 🎯 genel bakış ve masaustu ekosistemi

- **masaustu mimarisi:** saf yerel gui için slint, egui veya iced; zengin web tabanlı masaustu için hafif tauri hibriti.
- **asenkron servisler:** tokio çalışma zamanı ve axum mikroservis altyapısı.
- **guvenlik ve bellek:** unsafe bloklarından mutlak kaçınma, raii prensipleri ve sıfır bellek sızıntısı güvencesi.

## 🚨 temel kurallar

1. **oncelikli performans ve bellek (9. ve 10. kural):** kaynak sızıntılarını ve cpu kilitlenmelerini derleme aşamasında önleyin.
2. **kati api güvenliği (6. kural):** girdi doğrulaması ve tip seviyesinde guvenlik denetimi uygulayın.
