---
name: rag-implementation
description: üretim seviyesinde rag (retrieval-augmented generation) mimarisi. parçalama (chunking), hibrit arama ve yeniden sıralama.
when_to_use: "retrieval-augmented generation (rag), dokuman parcalama ve hibrit arama akislari insa edilirken kullanilir."
allowed-tools: Read, Write, Edit, Grep
version: 1.0.0
---

# kurumsal rag mimarisi (rag implementation)

> yuksek doğruluklu, kaynak referanslı (grounded) ve düşük yanılsamalı (low hallucination) kurumsal rag boru hatlari.

## 🎯 4 aşamalı rag boru hatti

1. **belge işleme ve parçalama (chunking):**
   - anlamsal parçalama (semantic chunking), 400-800 token aralığı, %10-15 başlık örtüşmesi (overlap).
2. **vektorlestirme ve gömümler (embeddings):**
   - amaca uygun model seçimi (text-embedding-3, bge-large), boyut optimizasyonu.
3. **hibrit arama (hybrid retrieval):**
   - vektör yakınlığı (dense) + kelime eşleşmesi (bm25 sparse) birleştirilir.
4. **yeniden sıralama (reranking):**
   - cross-encoder ile en alakah ilk 3-5 parça modele sunulur, token maliyeti düşürülür.

## 🚨 temel kurallar

1. **bellek ve maliyet optimizasyonu (9. kural):** gereksiz binlerce parçayı bağlama yüklemeyin.
2. **kesin varlık doğrulaması (18. kural):** üretilen yanıtlarda kaynak metin referansları gösterilir.
