---
name: skillify
description: tekrarlanan is akislarindan otomatik yeni beceriler üretme. cok adimli kalıpları yeniden kullanılabilir skill.md dosyalarına dönüştürür.
when_to_use: "kullanıcı 'bunu bir beceri yap', 'bunu kaydet' dediğinde veya tekrarlayan bir operasyonel süreç tespit edildiğinde kullanılır."
allowed-tools: Read, Write, Glob, Grep
version: 1.0.0
effort: low
---

# beceri üretici (skillify) — tekrarlanan süreçleri beceriye donusturme

> tekrarlayan operasyonel kalıpları yeniden kullanılabilir, kurumsal yapay zeka becerilerine dönüştürün. uc kez yaptıysanız, o artık bir beceri olmalıdır.

## 🎯 üretim adimlari

1. **kalip tespiti:** tekrarlanan surecin adımlarını, araçlarını ve doğrulama noktalarını çıkarın.
2. **standart yapilandirma:** SKILL.md formatında ad, aciklama, tetikleyiciler ve kurallar tanımlayın.
3. **kucuk harf ve türkçe standardi:** tum rehberi eksiksiz türkçe karakterlerle yapilandirin.
4. **katalog kaydi:** yeni beceriyi araç kiti manifestosuna ve bagimlilik grafiğine ekleyin.

## 🚨 temel kurallar

1. **46 temel kural hiyerarsisi:** üretilen yeni beceri sistemin p0 kurallarina tam uyumlu olmalıdır.
2. **test ve dogrulama:** oluşturulan becerinin validate_kit.py denetiminden başarıyla geçmesini sağlayın.
