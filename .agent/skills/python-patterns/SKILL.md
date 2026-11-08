---
name: python-patterns
description: kurumsal python geliştirme ilkeleri. çerçeve seçimi, tip ipuçları (type hints), asenkron desenler ve mimari yapı.
priority: p1-structural
version: 2.0.0
---

# kurumsal python geliştirme ve mimari standartları

bu beceri; modern, asenkron, tip güvenli, bellek dostu ve kurumsal standartlara uygun python (fastapi, pydantic, sqlalchemy) sistemleri inşa etmeyi yönetir.

---

## 🚨 kural öncelik hiyerarşisi

1. **p0 (mutlak öncelik - temel 14 kural):**
   - tüm çıktılar, açıklamalar ve dokümanlar küçük harfle yazılır ve türkçe karakterler (`ç, ğ, ı, ö, ş, ü`) eksiksiz kullanılır.
   - sorgusuz modüler icra esastır; kullanıcıya gereksiz sorular sorulmaz.
   - adım adım aşamalı yürütülür; her seferinde tek bir modül tamamlanır.
   - sadelik ve modern trend teknolojiler: python 3.12+, fastapi, pydantic v2, uv/poetry.
   - katı api güvenliği (6. kural), hassas veri koruması (7. kural) ve idor/bola önleme (8. kural).
   - bellek sızıntısı analizi (10. kural), sayfalama (11. kural) ve owasp oturum denetimi (14. kural).
2. **p1 (küresel kurallar):** `.agent/rules/gemini.md` yönergeleri.
3. **p2 (ajan kuralları):** aktif uzman ajanın `.agent/agents/{ajan}.md` dosyası.
4. **p3 (beceri kuralları):** bu dokümandaki python teknik standartları.

---

## 🐍 kurumsal python ilkeleri

### 1. katı tip güvenliği ve pydantic v2 (6. kural uyumu)
- tüm fonksiyon imzalarında, servis sınıflarında ve veri transfer nesnelerinde (dto) kapsamlı tip ipuçları (`type hints`) zorunludur:
  ```python
  from pydantic import BaseModel, Field, EmailStr

  class UserCreateSchema(BaseModel):
      email: EmailStr
      role: str = Field(default="user", pattern="^(user|editor|admin)$") # 5. kural
      
      class Config:
          extra = "forbid" # tanımsız alan enjeksiyonunu engelle (6. kural)
  ```

### 2. asenkron mimari ve g/ç bloklanmasını önleme (9. kural)
- web ve api katmanlarında `async / await` yapısı kullanılmalı, g/ç operasyonları (veritabanı sorguları, dış api çağrıları) asenkron kütüphanelerle (`asyncpg`, `httpx`, `aiofiles`) yürütülmelidir.
- cpu yoğun işler için olay döngüsünü (event loop) kilitlemek yerine `run_in_threadpool` veya arka plan işçileri (celery, rq, arq) kullanılmalıdır.

### 3. idor ve yetki denetimi (8. kural uyumu)
- fastapi bağımlılık enjeksiyonu (`Depends`) ile kaynak düzeyinde yetkilendirme doğrulaması:
  ```python
  from fastapi import Depends, HTTPException, status

  async def get_user_invoice(
      invoice_id: str, 
      current_user: User = Depends(get_current_active_user),
      db: AsyncSession = Depends(get_db)
  ) -> Invoice:
      # sahiplik ve organizasyon filtresi veritabanı sorgusunda zorunludur
      query = select(Invoice).where(
          Invoice.id == invoice_id,
          Invoice.owner_id == current_user.id
      )
      result = await db.execute(query)
      invoice = result.scalar_one_or_none()
      
      if not invoice:
          raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
              detail="kayıt bulunamadı"
          )
      return invoice
  ```

### 4. bellek yönetimi ve jeneratörler (generators) (9. ve 10. kural)
- büyük veri kitlelerini listeye yüklemek yerine bellek tüketimini sabit tutan jeneratörler veya asenkron yineleyiciler (`AsyncGenerator`) kullanılmalıdır:
  ```python
  async def stream_large_dataset(db: AsyncSession) -> AsyncGenerator[dict, None]:
      # verileri belleğe yığmadan parça parça akıt
      async for row in await db.stream(select(LargeModel)):
          yield row.to_dict()
  ```

### 5. hassas verilerin korunması ve ortam yönetimi (7. kural)
- pydantic-settings kullanılarak ortam değişkenleri tip kontrollü yüklenmeli, gizli anahtarlar için `SecretStr` kullanılmalıdır (böylece loglarda açığa çıkmaz):
  ```python
  from pydantic_settings import BaseSettings
  from pydantic import SecretStr

  class Settings(BaseSettings):
      database_url: SecretStr
      jwt_secret: SecretStr

      class Config:
          env_file = ".env"
  ```
