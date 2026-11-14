# donanım ve tescilli ağ protokolleri tersine mühendisliği (hardware & protocol re)

bu tarif, kapalı kaynaklı donanım cihazları (usb, hid, bluetooth le, seri port) ve özel ikili ağ protokollerinin (tcp/udp/websocket) delile dayalı olarak çözümlenmesi ve açık standartlara kavuşturulması için kullanılır.

---

## 🎯 temel felsefe ve yasal çerçeve (43. kural uyumu)
- **yalnızca dışarıdan gözlem:** donanım bellenimini (firmware) izinsiz kırmak yerine, cihazın gönderdiği ve aldığı ham veri paketleri (raw packets) analiz edilir.
- **temiz oda arayüzü:** analiz çıktısı tescilli bir sürücü kodu değil, saf bir protokol spesifikasyon belgesidir (`PROTOCOL_SPEC.md`).

---

## 🛠️ araç seti ve gözlem katmanları

| hedef katman | analiz aracı | gözlem yöntemi |
|---|---|---|
| **usb / hid++ cihazlar** | `wireshark` / `usbpcap` / `hidraw` | ham hid rapor tanımlayıcıları ve kesme (interrupt) paketleri |
| **bluetooth le (ble)** | `bettercap` / `gatttool` / `wireshark` | gatt servis ve karakteristik uuid'leri, bildirim (notification) akışları |
| **özel tcp / udp protokolü** | `mitmproxy` / `wireshark` / `tshark` | hex dökümü, paket başlıkları, sihirli baytlar (magic bytes) |
| **seri port / gömülü sistem** | `pyserial` / `minicom` | baud rate tespiti, cr/lf sonlandırıcılar, ascii/ikili çerçeveler |

---

## 🔬 4 aşamalı protokol analiz prosedürü

### 1. paket yakalama ve sihirli bayt (magic byte) tespiti
- cihaz normal çalışırken ve belirli bir eylem yapılırken (örneğin rgb ışık değiştirildiğinde veya tuşa basıldığında) paketler yakalanır.
- paketlerin başlangıç baytları (preamble/magic byte), uzunluk alanı ve yük (payload) sınırları ayrıştırılır:
  ```text
  [0xAA 0x55] (2 bayt başlangıç) | [0x08] (uzunluk) | [0x01] (komut: renk ayarla) | [0xFF 0x00 0x00] (rgb) | [0x12] (checksum)
  ```

### 2. kontrol toplamı (checksum / crc) çözümü
- paket sonundaki doğrulama baytları tespit edilir:
  - xor tabanlı mı? (`checksum = byte[0] ^ byte[1] ^ ...`)
  - toplamsal mı? (`checksum = sum(bytes) & 0xFF`)
  - standart crc mi? (crc-8, crc-16-ccitt, crc-32).

### 3. durum makinesi (state machine) ve el sıkışma (handshake)
- cihazın açılışta veya bağlantı anında gönderdiği sorgular (`ping/hello/auth`) ve beklediği yanıtlar haritalanır.
- zaman aşımı (timeout) ve kalp atışı (keep-alive/heartbeat) süreleri ölçülür.

### 4. python referans istemcisi oluşturma
- çözümlenen paket yapısı standart bir python sınıfı ile doğrulanır:
  ```python
  import struct

  class DeviceProtocol:
      MAGIC = b'\xAA\x55'

      @classmethod
      def build_packet(cls, command_id: int, payload: bytes) -> bytes:
          length = len(payload) + 1
          header = struct.pack('>2sBB', cls.MAGIC, length, command_id)
          checksum = sum(header + payload) & 0xFF
          return header + payload + bytes([checksum])
  ```

---

## 📋 çıktı formatı: `PROTOCOL_SPEC.md`
analiz tamamlandığında kod yazan ajana yalnızca şu başlıkları içeren belge teslim edilir:
1. **fiziksel / ağ katmanı:** port, baud rate, mtu boyutu.
2. **paket yapısı:** başlık, yük ve kontrol toplamı şeması.
3. **komut tablosu:** işlem kodu (opcode), parametreler ve beklenen yanıt.
4. **hata durumları:** cihazın dönebileceği hata kodları.
