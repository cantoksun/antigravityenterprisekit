# ⚡ electron uygulamaları tersine mühendislik kılavuzu (asar & ipc)

modern masaüstü uygulamalarının (notion, slack, discord, vs code vb.) büyük bölümü electron ile inşa edilmiştir. bu kılavuz, electron paketlerinin çözümlenmesi ve kurumsal temiz oda şartnamesi çıkarılmasını adım adım yönetir.

---

## 🏗️ electron mimari ayrımı ve hedef yüzey

electron uygulamaları üç ana katmandan oluşur:
1. **main process (`main.js`):** node.js ortamında çalışır. doğrudan işletim sistemi apı'lerine, dosya sistemine ve yerel soketlere erişebilir.
2. **preload script (`preload.js`):** `contextBridge.exposeInMainWorld` aracılığıyla renderer ile main process arasında güvenli köprü kurar.
3. **renderer process:** chromium içinde çalışan web arayüzüdür (`react`, `vue` vb.).

---

## 🛠️ adım adım analiz iş akışı

### 1. `app.asar` arşivini çıkarma
electron kodları genellikle `resources/app.asar` dosyası içinde paketlenir:
```bash
# asar paketini ayıklayın
npx @electron/asar extract resources/app.asar ./unpacked_app
```

### 2. `preload.js` ve bağlam köprüsü (contextbridge) tespiti
hedef işlevin ön yüz ile arka yüz arasındaki iletişim kanalını tespit edin:
- `unpacked_app` içinde `contextBridge.exposeInMainWorld` çağrılarını arayın:
```bash
grep -rn "contextBridge.exposeInMainWorld" ./unpacked_app
```
- dışarı açılan apı fonksiyonlarını ve `ipcRenderer.send / invoke` kanallarını belgeleyin.

### 3. ipc kanallarının dinleyicilerini bulma (main process)
renderer tarafından tetiklenen bir kanalın arkasındaki gerçek mantık main process'tedir:
```bash
# kanal adına göre ipcMain dinleyicilerini arayın
grep -rn "ipcMain.handle('kanal-adi'" ./unpacked_app
grep -rn "ipcMain.on('kanal-adi'" ./unpacked_app
```

### 4. temiz oda (clean-room) şartnamesine dönüştürme
kodun ham halini kopyalamayın. bulunan ipc kanalları için bir typescript tanımı oluşturun:
```typescript
// ipc-specification.ts
export interface ElectronBridgeSpec {
  // renderer'ın çağırdığı metod
  executeAction(payload: { id: string; action: string }): Promise<ActionResult>;
}
```
bu arayüzü sıfırdan modern bir tauri / rust veya yerel node servisinde temiz oda yaklaşımıyla uygulayın.
