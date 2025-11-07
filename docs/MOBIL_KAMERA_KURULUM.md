# 📱 Mobil Kamera Erişimi ve HTTPS Kurulum Rehberi

## 🚨 Problem
Modern tarayıcılar güvenlik nedeniyle kamera erişimi için **HTTPS bağlantısı** gerektirir.
HTTP üzerinden (http://) mobil cihazlardan kamera erişimi **engellenmiştir**.

## ✅ ÇÖZÜM 1: HTTPS ile Self-Signed Sertifika (ÖNERİLEN)

### Adım 1: SSL Sertifikası Oluştur

```bash
# Proje klasöründe
python generate_ssl_cert.py
```

Bu komut:
- ✅ `cert.pem` (sertifika) oluşturur
- ✅ `key.pem` (private key) oluşturur
- ✅ `.env` dosyasını otomatik günceller

### Adım 2: .env Dosyasını Kontrol Et

`.env` dosyasında şu satırın olduğundan emin olun:

```env
USE_HTTPS=true
```

### Adım 3: Uygulamayı Başlat

```bash
python app.py
```

Şu çıktıyı görmelisiniz:
```
🔒 HTTPS Aktif: https://0.0.0.0:5014
📱 Mobil erişim: https://<IP-ADRESINIZ>:5014
```

### Adım 4: Bilgisayarın IP Adresini Öğren

**Windows:**
```bash
ipconfig
```
IPv4 adresini not edin (örn: 192.168.1.100)

**Linux/Mac:**
```bash
ifconfig
# veya
ip addr show
```

### Adım 5: Mobil Cihazdan Bağlan

1. Mobil cihazınızı **aynı Wi-Fi ağına** bağlayın
2. Tarayıcıda şu adresi açın: `https://192.168.1.100:5014` (IP'nizi yazın)
3. Güvenlik uyarısı gelecek:

   **Chrome/Edge:**
   - "Advanced" veya "Gelişmiş"
   - "Proceed to site" veya "Siteye devam et"

   **Safari:**
   - "Show Details" veya "Ayrıntıları Göster"
   - "Visit this website" veya "Bu web sitesini ziyaret et"

4. ✅ Artık kamera erişimi isteyecek - "İzin Ver" seçin

---

## ✅ ÇÖZÜM 2: Manuel Oda Girişi (FALLBACK)

HTTPS kuramıyorsanız veya kamera çalışmıyorsa:

1. QR modal açıldığında altta:
   **"Manuel Oda Numarası Gir"** butonuna tıklayın

2. Kat ve Oda'yı normal dropdown'lardan seçin

---

## ✅ ÇÖZÜM 3: ngrok ile HTTPS Tüneli (GELİŞTİRME İÇİN)

ngrok ücretsiz bir HTTPS tüneli sağlar:

### Adım 1: ngrok İndir
https://ngrok.com/download

### Adım 2: Uygulamayı HTTP ile başlat
```bash
# .env'de USE_HTTPS=false olduğundan emin olun
python app.py
```

### Adım 3: ngrok Tüneli Aç
```bash
ngrok http 5014
```

### Adım 4: Verilen HTTPS URL'yi Kullan
ngrok size şöyle bir URL verir:
```
https://abc123.ngrok.io -> http://localhost:5014
```

Bu URL'yi mobil cihazınızdan açın - kamera çalışacaktır!

⚠️ **Not:** ngrok URL'si her seferinde değişir ve ücretsiz planda zaman limiti vardır.

---

## 🔍 Hata Giderme

### "Bağlantınız güvenli değil" Uyarısı
✅ **Normal:** Self-signed sertifika kullanıldığı için bu uyarı gelir.
➡️ "Advanced" > "Proceed" ile devam edin.

### Kamera İzni Verilmiyor
1. Tarayıcı ayarlarına gidin
2. Site ayarlarını bulun
3. Kamera iznini "İzin Ver" yapın
4. Sayfayı yenileyin

### IP'ye Bağlanmıyor
- ✅ Mobil ve PC aynı Wi-Fi'de mi?
- ✅ Windows Firewall 5014 portunu engelliyor mu?
  ```bash
  # Windows Firewall kuralı ekle (Yönetici olarak)
  netsh advfirewall firewall add rule name="Flask HTTPS" dir=in action=allow protocol=TCP localport=5014
  ```

### "SSL sertifikası bulunamadı" Hatası
```bash
python generate_ssl_cert.py
```
komutu ile sertifika oluşturun.

### OpenSSL Bulunamadı (Windows)
**Seçenek 1:** OpenSSL indir
https://slproweb.com/products/Win32OpenSSL.html

**Seçenek 2:** Git Bash kullan
Git Bash terminalinde `python generate_ssl_cert.py` çalıştırın

**Seçenek 3:** Manuel oluştur
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/C=TR/ST=Istanbul/L=Istanbul/O=Minibar/CN=localhost"
```

---

## 📋 Hızlı Kontrol Listesi

- [ ] SSL sertifikası oluşturuldu (`cert.pem`, `key.pem`)
- [ ] `.env` dosyasında `USE_HTTPS=true` var
- [ ] Uygulama HTTPS ile başladı
- [ ] Bilgisayarın IP adresi öğrenildi
- [ ] Mobil cihaz aynı Wi-Fi'de
- [ ] Tarayıcıda `https://IP:5014` açıldı
- [ ] Güvenlik uyarısı atlandı ("Proceed to site")
- [ ] Kamera izni verildi
- [ ] QR kod okuyucu çalışıyor ✅

---

## 🎯 Özet

| Yöntem | Avantaj | Dezavantaj |
|--------|---------|------------|
| **Self-Signed SSL** | ✅ En hızlı<br>✅ Kalıcı<br>✅ Ücretsiz | ⚠️ Güvenlik uyarısı |
| **Manuel Giriş** | ✅ HTTPS gerekmez<br>✅ Hemen kullan | ❌ QR avantajı yok |
| **ngrok** | ✅ Gerçek SSL<br>✅ Uyarı yok | ❌ Her seferinde yeni URL<br>❌ Zaman limiti |

**Öneri:** Geliştirme için **Self-Signed SSL**, production için **gerçek SSL sertifikası** kullanın.

---

## 📞 Ek Kaynaklar

- Flask SSL Docs: https://flask.palletsprojects.com/en/2.3.x/tutorial/deploy/
- Let's Encrypt (Ücretsiz SSL): https://letsencrypt.org/
- ngrok Docs: https://ngrok.com/docs

---

✅ Artık mobil cihazınızdan QR kod okutarak minibar kontrolü yapabilirsiniz!
