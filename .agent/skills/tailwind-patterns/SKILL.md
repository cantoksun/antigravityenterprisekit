---
name: tailwind-patterns
description: tailwind css modern kullanım ilkeleri, css-first yapılandırması, konteyner sorguları ve tasarım belirteçleri.
priority: p1-visual
version: 2.0.0
---

# modern tailwind css kurumsal stil ve tasarım standartları

bu beceri; tailwind css v4+, css-first yapılandırma, tasarım belirteçleri (tokens), bileşen varyantları ve performanslı arayüz kodlama standartlarını yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 14 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir modül tamamlanır.
   - sadelik ve modern trend teknolojiler: tailwind css v4+, cva (class-variance-authority), clsx/tailwind-merge (4. kural).
   - aşırı stil kirliliğini ve dom şişmesini engelleme (9. ve 13. kural).
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki tailwind tasarım ilkeleri.

---

## 🎨 modern tailwind css kurumsal ilkeleri

### 1. tasarım belirteçleri (design tokens) ve keyfi değer yasağı
- kod içinde rastgele keyfi değerler (`w-[347px]`, `bg-[#5f27cd]`) kullanmak yerine projenin tema değişkenlerini ve ölçeklerini kullanın:
  ```css
  /* globals.css - css-first yapılandırma */
  @theme {
    --color-primary: #0f172a;
    --color-accent: #2563eb;
    --font-sans: 'Inter', sans-serif;
  }
  ```
- tutarlı boşluk ve boyutlandırma ölçeği (4px, 8px, 12px, 16px, 24px - `p-2`, `p-4`, `p-6`) korunmalıdır.

### 2. bileşen varyant mimarisi (cva + tailwind-merge)
- uzayan karmaşık sınıf listelerini okunabilir ve tip güvenli hale getirmek için `class-variance-authority` (cva) ve `cn` yardımcı fonksiyonu kullanılır:
  ```typescript
  import { cva, type VariantProps } from 'class-variance-authority';
  import { clsx, type ClassValue } from 'clsx';
  import { twMerge } from 'tailwind-merge';

  export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
  }

  export const buttonVariants = cva(
    'inline-flex items-center justify-center rounded-lg text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
    {
      variants: {
        variant: {
          default: 'bg-primary text-white hover:bg-primary/90',
          outline: 'border border-slate-200 bg-transparent hover:bg-slate-100',
          destructive: 'bg-red-600 text-white hover:bg-red-700',
        },
        size: {
          default: 'h-10 px-4 py-2',
          sm: 'h-9 px-3',
          lg: 'h-11 px-8',
        },
      },
      defaultVariants: {
        variant: 'default',
        size: 'default',
      },
    }
  );
  ```

### 3. erişilebilirlik ve odak yönetimi (a11y)
- tüm etkileşimli öğeler (butonlar, linkler, girdi alanları) klavye ile gezildiğinde görünür bir odak göstergesine sahip olmalıdır:
  `focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:outline-none`.

### 4. duyarlı tasarım ve konteyner sorguları
- ekran boyutuna göre `sm:`, `md:`, `lg:` önekleri mantıksal bir akışla küçük ekrandan büyük ekrana (mobile-first) doğru kurgulanmalıdır.
- bağımsız kart bileşenlerinde ekran yerine bileşen genişliğine duyarlı olmak için konteyner sorguları (`@container`, `@md:grid-cols-2`) tercih edilmelidir.
