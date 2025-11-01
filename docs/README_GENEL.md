# 🏨 Otel Minibar Takip Sistemi

Modern otel işletmeleri için geliştirilmiş, web tabanlı minibar stok ve zimmet yönetim sistemi.

---

## 📋 Sistem Hakkında

**Otel Minibar Takip Sistemi**, otel odalarındaki minibar ürünlerinin takibi, stok yönetimi ve personel zimmet işlemlerini dijital ortamda yönetmenizi sağlayan kapsamlı bir web uygulamasıdır.

### Temel Özellikler

✅ **Stok Yönetimi** - Depo stok takibi, giriş-çıkış işlemleri  
✅ **Zimmet Sistemi** - Personele ürün zimmetleme ve takibi  
✅ **Minibar Takibi** - Oda bazlı minibar içerik kontrolü  
✅ **Tüketim Takibi** - Oda ve ürün bazlı tüketim raporları  
✅ **Çoklu Kullanıcı** - 4 farklı rol ve yetki seviyesi  
✅ **Raporlama** - Excel ve PDF formatında detaylı raporlar  
✅ **Güvenlik** - Şifreleme, CSRF koruması, oturum yönetimi  
✅ **Audit Trail** - Tüm işlemlerin detaylı kayıt altına alınması  

---

## 👥 Kullanıcı Rolleri

### 1. Sistem Yöneticisi 🔧
- Otel, kat ve oda tanımlamaları
- Personel yönetimi
- Sistem logları ve denetim kayıtları
- Admin yetkisi atama

### 2. Admin 📦
- Ürün grupları oluşturma
- Ürün tanımlama ve düzenleme
- Kritik stok seviyesi belirleme

### 3. Depo Sorumlusu 📊
- Stok giriş işlemleri
- Personele zimmet atama
- Minibar durumlarını izleme
- Stok ve zimmet raporları

### 4. Kat Sorumlusu 🛎️
- Minibar ilk dolum
- Oda kontrolü ve sayım
- Minibar doldurma (tekli/toplu)
- Zimmet kullanımı

---

## 🎯 Ana İşlevler

### Stok Yönetimi
- Ürün giriş, çıkış ve devir işlemleri
- Anlık stok hesaplama
- Kritik stok uyarıları
- Stok hareket geçmişi

### Zimmet Sistemi
- FIFO (İlk Giren İlk Çıkar) mantığı
- Personel bazlı zimmet takibi
- Otomatik stok düşümü
- İade ve iptal işlemleri

### Minibar İşlemleri
- **İlk Dolum:** Yeni odaların ilk defa doldurulması
- **Kontrol:** Mevcut durumun görüntülenmesi
- **Doldurma:** Tüketim sayımı ve yeniden doldurma
- **Toplu İşlem:** Birden fazla odaya aynı anda ürün ekleme

### Raporlama
- Stok durum raporu
- Zimmet özet ve detay raporları
- Minibar işlem raporları
- Tüketim analiz raporları
- Kat bazlı raporlar
- Excel/PDF export desteği

---

## 💻 Teknik Özellikler

### Teknoloji Yığını
- **Backend:** Python 3.11+ / Flask 3.0
- **Veritabanı:** MySQL 8.0+
- **ORM:** SQLAlchemy 2.0
- **Frontend:** HTML5, Tailwind CSS 3.4, Vanilla JS
- **Grafikler:** Chart.js 4.4
- **Güvenlik:** Flask-WTF CSRF, Flask-Limiter, Werkzeug

### Güvenlik Özellikleri
- Şifre hash'leme (Werkzeug)
- CSRF token koruması
- Rate limiting (Brute-force koruması)
- Session yönetimi
- Rol bazlı erişim kontrolü
- Audit trail (İşlem kayıtları)

### Performans
- Database indexleme
- Toplu işlem desteği
- AJAX ile dinamik yükleme
- Optimized SQL sorguları



---

## 📖 İlk Kullanım

### 1. İlk Kurulum (Setup)
- Tarayıcıda `/setup` sayfası otomatik açılır
- Otel bilgilerini girin
- Sistem yöneticisi hesabı oluşturun
- Kurulum tamamlanır

### 2. Otel Yapısını Oluşturun
- Sistem Yöneticisi ile giriş yapın
- Katları tanımlayın (Örn: Zemin Kat, 1. Kat, 2. Kat)
- Odaları oluşturun (Örn: 101, 102, 103...)
- Personel hesapları ekleyin

### 3. Ürünleri Tanımlayın
- Admin rolü ile giriş yapın
- Ürün grupları oluşturun (Örn: İçecekler, Atıştırmalıklar)
- Ürünleri ekleyin (Örn: Coca Cola, Fıstık, Çikolata)
- Kritik stok seviyelerini belirleyin

### 4. Stok Girişi Yapın
- Depo Sorumlusu ile giriş yapın
- Stok Giriş sayfasından ürün ekleyin
- Miktar ve birim fiyat bilgilerini girin

### 5. Zimmet Atayın
- Kat Sorumlusu personele zimmet atayın
- Ürün ve miktarları seçin
- Zimmet otomatik stoktan düşülür

### 6. Minibarları Doldurun
- Kat Sorumlusu ile giriş yapın
- İlk dolum ile odaları doldurun
- Zimmetten otomatik düşüm yapılır

---

## 📊 İş Akışı Örneği

```
1. STOK GİRİŞİ (Depo Sorumlusu)
   ↓
   Depo'ya 1000 adet Coca Cola geldi
   
2. ZİMMET ATAMA (Depo Sorumlusu)
   ↓
   Kat Sorumlusu'na 200 adet Coca Cola zimmetle
   
3. İLK DOLUM (Kat Sorumlusu)
   ↓
   101 numaralı odaya 5 adet Coca Cola koy
   
4. KONTROL (Kat Sorumlusu)
   ↓
   Oda 101'i kontrol et → 3 adet kaldı (2 tüketilmiş)
   
5. DOLDURMA (Kat Sorumlusu)
   ↓
   Gerçek sayım: 3 adet
   Ekle: 2 adet
   Tüketim: 2 adet → Kaydedilir
   Yeni stok: 5 adet
   
6. RAPORLAMA
   ↓
   Oda bazlı tüketim raporu
   Zimmet durum raporu
   Stok raporu
```

---

## 🔒 Güvenlik Özellikleri

### Kimlik Doğrulama
- Güçlü şifre politikası (min. 8 karakter, büyük/küçük harf, rakam)
- Şifre hash'leme (pbkdf2:sha256)
- Session tabanlı oturum yönetimi

### Koruma Mekanizmaları
- **CSRF:** Tüm formlar token korumalı
- **Rate Limiting:** Login 5 deneme/dakika
- **Brute-Force:** 5 başarısız denemeden sonra 1 saat bloke
- **XSS:** Template auto-escaping
- **SQL Injection:** Parametreli sorgular

### Audit Trail
- Tüm CRUD işlemleri kaydedilir
- Eski ve yeni değerler JSON formatında
- Kullanıcı, IP, zaman damgası
- Değişiklik özeti (insan okunabilir)

---

## 📈 Raporlar

### Mevcut Raporlar

1. **Stok Durum Raporu**
   - Tüm ürünlerin anlık stok durumu
   - Kritik stok uyarıları

2. **Zimmet Raporu**
   - Personel bazlı zimmet özeti
   - Teslim edilen, kullanılan, kalan

3. **Minibar İşlem Raporu**
   - Tarih aralığına göre tüm işlemler
   - Oda, personel, işlem tipi

4. **Tüketim Raporu**
   - Ürün bazlı toplam tüketim
   - En çok tüketilen ürünler

5. **Kat Bazlı Rapor**
   - Kat geneli ürün dağılımı
   - Oda detayları

6. **Personel Zimmet Detay**
   - Personel bazlı detaylı zimmet geçmişi

7. **Oda Bazlı Rapor**
   - Oda bazlı işlem ve tüketim

**Export Formatları:** Excel (.xlsx), PDF

---

## 🛠️ Önemli Özellikler

### FIFO Zimmet Sistemi
Zimmetten düşüm yapılırken en eski zimmet kaydından başlanır:
```
Örnek:
- Zimmet #1: 50 adet (01.10.2025)
- Zimmet #2: 200 adet (15.10.2025)

80 adet kullanım:
→ Zimmet #1'den 50 adet (tamamlandı)
→ Zimmet #2'den 30 adet (kalan 170)
```

### Toplu Oda Doldurma
Birden fazla odaya aynı anda ürün ekleme:
- Kat seçimi
- Çoklu oda seçimi
- Tek ürün, tek miktar
- Toplu işlem raporu

### Kritik Stok Uyarı Sistemi
- **Kritik:** Stok ≤ Kritik Seviye (Kırmızı)
- **Dikkat:** Stok ≤ Kritik × 1.5 (Sarı)
- **Yeterli:** Stok > Kritik × 1.5 (Yeşil)

### Dinamik Dashboard'lar
Her rol için özelleştirilmiş dashboard:
- İstatistik kartları
- Grafikler (Chart.js)
- Son işlemler
- Hızlı erişim butonları

---

