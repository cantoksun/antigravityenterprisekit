---
description: proje planlama, mimari analiz ve görev kırılımı prosedürü. kod yazılmaz; yalnızca modüler plan dosyası oluşturulur.
---

# 📋 /plan - proje planlama ve görev kırılımı iş akışı

bu iş akışı karmaşık geliştirme isteklerinde kod yazmadan önce mimari planlama ve aşama kırılımı oluşturur.

## 🎯 yürütülecek plan talebi
$ARGUMENTS

---

## 🚨 temel kurallar

1. **kod yazılmaz**: bu iş akışının çıktısı yalnızca yapılandırılmış bir plan belgesidir (`docs/plan-{task-slug}.md`).
2. **uzman ajan**: planlama `@[project-planner]` uzmanlığıyla yürütülür.
3. **modüler aşama tasarımı (3. ve 19. kural)**: plan tek seferde bitirilecek devasa bir blok değil, her turda tek bir bağımsız modülün bitirileceği adımlar şeklinde kurgulanır.
4. **dinamik isimlendirme**: talep başlığından 2-3 anahtar kelime türetilerek küçük harfli dosya adı oluşturulur (ör. `docs/plan-auth-system.md`).

---

## 📄 plan dosyası şablonu ve beklenen içerik

üretilecek plan dosyasında bulunması gereken zorunlu başlıklar:
- **özet ve iş değeri**: ne yapılıyor ve hedef ne?
- **etkilenecek bileşenler (18. kural teyidi)**: varlığı doğrulanmış dosya ve modeller.
- **aşama 1 - çekirdek & veritabanı**: yalın şema ve güvenlik modelleri (5., 6., 8. kural).
- **aşama 2 - arayüz & responsive ux**: alt çekmece/modal ayrımı ve sıfır kayma (15. kural).
- **aşama 3 - doğrulama & test**: checklist.py ve playwright testleri.

---

## 🚨 katı kurallar

- tüm metinler küçük harflerle ve türkçe karakterler (ç, ğ, ı, ö, ş, ü) eksiksiz kullanılarak yazılmalıdır.
- kullanıcıya gereksiz sorular sormadan doğrudan analiz ve modüler icra (2. kural) uygulanmalıdır.
