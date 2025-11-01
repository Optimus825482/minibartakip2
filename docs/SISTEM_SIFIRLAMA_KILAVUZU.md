# 🔴 SİSTEM SIFIRLAMA ÖZELLİĞİ

## 📋 Genel Bakış

Sistem sıfırlama özelliği, veritabanındaki **TÜM VERİLERİ SİLEREK** sistemi ilk kurulum aşamasına döndürür. Bu işlem **GERİ ALINAMAZ** ve özel bir şifre ile korunmaktadır.

---

## 🔐 Güvenlik

### Özel Şifre
```
Şifre: 518518Erkan!
```

**⚠️ UYARI:** Bu şifre sistemde sabit kodlanmıştır (`app.py` dosyasında `RESET_PASSWORD` değişkeni). Güvenlik için değiştirilebilir.

### Güvenlik Önlemleri
- ✅ Özel şifre koruması
- ✅ İki aşamalı onay sistemi
- ✅ Detaylı istatistik gösterimi
- ✅ Checkbox ile manuel onay
- ✅ JavaScript ile son onay pop-up
- ✅ Menülerde görünmez (direkt URL ile erişim)

---

## 🌐 Erişim

### URL
```
http://localhost:5000/resetsystem
```

**Not:** Bu sayfa menülerde görünmez, sadece direkt URL ile erişilebilir.

---

## 📊 İşlem Akışı

### 1. Şifre Girişi
- URL'ye gidin: `/resetsystem`
- Özel şifreyi girin: `518518Erkan!`
- **"🔍 İstatistikleri Göster"** butonuna tıklayın

### 2. İstatistikleri Görüntüleme
Sistem aşağıdaki istatistikleri gösterir:
- 👥 Kullanıcı sayısı
- 🏨 Otel sayısı
- 🏢 Kat sayısı
- 🚪 Oda sayısı
- 📦 Ürün grubu sayısı
- 🏷️ Ürün sayısı
- 📊 Stok hareket sayısı
- 📋 Zimmet kayıt sayısı
- 🍺 Minibar işlem sayısı
- 📝 Sistem log sayısı
- 🐛 Hata log sayısı
- 🔍 Audit trail kayıt sayısı

### 3. Manuel Onay
- Checkbox ile onay verin:
  > "Yukarıdaki tüm verilerin kalıcı olarak silineceğini ve bu işlemin geri alınamayacağını anladım..."

### 4. Son Onay (Pop-up)
- **"🗑️ SİSTEMİ SIFIRLA"** butonuna tıklayın
- JavaScript pop-up ile son onay verin
- Emin değilseniz **"İptal Et"** butonuna basın

### 5. Sıfırlama İşlemi
Sistem aşağıdaki sırayla tüm verileri siler:
1. ✗ Minibar işlem detayları
2. ✗ Minibar işlemleri
3. ✗ Zimmet detayları
4. ✗ Zimmet kayıtları
5. ✗ Stok hareketleri
6. ✗ Ürünler
7. ✗ Ürün grupları
8. ✗ Odalar
9. ✗ Katlar
10. ✗ Kullanıcılar
11. ✗ Oteller
12. ✗ Sistem logları
13. ✗ Hata logları
14. ✗ Audit trail kayıtları
15. ✗ Otomatik rapor ayarları
16. ✗ Setup ayarı sıfırlanır

### 6. Yönlendirme
- Session temizlenir
- `/setup` sayfasına yönlendirilir
- İlk kurulum başlatılır

---

## 🗑️ Silinen Veriler

### Tüm Tablolar Temizlenir
- **minibar_islem_detaylari** - Minibar işlem detayları
- **minibar_islemleri** - Minibar işlemleri
- **personel_zimmet_detaylari** - Zimmet detayları
- **personel_zimmetler** - Zimmet kayıtları
- **stok_hareketleri** - Stok hareketleri
- **urunler** - Ürün listesi
- **urun_gruplari** - Ürün grupları
- **odalar** - Oda tanımları
- **katlar** - Kat tanımları
- **kullanicilar** - Tüm kullanıcı hesapları (Sistem Yöneticisi dahil!)
- **oteller** - Otel bilgileri
- **sistem_loglari** - Sistem aktivite logları
- **hata_loglari** - Hata kayıtları
- **audit_logs** - Audit trail kayıtları
- **otomatik_raporlar** - Otomatik rapor ayarları
- **sistem_ayarlari** (setup_tamamlandi) - İlk kurulum ayarı

### Auto-Increment Sıfırlama
Tüm tabloların ID değerleri `1`'den başlatılır.

---

## 💻 Teknik Detaylar

### Dosyalar
```
templates/reset_system.html  → Arayüz
app.py                        → Backend (reset_system route)
```

### Route Bilgileri
```python
@app.route('/resetsystem', methods=['GET', 'POST'])
@csrf.exempt  # CSRF exempt (kendi validasyonu var)
def reset_system():
    # Şifre kontrolü
    # İstatistik gösterimi
    # Onay ve sıfırlama işlemi
```

### Veritabanı İşlemleri
```python
# Raw SQL kullanılır (foreign key sırasına dikkat)
db.session.execute(db.text("DELETE FROM tablo_adi"))
db.session.execute(db.text("ALTER TABLE tablo AUTO_INCREMENT = 1"))
db.session.commit()
```

---

## 🎨 Arayüz Özellikleri

### Renkli İstatistik Kartları
- 🔴 Kullanıcı (Red gradient)
- 🟠 Otel (Orange gradient)
- 🟡 Kat (Yellow gradient)
- 🟢 Oda (Green gradient)
- 🔵 Ürün (Blue gradient)
- 🟣 Stok (Purple gradient)
- 🟣 Zimmet (Pink gradient)
- 🔵 Minibar (Indigo gradient)
- ⚫ Log (Gray gradient)

### Uyarı Mesajları
- 🔴 Kırmızı arka plan ile kritik uyarılar
- ⚠️ İkonlar ve büyük fontlar
- 📋 Detaylı bilgilendirme listeleri
- ✓ Checkbox ile manuel onay

### Responsive Tasarım
- Mobile-first yaklaşım
- Tailwind CSS ile modern görünüm
- Gradient arka planlar
- Shadow ve hover efektleri

---

## ⚠️ Önemli Notlar

### 1. GERİ DÖNÜŞÜ YOK
```
Bu işlem sonrası TÜM VERİLER KALİCİ OLARAK SİLİNİR!
Yedek almadan ASLA kullanmayın!
```

### 2. Sistem Yöneticisi Silinir
```
Tüm kullanıcılar silindiği için
sistem yöneticisi hesabı da silinir!
İlk kurulumda yeniden oluşturulmalıdır.
```

### 3. Foreign Key Sıralaması
```
Silme işlemi foreign key kısıtlarına uygun sırada yapılır.
Sıralama önemlidir, değiştirmeyin!
```

### 4. Production Uyarısı
```
Production ortamında kullanmadan önce
mutlaka yedek alın!
```

### 5. Log Kaydı
```
Sıfırlama işlemi konsola (terminal) loglanır.
İşlem sırasında detaylı bilgi gösterilir.
```

---

## 🔧 Özelleştirme

### Şifreyi Değiştirme
`app.py` dosyasında:
```python
RESET_PASSWORD = "518518Erkan!"  # Burası değiştirilebilir
```

### CSRF Koruması
Route'ta `@csrf.exempt` kullanılmıştır çünkü:
- Kendi şifre validasyonu var
- POST işlemi özel olarak korunmuş
- İhtiyaç varsa CSRF eklenebilir

---

## 🚀 Kullanım Senaryoları

### Test Ortamı Sıfırlama
```
Geliştirme sırasında test verilerini temizlemek için kullanılır.
```

### Demo Reset
```
Demo sunumlarından önce sistemi temiz başlatmak için.
```

### Yanlış Kurulum Düzeltme
```
İlk kurulumda hata yapılırsa düzeltmek için.
```

### Müşteri Teslimi
```
Müşteriye teslim öncesi temiz sistem için.
```

---

## 📞 Destek

Herhangi bir sorun yaşarsanız:
1. Konsol loglarını kontrol edin
2. Veritabanı yedeklerinizi gözden geçirin
3. İşlem sırasında hata mesajlarını kaydedin

---

## 🎯 Sonuç

Bu özellik, sistemin hızlıca sıfırlanması için güçlü bir araçtır. Ancak **GERİ DÖNÜŞÜ OLMAYAN** bir işlem olduğu için dikkatli kullanılmalıdır!

**Son Güncelleme:** 1 Kasım 2025  
**Versiyon:** 1.0.0
