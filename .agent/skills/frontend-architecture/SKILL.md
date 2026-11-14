---
name: frontend-architecture
description: ön yüz kod mimarisi ve sorumluluk ayrımı (ui, mantık, veri, tip). dosya düzeni, durum katmanları, api servisleri ve doğrulama.
when_to_use: "ön yüz projesinin dizin ve katman mimarisi kurulurken; mantık, api istekleri ve durumun hangi katmanda yaşayacağı belirlenirken kullanılır."
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# ön yüz kod mimarisi (frontend architecture)

> ölçeklenebilir, bakımı kolay ve performanslı ön yüz mimarisi. klasör turu yerine sorumluluk ayrımı (separation of concerns).

## 🎯 4 katmanlı sorumluluk mimarisi

1. **sunum katmanı (ui / components):** saf bileşenler, props ile veri alır, yan etki (side-effect) içermez.
2. **mantik katmanı (hooks / composables):** is kuralları, reaktif durum yönetimi ve olay yöneticileri.
3. **veri ve servis katmanı (api / services):** http istekleri, fetch/axios soyutlamaları, etag ve önbellekleme.
4. **tip ve sema katmanı (types / schemas):** typescript arayüzleri, zod çalışma zamanı doğrulama şemaları.

## 🚨 temel kurallar

1. **tam responsive ve cihaz ayrımı (15. kural):** mobilde alt çekmece, masaüstünde modal pencereler.
2. **yatay taşma engeli (zero horizontal scroll):** tum ekran genişliklerinde kusursuz akış.
3. **guvenli veri yönetimi (14. kural):** client-side'da düz metin hassas veri saklama yasağı.
