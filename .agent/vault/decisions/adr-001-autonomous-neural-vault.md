---
id: adr-001-autonomous-neural-vault
title: "adr 001: obsidian uyumlu otonom nöral bilgi ağının (neural vault) benimsenmesi"
status: accepted
date: 2026-11-21
tags:
  - adr
  - architecture
  - memory
links:
  - "[[INDEX]]"
  - "[[architecture-overview]]"
---

# ⚖️ adr 001: otonom nöral bilgi ağının benimsenmesi

## 1. bağlam (context)
klasik claude ve obsidian entegrasyonları, yapay zekanın sadece notları okuduğu veya kullanıcının manuel link verdiği pasif bir modelle sınırlıdır. çoklu ajan mimarimizde ajanların bağımsız olarak bilgi kaydettiği, `[[wikilink]]` ile çift yönlü bağ kurduğu ve kullanıcının doğrudan obsidian ile görselleştirebileceği yaşayan bir hafıza gerekmektedir.

## 2. karar (decision)
`.agent/vault/` dizini altında obsidian uyumlu tam bir yerel vault yapısının kurulmasına karar verilmiştir.
- çift yönlü bağlantı: `[[dosya-adi]]` standardı.
- klasör yapısı: `concepts/`, `decisions/`, `playbooks/`, `episodes/`.
- grafik renkleri ve görünüm: `.obsidian/graph.json` üzerinden otomatik renk kodlu.

## 3. sonuçlar (consequences)
- **olumlu:** kullanıcı projeyi obsidian'da tek tıkla açıp interaktif graph view ile ajanların ürettiği tüm mimariyi zihin haritası olarak izleyebilir.
- **olumlu:** token tasarruflu, yalnızca ilgili düğümleri çağıran yerel nöral bellek altyapısı kazanıldı.

---

## 📌 ilgili bağlantılar
- ana indeks: [[INDEX]]
- sistem mimarisi: [[architecture-overview]]
