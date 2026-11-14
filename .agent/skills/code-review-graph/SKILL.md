---
name: code-review-graph
description: tree-sitter ast ve mcp tabanlı token tasarruflu kod inceleme. büyük kod tabanlarinda tum kodu okumak yerine etki alanını analiz eder.
when_to_use: "büyük kod tabanlarinda (500+ dosya), token maliyetlerini düşürmek gerektiğinde, monorepolarda veya çoklu dosya bağımlılıklarında kullanılır."
allowed-tools: Read, Grep, Glob, Bash
version: 1.0.0
effort: medium
---

# kod inceleme grafiği (code review graph) — ast ve mcp tabanlı analiz

> büyük kod tabanlarinda her seyi körü körüne okumak yerine yapısal harita çıkararak yapay zeka token tüketimini radikal bicimde azaltın.

## 🎯 genel bakış ve amac

kod inceleme grafiği, değişikliklerin etki alanını (blast radius) ast seviyesinde cikarir:
- yalnızca doğrudan değişen ve bunlara bağımlı olan dosyaları tespit eder
- ölü kod (dead code) ve yetim fonksiyonları ortaya cikarir
- mimari sınır ihlallerini ve döngüsel bağımlılıkları gorsellestirir
- sqlite graf veritabanı üzerinden hızlı yapısal sorgulama saglar

## 🚨 temel kurallar

1. **oncelikli performans ve bellek optimizasyonu (9. kural):** büyük repolarda gereksiz dosya okumalarindan kaçının.
2. **nesne seviyesinde yetki ve guvenlik (8. kural):** graf analizi yaparken guvenlik açıklarının etki alanını netleştirin.
3. **dogrulama ve temiz oda prensibi:** elde edilen bulguları somut testlerle destekleyin.
