---
id: architecture-overview
title: "kurumsal sistem mimarisi ve bileşen haritası"
type: concept
tags:
  - architecture
  - c4-model
  - enterprise
created: 2026-11-21
updated: 2026-11-21
links:
  - "[[INDEX]]"
  - "[[clean-code-principles]]"
  - "[[adr-001-autonomous-neural-vault]]"
---

# 🏛️ kurumsal sistem mimarisi (architecture overview)

bu düğüm, antigravity ekosisteminin çekirdek mimari bileşenlerini, ajan sorumluluklarını ve veri akış hiyerarşisini tanımlar.

---

## 🧩 mimari bileşenler ve etkileşim şeması

```mermaid
flowchart TD
    user["kullanıcı talebi / komut"] --> router["intelligent routing"]
    router --> orch["orchestrator (ana koordinatör)"]
    
    subgraph agents ["uzman yapay zeka ajanları"]
        orch --> front["frontend-specialist"]
        orch --> back["backend-specialist"]
        orch --> sec["security-auditor"]
        orch --> db["database-architect"]
    end
    
    subgraph neural_vault ["🧠 antigravity neural-os (yerel bilgi ağı)"]
        front <--> vault_concepts["concepts / bilgi düğümleri"]
        back <--> vault_decisions["decisions / adr kayıtları"]
        sec <--> vault_playbooks["playbooks / güvenlik & tasarım"]
        db <--> vault_episodes["episodes / oturum hafızası"]
    end
    
    agents --> delivery["sıfır kesintili dağıtım & doğrulama"]
```

---

## 📌 ilgili bağlantılar
- ana indeks: [[INDEX]]
- kodlama ilkeleri: [[clean-code-principles]]
- mimari karar: [[adr-001-autonomous-neural-vault]]
