# 🚀 Railway Hızlı Kurulum (5 Dakika)

## 1️⃣ Railway'de Proje Oluştur
1. https://railway.app → GitHub ile giriş
2. **New Project** → **Deploy from GitHub repo**
3. `Optimus825482/minibartakip2` seç

## 2️⃣ PostgreSQL Ekle
1. Proje içinde **New** → **Database** → **PostgreSQL**
2. Otomatik bağlanır ✅

## 3️⃣ Environment Variables Ayarla

**Variables** sekmesine git ve ekle:

```bash
SECRET_KEY=BURAYA_64_KARAKTERLIK_RANDOM_STRING_YAZ
FLASK_ENV=production
ENV=production
DB_TYPE=postgresql
```

### SECRET_KEY Oluştur:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## 4️⃣ Deploy Et
**Deploy** butonuna tıkla → Bekle (2-3 dakika)

## 5️⃣ İlk Superadmin Oluştur

Railway Dashboard → Service → **Shell** sekmesi:

```bash
python add_superadmin_railway.py
```

Kullanıcı adı: `superadmin`
Şifre: `Admin123!`

## ✅ Bitti!

URL'ni al: **Settings** → **Domains** → **Generate Domain**

Örnek: `https://minibartakip2-production.up.railway.app`

---

## 🔧 Sorun mu var?

### Database bağlanamıyor:
```bash
railway variables  # Değişkenleri kontrol et
railway restart    # Servisi yeniden başlat
```

### Migration hatası:
```bash
railway run python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Logs:
```bash
railway logs
```

---

## 📚 Detaylı Rehber
Daha fazla bilgi için: `RAILWAY_DEPLOYMENT.md`
