---
description: sistematik hata ayıklama, kök neden analizi ve kalıcı çözüm prosedürü.
---

# 🔍 /debug - sistematik hata ayıklama ve kök neden analizi iş akışı

bu iş akışı karşılaşılan hataları, beklenmedik sistem davranışlarını veya çökmeleri 4 aşamalı bilimsel yöntemle çözümler.

## 🎯 incelenecek hata veya sorun
$ARGUMENTS

---

## 🧭 sistematik hata ayıklama adımları

`/debug` komutu çalıştığında şu döngü işletilir:

1. **bilgi toplama ve belirti tespiti**:
   - hata mesajı ve yığın izi (stack trace).
   - yeniden üretme (reproduction) adımları.
   - beklenen davranış ile gerçekleşen davranış arasındaki fark.
   - 18. kural gereğince kodda gerçekten var olan değişken ve fonksiyonların teyidi.

2. **hipotezler oluşturma**:
   - olası nedenleri ihtimal sırasına göre listelemek.
   - bellek sızıntısı (10. kural), rls ihlali (12. kural) veya idor yetki açığı (8. kural) olup olmadığını değerlendirmek.

3. **kanıt odaklı eleme**:
   - her hipotezi log, kod okuma ve veri akışı incelemesiyle test etmek.
   - tahminle değil kanıtla ilerlemek.

4. **onarım ve kalıcı önleme**:
   - en yalın ve doğrudan düzeltmeyi uygulamak (4. kural).
   - kök nedeni net şekilde açıklamak ve regresyonu engelleyecek önlem/test eklemek.

---

## 📋 standart debug raporu formatı

```markdown
## 🔍 hata ayıklama raporu: [sorun başlığı]

### 1. ⚠️ belirti ve hata mesajı
- **hata dökümü**: `[hata metni / durum kodu]`
- **etkilenen dosya**: `[dosya_yolu]` (satır no: [x])

### 2. ❓ hipotezler
1. [en yüksek olasılıklı neden]
2. [ikinci olası neden]

### 3. 🔬 inceleme ve kanıt
- **hipotez 1 testi**: [yapılan inceleme] → [sonuç]
- **kök neden**: 🎯 [hatanın gerçek kaynağı]

### 4. 🛠️ uygulanan çözüm (önce / sonra)
```typescript
// önce (hatalı kod)
[hatalı kısım]

// sonra (düzeltilmiş kod)
[düzeltilmiş kısım]
```

### 5. 🛡️ kalıcı önleme
[benzer hataların tekrarlanmaması için eklenen birim test veya tip koruması]
```

---

## 🚨 katı kurallar

- tüm açıklamalar ve raporlar istisnasız küçük harflerle ve türkçe karakterler (ç, ğ, ı, ö, ş, ü) eksiksiz kullanılarak yazılmalıdır.
- kullanıcıya gereksiz sorular sormadan doğrudan analiz ve modüler icra (2. kural) uygulanmalıdır.
