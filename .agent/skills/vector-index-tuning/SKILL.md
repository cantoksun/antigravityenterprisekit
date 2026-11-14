---
name: vector-index-tuning
description: hnsw ve ivfflat indeks parametreleri, bellek/gecikme optimizasyonu, quantization (kuantalama) ve performans ince ayari.
when_to_use: "hnsw ve ivfflat indekslerinde gecikme, recall ve bellek kullanimini optimize ederken kullanilir."
allowed-tools: Read, Write, Edit, Grep, Bash
version: 1.0.0
---

# vektör indeks optimizasyonu ve ince ayar (vector index tuning)

> arama gecikmesi (latency), yakalama başarısı (recall) ve ram kullanımı arasindaki ödünleşimleri optimize edin.

## 🎯 indeks türleri ve parametreler

1. **hnsw (hierarchical navigable small world):**
   - yuksek yakalama başarısı, düşük sorgu gecikmesi.
   - `m` (bağlantı sayisi: 16-64) ve `efConstruction` (inşa derinligi: 64-256).
   - `efSearch`: çalışma zamanı gecikme/kalite dengesi (40-100).
2. **ivfflat (inverted file with flat):**
   - daha az ram tüketimi, büyük veri setlerinde hızlı eğitim.
3. **quantization (kuantalama):**
   - product quantization (pq) veya scalar quantization (sq) ile ram tuketiminde %75 tasarruf (9. kural).

## 🚨 temel kurallar

1. **once ölçüm (performans ilkesi):** parametre değişiklikleri recall ve latency testleriyle kanıtlanır.
2. **canli sistem güvencesi (39. kural):** büyük vektör indeks inşası arka planda yapilir, canlı trafiği kilitlemez.
