# 🏨 OTEL MİNİBAR TAKİP SİSTEMİ - KULLANIM KILAVUZU
## BÖLÜM 1: SİSTEM GENEL BAKIŞ VE KURULUM

**Versiyon:** 1.0  
**Tarih:** 31 Ekim 2025  
**Hazırlayan:** Sistem Dokümantasyon Ekibi

---

## 📑 İÇİNDEKİLER

### Bölüm 1: Sistem Genel Bakış ve Kurulum
- Sistem Hakkında
- Teknik Özellikler
- Kurulum Adımları
- İlk Yapılandırma

### Bölüm 2: Rol Tabanlı Kullanım Kılavuzları
- Sistem Yöneticisi
- Admin Kullanıcı
- Depo Sorumlusu
- Kat Sorumlusu

### Bölüm 3: Özellik Detayları ve İş Akışları
- Stok Yönetimi
- Zimmet Sistemi
- Minibar İşlemleri
- Raporlama

### Bölüm 4: Teknik Dokümantasyon
- API Endpoints
- Veritabanı Yapısı
- Güvenlik Özellikleri
- Sorun Giderme

---

## 1. SİSTEM HAKKINDA

### 1.1 Genel Tanım

Otel Minibar Takip Sistemi, otel işletmelerinde minibar stok yönetimini, personel zimmet takibini ve tüketim analizlerini dijital ortamda yönetmek için geliştirilmiş profesyonel bir web uygulamasıdır.

### 1.2 Temel Özellikler

#### ✅ Stok Yönetimi
- Gerçek zamanlı stok takibi
- Kritik stok uyarıları
- Otomatik stok hesaplama
- Giriş/Çıkış kayıtları
- Depo envanteri

#### 📦 Zimmet Sistemi
- Personel zimmet atama
- Zimmet kullanım takibi
- İade işlemleri
- Zimmet geçmişi
- Otomatik stok düşümü

#### 🛏️ Minibar Yönetimi
- Oda bazlı minibar takibi
- İlk dolum işlemleri
- Kontrol ve doldurma
- Tüketim analizi
- Toplu işlem desteği

#### 📊 Raporlama ve Analiz
- Detaylı stok raporları
- Tüketim analizleri
- Zimmet raporları
- Excel/PDF export
- Grafik ve görselleştirme

#### 🔒 Güvenlik
- Rol tabanlı erişim kontrolü
- CSRF koruması
- Rate limiting (DDoS koruması)
- Audit trail (denetim izi)
- Oturum güvenliği
- Şifreleme

### 1.3 Kullanıcı Rolleri

#### 🔐 Sistem Yöneticisi
- Tam sistem yetkisi
- Otel tanımlama
- Kat/Oda yönetimi
- Admin atama
- Sistem logları

#### 👔 Admin
- Ürün yönetimi
- Personel tanımlama
- Stok işlemleri
- Tüm raporlar
- Sistem ayarları

#### 📦 Depo Sorumlusu
- Stok giriş/çıkış
- Personel zimmet atama
- Minibar durum görüntüleme
- Stok raporları
- Zimmet takibi

#### 🧹 Kat Sorumlusu
- Minibar dolum/kontrol
- Zimmet kullanımı
- Oda işlemleri
- Kişisel raporlar
- Tüketim kayıtları

---

## 2. TEKNİK ÖZELLİKLER

### 2.1 Teknoloji Stack

#### Backend
- **Framework:** Flask 3.0.3
- **ORM:** SQLAlchemy 2.0.36
- **Veritabanı:** MySQL 8.0+
- **Python:** 3.11+

#### Frontend
- **CSS Framework:** Tailwind CSS 3.4
- **JavaScript:** Vanilla JS + Chart.js 4.4
- **Icons:** Heroicons
- **PWA:** Service Worker desteği

#### Güvenlik
- **CSRF:** Flask-WTF CSRFProtect
- **Rate Limiting:** Flask-Limiter
- **Password Hashing:** Werkzeug Security
- **Session:** Flask Secure Cookies

#### Reporting
- **Excel:** OpenPyXL 3.1.5
- **PDF:** ReportLab 4.2.5

### 2.2 Sistem Gereksinimleri

#### Sunucu Gereksinimleri
```
- İşletim Sistemi: Windows/Linux/macOS
- Python: 3.11 veya üzeri
- MySQL: 8.0 veya üzeri
- RAM: Minimum 2GB (Önerilen 4GB)
- Disk: Minimum 1GB
- İnternet: HTTPS için gerekli
```

#### İstemci Gereksinimleri
```
- Modern web tarayıcı:
  * Chrome 90+
  * Firefox 88+
  * Safari 14+
  * Edge 90+
- JavaScript aktif
- Cookies aktif
- Minimum 1280x720 ekran çözünürlüğü
```

### 2.3 Veritabanı Yapısı

#### Ana Tablolar
```
- oteller (Otel bilgileri)
- kullanicilar (Tüm kullanıcılar)
- katlar (Kat tanımları)
- odalar (Oda tanımları)
- urun_gruplari (Ürün kategorileri)
- urunler (Ürün tanımları)
- stok_hareketleri (Stok giriş/çıkış)
- personel_zimmet (Zimmet başlık)
- personel_zimmet_detay (Zimmet detay)
- minibar_islemleri (Minibar işlem başlık)
- minibar_islem_detay (Minibar işlem detay)
- sistem_loglari (İşlem logları)
- hata_loglari (Hata logları)
- audit_logs (Denetim izi)
- sistem_ayarlari (Sistem ayarları)
```

---

## 3. KURULUM

### 3.1 Railway ile Kurulum (Önerilen)

#### Adım 1: GitHub Repository Oluşturma
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

#### Adım 2: Railway Projesi Oluşturma
1. [Railway.app](https://railway.app) sitesine gidin
2. GitHub ile giriş yapın
3. "New Project" → "Deploy from GitHub repo" seçin
4. Repository'nizi seçin

#### Adım 3: MySQL Veritabanı Ekleme
1. Railway projenizde "New" → "Database" → "Add MySQL"
2. Otomatik `DATABASE_URL` environment variable oluşacak

#### Adım 4: Environment Variables Ayarlama
Railway projesinde Settings → Variables:
```env
SECRET_KEY=your-super-secret-key-change-this-min-32-chars
FLASK_ENV=production
```

⚠️ **Önemli:** `SECRET_KEY` minimum 32 karakter olmalı ve güçlü olmalıdır.

#### Adım 5: Deploy
- Railway otomatik deploy edecek
- İlk deploy sırasında `init_db.py` otomatik çalışarak tabloları oluşturacak
- Deploy tamamlandığında URL'niz hazır

### 3.2 Lokal Kurulum

#### Adım 1: Repository'yi Klonlama
```bash
git clone <repo-url>
cd prof
```

#### Adım 2: Virtual Environment Oluşturma
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

#### Adım 3: Bağımlılıkları Yükleme
```bash
pip install -r requirements.txt
```

#### Adım 4: .env Dosyası Oluşturma
Proje kök dizininde `.env` dosyası oluşturun:
```env
# Veritabanı Ayarları
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=minibar_takip
DB_PORT=3306

# Flask Ayarları
SECRET_KEY=your-super-secret-key-change-this-min-32-chars
FLASK_ENV=development

# Port (Opsiyonel)
PORT=5014
```

#### Adım 5: MySQL Veritabanı Oluşturma
```sql
CREATE DATABASE minibar_takip CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### Adım 6: Veritabanını Başlatma
```bash
python init_db.py
```

#### Adım 7: Uygulamayı Çalıştırma
```bash
python app.py
```

#### Adım 8: Tarayıcıda Açma
```
http://localhost:5014
```

---

## 4. İLK YAPILANDIRMA (SETUP)

### 4.1 Setup Süreci

Sistem ilk kez çalıştırıldığında otomatik olarak Setup sayfası açılır.

#### Setup Adımları

**1. Otel Bilgileri**
```
- Otel Adı: Otelin resmi adı
- Adres: Tam adres bilgisi (min 10 karakter)
- Telefon: İletişim telefonu
- E-posta: İletişim e-postası (opsiyonel)
- Vergi No: Vergi numarası (opsiyonel)
```

**2. Sistem Yöneticisi Bilgileri**
```
- Kullanıcı Adı: 3-50 karakter, harf/rakam/(_-.)
- Ad: Yöneticinin adı
- Soyad: Yöneticinin soyadı
- E-posta: Geçerli e-posta adresi
- Telefon: İletişim telefonu (opsiyonel)
- Şifre: Min 8 karakter, güçlü şifre
  * En az 1 büyük harf
  * En az 1 küçük harf
  * En az 1 rakam
  * En az 1 özel karakter (!@#$%^&*...)
- Şifre Onayı: Şifre tekrarı
```

**3. Setup Tamamlama**
- Tüm bilgiler doldurulduktan sonra "Kurulumu Tamamla" butonuna tıklayın
- Sistem otomatik olarak:
  - Otel kaydı oluşturur
  - Sistem Yöneticisi kullanıcısı oluşturur
  - Setup tamamlandı olarak işaretler
- Başarılı setup sonrası login sayfasına yönlendirilirsiniz

### 4.2 İlk Giriş

**1. Login Sayfası**
```
URL: http://localhost:5014/login (veya Railway URL'niz)
Kullanıcı Adı: Setup'ta belirlediğiniz kullanıcı adı
Şifre: Setup'ta belirlediğiniz şifre
```

**2. Güvenlik Kontrolleri**
- Rate Limiting: 5 deneme/dakika
- CSRF Token kontrolü
- Secure session
- IP ve tarayıcı loglanması

**3. İlk Giriş Sonrası**
- Sistem Yöneticisi dashboard'una yönlendirilirsiniz
- Hoş geldiniz mesajı görüntülenir
- İlk yapılandırma adımlarına geçebilirsiniz

### 4.3 Temel Yapılandırma Adımları

#### Adım 1: Kat Tanımlama
```
Menü: Sistem Yöneticisi → Kat Tanımla
- Kat Adı: Zemin Kat, 1. Kat, vb.
- Kat No: Sayısal değer (-5 ile 100 arası)
- Açıklama: Ek bilgiler (opsiyonel)
```

#### Adım 2: Oda Tanımlama
```
Menü: Sistem Yöneticisi → Oda Tanımla
- Kat: Dropdown'dan kat seçimi
- Oda Numarası: Benzersiz oda no (örn: 101, 102)
- Oda Tipi: Standart, Suit, Deluxe vb.
- Kapasite: Kişi sayısı (1-20)
```

#### Adım 3: Admin Kullanıcı Atama
```
Menü: Sistem Yöneticisi → Personel Tanımla
- Kullanıcı Adı, Ad, Soyad, E-posta
- Rol: Admin seçimi
- Güçlü şifre belirleme
```

#### Adım 4: Ürün Grupları Oluşturma (Admin)
```
Admin olarak giriş yapın
Menü: Admin → Ürün Grupları
Örnek gruplar:
- İçecekler
- Atıştırmalıklar
- Alkollü İçecekler
- Soğuk İçecekler
```

#### Adım 5: Ürün Tanımlama (Admin)
```
Menü: Admin → Ürünler
Her ürün için:
- Ürün Grubu seçimi
- Ürün Adı
- Barkod (opsiyonel, benzersiz)
- Birim (Adet, Şişe, Kutu, vb.)
- Kritik Stok Seviyesi
```

#### Adım 6: Personel Tanımlama (Admin)
```
Menü: Admin → Personel Tanımla
Roller:
- Depo Sorumlusu: Stok ve zimmet yönetimi
- Kat Sorumlusu: Minibar işlemleri
```

#### Adım 7: İlk Stok Girişi (Depo Sorumlusu)
```
Depo Sorumlusu olarak giriş yapın
Menü: Depo Sorumlusu → Stok Girişi
- Ürün seçimi
- Hareket Tipi: Giriş/Devir/Sayım
- Miktar
- Açıklama
```

### 4.4 Sistem Hazır!

✅ **Kontrol Listesi**
- [ ] Setup tamamlandı
- [ ] Katlar oluşturuldu
- [ ] Odalar tanımlandı
- [ ] Admin kullanıcı atandı
- [ ] Ürün grupları oluşturuldu
- [ ] Ürünler tanımlandı
- [ ] Personeller oluşturuldu
- [ ] İlk stok girişi yapıldı

Sistem artık kullanıma hazır! 🎉

---

## 5. GÜVENLİK ÖNEMLERİ

### 5.1 Şifre Güvenliği
- Minimum 8 karakter
- Büyük/küçük harf, rakam ve özel karakter içermeli
- Varsayılan şifreler değiştirilmeli
- Periyodik şifre değişimi önerilir

### 5.2 Yetkilendirme
- Her kullanıcıya sadece gerekli yetkiler verilmeli
- Pasif kullanıcılar devre dışı bırakılmalı
- Şüpheli aktiviteler takip edilmeli

### 5.3 Veri Güvenliği
- Düzenli veritabanı yedekleri alınmalı
- Production ortamında HTTPS kullanılmalı
- `.env` dosyası git'e eklenmemeli
- SECRET_KEY güçlü ve benzersiz olmalı

### 5.4 Audit Trail
- Tüm kritik işlemler loglanır
- Kullanıcı aktiviteleri izlenir
- Veri değişiklikleri kaydedilir
- Güvenlik ihlalleri raporlanır

---

**BÖLÜM 1 SONU**

**Sonraki Bölüm:** Rol Tabanlı Kullanım Kılavuzları  
**Sayfa:** 2/4

---

*Bu dokümantasyon sürekli güncellenmektedir. Son güncelleme: 31 Ekim 2025*
