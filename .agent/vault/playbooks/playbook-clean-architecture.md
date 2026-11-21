---
id: playbook-clean-architecture
title: "temiz mimari ve servis katmanı uygulama rehberi"
type: playbook
tags:
  - playbook
  - patterns
  - backend
created: 2026-11-21
updated: 2026-11-21
links:
  - "[[INDEX]]"
  - "[[clean-code-principles]]"
---

# 📖 temiz mimari uygulama rehberi (playbook)

bu playbook, yeni bir servis veya backend bileşeni inşa edilirken izlenecek standartları tanımlar.

---

## 🏗️ katman düzeni
```text
src/
├── domain/       # saf iş mantığı ve tipler (harici bağımlılık yok)
├── services/     # kullanım senaryoları ve orkestrasyon
├── repositories/ # veritabanı ve dış kaynak erişimi
└── api/          # uç noktalar, girdi doğrulama (zod) ve güvenlik
```

---

## 📌 ilgili bağlantılar
- ana indeks: [[INDEX]]
- temiz kod kuralları: [[clean-code-principles]]
