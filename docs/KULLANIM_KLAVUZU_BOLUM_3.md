# 🏨 OTEL MİNİBAR TAKİP SİSTEMİ - KULLANIM KILAVUZU
## BÖLÜM 3: KAT SORUMLUSU VE ÖZELLİK DETAYLARI

**Versiyon:** 1.0  
**Tarih:** 31 Ekim 2025

---

## 1. KAT SORUMLUSU KULLANIM KILAVUZU

### 1.1 Dashboard

#### Erişim
```
URL: /kat-sorumlusu
Menü: Otomatik yönlendirme (login sonrası)
```

#### Dashboard Bileşenleri

**1. İstatistik Kartları**
- **Aktif Zimmetler:** Sahip olunan aktif zimmet sayısı
- **Zimmet Toplamı:** Zimmetteki toplam ürün miktarı

**2. Son Minibar İşlemleri**
- Son 10 işlem
- Oda, işlem tipi, tarih

**3. Grafikler**
- Zimmet kullanım durumu (Bar grafik - Ürün bazlı)
- Minibar işlem tipi dağılımı (Pasta grafik)

### 1.2 Zimmetim

#### Erişim
```
URL: /zimmetim
Menü: Kat Sorumlusu → Zimmetim
```

#### Zimmet Görüntüleme

**Zimmet İstatistikleri:**
- Toplam Zimmet: Teslim alınan toplam miktar
- Kullanılan: Minibar'lara aktarılan miktar
- Kalan: Henüz kullanılmayan miktar

**Aktif Zimmetler Listesi:**
```
Her Zimmet için:
- Zimmet No
- Zimmet Tarihi
- Teslim Eden (Depo Sorumlusu)
- Ürün Detayları (Genişletilebilir)

Ürün Detayları:
- Ürün Adı, Birim
- Teslim Edilen Miktar
- Kullanılan Miktar
- Kalan Miktar
- Kullanım Yüzdesi (Progress bar)
```

### 1.3 Minibar Kontrol

#### Erişim
```
URL: /minibar-kontrol
Menü: Kat Sorumlusu → Minibar Kontrol
```

#### İşlem Tipleri

**1. İlk Dolum**
- Yeni odanın ilk defa doldurulması
- Tüm ürünler için başlangıç stoku eklenir
- Zimmetten düşüm yapılır

**2. Kontrol**
- Minibar içeriğini görüntüleme
- Kayıt oluşturmaz (sadece görüntüleme)
- Mevcut stok bilgisi gösterilir

**3. Doldurma**
- Tüketilmiş ürünlerin yeniden doldurulması
- Gerçek sayım yapılır
- Tüketim hesaplanır
- Zimmetten düşüm yapılır

#### İlk Dolum İşlemi

**Adımlar:**

**1. Kat Seçimi**
- Dropdown'dan kat seçin
- Odalar otomatik yüklenir

**2. Oda Seçimi**
- Dropdown'dan oda seçin
- İlk dolum yapılmamış oda olmalı

**3. İşlem Tipi Seçimi**
- "İlk Dolum" seçin

**4. Ürün Seçimi ve Miktar Girişi**
```
- Ürün gruplarına göre listelenir
- Her ürün için:
  * Checkbox ile seçim
  * Miktar girişi
  * Zimmetteki miktar gösterilir
  * Yetersiz zimmet uyarısı
```

**5. Kaydetme**
- "Kaydet" butonuna tıklayın
- Zimmet kontrolü yapılır
- Minibar kaydı oluşturulur
- Zimmetten otomatik düşüm yapılır
- Başarı mesajı

#### Kontrol İşlemi

**Adımlar:**

**1. Kat ve Oda Seçimi**
- Daha önce dolum yapılmış oda seçin

**2. İşlem Tipi**
- "Kontrol" seçin

**3. Mevcut Durum Görüntüleme**
- Odanın son minibar durumu gösterilir
- Her ürün için mevcut stok
- Son işlem tarihi

**4. Kayıt**
- "Görüntüle" butonuna tıklayın
- Sistem logu oluşturulur
- Minibar kaydı oluşturulmaz

#### Doldurma İşlemi (Tekli)

**Adımlar:**

**1. Kat ve Oda Seçimi**
- İlk dolum yapılmış oda seçin

**2. İşlem Tipi**
- "Doldurma" seçin

**3. Mevcut Durum Yükleme**
- Odanın son minibar durumu otomatik yüklenir
- Her ürün için mevcut stok gösterilir

**4. Gerçek Sayım ve Doldurma**
```
Her Ürün için:
- Mevcut Stok: Kayıtlı değer (otomatik)
- Gerçek Stok: Sayım sonucu (manuel girilir)
- Eklenecek: Doldurulacak miktar (manuel girilir)

Hesaplama:
- Tüketim = Kayıtlı Stok - Gerçek Stok
- Yeni Stok = Gerçek Stok + Eklenecek
```

**5. Zimmet Kontrolü**
- Eklenen miktarlar zimmet ile karşılaştırılır
- Yetersiz zimmet uyarısı
- Kullanılabilir zimmet gösterilir

**6. Kaydetme**
- Tüm ürünler için bilgi girildikten sonra
- "Kaydet" butonuna tıklayın
- Minibar kaydı oluşturulur
- Tüketim kaydedilir
- Zimmetten düşüm yapılır

### 1.4 Toplu Oda Doldurma

#### Erişim
```
URL: /toplu-oda-doldurma
Menü: Kat Sorumlusu → Toplu Oda Doldurma
```

#### Özellikler

**Avantajlar:**
- Birden fazla odaya aynı anda ürün ekleme
- Zaman tasarrufu
- Toplu işlem desteği
- Detaylı durum raporlama

**Limitler:**
- Sadece doldurma işlemi (tüketim takibi yok)
- Direkt stok ekleme
- İlk dolum yapılmış odalara uygulanır

#### İşlem Adımları

**1. Kat Seçimi**
- Dropdown'dan kat seçin
- Odalar otomatik checkbox listesi olarak yüklenir

**2. Oda Seçimi**
- İstediğiniz odaları seçin (çoklu seçim)
- "Tümünü Seç" / "Tümünü Kaldır" butonları

**3. Ürün Seçimi**
- Ürün grubu seçin (opsiyonel filtreleme)
- Dropdown'dan ürün seçin

**4. Miktar Belirleme**
- Tüm seçili odalara eklenecek miktar
- Tek bir miktar değeri

**5. Mevcut Durum Görüntüleme**
- "Mevcut Durumu Göster" butonuna tıklayın
- Her oda için mevcut stok gösterilir
- Tablo formatında

**6. Zimmet Kontrolü**
```
Hesaplama:
Toplam Gerekli = Oda Sayısı × Eklenecek Miktar

Kontroller:
- Zimmette yeterli ürün var mı?
- Yetersiz zimmet uyarısı
- Kalan zimmet gösterimi
```

**7. Toplu Doldurma**
- "Toplu Doldur" butonuna tıklayın
- Her oda için işlem başlatılır
- İlerleme gösterilir

**8. Sonuç Raporu**
```
Gösterilen Bilgiler:
- Başarılı Oda Sayısı
- Başarısız Oda Sayısı
- Başarılı Odalar Listesi (Oda No)
- Başarısız Odalar ve Hata Mesajları
- Kullanılan Toplam Zimmet
```

#### Toplu İşlem Detayları

**Arka Plan İşlemi:**
1. Her oda için sırayla işlem yapılır
2. Mevcut minibar durumu alınır
3. Diğer ürünler değişmeden kopyalanır
4. Seçilen ürün için yeni kayıt oluşturulur
5. Zimmetten FIFO mantığıyla düşüm yapılır
6. Hata oluşursa o oda atlanır, diğerleri devam eder

**Önemli Notlar:**
- Tüketim takibi yapılmaz (direkt ekleme)
- Mevcut stoka eklenir
- İlk dolum yapılmamış odalara uygulanamaz
- Zimmetten otomatik düşüm yapılır

### 1.5 Kat Bazlı Rapor

#### Erişim
```
URL: /kat-bazli-rapor
Menü: Kat Sorumlusu → Raporlar → Kat Bazlı Rapor
```

#### Rapor Özellikleri

**Gösterilen Bilgiler:**
- Kat adı ve oda sayısı
- Her oda için:
  * Oda numarası
  * Son işlem tarihi
  * Ürün bazlı mevcut stok
  * Toplam tüketim
- Ürün özeti (Kat geneli)

**Filtreler:**
- Tarih Aralığı: Başlangıç - Bitiş

**İşlemler:**
1. Kat seçin
2. Tarih aralığı belirleyin (opsiyonel)
3. "Rapor Oluştur" butonuna tıklayın
4. Rapor dinamik olarak oluşturulur

**Rapor Bölümleri:**

**1. Kat Özeti**
- Kat adı
- Oda sayısı
- Toplam ürün çeşidi

**2. Oda Detayları**
```
Tablo Sütunları:
- Oda No
- Son İşlem Tarihi
- Ürün Listesi (Genişletilebilir)
  * Ürün Adı
  * Mevcut Stok
  * Tüketim
  * Birim
```

**3. Ürün Özeti**
```
Kat genelinde ürün bazlı toplam:
- Ürün Adı
- Toplam Tüketim
- Birim
Sıralama: En çok tüketilenden en aza
```

### 1.6 Kişisel Raporlar

#### Erişim
```
URL: /kat-raporlar
Menü: Kat Sorumlusu → Raporlar
```

#### Rapor Tipleri

**1. Minibar İşlem Raporu**
```
İçerik:
- Kendi yaptığı tüm minibar işlemleri
- Tarih, oda, işlem tipi, ürün sayısı

Filtreler:
- Tarih Aralığı
```

**2. Tüketim Raporu**
```
İçerik:
- Ürün bazlı toplam tüketim
- Sadece kendi işlemleri
- Ürün adı, toplam tüketim, işlem sayısı

Filtreler:
- Tarih Aralığı
```

**3. Oda Bazlı Rapor**
```
İçerik:
- Oda bazlı işlem ve tüketim istatistikleri
- Sadece kendi işlemleri
- Oda no, işlem sayısı, toplam tüketim, son işlem

Filtreler:
- Tarih Aralığı
```

---

## 2. STOK YÖNETİMİ DETAYLARI

### 2.1 Stok Hesaplama Algoritması

#### Temel Formül
```
Mevcut Stok = Giriş - Çıkış

Detaylı:
Giriş Toplamı = SUM(Giriş + Devir + Sayım)
Çıkış Toplamı = SUM(Çıkış)
Mevcut Stok = Giriş Toplamı - Çıkış Toplamı
```

#### Stok Hareket Tipleri

**1. Giriş**
- Yeni stok alımı
- Tedarikçiden gelen ürünler
- Stoku artırır

**2. Çıkış**
- Personel zimmet atama
- Stoku azaltır
- Otomatik oluşturulur (zimmet atamada)

**3. Devir**
- Başlangıç stoku
- Eski sistemden aktarım
- Stoku artırır

**4. Sayım**
- Sayım sonucu düzeltme
- Fire/Fazla düzeltme
- Pozitif/Negatif olabilir

### 2.2 Kritik Stok Uyarı Sistemi

#### Stok Seviyeleri

**1. Kritik (Kırmızı)**
```
Koşul: Mevcut Stok ≤ Kritik Seviye
Durum: Acil sipariş gerekli
Görünüm: Kırmızı badge, uyarı ikonu
```

**2. Dikkat (Sarı)**
```
Koşul: Kritik Seviye < Mevcut Stok ≤ (Kritik Seviye × 1.5)
Durum: Yakında sipariş gerekli
Görünüm: Sarı badge, dikkat ikonu
```

**3. Yeterli (Yeşil)**
```
Koşul: Mevcut Stok > (Kritik Seviye × 1.5)
Durum: Stok yeterli
Görünüm: Yeşil badge, onay ikonu
```

#### Kritik Stok Bildirimleri

**Dashboard'ta:**
- Kritik ürün sayısı gösterilir
- Kritik ürünler listesi
- Renk kodlu gösterimler

**Ürün Listesinde:**
- Her ürün için stok durumu badge'i
- Filtreleme seçeneği (Sadece Kritik)
- Mevcut stok ve kritik seviye gösterimi

### 2.3 Stok Takip Best Practices

**1. Düzenli Sayım**
- Periyodik fiziksel sayım yapın
- Sayım sonuçlarını sisteme girin
- Fire/Fazla nedenleri belirtin

**2. Kritik Seviye Ayarları**
- Gerçekçi kritik seviyeler belirleyin
- Tüketim hızına göre ayarlayın
- Tedarik süresini dikkate alın

**3. Zimmet Yönetimi**
- Gereksiz zimmetten kaçının
- Düzenli iade alın
- Kullanılmayan zimmetleri iptal edin

**4. Raporlama**
- Düzenli stok raporları alın
- Tüketim trendlerini takip edin
- Anomalileri araştırın

---

## 3. ZİMMET SİSTEMİ DETAYLARI

### 3.1 Zimmet Yaşam Döngüsü

#### Adımlar

**1. Zimmet Atama (Depo Sorumlusu)**
```
İşlem:
- Personel seçimi
- Ürün ve miktar belirleme
- Stok kontrolü
- Zimmet kaydı oluşturma
- Stoktan otomatik çıkış

Sonuç:
- Zimmet Durumu: Aktif
- Stok güncellenir
- Personele bildirim (opsiyonel)
```

**2. Zimmet Kullanımı (Kat Sorumlusu)**
```
İşlem:
- Minibar doldurma sırasında
- Otomatik zimmetten düşüm
- FIFO mantığı (İlk giren ilk çıkar)

Sonuç:
- Kullanılan miktar artar
- Kalan miktar azalır
- Zimmet detayı güncellenir
```

**3. Zimmet İadesi (Depo Sorumlusu)**
```
İşlem:
- Zimmet detay sayfasından
- İade miktarı girişi
- Açıklama ekleme

Sonuç:
- İade edilen miktar artar
- Kalan miktar azalır
- Stoka otomatik giriş
```

**4. Zimmet İptali (Depo Sorumlusu)**
```
İşlem:
- Tüm kalan ürünleri iade al
- Zimmet iptal et

Sonuç:
- Zimmet Durumu: İptal
- Tüm kalan ürünler stoka girer
- Zimmet kapatılır
```

**5. Zimmet Tamamlanması (Otomatik)**
```
Koşul:
- Tüm ürünler kullanıldı veya iade edildi
- Kalan miktar = 0

Sonuç:
- Zimmet Durumu: Tamamlandı
- Zimmet tarihi kaydedilir
```

### 3.2 Zimmet Algoritmaları

#### FIFO (First In First Out)

**Zimmet Kullanımında:**
```python
Senaryo:
Personelin 3 ayrı zimmet kaydı var:
- Zimmet 1: 100 adet (50 kullanılmış, 50 kalan)
- Zimmet 2: 200 adet (0 kullanılmış, 200 kalan)
- Zimmet 3: 150 adet (0 kullanılmış, 150 kalan)

80 adet kullanım yapılacak:
1. Zimmet 1'den 50 adet düşülür (tamamlandı)
2. Zimmet 2'den 30 adet düşülür
3. Toplam 80 adet

Sonuç:
- Zimmet 1: 100 kullanılmış, 0 kalan (Tamamlandı)
- Zimmet 2: 30 kullanılmış, 170 kalan
- Zimmet 3: 0 kullanılmış, 150 kalan
```

#### Zimmet Kontrolü

**Yeterlilik Kontrolü:**
```python
Kontrol:
1. Ürün ID'ye göre tüm aktif zimmetleri bul
2. Her zimmetteki kalan miktarı topla
3. Toplam kalan ≥ Kullanılacak miktar?
   - Evet: İşlem devam eder
   - Hayır: Hata mesajı gösterilir
```

**Zimmet Bilgilendirme:**
```
Kullanıcı Arayüzünde:
- Zimmetteki Miktar: Her ürün için gösterilir
- Renk Kodları:
  * Yeşil: Yeterli zimmet
  * Kırmızı: Yetersiz zimmet
- Tooltip: Detaylı zimmet bilgisi
```

### 3.3 Zimmet Raporlama

**Zimmet Özet Raporu:**
- Personel bazlı zimmet durumu
- Teslim edilen, kullanılan, kalan miktarlar
- Kullanım yüzdesi

**Zimmet Detay Raporu:**
- Ürün bazlı zimmet bilgileri
- Tüm zimmet hareketleri
- Tarih bazlı filtreleme

**Zimmet Geçmişi:**
- Personel bazlı tüm zimmet kayıtları
- Aktif, tamamlanmış, iptal edilmiş
- Detaylı zimmet analizi

---

## 4. MİNİBAR İŞLEMLERİ DETAYLARI

### 4.1 Minibar Veri Modeli

#### İşlem Başlık (MinibarIslem)
```
Alanlar:
- id: Benzersiz işlem no
- oda_id: Hangi oda
- personel_id: İşlemi yapan kat sorumlusu
- islem_tipi: ilk_dolum / kontrol / doldurma
- islem_tarihi: İşlem zamanı
- aciklama: Ek notlar
```

#### İşlem Detay (MinibarIslemDetay)
```
Alanlar:
- id: Benzersiz detay no
- islem_id: Hangi işleme ait
- urun_id: Hangi ürün
- baslangic_stok: İşlem öncesi stok
- bitis_stok: İşlem sonrası stok
- tuketim: Tüketilen miktar
- eklenen_miktar: Eklenen miktar
- zimmet_detay_id: Hangi zimmetten kullanıldı
```

### 4.2 İşlem Tipi Algoritmaları

#### İlk Dolum
```
Adımlar:
1. Oda seçimi (ilk dolum yapılmamış)
2. Ürün ve miktar seçimi
3. Zimmet kontrolü
4. MinibarIslem kaydı oluştur (islem_tipi: ilk_dolum)
5. Her ürün için MinibarIslemDetay oluştur:
   - baslangic_stok = 0
   - eklenen_miktar = Girilen miktar
   - bitis_stok = Eklenen miktar
   - tuketim = 0
6. Zimmetten düşüm yap (FIFO)
7. Başarı mesajı
```

#### Kontrol
```
Adımlar:
1. Oda seçimi (daha önce dolum yapılmış)
2. İşlem tipi: Kontrol
3. Son minibar durumu gösterilir
4. Kayıt OLUŞTURULMAZ (sadece görüntüleme)
5. Sistem logu kaydedilir
6. İşlem tamamlandı mesajı
```

#### Doldurma (Tekli)
```
Adımlar:
1. Oda seçimi
2. Son minibar durumu yüklenir (otomatik)
3. Her ürün için:
   a. Gerçek stok sayımı (manuel giriş)
   b. Eklenecek miktar (manuel giriş)
   c. Tüketim hesaplama:
      Tüketim = Kayıtlı Stok - Gerçek Stok
   d. Yeni stok hesaplama:
      Yeni Stok = Gerçek Stok + Eklenecek
4. Zimmet kontrolü (Eklenen miktar için)
5. MinibarIslem kaydı oluştur (islem_tipi: doldurma)
6. Diğer ürünleri kopyala (değişmeden)
7. Her değişen ürün için MinibarIslemDetay oluştur:
   - baslangic_stok = Gerçek Stok
   - eklenen_miktar = Eklenecek
   - bitis_stok = Yeni Stok
   - tuketim = Hesaplanan tüketim
8. Zimmetten düşüm yap (FIFO, sadece eklenen miktar)
9. Başarı mesajı
```

#### Doldurma (Toplu)
```
Adımlar:
1. Kat ve odalar seçimi (çoklu)
2. Ürün ve miktar seçimi (tek ürün, tek miktar)
3. Toplam zimmet kontrolü:
   Gerekli = Oda Sayısı × Miktar
4. Her oda için sırayla:
   a. Son minibar durumu al
   b. MinibarIslem kaydı oluştur
   c. Diğer ürünleri kopyala
   d. Seçilen ürün için detay oluştur:
      - baslangic_stok = Mevcut
      - eklenen_miktar = Miktar
      - bitis_stok = Mevcut + Miktar
      - tuketim = 0 (Toplu işlemde tüketim takibi yok)
   e. Zimmetten düşüm yap
   f. Hata varsa logla ve devam et
5. Sonuç raporu göster:
   - Başarılı odalar
   - Başarısız odalar ve hata mesajları
```

### 4.3 Minibar Mevcut Durum Hesaplama

#### Algoritma
```
Oda için son işlem:
1. MinibarIslem tablosunda oda_id ile son kaydı bul
2. Bu işleme ait tüm MinibarIslemDetay kayıtlarını al
3. Her detay için bitis_stok değerini al
4. Bu değerler = Mevcut minibar içeriği
```

#### API Endpoint
```
GET /api/minibar-icerigi/<oda_id>

Yanıt:
{
  "success": true,
  "urunler": [
    {
      "urun_id": 1,
      "urun_adi": "Coca Cola",
      "grup_adi": "İçecekler",
      "birim": "Şişe",
      "mevcut_stok": 5,
      "son_islem_tarihi": "31.10.2025 14:30"
    }
  ],
  "ilk_dolum": false,
  "son_islem_tipi": "doldurma"
}
```

### 4.4 Minibar Geçmiş

#### Görüntüleme
```
Erişim: Depo Sorumlusu → Minibar Durumları → Ürün Geçmişi

Bilgiler:
- Tüm işlemler kronolojik (Yeniden eskiye)
- Her işlem için:
  * İşlem tarihi ve saati
  * İşlem tipi (İlk Dolum/Kontrol/Doldurma)
  * Personel adı
  * Başlangıç stok
  * Eklenen miktar
  * Tüketim
  * Bitiş stok
  * Açıklama
```

#### API Endpoint
```
GET /minibar-urun-gecmis/<oda_id>/<urun_id>

Yanıt:
{
  "success": true,
  "oda": "101",
  "urun": "Coca Cola",
  "gecmis": [...]
}
```

---

**BÖLÜM 3 SONU**

**Sonraki Bölüm:** Teknik Dokümantasyon ve Akış Şemaları  
**Sayfa:** 4/4

---

*Bu dokümantasyon sürekli güncellenmektedir. Son güncelleme: 31 Ekim 2025*
