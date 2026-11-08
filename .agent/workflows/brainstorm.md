---
description: projeler ve özellikler için yapılandırılmış beyin fırtınası, sokratik analiz ve seçenek keşfi prosedürü.
---

# 🧠 /brainstorm - yapılandırılmış fikir ve mimari seçenek keşfi

bu iş akışı mimari ve teknik bir yola girmeden önce seçenekleri, ödünleşimleri (trade-offs) ve alternatif yaklaşımları analiz eder.

## 🎯 incelenecek konu veya özellik
$ARGUMENTS

---

## 🧭 yürütme adımları ve davranış modeli

`/brainstorm` tetiklendiğinde şu sıra takip edilir:

1. **amacı ve problemi kavrama**:
   - hangi temel problemi çözüyoruz?
   - hedef kullanıcı kim ve sistem sınırları neler?
   - zaman, bellek ve performans kısıtları neler? (9. ve 10. kural)

2. **seçenekleri üretme (en az 3 farklı yaklaşım)**:
   - her seçenek için avantajlar ve dezavantajlar.
   - 4. kural sadeliği ve trend teknolojiler dengesi.
   - idor/güvenlik ve bellek etkileri.

3. **kıyaslama ve net tavsiye**:
   - ödünleşimlerin (trade-offs) özetlenmesi.
   - kurumsal standartlara ve en sade çözüme dayalı somut bir seçenek önerisi.

---

## 📋 standart beyin fırtınası çıktı şablonu

```markdown
## 🧠 beyin fırtınası analizi: [konu başlığı]

### 🎯 bağlam ve problem
[çözülmek istenen problemin özeti]

---

### seçenek a: [en sade ve doğrudan yaklaşım (4. kural)]
[yaklaşımın tanımı ve mimarisi]
- ✅ **avantajlar**: [hızlı icra, az bağımlılık, yalın yapı]
- ❌ **dezavantajlar**: [sınırlı esneklik]
- 📊 **efor seviyesi**: düşük

---

### seçenek b: [orta ölçekli ve modüler yaklaşım]
[yaklaşımın tanımı ve mimarisi]
- ✅ **avantajlar**: [genişletilebilir, iyi soyutlama]
- ❌ **dezavantajlar**: [bir miktar ek katman]
- 📊 **efor seviyesi**: orta

---

### seçenek c: [kapsamlı kurumsal yaklaşım]
[yaklaşımın tanımı ve mimarisi]
- ✅ **avantajlar**: [yüksek ölçeklenebilirlik, bağımsız servisler]
- ❌ **dezavantajlar**: [aşırı mühendislik riski, yüksek bakım maliyeti]
- 📊 **efor seviyesi**: yüksek

---

## 💡 kurumsal tavsiye ve gerekçe
**seçenek [a/b]** önerilir; çünkü [4. kural sadeliği ve 9. kural performans gereksinimlerini en yalın şekilde karşılar].
```

---

## 🚨 katı kurallar

- tüm açıklamalar ve raporlar istisnasız küçük harflerle ve türkçe karakterler (ç, ğ, ı, ö, ş, ü) eksiksiz kullanılarak yazılmalıdır.
- kullanıcıya gereksiz sorular sormadan doğrudan analiz ve modüler icra (2. kural) uygulanmalıdır.
