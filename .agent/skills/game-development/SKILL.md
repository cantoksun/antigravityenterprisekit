---
name: game-development
description: oyun mantığı, döngü yönetimi, fizik etkileşimleri ve platforma özel optimizasyon becerisi.
priority: p2-specialized
version: 2.0.0
---

# kurumsal oyun geliştirme ve grafik döngüsü standartları

bu beceri; oyun motorları (phaser, pixijs, three.js, unity, godot), oyun döngüsü optimizasyonu, nesne havuzlama, bellek yönetimi ve kare hızı kararlılığını yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 16 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir oyun mekaniği modülü tamamlanır.
   - sadelik ve modern trend teknolojiler (4. kural).
   - bellek optimizasyonu, çöp toplayıcı (gc) duraklamalarını önleme ve nesne sızıntısı analizi (9. ve 10. kural).
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki oyun geliştirme yönergeleri.

---

## 🎮 kurumsal oyun mimarisi ilkeleri

### 1. kare hızından bağımsız oyun döngüsü (delta-time loop)
- fizik ve hareket hesaplamaları sabit kare sayısına değil, geçen süreye (`delta time - dt`) bağlı olmalıdır:
  ```typescript
  function update(dt: number) {
    // dt saniye cinsindendir; 60 fps'de de 144 fps'de de nesne aynı hızda hareket eder
    player.x += player.vx * dt;
    player.y += player.vy * dt;
  }
  ```

### 2. nesne havuzlama (object pooling - 9. ve 10. kural uyumu)
- mermi, parçacık efekti veya düşman gibi sürekli üretilip yok edilen nesneler için döngü içinde `new Object()` çağrısı yapmak çöp toplayıcıyı (garbage collector) tetikler ve mikro takılmalara (stuttering) yol açar.
- önceden oluşturulmuş bir nesne havuzu (pool) kullanılmalıdır:
  ```typescript
  export class BulletPool {
    private pool: Bullet[] = [];

    getBullet(): Bullet {
      return this.pool.pop() || new Bullet();
    }

    releaseBullet(bullet: Bullet): void {
      bullet.reset(); // durumu sıfırla
      this.pool.push(bullet); // belleği yok etmek yerine havuza geri ver (10. kural)
    }
  }
  ```

### 3. doku ve gpu bellek temizliği (10. kural uyumu)
- sahne değiştiğinde veya oyun sonlandığında kullanılmayan dokular (textures), geometriler ve ses tamponları mutlaka gpu belleğinden serbest bırakılmalıdır (`texture.destroy()`, `geometry.dispose()`).

### 4. sonlu durum makinesi (finite state machine - fsm)
- oyun durumları (yükleniyor, ana menü, oyun içi, duraklatıldı, oyun bitti) ve karakter durumları (koşma, zıplama, saldırı) spagetti `if-else` blokları yerine fsm ile yönetilmelidir.
