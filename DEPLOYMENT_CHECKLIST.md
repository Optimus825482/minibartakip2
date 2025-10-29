# 🚀 Railway Deployment Checklist

## ✅ Pre-Deployment

- [ ] `.env` dosyası `.gitignore`'da
- [ ] `requirements.txt` güncel
- [ ] `Procfile` mevcut
- [ ] `railway.json` konfigüre edilmiş
- [ ] `runtime.txt` Python versiyonu belirtilmiş
- [ ] `README.md` ve dokümantasyon hazır
- [ ] Gereksiz dosyalar temizlenmiş (migration scripts, __pycache__, vb.)

## ✅ GitHub Push

```bash
git status                                    # Değişiklikleri kontrol et
git add .                                     # Tüm dosyaları ekle
git commit -m "Production ready deployment"   # Commit
git push origin main                          # Push
```

## ✅ Railway Setup

### 1. Proje Oluştur
- [ ] Railway.app'e giriş yap
- [ ] "New Project" → "Deploy from GitHub repo"
- [ ] Repository seç

### 2. MySQL Ekle
- [ ] "New" → "Database" → "Add MySQL"
- [ ] `DATABASE_URL` otomatik oluştu mu? ✓

### 3. Environment Variables
Railway Settings → Variables:

```
SECRET_KEY=<32+ karakter random key>
FLASK_ENV=production
```

**SECRET_KEY oluştur:**
```python
import secrets
print(secrets.token_hex(32))
```

### 4. Deploy
- [ ] Build başladı mı?
- [ ] Build başarılı oldu mu?
- [ ] `init_db.py` çalıştı mı? (Logs'da kontrol et)
- [ ] Uygulama "Running" durumunda mı?

## ✅ Post-Deployment Tests

### 1. URL Testi
- [ ] Railway URL'i aç
- [ ] SSL sertifikası çalışıyor mu? (https://)
- [ ] İlk Kurulum sayfası açılıyor mu?

### 2. Database Testi
Railway → MySQL → Connect
```sql
SHOW TABLES;
-- 13 tablo görünmeli
```

Beklenen tablolar:
- [ ] oteller
- [ ] kullanicilar
- [ ] katlar
- [ ] odalar
- [ ] urun_gruplari
- [ ] urunler
- [ ] stok_hareketleri
- [ ] personel_zimmet
- [ ] personel_zimmet_detay
- [ ] minibar_islemleri
- [ ] minibar_islem_detay
- [ ] sistem_ayarlari
- [ ] sistem_loglari

### 3. Fonksiyon Testi
- [ ] İlk kurulum sayfası çalışıyor
- [ ] Otel ve Sistem Yöneticisi oluşturuldu
- [ ] Login başarılı
- [ ] Dashboard açılıyor
- [ ] Menüler görünüyor

## 🔍 Sorun Giderme

### Build Fails
```bash
# Railway logs'u kontrol et
# Genelde eksik paket veya Python versiyonu sorunu
```

### Database Connection Error
- [ ] MySQL servisi "Active" mi?
- [ ] `DATABASE_URL` environment variable var mı?
- [ ] Format doğru mu? `mysql://user:pass@host:port/dbname`

### Tables Not Created
- [ ] Deploy logs'da `init_db.py` çıktısını kontrol et
- [ ] MySQL'e manuel bağlan ve `SHOW TABLES;` çalıştır
- [ ] Hata varsa Railway → MySQL → Query ile manuel çalıştır

## 📊 Monitoring

Railway Dashboard'da izle:
- [ ] CPU kullanımı
- [ ] Memory kullanımı
- [ ] Network trafiği
- [ ] Deploy frequency

## 🔒 Security

- [ ] SECRET_KEY güçlü (min 32 karakter)
- [ ] `.env` dosyası repository'de YOK
- [ ] MySQL şifresi güçlü
- [ ] HTTPS aktif (Railway otomatik)
- [ ] CORS ayarları kontrol edildi

## 💾 Backup

Railway → MySQL → Settings:
- [ ] Otomatik backup aktif
- [ ] Backup frequency ayarla (Günlük önerili)

## 📈 Production Monitoring

İzlenmesi gerekenler:
- [ ] Error logs (Railway → Logs)
- [ ] Database boyutu
- [ ] Response times
- [ ] User activity

## 🎉 Deployment Complete!

✅ Tüm kontroller başarılı
✅ Uygulama production'da çalışıyor
✅ İlk kullanıcı oluşturuldu

**Next Steps:**
1. Domain ekle (opsiyonel)
2. Monitoring setup
3. Backup stratejisi
4. User documentation

---

Deployment Tarihi: _____________
Railway URL: _____________
MySQL Host: _____________
Deployed By: _____________
