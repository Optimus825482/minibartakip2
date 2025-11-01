# 🏨 Otel Minibar Takip Sistemi

Flask tabanlı, MySQL veritabanı kullanan profesyonel otel minibar yönetim sistemi.

## 🚀 Özellikler

- ✅ Rol tabanlı yetkilendirme (Sistem Yöneticisi, Admin, Depo Sorumlusu, Kat Sorumlusu)
- 📊 Stok yönetimi ve takibi
- 🛏️ Oda bazlı minibar işlemleri
- 📦 Personel zimmet sistemi
- 📈 Detaylı raporlama ve analiz
- 🎯 Minibar tüketim takibi
- 🔔 Kritik stok uyarıları

## 📋 Gereksinimler

- Python 3.11+
- MySQL 8.0+
- pip (Python paket yöneticisi)

## 🛠️ Kurulum

### Railway ile Deploy (Önerilen)

1. **GitHub Repository Oluştur**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Railway'de Proje Oluştur**
   - [Railway.app](https://railway.app) sitesine gidin
   - "New Project" → "Deploy from GitHub repo" seçin
   - Repository'nizi seçin

3. **MySQL Veritabanı Ekle**
   - Railway projenizde "New" → "Database" → "Add MySQL"
   - Otomatik `DATABASE_URL` environment variable oluşacak

4. **Environment Variables Ayarla**
   Railway projesinde Settings → Variables:
   ```
   SECRET_KEY=your-super-secret-key-change-this
   FLASK_ENV=production
   ```

5. **Deploy**
   - Railway otomatik deploy edecek
   - İlk deploy sırasında `init_db.py` otomatik çalışarak tabloları oluşturacak

### Local Kurulum

1. **Repository'yi klonlayın**
   ```bash
   git clone <repo-url>
   cd prof
   ```

2. **Virtual environment oluşturun**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Paketleri yükleyin**
   ```bash
   pip install -r requirements.txt
   ```

4. **.env dosyası oluşturun**
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=minibar_takip
   DB_PORT=3306
   SECRET_KEY=your-secret-key
   ```

5. **Veritabanını başlatın**
   ```bash
   python init_db.py
   ```

6. **Uygulamayı çalıştırın**
   ```bash
   python app.py
   ```

7. **Tarayıcıda açın**
   ```
   http://localhost:5014
   ```

## 📁 Proje Yapısı

```
prof/
├── app.py                  # Ana Flask uygulaması
├── config.py              # Konfigürasyon ayarları
├── models.py              # Veritabanı modelleri
├── forms.py               # Form tanımlamaları
├── init_db.py             # Veritabanı başlatma scripti
├── requirements.txt       # Python bağımlılıkları
├── Procfile              # Railway/Heroku deploy komutu
├── railway.json          # Railway konfigürasyonu
├── runtime.txt           # Python versiyonu
├── .gitignore            # Git ignore kuralları
├── docs/                 # 📚 Dokümantasyon (detaylı kılavuzlar)
│   ├── README.md         # Dokümantasyon indeksi
│   ├── KULLANIM_KLAVUZU_BOLUM_1.md
│   ├── KULLANIM_KLAVUZU_BOLUM_2.md
│   ├── KULLANIM_KLAVUZU_BOLUM_3.md
│   ├── akis_sema.md      # 14 akış diyagramı
│   ├── SISTEM_SIFIRLAMA_KILAVUZU.md
│   ├── SILME_SIRASI.md
│   ├── TABLO_ISIMLERI.md
│   └── ... (daha fazla)
├── templates/            # HTML şablonları
│   ├── base.html
│   ├── login.html
│   ├── setup.html
│   ├── reset_system.html  # Sistem sıfırlama
│   ├── admin/
│   ├── depo_sorumlusu/
│   ├── kat_sorumlusu/
│   ├── sistem_yoneticisi/
│   └── errors/
├── static/               # Statik dosyalar
│   ├── js/
│   ├── icons/
│   ├── manifest.json
│   └── service-worker.js
├── utils/                # Yardımcı modüller
│   ├── audit.py          # Audit trail
│   ├── decorators.py
│   └── helpers.py
└── tests/                # Test dosyaları
    └── test_config.py
```

## 👥 Kullanıcı Rolleri

### 1. Sistem Yöneticisi
- Otel tanımlama
- Admin kullanıcı atama
- Kat ve oda yönetimi
- Sistem logları

### 2. Admin
- Ürün ve grup yönetimi
- Personel tanımlama
- Tüm raporlara erişim

### 3. Depo Sorumlusu
- Stok girişi ve çıkışı
- Personel zimmet yönetimi
- Minibar durumları
- Tüketim raporları

### 4. Kat Sorumlusu
- Minibar dolum/kontrol
- Zimmet kullanımı
- Kişisel raporlar

## 🔒 İlk Giriş

1. Tarayıcıda uygulamayı açın
2. "İlk Kurulum" sayfası otomatik açılacak
3. Otel bilgileri ve Sistem Yöneticisi oluşturun
4. Giriş yapın ve diğer kullanıcıları ekleyin

## � Sistem Sıfırlama

Sistemi tamamen sıfırlamak ve ilk kuruluma dönmek için:

- **URL**: `/resetsystem`
- **Özel Şifre**: `518518Erkan!`
- **İşlev**: Tüm veritabanı tablolarını temizler ve sistemi ilk kuruluma döndürür

⚠️ **UYARI**: Bu işlem geri alınamaz! Tüm veriler silinir.

📖 Detaylı bilgi için: [docs/SISTEM_SIFIRLAMA_KILAVUZU.md](docs/SISTEM_SIFIRLAMA_KILAVUZU.md)

## �📊 Raporlar

- **Stok Durum Raporu**: Mevcut stok durumu
- **Stok Hareket Raporu**: Tüm stok hareketleri
- **Zimmet Raporu**: Personel zimmet durumu
- **Minibar Tüketim Raporu**: Oda bazlı tüketim analizi
- **Ürün Grubu Raporu**: Grup bazlı istatistikler

## 📚 Detaylı Dokümantasyon

Sistem hakkında detaylı bilgi için **[docs/](docs/)** klasörüne bakın:

- 📖 **4 Bölümlük Kullanım Kılavuzu** (2750+ satır)
- 📊 **14 Akış Diyagramı** (Mermaid format)
- 🔧 **Teknik Dokümantasyon** (Veritabanı, API, Template)
- ⚙️ **Sistem Yönetimi** (Sıfırlama, Backup, Deployment)

## 🔧 Teknolojiler

- **Backend**: Flask 3.0
- **Database**: MySQL 8.0 + SQLAlchemy ORM
- **Frontend**: Tailwind CSS 3.x
- **Charts**: Chart.js 4.4
- **Reports**: OpenPyXL, ReportLab
- **Deployment**: Railway.app

## 🐛 Sorun Giderme

### Veritabanı Bağlantı Hatası
```bash
# MySQL servisini kontrol edin
# Windows
net start MySQL80

# Linux
sudo systemctl start mysql
```

### Port Kullanımda Hatası
```bash
# .env dosyasında farklı port belirleyin
PORT=5015
```

### Railway Deploy Sorunları
- `DATABASE_URL` environment variable'ın otomatik oluştuğundan emin olun
- Build logs'u kontrol edin: Railway Dashboard → Deployments → View Logs

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👨‍💻 Geliştirici

Otel Minibar Takip Sistemi v1.0

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📞 Destek

Sorularınız için issue açabilirsiniz.

---

**Not**: Production ortamında mutlaka güçlü `SECRET_KEY` kullanın, HTTPS üzerinden yayın yapın (config üretimde `SESSION_COOKIE_SECURE=True` olarak gelir) ve `.env` dosyasını repository'ye eklemeyin!
