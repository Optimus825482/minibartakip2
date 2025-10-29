# Railway Deployment Guide

Bu dosya Railway'e deploy etmek için gereken adımları içerir.

## Önemli Notlar

✅ **Hazır Dosyalar:**
- `Procfile` - Railway start komutu
- `railway.json` - Railway konfigürasyonu
- `runtime.txt` - Python 3.11.9
- `requirements.txt` - Tüm bağımlılıklar
- `.gitignore` - Git ignore kuralları
- `README.md` - Detaylı dokümantasyon

## Deployment Adımları

### 1. GitHub'a Push

```bash
# İlk commit
git init
git add .
git commit -m "Initial commit - Otel Minibar Takip Sistemi"

# Remote repository ekle
git remote add origin https://github.com/kullaniciadi/repo-adi.git
git branch -M main
git push -u origin main
```

### 2. Railway'de Proje Oluştur

1. [Railway.app](https://railway.app) → Login with GitHub
2. "New Project" butonu
3. "Deploy from GitHub repo" seçin
4. Repository'nizi seçin

### 3. MySQL Veritabanı Ekle

1. Railway projenizde sağ üstten "New" → "Database" → "Add MySQL"
2. Otomatik olarak `DATABASE_URL` environment variable oluşacak
3. Format: `mysql://user:pass@host:port/dbname`

### 4. Environment Variables

Railway projesinde **Settings → Variables** bölümünden ekleyin:

```
SECRET_KEY=<random-32-karakter-güçlü-key>
FLASK_ENV=production
```

**SECRET_KEY oluşturmak için:**
```python
import secrets
print(secrets.token_hex(32))
```

### 5. Deploy

- Railway otomatik deploy başlatacak
- Build logs'u takip edin
- İlk deploy sırasında `init_db.py` otomatik çalışacak
- MySQL tabloları otomatik oluşacak

### 6. İlk Giriş

1. Railway'in verdiği URL'i açın (örn: `https://your-app.railway.app`)
2. İlk Kurulum sayfası açılacak
3. Otel bilgileri ve Sistem Yöneticisi oluşturun
4. Giriş yapın!

## Veritabanı Bağlantısı

Sistem otomatik olarak şu sırayla çalışır:

1. `DATABASE_URL` var mı? (Railway MySQL)
2. Yoksa `.env` dosyasındaki bilgileri kullan (Local development)

## Deployment Sonrası Kontroller

✅ Deployment başarılı mı?
- Railway Dashboard → Deployments → View Logs

✅ Veritabanı bağlantısı çalışıyor mu?
- URL'i açın, hata var mı?

✅ Tablolar oluştu mu?
- Railway → MySQL → Connect → Tabloya bak

## Sorun Giderme

### Build Hatası
- `railway.json` dosyası var mı?
- `requirements.txt` doğru mu?
- Python versiyonu uyumlu mu? (runtime.txt)

### Database Connection Error
- MySQL servisi eklenmiş mi?
- `DATABASE_URL` environment variable var mı?
- Railway Dashboard'da MySQL durumu "Active" mi?

### Tablolar Oluşmadı
- `init_db.py` çalıştı mı? (Deploy logs'da kontrol edin)
- MySQL bağlantısı başarılı mı?

## Custom Domain (Opsiyonel)

Railway → Settings → Domains → Custom Domain ekleyebilirsiniz.

## Logs İzleme

```bash
# Railway CLI ile (opsiyonel)
railway login
railway logs
```

## Güvenlik Önerileri

⚠️ **Production'da MUTLAKA:**
1. Güçlü `SECRET_KEY` kullanın (min 32 karakter)
2. `.env` dosyasını repository'ye eklemeyin
3. HTTPS kullanın (Railway otomatik sağlar)
4. MySQL şifresini güçlü tutun

## Yedekleme

Railway MySQL'i düzenli yedekleyin:
- Railway Dashboard → MySQL → Backups

---

Başarılar! 🚀
