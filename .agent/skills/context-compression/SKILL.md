---
name: context-compression
description: uzun oturumlarda baglam yönetimi ve sıkıştırma. tamamlanan aşamaları ozetler, eski bulguları arşivler ve ana kararları korur.
when_to_use: "oturum 20+ tura ulaştığında, baglam şiştiğinde, model önceki kararları unutmaya başladığında veya kullanıcı 'ozetle' dediğinde kullanılır."
allowed-tools: Read, Write, Grep
version: 1.0.0
effort: low
---

# baglam sıkıştırma (context compression) — uzun oturum yonetimi

> tamamlanan işleri özetleyip ana mimari kararları koruyarak uzun oturumlarda baglam yorgunluğunu önleyin.

## 🎯 genel bakis

uzun soluklu geliştirme süreçlerinde modelin odak noktasini korumak için kullanilir:
- tamamlanan modülleri maddeler halinde arsivler
- açık kalan görevleri ve sıradaki aşamayı belirgin tutar
- mimari kararları (adr) ve cevre değişkeni ayarlarını muhafaza eder

## 🚨 temel kurallar

1. **kapsam şeffaflığı (19. kural):** neyin tamamlandığını ve neyin kaldığını net bicimde özetleyin.
2. **karar butunlugu:** alınan mimari ve guvenlik kararlarini asla sıkıştırma esnasında kaybetmeyin.
3. **dil disiplini (1. kural):** tum ozet ve kayıtlar eksiksiz türkçe ve küçük harfle tutulur.
