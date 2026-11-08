---
name: server-management
description: kurumsal sunucu yönetimi, süreç yönetimi, sistem izleme ve ölçeklendirme stratejileri.
priority: p1-operations
version: 2.0.0
---

# kurumsal sunucu yönetimi ve sistem dayanıklılığı standartları

bu beceri; sunucu süreç yönetimi, sistem kaynak izleme, bellek taşmalarının engellenmesi, log rotasyonu ve güvenlik sertleştirme (hardening) süreçlerini yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 15 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir operasyon modülü tamamlanır.
   - sadelik ve modern trend teknolojiler: systemd, pm2, caddy/nginx, prometheus/grafana.
   - katı sunucu güvenliği, port kısıtlamaları ve ssh sertleştirme.
   - bellek yönetimi (9. ve 10. kural) ve servis kesintisizliği.
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki sunucu standartları.

---

## 🖥️ kurumsal sunucu süreç ve kaynak standartları

### 1. süreç yöneticisi ve otomatik yeniden başlatma (pm2 / systemd)
- uygulamalar doğrudan terminalde çalıştırılamaz; daima bir süreç yöneticisi altında çalışmalıdır.
- **bellek sınırı ve otomatik yeniden başlatma:** uygulamanın bellek sızıntısı durumunda sunucuyu çökertmemesi için üst bellek sınırı (max-memory-restart) tanımlanır:
  ```json
  // ecosystem.config.js (pm2)
  module.exports = {
    apps: [{
      name: "api-service",
      script: "dist/index.js",
      instances: "max",
      exec_mode: "cluster",
      max_memory_restart: "500M", // 500mb aşılırsa zarifçe yeniden başlat
      env_production: {
        NODE_ENV: "production"
      }
    }]
  };
  ```

### 2. güvenlik sertleştirme (server hardening)
- **ssh güvenliği:** şifreli giriş kapatılmalı (`PasswordAuthentication no`), yalnızca güçlü ed25519 ssh anahtarları kullanılmalı ve `root` girişi engellenmelidir (`PermitRootLogin no`).
- **güvenlik duvarı (ufw):** yalnızca zorunlu portlar (80, 443 ve özel ssh portu) dış dünyaya açılmalı; veritabanı (5432, 27017, 6379) portları kesinlikle dış ağa kapatılmalıdır (`localhost` veya özel ağ içi dinleme).
- **tersine vekil (reverse proxy):** caddy veya nginx arkasında çalıştırma, otomatik letsencrypt tls 1.3 sertifikalandırması ve http/2-http/3 desteği.

### 3. log rotasyonu ve disk dolmasını önleme
- kontrolsüz log birikmesi sunucu diskini doldurarak sistemi kilitler.
- `logrotate` ile log dosyaları günlük sıkıştırılmalı, maksimum 14 gün saklanmalı ve boyut sınırı (örneğin 100mb) konulmalıdır:
  ```plaintext
  /var/log/app/*.log {
      daily
      rotate 14
      compress
      missingok
      notifempty
      copytruncate
  }
  ```

### 4. kaynak izleme ve uyarı eşikleri
- cpu kullanımı > %85 (10 dakika boyunca), ram kullanımı > %90 veya disk doluluğu > %80 olduğunda otomatik uyarı (alert) tetiklenmeli ve süreçler incelenmelidir.
