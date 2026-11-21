---
name: design-system-tokens
description: figma belirteçleri, css custom properties, tema değiştirici ve çoklu marka tasarım sistemi mimarisi.
priority: standard
version: 1.0.0
when_to_use: "figma belirteçleri, css custom properties, tema değiştirici ve çoklu marka tasarım sistemi mimarisi."
allowed-tools: [Read, Grep, Glob, Bash, Write, Edit]
---

# kurumsal tasarım belirteçleri ve çoklu tema mimarisi (design system tokens)

bu beceri; web ve mobil arayüzlerde renk, tipografi, boşluk (spacing), yarıçap (border-radius) ve gölge belirteçlerinin figma'dan koda (design-to-code) kayıpsız aktarılmasını ve dinamik tema (dark/light/custom) mimarisini kurumsal standartlarda tanımlar.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (temel anayasa kuralları):**
   - tüm çıktılar ve açıklamalar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır (1. kural).
   - **15. kural (tam responsive ve responsive ux):** tüm ekran boyutlarında kusursuz duyarlılık, yatay taşma (overflow-x) yasağı.
   - **16. kural (font sınırlandırması ve tipografi disiplini):** rastgele font yasaktır, en fazla 2-3 font ailesi ve standart ölçek.
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** `frontend-specialist` ve `mobile-developer`.
4. **p3 (beceri kuralları):** bu dokümandaki tasarım sistemi standartları.

---

## 🎨 belirteç katmanları ve css custom properties şablonu

tasarım belirteçleri 3 katmanlı semantik hiyerarşiyle yönetilir:
1. **global / ham belirteçler (primitive tokens):** ham renkler (ör. `blue-500: #3b82f6`). doğrudan bileşenlerde kullanılmaz.
2. **semantik belirteçler (semantic tokens):** amaca yönelik renkler (ör. `surface-primary`, `text-muted`, `border-focus`).
3. **bileşen belirteçleri (component tokens):** spesifik bileşenler (ör. `btn-primary-bg`, `card-shadow`).

```css
:root {
  /* 1. boşluk ölçeği (4px bazlı ritim) */
  --space-xs: 0.25rem; /* 4px */
  --space-sm: 0.5rem;  /* 8px */
  --space-md: 1rem;    /* 16px */
  --space-lg: 1.5rem;  /* 24px */
  --space-xl: 2rem;    /* 32px */

  /* 2. semantik renkler (açık tema) */
  --bg-app: #ffffff;
  --bg-surface: #f8fafc;
  --text-primary: #0f172a;
  --text-secondary: #64748b;
  --border-default: #e2e8f0;
  --accent-primary: #0284c7;

  /* 3. yarıçap ve odak */
  --radius-sm: 0.375rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --focus-ring: 0 0 0 2px #0284c7;
}

[data-theme="dark"] {
  --bg-app: #090d16;
  --bg-surface: #111827;
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --border-default: #1e293b;
  --accent-primary: #38bdf8;
}
```
