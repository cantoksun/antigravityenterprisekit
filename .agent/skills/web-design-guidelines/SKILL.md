---
name: web-design-guidelines
description: modern web ve mobil arayüz yönergeleri, tam responsive standartlar, yatay taşma engeli, cihaz odaklı ux ayrımı ve erişilebilirlik.
priority: p1-visual
version: 2.2.0
---

# kurumsal arayüz ve kullanıcı deneyimi yönergeleri (tam responsive ux)

bu beceri; tüm ekran boyutlarında (mobil, tablet, masaüstü) arayüzün kusursuz ve tam duyarlı (responsive) olmasını, yatay taşmaların (horizontal scroll) engellenmesini, masaüstü modal ve mobil alt çekmece (drawer / bottom sheet) ayrımını ve erişilebilirlik standartlarını yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 18 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır (1. kural).
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz (2. kural).
   - adım adım aşamalı yürütülür; her seferinde tek bir modül tamamlanır (3. kural).
   - sadelik ve modern trend teknolojiler (shadcn/ui, radix-ui, tailwind css).
   - katı güvenlik, bellek optimizasyonu, sayfalama ve lazy loading ilkeleri.
   - **15. kural (tam responsive ve cihaz odaklı deneyim ayrımı):** tüm ekranlarda sıfır yatay taşma ile tam duyarlılık; masaüstünde modal/dialog, mobilde drawer/bottom sheet ayrımı.
   - font sınırlandırması ve tipografi disiplini (16. kural).
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki arayüz yönergeleri.

---

## 📱🖥️ 15. kural: tam responsive standartlar ve cihaz odaklı ux ayrımı

### 1. sıfır yatay taşma kuralı (zero horizontal scroll)
- mobil cihazlardan 4k monitörlere kadar hiçbir ekranda sayfa gövdesinde istemsiz yatay kaydırma çubuğu (`overflow-x`) oluşamaz.
- sabit piksel genişlikleri (`width: 800px`) yerine daima esnek ve yüzdelik genişlikler (`w-full`, `max-w-4xl`, `min-w-0`), esnek ızgaralar (`grid-cols-1 sm:grid-cols-2 lg:grid-cols-3`) ve taşmayı önleyen kutu modelleri kullanılır.

### 2. etkileşimli pencereler: modal vs alt çekmece (drawer)
- **mobilde (ekran < 768px):**
  - ortalanmış küçük pencereler (modal dialog) mobilde başparmakla erişilemez ve klavye açıldığında içeriği kilitler.
  - mobilde daima **alt çekmece (bottom sheet / drawer)** kullanılmalıdır. kullanıcı içeriği tek elle aşağı kaydırarak kapatabilmeli, kapatma butonu başparmak menzilinde olmalıdır.
- **masaüstünde (ekran >= 768px):**
  - fare ve geniş ekran odağıyla merkezlenmiş **modal dialog** veya bağlamsal **açılır pencere (popover)** kullanılır. `esc` tuşu ile kapatma ve odak tuzağı (focus trap) sağlanmalıdır.

### 3. duyarlı bileşen mimarisi (responsive modal / drawer örneği)
```tsx
import * as React from 'react';
import { useMediaQuery } from '@/hooks/use-media-query';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Drawer, DrawerContent, DrawerHeader, DrawerTitle } from '@/components/ui/drawer';

interface ResponsiveModalProps {
  title: string;
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}

export function ResponsiveModal({ title, isOpen, onClose, children }: ResponsiveModalProps) {
  const isDesktop = useMediaQuery('(min-width: 768px)');

  // 15. kural: masaüstünde modal dialog, mobilde alt çekmece (drawer)
  if (isDesktop) {
    return (
      <Dialog open={isOpen} onOpenChange={onClose}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>{title}</DialogTitle>
          </DialogHeader>
          {children}
        </DialogContent>
      </Dialog>
    );
  }

  return (
    <Drawer open={isOpen} onOpenChange={onClose}>
      <DrawerContent>
        <DrawerHeader className="text-left">
          <DrawerTitle>{title}</DrawerTitle>
        </DrawerHeader>
        <div className="p-4">{children}</div>
      </DrawerContent>
    </Drawer>
  );
}
```

### 4. menü ve gezinme ayrımı
- **mobilde:** ekranın altında sabitlenen alt gezinme çubuğu (bottom navigation bar) veya sağdan/alttan açılan çekmece menü.
- **masaüstünde:** üst yatay gezinme çubuğu (navbar) veya genişletilmiş sol yan panel (sidebar).
