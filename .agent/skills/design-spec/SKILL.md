---
name: design-spec
description: modern arayuzler için design.md belirteç (token) ve tasarim manifestosu oluşturma ilkeleri. arayüz kodlanmadan once tasarim kaynağı tanımlar.
when_to_use: "herhangi bir kullanıcı arayüzü (web veya mobil) inşa edilmeden once, tasarim belirteçleri ve görsel dil kuralları tanımlanırken kullanılır."
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# design.md tasarim belirteçleri ve sartnamesi

> bir arayüz inşa edilmeden once projenin görsel dili ve tek gerçeklik kaynağı (source of truth) design.md icinde tanimlanmalidir.

## 🎯 genel bakis

tasarim şartnamesi iki katmandan olusur:
1. **makinece okunabilir belirteçler (yaml frontmatter):** renk paletleri, tipografi ölçekleri, boşluklar, yuvarlatmalar.
2. **insanca okunabilir mantık (markdown gövdesi):** tasarim kararlarinin gerekçeleri, kullanıcı deneyimi ilkeleri.

## 🚨 tasarim kuralları ve yasaklar

1. **mor renk yasağı (purple ban):** kurumsal ve özgün projelerde mor/eflatun/violet tonlari varsayılan olarak yasaktır.
2. **sablon yasağı (anti-cliche):** yapay zeka klişesi olan jenerik kartlar ve asiri gradyanlar engellenir.
3. **60-30-10 renk dengesi:** %60 arka plan / yüzey, %30 yapısal elemanlar, %10 odak eylem (cta) renkleri.
4. **tipografi disiplini (16. kural):** 2-3 font ailesi ile sınırlı kalinir.
