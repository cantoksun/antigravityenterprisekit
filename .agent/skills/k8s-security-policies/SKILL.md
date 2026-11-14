---
name: k8s-security-policies
description: kubernetes küme güvenliği, pod security standards (pss), ağ politikaları (network policies) ve rbac erişim kontrolü.
when_to_use: "pod security standards, network policies ve k8s kume ici erisim politikalari yapilandirilirken kullanilir."
allowed-tools: Read, Write, Edit, Glob
version: 1.0.0
---

# kubernetes güvenlik politikaları (k8s security policies)

> pod güvenlik standartları (pss), sıfır güven (zero trust) ağ politikaları ve en az yetki prensibiyle rbac yapılandırması.

## 🎯 temel güvenlik katmanlari

1. **pod security standards (restricted profili):**
   - root yetkilerinin kaldırılması (`runAsNonRoot: true`).
   - yetki yükseltmenin engellenmesi (`allowPrivilegeEscalation: false`).
   - linux yetkilerinin kısıtlanması (`capabilities: drop: ["ALL"]`).
2. **ag politikaları (network policies):**
   - varsayilan tum giriş ve çıkışlar reddedilir (`default deny all ingress/egress`).
   - yalnızca yetkili servisler arası trafik etiketlerle (labels) açılır.
3. **rol bazli erişim denetimi (rbac):**
   - servis hesaplarina (serviceaccount) asgari yetki verilir (`cluster-admin` rolu kesinlikle dağıtılmaz).

## 🚨 temel kurallar

1. **kati api ve nesne yetkisi (6. ve 8. kural):** küme ici erisimler daima doğrulanır.
2. **sirlarin korunması (7. kural):** etcd uzerindeki sırlar şifrelenmiş tutulur.
