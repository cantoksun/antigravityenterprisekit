---
name: i18n-localization
description: uluslararasılaştırma ve yerelleştirme ilkeleri. sabit kodlanmış metinleri tespit etme, çeviri dosyaları ve çoklu dil desteği.
priority: p2-specialized
version: 2.0.0
---

# kurumsal uluslararasılaştırma (i18n) ve yerelleştirme (l10n) standartları

bu beceri; kurumsal yazılımlarda çoklu dil mimarisi, sabit metinlerin temizlenmesi, yerel tarih/saat/para birimi biçimlendirmesi ve sağdan sola (rtl) dil desteğini yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 16 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır (1. kural).
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir yerelleştirme modülü tamamlanır.
   - sadelik ve modern trend teknolojiler: next-intl, i18next, react-intl.
   - tipografi ve font disiplini: seçilen 2-3 font ailesinin tüm hedef dillerin karakter setlerini (örneğin türkçe için `latin-ext`) desteklemesi zorunludur (16. kural).
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki i18n/l10n yönergeleri.

---

## 🌐 kurumsal i18n ve yerelleştirme ilkeleri

### 1. sabit kodlanmış metin yasağı (zero hardcoded strings)
- kullanıcı arayüzünde görünen hiçbir metin jsx/html içine doğrudan yazılmaz.
- tüm metinler modüler json veya typescript sözlük dosyalarından dil anahtarları (translation keys) aracılığıyla çağrılmalıdır:
  ```tsx
  // yanlış (sabit metin):
  <button>giriş yap</button>

  // doğru ve kurumsal:
  const t = useTranslations('auth');
  <button>{t('loginButton')}</button>
  ```

### 2. anlamsal ve hiyerarşik anahtar yapısı
çeviri anahtarları düz bir liste yerine etki alanlarına göre kategorize edilmelidir:
```json
{
  "common": {
    "save": "kaydet",
    "cancel": "iptal",
    "delete": "sil"
  },
  "auth": {
    "title": "hesabınıza giriş yapın",
    "emailLabel": "e-posta adresi",
    "loginButton": "giriş yap"
  },
  "errors": {
    "networkError": "sunucuya ulaşılamadı, lütfen bağlantınızı kontrol edin",
    "unauthorized": "bu işlem için yetkiniz bulunmuyor"
  }
}
```

### 3. parametrik çeviriler ve çoğullaştırma (pluralization)
- dinamik metinlerde dize birleştirme (`"merhaba " + name`) yapılmaz; parametre enjeksiyonu kullanılır:
  ```json
  {
    "greeting": "merhaba, {name}!",
    "cartItemCount": "{count, plural, =0 {sepetiniz boş} one {# ürün} other {# ürün}}"
  }
  ```

### 4. tarih, saat ve para birimi biçimlendirmesi (intl api)
- tarih ve para birimleri elle biçimlendirilmez; tarayıcının veya sunucunun yerel `Intl` motoru kullanılır:
  ```typescript
  // para birimi: tr-TR için 1.250,50 ₺, en-US için $1,250.50
  new Intl.NumberFormat(locale, { style: 'currency', currency: 'TRY' }).format(1250.50);

  // tarih formatı:
  new Intl.DateTimeFormat(locale, { dateStyle: 'long' }).format(new Date());
  ```

### 5. sağdan sola (rtl) arayüz desteği
- arapça veya ibranice gibi dillerde css akışı için sabit `left`/`right` yerine mantıksal css özellikleri (`ms-` / `me-` / `start-` / `end-`) tercih edilmelidir:
  `mr-4` yerine `me-4` (margin-inline-end).
