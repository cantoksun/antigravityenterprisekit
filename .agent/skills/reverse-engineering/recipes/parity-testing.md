# ⚖️ davranışsal eşdeğerlik ve parity test kalıbı (parity testing)

bu kılavuz; tersine mühendislikle çözümlenen eski/kapalı bir sistemin yerine, **temiz oda ("clean-room rewrite")** yaklaşımıyla sıfırdan yazılan yeni sistemin **birebir aynı davranış ve doğruluğu** sağladığını kanıtlamak için kullanılır (dx-ball vaka standardı: 3.205 test senaryosu doğrulaması).

---

## 🎯 temel amaç
yeni kodun orijinal sistemle:
1. aynı girdilerde aynı çıktıları ürettiğini (byte-level / value parity),
2. sınır durumlarda (edge cases) aynı hata kodlarını fırlattığını,
3. performans ve bellek tüketiminde orijinal sistemden daha verimli olduğunu kanıtlamaktır.

---

## 📋 3 aşamalı parity test süreci

```
[orijinal sistem / ikili dosya] ──(test girdileri)──► [altın çıktı dökümü (golden master)]
                                                                  ▲
                                                                  │ (karşılaştırma)
                                                                  ▼
[yeni clean-room sistem]       ──(aynı girdiler)───► [yeni çıktı dökümü]
```

### 1. aşama: altın veri seti çıkarma (golden recording)
orijinal sistem çalışırken veya analiz edilirken girdi/çıktı çiftleri kaydedilir (`fixtures/parity_cases.json`):
```json
[
  {
    "input": { "angle": 0, "volume": 100 },
    "expected_output": { "left": 100, "right": 0 }
  },
  {
    "input": { "angle": 90, "volume": 100 },
    "expected_output": { "left": 70, "right": 70 }
  }
]
```

### 2. aşama: otomatik parity test süiti
yeni yazılan modül üzerinde altın veri seti koşturulur:

```typescript
// parity.test.ts
import { soundPanFunction } from './rebuilt-sound';
import testCases from './fixtures/parity_cases.json';

describe('Parity Verification (43. Kural)', () => {
  testCases.forEach((tc, index) => {
    it(`Senaryo #${index} orijinal davranışla birebir eşleşmeli`, () => {
      const result = soundPanFunction(tc.input);
      expect(result).toEqual(tc.expected_output);
    });
  });
});
```

### 3. aşama: delil ve doğrulama raporu
tüm testler başarıyla geçtiğinde, yeniden yazımın doğruluğu somut kanıtlarla belgelenir.
