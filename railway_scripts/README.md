# Railway ML Migration Scripts

Railway veritabanına ML (Machine Learning) sistemini kurmak için kullanılan scriptler.

## 📋 Scriptler

### 1. Kurulum Scriptleri

#### `apply_ml_migration_railway.py`
ML tablolarını Railway veritabanına oluşturur.
```bash
python railway_scripts/apply_ml_migration_railway.py
```

**Oluşturduğu Tablolar:**
- `ml_metrics` (11 kolon)
- `ml_models` (11 kolon)
- `ml_alerts` (15 kolon)
- `ml_training_logs` (10 kolon)

#### `fix_ml_alerts_railway.py`
ml_alerts tablosundaki kolon uyumsuzluğunu düzeltir.
```bash
python railway_scripts/fix_ml_alerts_railway.py
```

### 2. Enum Güncelleme Scriptleri

#### `railway_update_ml_enums.py` (Phase 2)
Zimmet ve doluluk metriklerini ekler.
```bash
python railway_scripts/railway_update_ml_enums.py
```

**Eklediği Metrikler:**
- zimmet_kullanim
- zimmet_fire
- doluluk_oran
- bosta_tuketim

#### `railway_update_ml_enums_phase3.py` (Phase 3)
QR ve Talep sistemi metriklerini ekler.
```bash
python railway_scripts/railway_update_ml_enums_phase3.py
```

**Eklediği Metrikler:**
- talep_yanit_sure
- talep_yogunluk
- qr_okutma_siklik

### 3. Kontrol ve Test Scriptleri

#### `railway_check_ml_tables.py`
ML tablolarının durumunu kontrol eder.
```bash
python railway_scripts/railway_check_ml_tables.py
```

#### `railway_ml_final_test.py`
Tüm ML bileşenlerinin çalıştığını doğrular.
```bash
python railway_scripts/railway_ml_final_test.py
```

**Test Ettiği Bileşenler:**
- ✅ Bağlantı testi
- ✅ ML tabloları
- ✅ Enum değerleri
- ✅ Index'ler
- ✅ Foreign key'ler
- ✅ Test sorguları

#### `verify_ml_tables_railway.py`
ML tablolarının model ile uyumunu kontrol eder.

#### `check_ml_alerts_columns.py`
ml_alerts tablosunun kolon yapısını kontrol eder.

#### `check_ml_tables_railway.py`
ML tablolarının detaylı bilgilerini gösterir.

#### `list_railway_tables.py`
Railway veritabanındaki tüm tabloları listeler.

#### `test_railway_connection.py`
Railway bağlantısını ve ML tablolarını test eder.

## 🚀 Kurulum Sırası

Railway'e ML sistemini kurmak için şu sırayı izleyin:

```bash
# 1. ML tablolarını oluştur
python railway_scripts/apply_ml_migration_railway.py

# 2. ml_alerts tablosunu düzelt (gerekirse)
python railway_scripts/fix_ml_alerts_railway.py

# 3. Phase 2 enum'ları ekle
python railway_scripts/railway_update_ml_enums.py

# 4. Phase 3 enum'ları ekle
python railway_scripts/railway_update_ml_enums_phase3.py

# 5. Final test
python railway_scripts/railway_ml_final_test.py
```

## 📊 Sonuç

Tüm scriptler başarıyla çalıştıktan sonra:

- **4 ML tablosu** oluşturulur
- **15 index** kurulur
- **5 foreign key** ilişkisi tanımlanır
- **12 metrik tipi** kullanılabilir hale gelir
- **12 alert tipi** tanımlanır
- **4 severity seviyesi** kullanılabilir

## ⚙️ Gereksinimler

```
python-dotenv
SQLAlchemy
psycopg2-binary
```

## 📝 .env.railway Dosyası

Scriptlerin çalışması için `.env.railway` dosyasında şu değişken olmalı:

```bash
RAILWAY_DATABASE_URL=postgresql://postgres:PASSWORD@shinkansen.proxy.rlwy.net:PORT/railway
```

## 🔧 Sorun Giderme

### Bağlantı Hatası
```bash
# Bağlantıyı test edin
python railway_scripts/test_railway_connection.py
```

### Enum Hatası
Enum zaten varsa hata vermez, zaten mevcut olduğunu bildirir.

### Tablo Hatası
```bash
# Tabloları kontrol edin
python railway_scripts/railway_check_ml_tables.py
```

## 📅 Tarihçe

- **09.11.2025** - Phase 3 eklendi (QR & Talep metrikleri)
- **09.11.2025** - Phase 2 eklendi (Zimmet & Doluluk metrikleri)
- **09.11.2025** - İlk ML tabloları oluşturuldu
- **09.11.2025** - ml_alerts tablosu düzeltildi

## 🎯 İletişim

Sorularınız için: Optimus825482

## 📜 Lisans

Minibar Takip Sistemi - 2025
