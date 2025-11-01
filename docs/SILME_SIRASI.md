# 🔄 SİSTEM SIFIRLAMA - SİLME SIRASI

## ⚠️ KRİTİK: Foreign Key Sıralaması

Veritabanı tablolarını silerken **foreign key kısıtlarına** uygun sıralama şarttır!

---

## 📋 Doğru Silme Sırası

### 1️⃣ Detay Tabloları (En Bağımlı)

```sql
-- Minibar detayları (foreign key: minibar_islemleri)
DELETE FROM minibar_islem_detay;

-- Minibar işlemleri
DELETE FROM minibar_islemleri;

-- Zimmet detayları (foreign key: personel_zimmet)
DELETE FROM personel_zimmet_detay;

-- Zimmet ana tablo
DELETE FROM personel_zimmet;
```

### 2️⃣ Stok ve Ürün Tabloları

```sql
-- Stok hareketleri (foreign key: urunler)
DELETE FROM stok_hareketleri;

-- Ürünler (foreign key: urun_gruplari)
DELETE FROM urunler;

-- Ürün grupları
DELETE FROM urun_gruplari;
```

### 3️⃣ Oda ve Kat Tabloları

```sql
-- Odalar (foreign key: katlar)
DELETE FROM odalar;

-- Katlar (foreign key: oteller)
DELETE FROM katlar;
```

### 4️⃣ Log ve Audit Tabloları (Foreign Key: kullanicilar!)

**⚠️ ÖNEMLİ:** Kullanıcılar silinmeden önce log tabloları silinmeli!

```sql
-- Sistem logları (foreign key: kullanicilar)
DELETE FROM sistem_loglari;

-- Hata logları (foreign key: kullanicilar)
DELETE FROM hata_loglari;

-- Audit trail (foreign key: kullanicilar)
DELETE FROM audit_logs;

-- Otomatik raporlar (foreign key: kullanicilar - varsa)
DELETE FROM otomatik_raporlar;
```

### 5️⃣ Kullanıcı ve Otel Tabloları

```sql
-- Kullanıcılar (foreign key: oteller)
DELETE FROM kullanicilar;

-- Oteller (ana tablo)
DELETE FROM oteller;
```

### 6️⃣ Sistem Ayarları

```sql
-- Setup ayarını sıfırla
DELETE FROM sistem_ayarlari WHERE anahtar = 'setup_tamamlandi';
```

---

## 🔴 Yaygın Hatalar ve Çözümleri

### Hata 1: Foreign Key Constraint Failure

```
❌ ERROR: Cannot delete or update a parent row: 
   a foreign key constraint fails
   (audit_logs_ibfk_1 FOREIGN KEY (kullanici_id) 
   REFERENCES kullanicilar (id))
```

**Sebep:** Kullanıcılar silinmeden önce audit_logs silinmeli!

**Çözüm:**
```python
# YANLIŞ SIRA:
DELETE FROM kullanicilar;  # ❌ Önce bu
DELETE FROM audit_logs;    # ❌ Sonra bu - HATA!

# DOĞRU SIRA:
DELETE FROM audit_logs;     # ✅ Önce bağımlı tablo
DELETE FROM kullanicilar;   # ✅ Sonra ana tablo
```

### Hata 2: Tablo Bulunamadı

```
❌ ERROR: Table 'minibar_takip.minibar_islem_detaylari' doesn't exist
```

**Sebep:** Tablo ismi yanlış!

**Çözüm:** 
- ❌ `minibar_islem_detaylari` (Yanlış)
- ✅ `minibar_islem_detay` (Doğru - tekil!)

---

## 🔍 Foreign Key İlişkileri

### Hangi Tablolar Hangi Tablolara Bağlı?

```
minibar_islem_detay
  └─► minibar_islemleri (islem_id)
  └─► urunler (urun_id)
  └─► personel_zimmet_detay (zimmet_detay_id)

minibar_islemleri
  └─► odalar (oda_id)
  └─► kullanicilar (personel_id)

personel_zimmet_detay
  └─► personel_zimmet (zimmet_id)
  └─► urunler (urun_id)

personel_zimmet
  └─► kullanicilar (personel_id)
  └─► kullanicilar (teslim_eden_id)

stok_hareketleri
  └─► urunler (urun_id)
  └─► kullanicilar (kullanici_id)

urunler
  └─► urun_gruplari (grup_id)

odalar
  └─► katlar (kat_id)

katlar
  └─► oteller (otel_id)

kullanicilar
  └─► oteller (otel_id)

sistem_loglari
  └─► kullanicilar (kullanici_id)

hata_loglari
  └─► kullanicilar (kullanici_id)

audit_logs
  └─► kullanicilar (kullanici_id)
```

---

## ⚙️ Python Kod Bloğu

```python
# DOĞRU SIRA - app.py içindeki reset_system fonksiyonu

# 1. Minibar detay ve işlemleri
db.session.execute(db.text("DELETE FROM minibar_islem_detay"))
db.session.execute(db.text("DELETE FROM minibar_islemleri"))

# 2. Zimmet detay ve ana tablo
db.session.execute(db.text("DELETE FROM personel_zimmet_detay"))
db.session.execute(db.text("DELETE FROM personel_zimmet"))

# 3. Stok hareketleri
db.session.execute(db.text("DELETE FROM stok_hareketleri"))

# 4. Ürünler ve gruplar
db.session.execute(db.text("DELETE FROM urunler"))
db.session.execute(db.text("DELETE FROM urun_gruplari"))

# 5. Odalar ve katlar
db.session.execute(db.text("DELETE FROM odalar"))
db.session.execute(db.text("DELETE FROM katlar"))

# 6. LOG TABLOLARI - KULLANICILARDAN ÖNCE!
db.session.execute(db.text("DELETE FROM sistem_loglari"))
db.session.execute(db.text("DELETE FROM hata_loglari"))
db.session.execute(db.text("DELETE FROM audit_logs"))
db.session.execute(db.text("DELETE FROM otomatik_raporlar"))

# 7. Kullanıcılar ve oteller
db.session.execute(db.text("DELETE FROM kullanicilar"))
db.session.execute(db.text("DELETE FROM oteller"))

# 8. Setup ayarı sıfırla
db.session.execute(db.text("DELETE FROM sistem_ayarlari WHERE anahtar = 'setup_tamamlandi'"))

# 9. Commit
db.session.commit()
```

---

## 📊 Tablo Bağımlılık Grafiği

```
SEVIYE 0 (Hiç bağımlı değil):
└─ urun_gruplari
└─ oteller
└─ sistem_ayarlari

SEVIYE 1 (Seviye 0'a bağlı):
├─ urunler (→ urun_gruplari)
├─ katlar (→ oteller)
└─ kullanicilar (→ oteller)

SEVIYE 2 (Seviye 1'e bağlı):
├─ odalar (→ katlar)
├─ personel_zimmet (→ kullanicilar)
├─ stok_hareketleri (→ urunler, kullanicilar)
├─ sistem_loglari (→ kullanicilar)
├─ hata_loglari (→ kullanicilar)
├─ audit_logs (→ kullanicilar)
└─ otomatik_raporlar (→ kullanicilar)

SEVIYE 3 (Seviye 2'ye bağlı):
├─ minibar_islemleri (→ odalar, kullanicilar)
└─ personel_zimmet_detay (→ personel_zimmet, urunler)

SEVIYE 4 (En bağımlı):
└─ minibar_islem_detay (→ minibar_islemleri, urunler, personel_zimmet_detay)

SİLME SIRASI: SEVIYE 4 → SEVIYE 3 → SEVIYE 2 → SEVIYE 1 → SEVIYE 0
```

---

## ✅ Kontrol Listesi

Sistem sıfırlama öncesi kontrol edin:

- [ ] Yedek alındı mı? 💾
- [ ] Production ortamında mı? ⚠️
- [ ] Silme sırası doğru mu? 📋
- [ ] Log tabloları kullanıcılardan önce mi? 🔴
- [ ] Tablo isimleri doğru mu? (tekil/çoğul) ✏️
- [ ] Foreign key kısıtları dikkate alındı mı? 🔗
- [ ] Auto-increment sıfırlanacak mı? 🔄

---

## 🚨 Acil Durum Kurtarma

Eğer hata olursa:

### 1. Rollback
```python
db.session.rollback()
```

### 2. Foreign Key Kontrolünü Geçici Olarak Kapat (Dikkatli!)
```sql
SET FOREIGN_KEY_CHECKS = 0;
-- Silme işlemleri
DELETE FROM ...
SET FOREIGN_KEY_CHECKS = 1;
```

**⚠️ UYARI:** Production'da kullanmayın! Veri bütünlüğünü bozabilir.

---

## 📝 Versiyon Geçmişi

### v1.0.2 (1 Kasım 2025) - KRİTİK FİX
**Değişiklik:** Log tabloları kullanıcılardan ÖNCE siliniyor

**Sebep:** 
```
audit_logs.kullanici_id → kullanicilar.id
sistem_loglari.kullanici_id → kullanicilar.id
hata_loglari.kullanici_id → kullanicilar.id
```

**Eski Sıra (HATALI):**
```python
DELETE FROM kullanicilar;  # ❌ Önce kullanıcılar
DELETE FROM audit_logs;    # ❌ Hata: Foreign key!
```

**Yeni Sıra (DOĞRU):**
```python
DELETE FROM audit_logs;     # ✅ Önce log tabloları
DELETE FROM kullanicilar;   # ✅ Sonra kullanıcılar
```

### v1.0.1 (1 Kasım 2025)
- Tablo isimleri düzeltildi (tekil/çoğul)

### v1.0.0 (1 Kasım 2025)
- İlk sürüm

---

**Son Güncelleme:** 1 Kasım 2025  
**Kritik Fix:** Log tabloları sırası düzeltildi ✅
