---
name: lint-and-validate
description: otomatik kalite kontrolü, linting ve statik analiz prosedürleri. sözdizimi doğruluğunu ve proje standartlarını sağlamak için her kod değişikliğinden sonra kullanılır.
priority: p1-quality
version: 2.0.0
---

# otomatik kalite kontrolü, linting ve statik analiz standartları

bu beceri; kod tabanında sözdizimi hatalarını, tip uyumsuzluklarını, kodlama tarzı ihlallerini ve kullanılmayan kodları otomatik olarak denetleyip doğrulamayı yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 16 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir doğrulama modülü tamamlanır.
   - sadelik ve modern trend teknolojiler: eslint (flat config), prettier, ruff, biome, typescript (`tsc --noEmit`), mypy (4. kural).
   - statik analiz seviyesinde sır taraması (7. kural) ve bellek sızıntısı analizleri (10. kural).
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki statik analiz yönergeleri.

---

## 🔍 otomatik doğrulama prosedürü

her kod değişikliğinin ardından aşağıdaki 3 katmanlı denetim işletilmelidir:

### 1. tip denetimi (type checking - sıfır tolerans)
- typescript projelerinde: `npx tsc --noEmit`
- python projelerinde: `mypy .`
- `any` tipi veya `@ts-ignore` kullanımı acil durumlar hariç yasaktır; eksik tipler açıkça tanımlanmalıdır.

### 2. linter ve stil denetimi (linting)
- javascript/typescript: `npx eslint . --max-warnings 0` veya `npx biome check .`
- python: `ruff check .`
- kullanılmayan değişkenler, döngü içi hatalı fonksiyon tanımları ve gereksiz importlar temizlenmelidir.

### 3. güvenlik ve sır taraması (7. ve 14. kural)
- statik analiz araçları kod içinde `.env` değişkenleri yerine sabitlenmiş şifreleri (`apiKey = "..."`) ve güvensiz `localStorage` kullanımlarını aramalı ve derleme öncesi uyarmalıdır.

---

## 🛠️ pre-commit ve git hooks entegrasyonu (husky / lint-staged)

kurumsal projelerde hatalı kodun depoya girmesini önlemek için yerel git kancaları kurulmalıdır:

```json
// package.json
{
  "lint-staged": {
    "*.{ts,tsx,js,jsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.py": [
      "ruff check --fix",
      "ruff format"
    ]
  }
}
```
