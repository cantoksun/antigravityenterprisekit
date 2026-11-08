---
description: karmaşık ve çok disiplinli görevlerde birden fazla uzman ajanın koordinasyonu, modüler iş bölümü ve aşamalı yürütme prosedürü.
---

# 🎼 çoklu ajan orkestrasyonu (multi-agent orchestration)

bu iş akışı birden fazla uzmanlık alanı gerektiren karmaşık görevlerde, uzman ajanları modüler bir hiyerarşiyle koordine eder.

## 🎯 yürütülecek görev
$ARGUMENTS

---

## 🚨 temel orkestrasyon kuralı: minimum ajan gereksinimi

> ⚠️ **orkestrasyon = en az 3 farklı uzman ajanın devreye girmesi demektir.**
>
> 3'ten az ajan kullanılıyorsa bu bir orkestrasyon değil, yalnızca basit bir yetkilendirmedir.
> 
> **tamamlama öncesi doğrulama:**
> - görevlendirilen ajan sayısını kontrol edin.
> - `ajan_sayısı < 3` ise durun ve ilgili alan uzmanlarını dahil edin.

### 📋 görev türü ve asgari ajan eşleşme matrisi

| görev türü | zorunlu asgari uzman ajanlar |
|---|---|
| **web uygulaması** | `frontend-specialist`, `backend-specialist`, `test-engineer` |
| **api ve servisler** | `backend-specialist`, `security-auditor`, `test-engineer` |
| **arayüz ve tasarım** | `frontend-specialist`, `performance-optimizer`, `seo-specialist` |
| **veritabanı ve modelleme** | `database-architect`, `backend-specialist`, `security-auditor` |
| **uçtan uca tam yığın (full stack)**| `project-planner`, `frontend-specialist`, `backend-specialist`, `qa-automation-engineer` |
| **hata ayıklama ve düzeltme** | `debugger`, `explorer-agent`, `test-engineer` |
| **güvenlik denetimi ve sızma** | `security-auditor`, `penetration-tester`, `devops-engineer` |

---

## 🛑 2 aşamalı katı yürütme modeli (3. ve 19. kural uyumlu)

### aşama 1: planlama ve keşif (sıralı yürütme)
1. `explorer-agent`: mevcut kod tabanını, bağımlılıkları ve varlıkları haritalandırır (18. kural - kesin varlık doğrulaması).
2. `project-planner`: teknik görev kırılımını ve modüler adımları belirler.

### aşama 2: modüler ve şeffaf icra (aşamalı yürütme)
- **temel katman**: `database-architect` (yalın şema, 5. kural) + `security-auditor` (idor/bola taraması, 8. kural).
- **çekirdek mantık**: `backend-specialist` (katı api güvenliği, 6. kural) + `frontend-specialist` (responsive ux, drawer/modal ayrımı, 15. kural).
- **kalite ve doğrulama**: `qa-automation-engineer` (playwright e2e) + `performance-optimizer` (bellek sızıntısı analizi, 10. kural).

> 🔴 **şeffaf aşama taahhüdü (19. kural):** iş parçalara bölündüğünde tamamlanan aşama ile kalan aşamalar kullanıcıya açıkça bildirilir; kullanıcı "eksik mi yapıldı?" şüphesine düşürülmeden kalan adımlar proaktif olarak tamamlanır.

---

## 🚨 katı kurallar

- tüm metinler, başlıklar ve raporlar istisnasız küçük harflerle ve türkçe karakterler (ç, ğ, ı, ö, ş, ü) eksiksiz kullanılarak yazılmalıdır.
- kullanıcıya gereksiz sorular sormadan doğrudan analiz ve modüler icra (2. kural) uygulanmalıdır.
