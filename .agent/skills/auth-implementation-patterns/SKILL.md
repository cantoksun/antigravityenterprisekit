---
name: auth-implementation-patterns
description: kurumsal oauth2, openid connect (oidc), jwt ömür döngüsü, session yönetimi, mfa ve rbac/abac mimarileri.
when_to_use: "oauth2, oidc, mfa, jwt oturum omur dongusu ve rbac yetki mimarisi kurulurken kullanilir."
allowed-tools: Read, Write, Edit, Grep
version: 1.0.0
---

# kurumsal kimlik doğrulama ve yetkilendirme (auth implementation patterns)

> endüstri standardi oauth2, oidc, güvenli çerez tabanlı oturum yönetimi ve rol bazli erişim denetimi.

## 🎯 mimari bilesenler

1. **token ve oturum ömür dongusu:**
   - access token: kısa ömürlü (5-15 dakika), yalnızca ram'de veya httponly çerezde tutulur.
   - refresh token: dönen belirteç (token rotation), yetkisiz kullanımda oturumu kilitler.
2. **istemci tarafı güvenlik (14. kural):**
   - hassas belirteçler asla `localStorage` icinde tutulmaz; `httpOnly, Secure, SameSite=Strict` cerezler zorunludur.
3. **rol ve yetki modeli (5. ve 8. kural):**
   - sade `role` ve `permissions` modeli. her api uc noktasında nesne seviyesi yetki denetimi (`resource.owner_id === user.id`).

## 🚨 temel kurallar

1. **kati api güvenliği (6. kural):** girdi doğrulama ve brute-force engeli.
2. **sifre ve sir koruması (7. kural):** argon2/bcrypt ile güçlü özetleme (hashing).
