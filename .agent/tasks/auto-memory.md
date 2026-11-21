# 🧠 sıfır sürtünmeli otonom ajan-hafıza entegrasyon planı (auto-memory.md)

> bu plan; kullanıcının herhangi bir komut girmesine, script çalıştırmasına veya manuel hafıza yönetimiyle uğraşmasına gerek kalmadan, 20 uzman ajanın görev yaparken arka planda otonom olarak neural-os hafızasını okumasını, kararları işlemesini ve zihin grafiğini canlı tutmasını hedefler (kural 17: zero friction).

---

## 1. 🔍 mevcut problem ve sürtünme analizi (friction analysis)

şu anki sistemde:
1. **kullanıcı eforu (friction):** kullanıcı terminale gidip `python .agent/scripts/neural_os.py ...` çalıştırmak zorunda hissediyor.
2. **manuel çağrı zorunluluğu:** ajanlar geçmiş kararları ancak akıllarına gelirse veya kullanıcı isterse arıyor.
3. **otonom olmayan kayıt:** mimari bir karar alındığında veya kritik bir refactor yapıldığında ajan hafızaya otomatik düğüm atmayı unutabiliyor.

---

## 2. 🎯 çözüm mimarisi: görünmez otonom refleksler (invisible autonomous reflexes)

kullanıcı hiçbir şey yapmaz; normal şekilde talebini iletir ("bana bir auth servisi kur", "veritabanı şemasını optimize et" vb.). sistem şu üç görünmez refleksi otomatik çalıştırır:

1. **otonom bağlam çağırma (pre-execution memory context injection):**
   - plan veya mimari aşamasına giren ajan (`project-planner`, `orchestrator`, `backend-specialist`), kullanıcı talebini alır almaz arka planda neural-os motorunu sorgular.
   - geçmişte alınmış kararları (`adr`) ve ilgili standartları belleğe otomatik çeker; kullanıcıya "geçmiş kararlar hafızadan okundu" şeklinde tek satırlık şeffaf bilgi verir.
2. **otonom karar ve epizot kaydı (post-execution auto-recording):**
   - görev tamamlandığında veya kritik bir mimari tercih yapıldığında, ajan kural 17 gereğince kullanıcıya sormadan arka planda hafızaya yeni bir `decision` (adr) veya `episode` düğümü ekler ve ilgili kavramlara `[[wikilink]]` ile bağlar.
3. **tek tıkla açılan arka plan paneli (silent daemon server):**
   - kullanıcı zihin haritasını görmek istediğinde sunucuyu terminalde asılı bırakmak zorunda kalmaz; arayüz arka planda sessiz bir servis (daemon/subagent) olarak tek tıkla ayağa kaldırılır.

---

## 3. 📋 aşamalı icra planı

> **kural 2 & kural 3 gereğince:** her aşama bağımsız olarak tamamlanacak, doğrulanacak ve sırayla onayınıza sunulacaktır.

### 🔹 modül 1: otonom ajan hafıza protokolü (`auto_memory.py`)
- ajanların tek satır python veya cli fonksiyonuyla hafızadan en alakalı bağlamı anında okumasını sağlayan hafif kütüphane (`get_relevant_context(prompt)`).
- mimari bir karar alındığında otomatik adr üreten ve epizot kaydeden akıllı fonksiyon (`auto_record_decision(...)`, `auto_record_episode(...)`).

### 🔹 modül 2: temel uzman ajanlara otonom reflekslerin kazandırılması
- `orchestrator.md`, `project-planner.md`, `backend-specialist.md`, `security-auditor.md` ajan kurallarına "her görev başlangıcında neural-os bağlamını oku, görev bitiminde otomatik hafızaya işle" otonom kuralının (p0 seviyesinde) eklenmesi.

### 🔹 modül 3: sıfır sürtünmeli görselleştirme ve arka plan servis entegrasyonu
- terminali kilitlemeyen arka plan web servisi ve `checklist.py` / doğrulama akışlarına otomatik grafik denetiminin (`neural-os audit`) dahil edilmesi.
- `main` dalına nihai birleştirme.
