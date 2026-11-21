---
id: clean-code-principles
title: "yalın kodlama ve katı kurumsal standartlar"
type: concept
tags:
  - clean-code
  - performance
  - security
created: 2026-11-21
updated: 2026-11-21
links:
  - "[[INDEX]]"
  - "[[architecture-overview]]"
  - "[[playbook-clean-architecture]]"
---

# 🧹 yalın kodlama ve kurumsal standartlar (clean code principles)

antigravity çatısı altında üretilen tüm kodların uymak zorunda olduğu mutlak kurallardır.

---

## ⚡ temel ilkeler
1. **aşırı mühendislik yasağı (anti-overengineering):** ihtiyacın ötesinde soyutlama veya hayali yapılar eklenemez.
2. **katı api güvenliği:** girdi doğrulama, rate limit ve idor/bola kontrolleri zorunludur.
3. **bellek hijyeni:** kapatılmamış soketler ve event listener bellek sızıntıları engellenir.
4. **n+1 sorgu engeli:** eager loading veya batch fetching uygulanır.

---

## 📌 ilgili bağlantılar
- ana indeks: [[INDEX]]
- sistem mimarisi: [[architecture-overview]]
- uygulama rehberi: [[playbook-clean-architecture]]
