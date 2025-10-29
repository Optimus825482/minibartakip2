# 🏨 Otel Minibar Takip Sistemi - Kurulum Rehberi

## 📋 Gereksinimler

- Python 3.11+
- MySQL 8.0+
- pip (Python paket yöneticisi)

## 🚀 Kurulum Adımları

### 1. Projeyi İndir

```bash
cd D:\Claude\prof
```

### 2. Python Paketlerini Yükle

```bash
pip install -r requirements.txt
```

### 3. .env Dosyası Oluştur

Proje klasöründe `.env` dosyası oluşturun ve aşağıdaki bilgileri ekleyin:

```env
# Flask Konfigürasyonu
SECRET_KEY=supersecretkey123456789_degistir

# MySQL Veritabanı Ayarları
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=BURAYA_MYSQL_SIFRENIZI_YAZIN
MYSQL_DB=minibar_takip
MYSQL_PORT=3306

# Uygulama Ayarları
FLASK_ENV=development
DEBUG=True
```

**ÖNEMLİ:** 
- `MYSQL_PASSWORD` alanına kendi MySQL şifrenizi yazın
- `SECRET_KEY` alanını güvenli bir değer ile değiştirin

### 4. Veritabanı ve Tabloları Oluştur

**Yöntem 1: Otomatik Kurulum (Önerilen)**

```bash
python init_db.py
```

Bu script:
- ✅ MySQL bağlantısını kontrol eder
- ✅ `minibar_takip` veritabanını oluşturur
- ✅ Tüm tabloları otomatik oluşturur
- ✅ Kurulumu doğrular

**Yöntem 2: Manuel Kurulum**

MySQL'e bağlanın ve şu komutu çalıştırın:

```sql
CREATE DATABASE IF NOT EXISTS minibar_takip 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

### 5. Uygulamayı Başlat

```bash
python app.py
```

Başarılı olursa şunu göreceksiniz:

```
============================================================
🏨 OTEL MİNİBAR TAKİP SİSTEMİ
============================================================

✅ Veritabanı tabloları kontrol edildi ve hazır.

🚀 Uygulama başlatılıyor...
📍 Adres: http://localhost:5014
🌙 Dark/Light tema: Sağ üstten değiştirilebilir

Durdurmak için CTRL+C kullanın
============================================================
```

### 6. Tarayıcıda Aç

```
http://localhost:5014
```

## 🎯 İlk Kullanım

1. **Setup Sayfası**: İlk açılışta otomatik olarak `/setup` sayfasına yönlendirileceksiniz
2. **Sistem Yöneticisi Oluştur**: 
   - Kullanıcı adı girin
   - Güçlü bir şifre belirleyin
   - Ad-Soyad bilgilerinizi girin
3. **Giriş Yapın**: Oluşturduğunuz hesap ile giriş yapın
4. **Otel Tanımlayın**: Sistem yöneticisi dashboard'undan otel bilgilerini girin
5. **Yapıyı Kurun**: Kat → Oda → Admin → Personel → Ürünler → Stok

## ⚠️ Sorun Giderme

### Hata: "Unknown database 'minibar_takip'"

**Çözüm:**
```bash
python init_db.py
```

### Hata: "Access denied for user 'root'@'localhost'"

**Çözüm:**
- `.env` dosyasındaki `MYSQL_PASSWORD` değerini kontrol edin
- MySQL kullanıcı adını ve şifresini doğrulayın

### Hata: "Can't connect to MySQL server"

**Çözüm:**
- MySQL servisinin çalıştığından emin olun
- Windows: `services.msc` → MySQL80 servisi başlatın

### Hata: "ModuleNotFoundError"

**Çözüm:**
```bash
pip install -r requirements.txt
```

## 📊 Veritabanı Tabloları

Sistem şu tabloları oluşturur:

1. `oteller` - Otel bilgileri
2. `kullanicilar` - Tüm kullanıcılar (rol bazlı)
3. `katlar` - Kat tanımları
4. `odalar` - Oda tanımları
5. `urun_gruplari` - Ürün kategorileri
6. `urunler` - Ürün tanımları
7. `stok_hareketleri` - Depo giriş/çıkış kayıtları
8. `personel_zimmetler` - Zimmet başlık tablosu
9. `personel_zimmet_detaylari` - Zimmet detay tablosu
10. `minibar_islemleri` - Minibar işlem başlık tablosu
11. `minibar_islem_detaylari` - Minibar işlem detay tablosu

## 🎨 Özellikler

- ✅ **4 Kullanıcı Rolü**: Sistem Yöneticisi, Admin, Depo Sorumlusu, Kat Sorumlusu
- ✅ **Stok Yönetimi**: Girişler, çıkışlar, zimmet takibi
- ✅ **Minibar Kontrol**: Başlangıç/bitiş stok, otomatik tüketim
- ✅ **Raporlama**: Excel ve PDF export
- ✅ **Dark/Light Tema**: Otomatik tema kaydı
- ✅ **Mobile Responsive**: Tablet ve telefon uyumlu

## 📞 Destek

Herhangi bir sorun yaşarsanız, lütfen geliştiriciye ulaşın.

---

**Geliştirici:** AI Assistant
**Versiyon:** 1.0.0
**Son Güncelleme:** 14 Ekim 2025

