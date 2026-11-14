---
name: k8s-manifest-generator
description: deployment, service, configmap ve secret için kurumsal standartlarda kubernetes manifestoları üretimi. kaynak limitleri, sağlık denetimleri ve güvenlik baglamlari.
when_to_use: "kubernetes deployment, service, secret veya configmap manifestolari hazirlarken kullanilir."
allowed-tools: Read, Write, Edit, Glob
version: 1.0.0
---

# kubernetes manifesto üretimi (k8s manifest generator)

> üretim ortamlarina hazır, güvenli ve kaynak sınırları belirlenmiş kubernetes manifestoları olusturma ilkeleri.

## 🎯 genel bakış ve üretim standartlari

kurumsal kubernetes dagitimlarinda su kaynaklar eksiksiz yapilandirilir:
- **deployments:** dönel güncelleme (rolling update), hazır olma (readiness) ve canlilik (liveness) probları (31. kural).
- **kaynak limitleri:** `requests` ve `limits` (cpu & ram) mutlaka tanimlanir; kontrolsüz pod şişmesi engellenir (9. kural).
- **guvenlik bağlamı (securitycontext):** `runAsNonRoot: true`, `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`.
- **secrets & configmaps:** hassas veriler düz metin gömülmez, secret referansları ile verilir (7. kural).

## 🚨 temel kurallar

1. **p0 kuralları mutlak baglayicidir:** açıklamalar küçük harfle ve türkçe karakterlerle sunulur.
2. **otonom hijyen (45. kural):** geçici yaml denemeleri ana kod ağacında bırakılmaz.
