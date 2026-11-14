---
name: memory-system
description: oturumlar arası kalıcı bellek yönetimi. kullanıcı tercihlerini, proje kurallarini ve geçmiş mimari kararları hatırlar.
when_to_use: "kullanıcı 'bunu unutma', 'hafizaya kaydet', 'hatirla' dediğinde veya yeni oturumda geçmiş baglami çağırmak gerektiğinde kullanılır."
allowed-tools: Read, Write, Grep, Glob
version: 1.0.0
effort: low
---

# kalıcı bellek sistemi (memory system) — oturumlar arası hafiza

> oturumlar arasında baglami ve öğrenilenleri kalıcı tutun. keşfedilmiş bilgileri tekrar aramakla zaman kaybetmeyin.

## 🎯 genel bakis

kalici bellek sistemi, projeye özgü tercihleri ve mimari kararları .agent/memory/ dizininde yapısal dosyalarda saklar:
- user_preferences.md: kullanıcının kodlama, dil ve çalışma tercihleri
- project_decisions.md: alınan kritik mimari ve veritabanı kararlari
- environment_notes.md: yerel geliştirme portları ve özel araç yollari

## 🚨 temel kurallar

1. **hassas verilerin korunması (7. kural):** asla api anahtarı veya parola gibi gizli verileri belleğe düz metin yazmayın.
2. **yalinlik ve temizlik (4. kural):** gereksiz ayrıntıları eleyin, sadece dönüştürücü kararları saklayın.
