---
name: threat-mitigation-mapping
description: tespit edilen güvenlik açıklarını ve tehditleri mitre att&ck, owasp ve cwe savunma kalıplarıyla eşleme.
when_to_use: "tespit edilen guvenlik tehditlerini owasp ve mitre savunma kaliplariyla eslerken kullanilir."
allowed-tools: Read, Write, Grep, Glob
version: 1.0.0
---

# tehdit azaltma ve önlem haritalama (threat mitigation mapping)

> her güvenlik tehdidini kanitlanmis kurumsal savunma kalıpları ve karşıt tedbirlerle (mitigations) eşleştirin.

## 🎯 haritalama disiplini

- **owasp api top 10 eslemesi:** bola/bfla -> 8. kural sahiplik denetimi, rate limiting -> 41. kural token bucket.
- **mitre att&ck savunma stratejisi:** ilk erişim, yetki yükseltme ve yatay hareket noktalarına spesifik kontroller.
- **onceliklendirme matrisi:** tehdidin olasılığı ve etkisi hesaplanarak `p0 (kritik)` ile `p3 (düşük)` arasında derecelendirilir.

## 🚨 temel kurallar

1. **kapsam şeffaflığı (19. kural):** hangi riskin nasıl bertaraf edildiği açıkça raporlanır.
2. **somut düzeltme opsiyonları (12. ve 14. kural):** soyut uyarı yerine somut kod düzeltmesi sunulur.
