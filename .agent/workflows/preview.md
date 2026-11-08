---
description: arayüz bileşenlerini, responsive düzenleri ve temaları yerel ortamda önizleyin ve test edin.
priority: p1-workflow
version: 2.0.0
---

# arayüz önizleme ve görsel doğrulama iş akışı (/preview)

bu iş akışı; `frontend-specialist` ve `mobile-developer` liderliğinde geliştirilen arayüz bileşenlerinin, masaüstü ve mobil deneyim ayrımının (15. kural) ve tipografi disiplininin (16. kural) görsel olarak önizlenmesini ve test edilmesini yönetir.

---

## 🚨 temel kurallar uyumu (en yüksek öncelik)

1. **türkçe ve küçük harf standardı:** tüm önizleme açıklamaları ve yönlendirmeler küçük harfle ve türkçe karakterlerle (`ç, ğ, ı, ö, ş, ü`) yazılır (1. kural).
2. **sorgusuz modüler icra:** geliştirme sunucusu ve önizleme ortamı kullanıcıya teknik soru sormadan doğrudan başlatılır (2. kural).
3. **cihaz odaklı arayüz ayrımı (15. kural):** önizleme esnasında hem mobil görünüm (alt çekmece / drawer) hem masaüstü görünüm (dialog / modal) test edilir.
4. **font disiplini (16. kural):** arayüzde 2-3 font ailesinden fazlasının yüklenmediği ve düzen kayması (cls) yapmadığı doğrulanır.
5. **kullanıcıyı yormama (17. kural):** önizleme portu veya komutları kullanıcıya havale edilmez; doğrudan sistemce tetiklenir.

---

## 🖥️📱 önizleme adımları

### 1. geliştirme sunucusunu başlatma (17. kural uyumu)
geliştirme sunucusu arka planda doğrudan ayağa kaldırılır:
```bash
npm run dev # veya vite / next dev
```

### 2. duyarlı (responsive) görünüm kontrolü (15. kural)
- **mobil görünüm (viewport < 768px):**
  - başparmak erişimi rahat mı?
  - pencereler alt çekmece (drawer / bottom sheet) olarak açılıyor mu?
  - dokunma hedefleri minimum 48x48dp boyutunda mı?
- **masaüstü görünüm (viewport >= 768px):**
  - geniş ekran verimli kullanılmış mı?
  - pencereler modal dialog olarak açılıyor mu?
  - klavye odak halkaları (`focus-visible`) düzgün çalışıyor mu?

### 3. tipografi ve font kontrolü (16. kural)
- kullanılan fontların toplam sayısı 2-3 ile sınırlı mı?
- türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) bozulmadan veya sistem varsayılanına düşmeden doğru fontla render ediliyor mu?

---

## 📢 önizleme bildirim formatı

önizleme hazır olduğunda kullanıcıya şu özet sunulur:

```markdown
🚀 **arayüz önizlemesi hazır:**
- **yerel adres:** `http://localhost:[port]`
- **cihaz uyumu (15. kural):** mobilde alt çekmece (drawer), masaüstünde modal doğrulandı.
- **tipografi (16. kural):** [x] adet font ailesi kullanılıyor, türkçe karakterler eksiksiz.
```
