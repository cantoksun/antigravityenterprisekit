---
name: coordinate
description: paralel dağıtım ve sentez ile gelişmiş çoklu ajan koordinasyonu. birden fazla uzmanın perspektifini gerektiren karmaşık görevlerde kullanılır.
version: 1.0.0
requires_agents: orchestrator
requires_skills: coordinator-mode, parallel-agents
artifact_outputs: coordination-plan, phase-status
---

# /coordinate — gelişmiş çoklu ajan koordinasyonu ve görev sentezi

bu iş akışı, karmaşık ve cok disiplinli gorevleri paralel uzman ajanlara paylaştırır, sonuçları sentezler ve moduler ilerlemeyi yönetir.

## 🎯 incelenecek konu veya gorev
$ARGUMENTS

---

## 🧭 yürütme adımları ve davranış modeli

1. **gorev ayrıştırma ve uzman secimi:**
   - talep bağımsız alt modullere bölünür.
   - her modul için en uygun birincil uzman ajan (frontend, backend, güvenlik, mobil vb.) belirlenir.
2. **paralel görevlendirme ve sınır tanimi:**
   - her ajana net sorumluluk alanı ve cikti formatı atanır.
   - 46 p0 temel kural hiyerarşisine tam uyum şartı koşulur.
3. **sonuc sentezi ve kural uyumu:**
   - uzmanlardan gelen çıktılar birleştirilir.
   - çelişen kararlar p0 kurallari doğrultusunda çözülür.
4. **seffaf raporlama ve onay kapısı (3. kural):**
   - tamamlanan modul raporlanır, sıradaki modul için kullanıcı onayı beklenir.

---

## 🚨 katı kurallar

- tum açıklamalar ve raporlar küçük harflerle ve türkçe karakterler (c, g, i, o, s, u) eksiksiz kullanilarak yazılmalıdır.
- tek turda yalnızca tek bir modul icra edilir; kullanıcı onay vermeden sonraki aşamaya geçilemez (3. kural).
