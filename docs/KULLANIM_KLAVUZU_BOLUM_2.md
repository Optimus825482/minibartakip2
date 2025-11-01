# 🏨 OTEL MİNİBAR TAKİP SİSTEMİ - KULLANIM KILAVUZU
## BÖLÜM 2: ROL TABANLI KULLANIM KLAVUZLARI

**Versiyon:** 1.0  
**Tarih:** 31 Ekim 2025

---

## 1. SİSTEM YÖNETİCİSİ KULLANIM KILAVUZU

### 1.1 Dashboard (Ana Sayfa)

#### Erişim
```
URL: /sistem-yoneticisi
Menü: Otomatik yönlendirme (login sonrası)
```

#### Dashboard Bileşenleri

**1. İstatistik Kartları**
- **Toplam Kat:** Sistemdeki aktif kat sayısı
- **Toplam Oda:** Sistemdeki aktif oda sayısı
- **Toplam Kullanıcı:** Admin + Personel sayısı
- **Toplam Personel:** Depo + Kat sorumlusu sayısı

**2. Hızlı Erişim Kartları**
- Ürün Grupları ve Toplam Ürün
- Kritik Stoklu Ürünler
- Stok Durum Özeti (Kritik/Dikkat/Normal)

**3. Son Eklenenler**
- Son 5 kat
- Son 5 oda
- Son 5 personel
- Son 5 ürün

**4. Grafikler**
- Kullanıcı rol dağılımı (Pasta grafik)
- Kat bazlı oda sayıları (Bar grafik)
- Ürün tüketim trendleri (Line grafik)

### 1.2 Otel Tanımlama

#### Erişim
```
Menü: Sistem Yöneticisi → Otel Tanımla
URL: /otel-tanimla
```

#### İşlem Adımları

**1. Otel Bilgilerini Görüntüleme**
- Mevcut otel bilgileri formda gösterilir
- Setup'ta oluşturulan otel otomatik yüklenir

**2. Otel Bilgilerini Güncelleme**
```
Form Alanları:
- Otel Adı: (Zorunlu, 2-200 karakter)
- Adres: (Zorunlu, 10-500 karakter)
- Telefon: (Zorunlu, 10-20 karakter)
- E-posta: (Opsiyonel, geçerli e-posta)
- Vergi No: (Opsiyonel, max 50 karakter)
```

**3. Kaydetme**
- "Kaydet" butonuna tıklayın
- Başarı mesajı görüntülenir
- Değişiklikler audit log'a kaydedilir

### 1.3 Kat Yönetimi

#### Kat Tanımlama

**Erişim:** `/kat-tanimla`

**1. Yeni Kat Ekleme**
```
Form Alanları:
- Kat Adı: (Zorunlu, örn: "Zemin Kat", "1. Kat")
- Kat No: (Zorunlu, -5 ile 100 arası)
- Açıklama: (Opsiyonel, max 500 karakter)
```

**2. Kat Listesi**
- Tüm aktif katlar tablo halinde gösterilir
- Kat No'ya göre sıralıdır
- Her kat için işlem butonları:
  - 🖊️ Düzenle
  - 🗑️ Sil

**3. Kat Düzenleme**
- Düzenle butonuna tıklayın
- Kat bilgilerini güncelleyin
- "Güncelle" butonuna tıklayın

**4. Kat Silme**
⚠️ **Uyarı:** Pasif yapılır, kalıcı olarak silinmez
- Sil butonuna tıklayın
- Onay mesajı gelir
- Kat pasif duruma geçer

#### Kat Düzenleme

**Erişim:** `/kat-duzenle/<kat_id>`

**İşlemler:**
- Kat adı değiştirme
- Kat no değiştirme (benzersiz olmalı)
- Açıklama güncelleme

### 1.4 Oda Yönetimi

#### Oda Tanımlama

**Erişim:** `/oda-tanimla`

**1. Yeni Oda Ekleme**
```
Form Alanları:
- Kat: (Dropdown, aktif katlar)
- Oda Numarası: (Zorunlu, benzersiz, 1-20 karakter)
  Örnek: 101, 102, 201-A, vb.
- Oda Tipi: (Opsiyonel, max 50 karakter)
  Örnek: Standart, Suit, Deluxe
- Kapasite: (Opsiyonel, 1-20 kişi)
```

**2. Oda Listesi**
- Tüm aktif odalar tablo halinde
- Oda no'ya göre sıralı
- Kat bilgisi gösterilir
- İşlem butonları:
  - 🖊️ Düzenle
  - 🗑️ Sil

**3. Oda Düzenleme**
- Kat değiştirebilme
- Oda no değiştirebilme (benzersiz)
- Oda tipi ve kapasite güncelleyebilme

**4. Oda Silme**
⚠️ **Uyarı:** Minibar kaydı olan odalar silinemez
- Sil butonuna tıklayın
- Onay mesajı
- Oda kalıcı olarak silinir

### 1.5 Personel Yönetimi (Admin Atama)

#### Personel Tanımlama

**Erişim:** `/personel-tanimla`

**1. Yeni Personel Ekleme**
```
Form Alanları:
- Kullanıcı Adı: (Zorunlu, 3-50 karakter, benzersiz)
  * Sadece harf, rakam, (_-.)
- Ad: (Zorunlu, 2-50 karakter)
- Soyad: (Zorunlu, 2-50 karakter)
- E-posta: (Opsiyonel, benzersiz)
- Telefon: (Opsiyonel, max 20 karakter)
- Rol: (Dropdown)
  * Admin
  * Depo Sorumlusu
  * Kat Sorumlusu
- Şifre: (Zorunlu, min 8 karakter, güçlü)
```

**2. Şifre Gereksinimleri**
```
✓ Minimum 8 karakter
✓ En az 1 büyük harf
✓ En az 1 küçük harf
✓ En az 1 rakam
✓ En az 1 özel karakter (!@#$%^&*...)
```

**3. Personel Listesi**
- Tüm personeller tablo halinde
- Rol bazlı filtreleme
- Aktif/Pasif durumu
- İşlem butonları:
  - 🖊️ Düzenle
  - 🔒 Pasif Yap
  - 🔓 Aktif Yap

**4. Personel Düzenleme**
- Kullanıcı bilgilerini güncelleme
- Rol değiştirme
- Şifre sıfırlama (opsiyonel)

**5. Personel Pasif/Aktif Yapma**
- Pasif: Kullanıcı giriş yapamaz
- Aktif: Kullanıcı tekrar giriş yapabilir
- Pasif kullanıcılar silinmez, devre dışı bırakılır

### 1.6 Sistem Logları

#### Erişim
```
URL: /sistem-loglari
Menü: Sistem Yöneticisi → Sistem Logları
```

#### Log Görüntüleme

**1. Filtreler**
```
- İşlem Tipi: Tümü/Ekleme/Güncelleme/Silme/Giriş/Çıkış
- Modül: Tümü/Urun/Stok/Zimmet/Minibar/vb.
- Kullanıcı: Dropdown ile seçim
- Sayfa: Pagination (50 kayıt/sayfa)
```

**2. Log Bilgileri**
```
Tablo Sütunları:
- ID
- Tarih/Saat
- Kullanıcı (Ad Soyad)
- İşlem Tipi
- Modül
- Detay (JSON formatında)
- IP Adresi
```

**3. Log Detayları**
- Her log satırına tıklayarak detay görülebilir
- JSON formatında işlem bilgileri
- İşlem öncesi/sonrası değerler

### 1.7 Audit Trail (Denetim İzi)

#### Erişim
```
URL: /sistem-yoneticisi/audit-trail
Menü: Sistem Yöneticisi → Audit Trail
```

#### Özellikler

**1. Tam Denetim İzi**
- Tüm veri değişiklikleri kaydedilir
- Eski ve yeni değerler saklanır
- Değişiklik özeti oluşturulur
- Kim, ne, ne zaman, nereden

**2. Filtreler**
```
- Kullanıcı: Dropdown seçim
- İşlem Tipi: create/update/delete/login/logout/view/export
- Tablo: Dropdown seçim
- Tarih Aralığı: Başlangıç-Bitiş
```

**3. Audit Log Detayı**
```
Bilgiler:
- Kullanıcı bilgisi (ID, Ad, Rol)
- İşlem tipi ve tarih
- Etkilenen tablo ve kayıt ID
- Eski değerler (JSON)
- Yeni değerler (JSON)
- Değişiklik özeti (okunabilir)
- HTTP bilgileri (Method, URL, Endpoint)
- Ağ bilgileri (IP, User Agent)
- Başarı durumu ve hata mesajı
```

**4. Excel Export**
- Filtrelenmiş logları Excel'e aktarma
- Maksimum 10,000 kayıt
- Otomatik sütun genişlik ayarı
- Başlık formatlaması

**5. İstatistikler**
```
- Bugün: Bugünün toplam log sayısı
- Bu Hafta: Haftalık toplam
- Bu Ay: Aylık toplam
```

---

## 2. ADMİN KULLANICI KULLANIM KILAVUZU

### 2.1 Dashboard

Admin kullanıcılar Sistem Yöneticisi ile aynı dashboard'u kullanır ve tüm yetkilere sahiptir.

### 2.2 Ürün Grup Yönetimi

#### Erişim
```
URL: /urun-gruplari
Menü: Admin → Ürün Grupları
```

#### Yeni Grup Ekleme

**1. Form Doldurma**
```
- Grup Adı: (Zorunlu, 2-100 karakter, benzersiz)
  Örnek: İçecekler, Atıştırmalıklar, Alkollü İçecekler
- Açıklama: (Opsiyonel, max 500 karakter)
```

**2. Kaydetme**
- "Ekle" butonuna tıklayın
- Başarı mesajı
- Grup listesinde görünür

#### Grup Listesi

**Görünüm:**
- Tüm gruplar tablo halinde
- Grup adına göre alfabetik sıralı
- Aktif/Pasif durumu
- İşlem butonları

**İşlem Butonları:**
- 🖊️ **Düzenle:** Grup adı ve açıklama değiştir
- 🗑️ **Sil:** Grubu sil (ürün yoksa)
- 🔒 **Pasif Yap:** Grubu pasif et
- 🔓 **Aktif Yap:** Grubu aktif et

⚠️ **Önemli:** Gruba ait ürün varsa silinemez!

### 2.3 Ürün Yönetimi

#### Erişim
```
URL: /urunler
Menü: Admin → Ürünler
```

#### Yeni Ürün Ekleme

**1. Form Doldurma**
```
- Ürün Grubu: (Dropdown, zorunlu)
- Ürün Adı: (Zorunlu, 2-200 karakter)
  Örnek: Coca Cola 330ml, Çikolata, Cips
- Barkod: (Opsiyonel, max 50 karakter, benzersiz)
  Örnek: 8690504123456
- Birim: (Dropdown, zorunlu)
  Seçenekler: Adet, Şişe, Kutu, Paket, Gram, Kilogram, Litre
- Kritik Stok Seviyesi: (Zorunlu, 0-10000)
  Bu seviyenin altında uyarı verilir
```

**2. Kaydetme**
- "Ekle" butonuna tıklayın
- Başarı mesajı
- Ürün listesinde görünür
- Stok hareketi otomatik başlatılır (0 stok)

#### Ürün Listesi

**Görünüm:**
- Tüm ürünler tablo halinde
- Filtreleme ve arama
- Grup bilgisi gösterilir
- Mevcut stok gösterilir
- Stok durumu badge'i (Kritik/Dikkat/Normal)

**Stok Durumu Göstergeleri:**
```
🔴 Kritik: Stok ≤ Kritik Seviye
🟡 Dikkat: Stok ≤ Kritik Seviye × 1.5
🟢 Yeterli: Stok > Kritik Seviye × 1.5
```

**İşlem Butonları:**
- 🖊️ **Düzenle:** Ürün bilgilerini güncelle
- 🗑️ **Sil:** Ürünü sil (stok hareketi yoksa)
- 🔒 **Pasif Yap:** Ürünü pasif et
- 🔓 **Aktif Yap:** Ürünü aktif et

#### Ürün Düzenleme

**Güncellenebilir Alanlar:**
- Ürün adı
- Ürün grubu
- Barkod
- Birim
- Kritik stok seviyesi

**Güncellenemez:**
- ID (otomatik)
- Oluşturma tarihi

### 2.4 Personel Yönetimi

Admin kullanıcılar, Sistem Yöneticisi ile aynı personel yönetimi yetkilerine sahiptir.

**Erişim:** `/personel-tanimla`

**Yetkiler:**
- Yeni personel ekleme
- Personel düzenleme
- Personel pasif/aktif yapma
- Şifre sıfırlama

---

## 3. DEPO SORUMLUSU KULLANIM KILAVUZU

### 3.1 Dashboard

#### Erişim
```
URL: /depo
Menü: Otomatik yönlendirme (login sonrası)
```

#### Dashboard Bileşenleri

**1. İstatistik Kartları**
- **Toplam Ürün:** Aktif ürün sayısı
- **Kritik Ürün:** Kritik stokta olan ürünler
- **Aktif Zimmetler:** Devam eden zimmet sayısı
- **Bu Ay İadeler:** Aylık iade işlemi sayısı

**2. Stok Durum Özeti**
- Kritik stokta olanlar (Kırmızı)
- Dikkat gerektiren (Sarı)
- Yeterli stokta olanlar (Yeşil)

**3. Son Stok Hareketleri**
- Son 10 işlem
- Tarih, ürün, hareket tipi, miktar

**4. Grafikler**
- Grup bazlı stok durumu (Bar grafik)
- Son 7 günün stok hareketleri (Line grafik)
- Ürün bazlı tüketim (Bar grafik)

### 3.2 Stok Girişi

#### Erişim
```
URL: /stok-giris
Menü: Depo Sorumlusu → Stok Girişi
```

#### Stok Girişi Yapma

**1. Form Doldurma**
```
- Ürün: (Dropdown, aktif ürünler)
- Hareket Tipi: (Dropdown)
  * Giriş: Yeni stok girişi
  * Devir: Devir stok
  * Sayım: Sayım düzeltmesi
- Miktar: (Pozitif sayı, 1-1,000,000)
- Açıklama: (Opsiyonel, max 500 karakter)
```

**2. Kaydetme**
- "Kaydet" butonuna tıklayın
- Stok otomatik güncellenir
- İşlem loglanır
- Başarı mesajı görüntülenir

#### Stok Hareketleri Listesi

**Görünüm:**
- Son 50 hareket gösterilir
- Tarih, ürün, hareket tipi, miktar, açıklama
- İşlem yapan kullanıcı
- Filtreleme ve arama

**İşlem Butonları:**
- 🖊️ **Düzenle:** Hareketi düzenle
- 🗑️ **Sil:** Hareketi sil

⚠️ **Uyarı:** Stok düzenlemesi ve silme işlemleri dikkatle yapılmalıdır!

### 3.3 Personel Zimmet

#### Erişim
```
URL: /personel-zimmet
Menü: Depo Sorumlusu → Personel Zimmet
```

#### Yeni Zimmet Atama

**1. Personel Seçimi**
- Dropdown'dan Kat Sorumlusu seçin
- Sadece aktif kat sorumluları görünür

**2. Ürün Seçimi**
```
- Ürün Gruplarına Göre Listeleme
- Her ürün için:
  * Checkbox ile seçim
  * Miktar girişi
  * Mevcut stok gösterimi
  * Birim bilgisi
```

**3. Stok Kontrolü**
- Seçilen ürünler için toplam miktar hesaplanır
- Stok uygunluğu kontrol edilir
- Yetersiz stokta uyarı verilir
- Detaylı hata mesajları

**4. Zimmet Oluşturma**
```
- Açıklama: (Opsiyonel)
- "Zimmet Ata" butonuna tıklayın
```

**5. İşlem Sonuçları**
- Zimmet başlık kaydı oluşturulur
- Her ürün için detay kaydı oluşturulur
- Stoktan otomatik çıkış yapılır
- Personelin zimmeti güncellenir
- Başarı mesajı

#### Aktif Zimmetler Listesi

**Görünüm:**
- Tüm aktif zimmetler tablo halinde
- Personel adı
- Zimmet tarihi
- Ürün sayısı
- Toplam miktar
- İşlem butonları

**İşlem Butonları:**
- 👁️ **Detay:** Zimmet detaylarını görüntüle
- ❌ **İptal:** Zimmeti iptal et (tümünü iade al)

#### Zimmet Detay

**Erişim:** `/zimmet-detay/<zimmet_id>`

**Görüntülenen Bilgiler:**
```
Zimmet Başlık:
- Zimmet No
- Personel Adı
- Teslim Eden
- Zimmet Tarihi
- Durum (Aktif/Tamamlandı/İptal)
- Açıklama

Zimmet Detayları (Ürünler):
- Ürün Adı, Birim
- Teslim Edilen Miktar
- Kullanılan Miktar
- İade Edilen Miktar
- Kalan Miktar
- İşlem Butonu: 📥 İade Al
```

**İade Alma İşlemi:**
1. İade Al butonuna tıklayın
2. İade miktarı girin (maksimum: kalan miktar)
3. Açıklama ekleyin (opsiyonel)
4. "İade Al" butonuna tıklayın
5. Stoka otomatik giriş yapılır
6. Zimmet detayı güncellenir

**Zimmet İptal:**
- Tüm kalan ürünler depoya iade edilir
- Zimmet durumu "İptal" olur
- Stok otomatik güncellenir

### 3.4 Minibar Durumları

#### Erişim
```
URL: /minibar-durumlari
Menü: Depo Sorumlusu → Minibar Durumları
```

#### Minibar Görüntüleme

**1. Kat Seçimi**
- Dropdown'dan kat seçin
- Odalar otomatik yüklenir

**2. Oda Seçimi**
- Dropdown'dan oda seçin
- Minibar içeriği yüklenir

**3. Minibar İçeriği**
```
Gösterilen Bilgiler:
- Oda bilgisi (Kat, Oda No)
- Son işlem tarihi ve tipi
- Ürün listesi:
  * Ürün adı
  * Mevcut stok
  * Toplam eklenen
  * Toplam tüketim
  * Birim
```

**4. Ürün Geçmişi**
- Her ürün için "Geçmiş" butonuna tıklayın
- Modal popup açılır
- Tüm minibar işlemleri kronolojik gösterilir
- İşlem tarihi, tipi, başlangıç, eklenen, tüketim, bitiş

### 3.5 Raporlar

#### Erişim
```
URL: /depo-raporlar
Menü: Depo Sorumlusu → Raporlar
```

#### Rapor Tipleri

**1. Stok Durum Raporu**
```
İçerik:
- Tüm ürünlerin mevcut stok durumu
- Ürün adı, grup, birim
- Mevcut stok, kritik seviye
- Durum (Kritik/Normal)

Filtreler:
- Ürün Grubu
```

**2. Stok Hareket Raporu**
```
İçerik:
- Detaylı stok hareketleri
- Tarih, ürün, hareket tipi, miktar
- İşlem yapan, açıklama
- Zimmet bilgisi (varsa)

Filtreler:
- Tarih Aralığı
- Ürün/Ürün Grubu
- Hareket Tipi (Giriş/Çıkış)
```

**3. Zimmet Raporu**
```
İçerik:
- Tüm zimmet kayıtları
- Zimmet no, personel, tarih
- Ürün sayısı, toplam miktar
- Durum (Aktif/Tamamlandı/İptal)

Filtreler:
- Tarih Aralığı
- Personel
```

**4. Zimmet Detay Raporu**
```
İçerik:
- Ürün bazlı zimmet bilgileri
- Personel, ürün, miktar
- Kullanım durumu

Filtreler:
- Tarih Aralığı
- Personel
- Ürün/Ürün Grubu
```

**5. Minibar Tüketim Raporu**
```
İçerik:
- Oda bazlı tüketim kayıtları
- Sadece gerçek tüketim (kontrol/doldurma)
- Ürün, oda, kat, tarih, tuketim
- Kat sorumlusu bilgisi

Filtreler:
- Tarih Aralığı
- Personel
- Ürün/Ürün Grubu
```

**6. Ürün Grubu Raporu**
```
İçerik:
- Grup bazlı stok istatistikleri
- Grup adı
- Toplam ürün sayısı
- Kritik stoklu ürün sayısı
```

**7. Özet Rapor**
```
İçerik:
- Genel sistem durumu
- Toplam ürün
- Kritik ürün sayısı
- Aktif zimmet
- Bugünkü giriş/çıkış
- Bu ayki zimmet sayısı
```

#### Rapor Export

**Excel Export:**
- Her rapor için Excel butonu
- Filtrelenmiş veriler export edilir
- Otomatik formatlanmış tablo
- Başlık ve stil uygulanır

**PDF Export:**
- Her rapor için PDF butonu
- Filtrelenmiş veriler export edilir
- Türkçe karakter desteği (ASCII dönüşüm)
- Tablo formatında çıktı
- Maksimum 100 kayıt (performans için)

---

**BÖLÜM 2 SONU**

**Sonraki Bölüm:** Kat Sorumlusu ve Özellik Detayları  
**Sayfa:** 3/4

---

*Bu dokümantasyon sürekli güncellenmektedir. Son güncelleme: 31 Ekim 2025*
