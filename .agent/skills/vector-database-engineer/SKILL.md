---
name: vector-database-engineer
description: pgvector, qdrant, pinecone ve weaviate üzerinde vektör indeksleme, semantik arama ve meta veri filtreleme.
when_to_use: "pgvector, qdrant, pinecone vektor veritabanlarinda indeksleme ve meta veri filtreleme yapilirken kullanilir."
allowed-tools: Read, Write, Edit, Grep
version: 1.0.0
---

# vektör veritabanı uzmanlığı (vector database engineer)

> yuksek boyutlu gömümlerin verimli depolanması, indekslenmesi ve milisaniye seviyesinde benzerlik araması.

## 🎯 veritabanı seçimi ve kalip

- **iliskisel + vektör hibriti:** postgresql üzerinde `pgvector` (5. kural yalın veritabanı ilkesiyle tam uyumlu).
- **ozellestirilmis vektör motoru:** büyük ölçekli sistemlerde `qdrant` veya `pinecone`.
- **meta veri filtreleme:** sorgu maliyetini düşürmek için arama öncesi (pre-filtering) meta veri kısıtlaması.

## 🚨 temel kurallar

1. **sayfalama disiplini (11. kural):** benzerlik sorgularında limitsiz arama yapilamaz; `limit` ve `score_threshold` zorunludur.
2. **rls ve yetki denetimi (8. ve 12. kural):** kullanıcılar yalnızca kendi erişim yetkisinde olan doküman vektörlerini sorgulayabilir.
