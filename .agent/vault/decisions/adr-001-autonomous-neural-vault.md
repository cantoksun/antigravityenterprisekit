---
id: adr-001-autonomous-neural-vault
title: "adr 001: antigravity kitine özgü bağımsız nöral bilgi ağının (neural vault) benimsenmesi"
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

# ⚖️ adr 001: kite özgü otonom nöral bilgi ağının benimsenmesi

## 1. bağlam (context)
harici üçüncü parti masaüstü uygulamaları kullanıcının ortam değiştirmesini gerektirir ve kite bağımlılık getirir. çoklu ajan mimarimizde ajanların bağımsız olarak bilgi kaydettiği, `[[wikilink]]` ile çift yönlü bağ kurduğu ve kitin kendi içindeki web sunucusu üzerinden görselleştirilebilen bağımsız bir ikinci beyin gerekmektedir.

## 2. karar (decision)
`.agent/vault/` dizini altında harici hiçbir masaüstü aracına ihtiyaç duymayan, tamamen kitin kendi web canvas motoruyla çalışan yerel bir vault yapısının kurulmasına karar verilmiştir.
- çift yönlü bağlantı: `[[dosya-adi]]` standardı.
- klasör yapısı: `concepts/`, `decisions/`, `playbooks/`, `episodes/`.
- grafik arayüzü: kitin yerleşik `http://127.0.0.1:8990` web paneli üzerinden kuvvet odaklı fizik motoru.

## 3. sonuçlar (consequences)
- **olumlu:** kullanıcı harici hiçbir uygulama kurmadan doğrudan tarayıcıdan interaktif zihin haritasını izleyebilir.
- **olumlu:** token tasarruflu, yalnızca ilgili düğümleri çağıran yerel nöral bellek altyapısı kazanıldı.

---

## 📌 ilgili bağlantılar
- ana indeks: [[INDEX]]
- sistem mimarisi: [[architecture-overview]]
