---
name: desktop-rust-patterns
description: kurumsal masaüstü uygulama mimarisi ve rust ekosistemi standartları. slint, egui, iced ile saf yerel arayüzler ve tauri ile hafif webview hibrit kalıpları, bellek yönetimi ve sistem güvenliği ilkeleri.
---

# 🦀 masaüstü geliştirme ve kurumsal rust standartları (desktop-rust-patterns)

bu beceri; masaüstü uygulaması geliştirirken birincil tercih olan **rust** dili, mimari karar ağaçları, bellek yönetimi, yerel gui ve tauri entegrasyonu yönergelerini içerir.

## 🧭 temel felsefe

> "masaüstü uygulamalarında kullanıcı donanımına saygı esastır: sıfır maliyetli soyutlama, mutlak bellek güvenliği, anlık tepki ve mikro ram tüketimi (rust)."

---

## 🎯 masaüstü mimari seçim matrisi

| gereksinim türü | önerilen rust çerçevesi | ram tüketimi | dağıtım boyutu | odak alanı |
|---|---|---|---|---|
| **hafif saf yerel gui** | **slint** veya **iced** | 10-25 mb | 5-15 mb | işletim sistemi araçları, şık yerel arayüzler |
| **veri/grafik/araç (hızlı geliştirme)** | **egui** | 15-30 mb | 8-15 mb | dahili araçlar, mühendislik panelleri, anlık render |
| **esnek ve zengin web tabanlı ui** | **tauri (rust + typescript/react)** | 30-50 mb | 10-20 mb | modern saas masaüstü sürümleri, zengin web bileşenleri |
| **ağır electron kalıbı** | ❌ **kaçınılır** | 200+ mb | 120+ mb | 9. ve 10. kural gereğince zorunlu olmadıkça kullanılmaz |

---

## 🏗️ rust masaüstü mimari ilkeleri

### 1. sahiplik (ownership) ve bellek sızıntısı engeli (9. ve 10. kural)
- çöp toplayıcı (gc) olmadığı için arka planda takılma (stutter) yaşanmaz.
- uzun ömürlü durumları (state) yönetirken `Arc<Mutex<T>>` veya `Arc<RwLock<T>>` yerine kanal tabanlı (`tokio::sync::mpsc` veya `crossbeam`) mesajlaşma önceliklendirilir.
- pencere kapandığında sistem arka planında asılı kalan thread'ler ve soketler kesinlikle sonlandırılır.

### 2. asenkron çalışma ve arayüz kilitlenmesini engelleme (ui thread non-blocking)
- ana iş parçacığı (main / ui thread) asla ağır disk okuma, ağ isteği veya ağır cpu hesaplamasıyla kilitlenemez.
- ağır işlemler doğrudan `tokio` veya `rayon` iş parçacığı havuzlarına (thread pool) devredilir; sonuçlar arayüze olay (event) olarak bildirilir.

### 3. yerel sistem ve donanım entegrasyonu
- dosya sistemi, seri port, sistem tepsisi (system tray), küresel kısayollar ve bildirimler rust yerel kütüphaneleri (`notify`, `tray-icon`, `global-hotkey`) ile yönetilir.
- güvenlik gereği kullanıcı dosya sistemine erişirken en kısıtlı izin (least privilege) prensibi uygulanır.

---

## 📋 tauri (rust + typescript) kurumsal kalıbı

eğer web tabanlı zengin bileşenler kullanılacaksa `tauri` kullanılırken şu kalıplar zorunludur:

```rust
// src-tauri/src/main.rs - güvenli komut ve hata yönetimi
#[tauri::command]
async fn read_system_metrics() -> Result<MetricsData, String> {
    // ağır işlem asenkron yürütülür, arayüz asla kilitlenmez
    metrics::collect_async().await.map_err(|e| e.to_string())
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![read_system_metrics])
        .run(tauri::generate_context!())
        .expect("tauri uygulaması başlatılırken hata oluştu");
}
```

---

## 🚨 katı kurallar

- tüm açıklamalar ve raporlar istisnasız küçük harflerle ve türkçe karakterler (ç, ğ, ı, ö, ş, ü) eksiksiz kullanılarak yazılmalıdır.
- masaüstü taleplerinde aksi açıkça istenmedikçe electron önerilmez; birincil tercih rust (`slint`, `egui` veya `tauri`) olmalıdır.
- ana arayüz iş parçacığı (ui thread) asla bloke edilmemelidir.
