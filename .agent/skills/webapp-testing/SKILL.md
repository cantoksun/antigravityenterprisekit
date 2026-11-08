---
name: webapp-testing
description: modern web uygulamaları için uçtan uca (e2e) ve playwright tabanlı derin test stratejileri.
priority: p1-quality
version: 2.0.0
---

# kurumsal web uygulaması e2e test standartları (playwright)

bu beceri, tarayıcı ortamında gerçek kullanıcı etkileşimlerini simüle eden, kararlı (flaky olmayan), performans ve güvenlik odaklı uçtan uca (e2e) test süreçlerini yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 14 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir test modülü tamamlanır.
   - sadelik ve modern trend teknolojiler: playwright endüstri standardı olarak kullanılır (4. kural).
   - katı api güvenliği, owasp oturum kontrolleri (14. kural) ve yetki denetimleri (8. kural).
   - sayfalama, lazy loading (13. kural) ve bellek sızıntısı denetimi (10. kural).
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki e2e test yönergeleri.

---

## 🎭 playwright e2e test standartları

### 1. kullanıcı odaklı erişilebilir seçiciler (accessible locators)
- css sınıfları (`.btn-primary`), id'ler (`#submit`) veya kırılgan xpath'ler yerine, kullanıcının gördüğü ve ekran okuyucuların anladığı seçiciler kullanılmalıdır:
  ```typescript
  // doğru ve dayanıklı yaklaşım:
  page.getByRole('button', { name: 'giriş yap' });
  page.getByLabel('e-posta adresi');
  page.getByPlaceholder('şifrenizi girin');
  page.getByText('hoş geldiniz');
  ```

### 2. otomatik bekleme (auto-waiting) ve statik uyku yasağı
- kodda asla `page.waitForTimeout(3000)` gibi statik gecikmeler kullanılmaz.
- playwright'ın yerleşik otomatik bekleme özelliği (`await expect(locator).toBeVisible()`, `.toBeEnabled()`) tercih edilir.

### 3. oturum yönetimi ve owasp denetimi (14. kural testi)
- e2e testlerinde her test için baştan giriş yapmak yerine `storageState` kullanılarak oturum yeniden kullanılır:
  ```typescript
  // auth setup: güvenli oturum çerezlerini testler arasında paylaştır
  test.use({ storageState: 'playwright/.auth/user.json' });
  ```
- **xss & yetkisiz erişim testi:** localstorage içinde hassas token tutulmadığı, çerezlerin `httpOnly` ve `secure` olduğu e2e seviyesinde doğrulanır.

### 4. lazy loading ve sonsuz kaydırma testi (13. kural testi)
- sayfadaki liste veya medya öğelerinin kademeli yüklendiğini ve dom şişkinliği yapmadığını doğrulamak için:
  ```typescript
  test('sonsuz kaydırmada sonraki 20 öğe başarıyla yüklenmeli', async ({ page }) => {
    await page.goto('/feed');
    const items = page.getByRole('article');
    await expect(items).toHaveCount(20);

    // sayfanın sonuna kaydır
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    
    // kademeli olarak 40 öğeye ulaşmalı
    await expect(items).toHaveCount(40);
  });
  ```

---

## 📁 sayfa nesnesi modeli (page object model - pom)

büyük ölçekli web uygulamalarında e2e test kodunun tekrarını önlemek için sayfa nesnesi modeli uygulanır:

```typescript
export class LoginPage {
  constructor(private readonly page: Page) {}

  readonly emailInput = this.page.getByLabel('e-posta adresi');
  readonly passwordInput = this.page.getByLabel('şifre');
  readonly submitButton = this.page.getByRole('button', { name: 'giriş yap' });

  async login(email: string, pass: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(pass);
    await this.submitButton.click();
  }
}
```
