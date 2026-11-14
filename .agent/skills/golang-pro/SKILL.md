---
name: golang-pro
description: modern go (golang), goroutine ve channel eszamanliligi, yuksek performansli mikroservisler, rest/grpc api tasarimi.
when_to_use: "modern go (golang) mikroservisleri, goroutine eszamanliligi ve grpc servisleri gelistirilirken kullanilir."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---

# modern go uzmanlığı (golang-pro) — yuksek başarımlı sistemler

> sade, hızlı, ölçeklenebilir mikroservisler, eşzamanlılık modelleri ve düşük bellek ayak izi.

## 🎯 kurumsal go kaliplari

1. **eszamanlilik ve kaynak yonetimi:**
   - `goroutine` sızıntılarını önlemek için mutlaka `context.Context` zaman aşımı (28. kural) ile yönetilir.
   - sınırsız goroutine acilmaz; `worker pool` veya sınırlı kanal (buffered channel) kullanılır.
2. **zarif kapanış (graceful shutdown) (27. kural):**
   - `os.Interrupt` ve `syscall.SIGTERM` sinyalleri dinlenir, aktif istekler temizce tamamlanır.
3. **hata yonetimi:**
   - `panic` yerine açık hata dönüşü (`if err != nil`).
4. **api ve protokoller:**
   - `chi` / `gin` veya standart `net/http` ile rest; ic iletişimde yuksek performansli `gRPC`.

## 🚨 temel kurallar

1. **kati api güvenliği (6. kural):** girdi doğrulaması (`validator/v10`) ve rate limiting.
2. **sadelik (4. kural):** asiri soyutlamalardan (over-engineering) ve gereksiz interface yığınından kaçının.
