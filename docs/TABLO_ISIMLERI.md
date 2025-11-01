# 🗂️ VERİTABANI TABLO İSİMLERİ

## 📋 Doğru Tablo İsimleri

Veritabanında kullanılan **gerçek** tablo isimleri (models.py'den alınmıştır):

### Ana Tablolar
| Model Adı | Tablo Adı |
|-----------|-----------|
| `Otel` | `oteller` |
| `Kullanici` | `kullanicilar` |
| `Kat` | `katlar` |
| `Oda` | `odalar` |
| `UrunGrup` | `urun_gruplari` |
| `Urun` | `urunler` |

### İşlem Tabloları
| Model Adı | Tablo Adı |
|-----------|-----------|
| `StokHareket` | `stok_hareketleri` |
| `PersonelZimmet` | `personel_zimmet` ⚠️ (tekil!) |
| `PersonelZimmetDetay` | `personel_zimmet_detay` ⚠️ (tekil!) |
| `MinibarIslem` | `minibar_islemleri` |
| `MinibarIslemDetay` | `minibar_islem_detay` ⚠️ (tekil!) |

### Sistem Tabloları
| Model Adı | Tablo Adı |
|-----------|-----------|
| `SistemAyar` | `sistem_ayarlari` |
| `SistemLog` | `sistem_loglari` |
| `HataLog` | `hata_loglari` |
| `AuditLog` | `audit_logs` ⚠️ (İngilizce!) |
| `OtomatikRapor` | `otomatik_raporlar` |

---

## ⚠️ Önemli Notlar

### Tekil vs Çoğul Karışıklığı

**Çoğul (çokluk eki -ler/-lar):**
- ✅ `oteller`
- ✅ `kullanicilar`
- ✅ `katlar`
- ✅ `odalar`
- ✅ `urun_gruplari`
- ✅ `urunler`
- ✅ `stok_hareketleri`
- ✅ `minibar_islemleri`
- ✅ `sistem_ayarlari`
- ✅ `sistem_loglari`
- ✅ `hata_loglari`
- ✅ `otomatik_raporlar`

**Tekil (çokluk eki YOK!):**
- ⚠️ `personel_zimmet` (personel_zimmetler ❌)
- ⚠️ `personel_zimmet_detay` (personel_zimmet_detaylari ❌)
- ⚠️ `minibar_islem_detay` (minibar_islem_detaylari ❌)

**İngilizce:**
- 🔤 `audit_logs` (denetim_kayitlari değil!)

---

## 🔧 Sistem Sıfırlama İçin Doğru Sıralama

Foreign key kısıtları nedeniyle silme sırası önemlidir:

```sql
-- 1. Detay tabloları önce (foreign key var)
DELETE FROM minibar_islem_detay;        -- ⚠️ TEKİL!
DELETE FROM minibar_islemleri;

DELETE FROM personel_zimmet_detay;      -- ⚠️ TEKİL!
DELETE FROM personel_zimmet;            -- ⚠️ TEKİL!

DELETE FROM stok_hareketleri;

-- 2. Ürün tabloları
DELETE FROM urunler;
DELETE FROM urun_gruplari;

-- 3. Oda ve kat tabloları
DELETE FROM odalar;
DELETE FROM katlar;

-- 4. Kullanıcı ve otel tabloları
DELETE FROM kullanicilar;
DELETE FROM oteller;

-- 5. Log tabloları
DELETE FROM sistem_loglari;
DELETE FROM hata_loglari;
DELETE FROM audit_logs;                 -- ⚠️ İNGİLİZCE!
DELETE FROM otomatik_raporlar;

-- 6. Sistem ayarları
DELETE FROM sistem_ayarlari WHERE anahtar = 'setup_tamamlandi';
```

---

## 🚨 Yaygın Hatalar

### ❌ YANLIŞ
```python
DELETE FROM minibar_islem_detaylari  # Tablo yok!
DELETE FROM personel_zimmet_detaylari  # Tablo yok!
DELETE FROM personel_zimmetler  # Tablo yok!
DELETE FROM denetim_kayitlari  # Tablo yok!
```

### ✅ DOĞRU
```python
DELETE FROM minibar_islem_detay  # ✓
DELETE FROM personel_zimmet_detay  # ✓
DELETE FROM personel_zimmet  # ✓
DELETE FROM audit_logs  # ✓
```

---

## 📝 SQL Sorgu Örnekleri

### Tüm Tabloları Listele
```sql
SHOW TABLES;
```

### Tablo Yapısını Görüntüle
```sql
DESCRIBE personel_zimmet_detay;
DESCRIBE minibar_islem_detay;
DESCRIBE audit_logs;
```

### Kayıt Sayılarını Kontrol Et
```sql
SELECT 
    'personel_zimmet' as tablo, COUNT(*) as kayit FROM personel_zimmet
UNION ALL
SELECT 
    'personel_zimmet_detay', COUNT(*) FROM personel_zimmet_detay
UNION ALL
SELECT 
    'minibar_islem_detay', COUNT(*) FROM minibar_islem_detay;
```

---

## 🔄 Düzeltme Geçmişi

### Versiyon 1.0.1 (1 Kasım 2025)
- ❌ Hatalı: `minibar_islem_detaylari`
- ✅ Düzeltildi: `minibar_islem_detay`

- ❌ Hatalı: `personel_zimmet_detaylari`
- ✅ Düzeltildi: `personel_zimmet_detay`

- ❌ Hatalı: `personel_zimmetler`
- ✅ Düzeltildi: `personel_zimmet`

---

## 🎯 Kontrol Listesi

Yeni bir SQL sorgusu yazarken kontrol edin:

- [ ] `personel_zimmet` - TEKİL ✓
- [ ] `personel_zimmet_detay` - TEKİL ✓
- [ ] `minibar_islem_detay` - TEKİL ✓
- [ ] `audit_logs` - İNGİLİZCE ✓
- [ ] Diğer tablolar - ÇOĞUL ✓

---

**Son Güncelleme:** 1 Kasım 2025  
**Durum:** ✅ Tüm tablo isimleri düzeltildi
