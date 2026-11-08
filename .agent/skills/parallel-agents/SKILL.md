---
name: parallel-agents
description: çoklu ajan orkestrasyon kalıpları. birden fazla bağımsız görev farklı uzmanlık alanlarıyla çalışabileceğinde veya kapsamlı analiz için birden fazla bakış açısı gerektiğinde kullanılır.
---

# paralel ajan orkestrasyonu

bu beceri, birden fazla uzman ajanın eş zamanlı ve senkronize olarak nasıl çalıştırılacağını belirler.

## temel ilkeler

1. **bağımsız görev ayrımı**: birbiriyle doğrudan bağımlılığı olmayan görevler eş zamanlı (paralel) alt ajanlara dağıtılır.
2. **rol sınırları**: her alt ajan yalnızca kendi uzmanlık alanına (frontend, backend, güvenlik, test) odaklanır; sınır aşımı yapılmaz.
3. **sonuçların sentezlenmesi**: orkestratör tüm alt ajanlardan gelen çıktıları toplar, çelişkileri çözer ve tek bir uyumlu kurumsal çözüm sunar.
4. **üslup kuralı**: tüm açıklamalar küçük harflerle ve türkçe karakterler (ç, ğ, ı, ö, ş, ü) eksiksiz kullanılarak yapılandırılmalıdır.
