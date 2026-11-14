---
name: coordinator-mode
description: paralel çalışanlar ve sentez protokolleri ile gelişmiş çoklu ajan orkestrasyonu. karmaşık işlerde paralel ajanlari yönlendirir.
when_to_use: "çoklu ajan koordinasyonu, paralel görev yürütme veya karmaşık cok disiplinli projelerde /coordinate veya /orchestrate çağrıldığında kullanılır."
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, Agent
version: 1.0.0
effort: high
---

# koordinatör modu (coordinator mode) — çoklu ajan orkestrasyonu

> ardışık ajan zincirlerini akilli, paralel ve sonuc sentezleyen kurumsal orkestrasyona dönüştürün.

## 🎯 genel bakış ve orkestrasyon dongusu

1. **kesif ve görev ayristirma:** problemi bağımsız, paralel yürütülebilir modullere ayırın.
2. **uzman ajan gorevlendirmesi:** frontend, backend, guvenlik ve qa uzmanlarına net sınırlar tanımlayın.
3. **sentez ve çatışma cozumu:** uzmanlardan gelen çıktıları birleştirin, çelişen kararları kural hiyerarşisine gore çözün.
4. **dogrulama kapisi:** tum çıktılar entegre edildikten sonra checklist ve testleri çalıştırın.

## 🚨 temel kurallar

1. **adim adim modüler icra (3. kural):** tek turda tek modül kuralına sadık kalın, her aşamada kullanıcıyı şeffafça bilgilendirin.
2. **kullaniciyi yormama (17. kural):** teknik pürüzleri ajanlar arası diyalogla otonom çözün.
