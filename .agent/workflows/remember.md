---
name: remember
description: oturumlar arası hatırlama için bilgileri kalıcı belleğe kaydetme. tercihleri, standartları, kararları ve bağlamı saklar.
version: 1.0.0
requires_agents: orchestrator
requires_skills: memory-system
artifact_outputs: memory-entry
---

# /remember — kalıcı bellek ve baglam yonetimi

bu iş akışı, kullanıcının önemli tercihlerini, mimari kararlarını ve proje kurallarını .agent/memory/ altında kalıcı olarak saklar.

## 🎯 kaydedilecek bilgi veya karar
$ARGUMENTS

---

## 🧭 yürütme adimlari

1. **bilgi siniflandirma:**
   - `user_preferences.md`: kodlama stili, dil ve iletişim tercihleri.
   - `project_decisions.md`: veritabanı, güvenlik ve mimari kararlar (adr).
   - `environment_notes.md`: yerel portlar, test hesaplari ve arac konfigürasyonları.
2. **hassas veri denetimi (7. kural):**
   - api anahtarları, şifreler veya kişisel veriler asla düz metin kaydedilmez.
3. **yalinlastirma ve guncelleme:**
   - var olan bilgilerle birleştirilir, çakışıyorsa en son karar güncellenir.

---

## 🚨 katı kurallar

- tum kayıtlar küçük harfle ve türkçe karakterlerle yapılandırılır (1. kural).
- gizli belirteçler belleğe acik metin olarak işlenemez (7. kural).
