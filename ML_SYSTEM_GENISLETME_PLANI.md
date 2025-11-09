# 🚀 ML ANOMALİ & ANALİZ SİSTEMİ GENİŞLETME PLANI

## 📊 MEVCUT DURUM (v1.0)

### İzlenen Metrikler
1. ✅ Stok Seviyeleri (ürün bazlı)
2. ✅ Tüketim Miktarları (oda bazlı)
3. ✅ Dolum Süreleri (personel bazlı)

### Özellikler
- Veri toplama (15 dakika)
- Anomali tespiti (Z-Score, Isolation Forest)
- Stok bitiş tahmini
- 4 seviyeli uyarı sistemi
- Dashboard ve raporlama

---

## 🎯 GENİŞLETME PLANI

### PHASE 2: Gelir ve Karlılık Analizi (Kısa Vade - 1 Hafta)

#### 2.1 Gelir Anomalileri
**Amaç**: Oda ve ürün bazlı gelir sapmaları tespit etmek

**Yeni Metrikler**:
```python
# models.py - Yeni enum değerleri
class MLMetricType(str, enum.Enum):
    # Mevcut
    STOK_SEVIYE = 'stok_seviye'
    TUKETIM_MIKTAR = 'tuketim_miktar'
    DOLUM_SURE = 'dolum_sure'
    STOK_BITIS_TAHMINI = 'stok_bitis_tahmini'
    
    # YENİ
    GELIR_ODA = 'gelir_oda'              # Oda bazlı minibar geliri
    GELIR_URUN = 'gelir_urun'            # Ürün bazlı gelir
    KARLILIK_ODA = 'karlilik_oda'        # Oda karlılığı
    ORTALAMA_SEPET = 'ortalama_sepet'    # Ortalama sepet değeri

class MLAlertType(str, enum.Enum):
    # Mevcut
    STOK_ANOMALI = 'stok_anomali'
    TUKETIM_ANOMALI = 'tuketim_anomali'
    DOLUM_GECIKME = 'dolum_gecikme'
    STOK_BITIS_UYARI = 'stok_bitis_uyari'
    
    # YENİ
    GELIR_ANOMALI = 'gelir_anomali'      # Anormal gelir düşüşü/artışı
    KARLILIK_DUSUK = 'karlilik_dusuk'    # Düşük karlılık uyarısı
```

**Veri Toplama**:
```python
# utils/ml/data_collector.py
def collect_revenue_metrics(self):
    """Gelir metriklerini topla"""
    # Oda bazlı son 24 saat geliri
    # Ürün bazlı satış geliri
    # Ortalama sepet değeri
```

**Anomali Tespiti**:
```python
# utils/ml/anomaly_detector.py
def detect_revenue_anomalies(self):
    """Gelir anomalilerini tespit et"""
    # %40+ gelir düşüşü → YÜKSEK alert
    # %60+ gelir artışı → ORTA alert (fiyat hatası?)
```

**Örnek Uyarılar**:
```
🔴 YÜKSEK: "Oda 305 geliri normalden %65 düşük"
   → Bu hafta: 150 TL, Ortalama: 450 TL
   → Önerilen Aksiyon: Fiyatlandırma ve tüketim kontrolü

🟡 ORTA: "Coca Cola geliri normalden %45 yüksek"
   → Bu hafta: 2.500 TL, Ortalama: 1.700 TL
   → Önerilen Aksiyon: Fiyat kontrolü, stok kontrolü
```

---

#### 2.2 Zimmet Analizi
**Amaç**: Personel zimmet kullanımı ve fire oranlarını izlemek

**Yeni Metrikler**:
```python
ZIMMET_KULLANIM = 'zimmet_kullanim'      # Zimmet kullanım oranı
ZIMMET_FIRE = 'zimmet_fire'              # Fire/kayıp oranı
ZIMMET_IADE = 'zimmet_iade'              # İade oranı
```

**Veri Toplama**:
```python
def collect_zimmet_metrics(self):
    """Zimmet metriklerini topla"""
    # Personel bazlı zimmet kullanım oranı
    # Fire oranı (zimmet - kullanılan - iade)
    # İade süresi
```

**Anomali Tespiti**:
```python
def detect_zimmet_anomalies(self):
    """Zimmet anomalilerini tespit et"""
    # %20+ fire oranı → YÜKSEK alert
    # %50+ kullanım oranı → ORTA alert (yüksek performans)
```

**Örnek Uyarılar**:
```
🔴 YÜKSEK: "Mehmet Yılmaz fire oranı %35"
   → Zimmet: 100 ürün, Kullanılan: 60, İade: 5, Fire: 35
   → Önerilen Aksiyon: Zimmet kontrolü, kayıp araştırması

🟢 DÜŞÜK: "Ayşe Demir fire oranı %2"
   → Zimmet: 100 ürün, Kullanılan: 95, İade: 3, Fire: 2
   → Önerilen Aksiyon: Örnek performans, ödüllendirme
```

---

#### 2.3 Oda Doluluk Korelasyonu
**Amaç**: Doluluk oranı ile tüketim ilişkisini analiz etmek

**Yeni Metrikler**:
```python
DOLULUK_ORAN = 'doluluk_oran'            # Otel doluluk oranı
DOLULUK_TUKETIM = 'doluluk_tuketim'      # Doluluk-tüketim korelasyonu
BOSTA_TUKETIM = 'bosta_tuketim'          # Boş odada tüketim (hırsızlık?)
```

**Veri Toplama**:
```python
def collect_occupancy_metrics(self):
    """Doluluk metriklerini topla"""
    # misafir_kayitlari tablosundan doluluk hesapla
    # Dolu oda vs tüketim korelasyonu
    # Boş oda ama tüketim var mı?
```

**Anomali Tespiti**:
```python
def detect_occupancy_anomalies(self):
    """Doluluk anomalilerini tespit et"""
    # Dolu oda ama sıfır tüketim → ORTA alert
    # Boş oda ama tüketim var → KRİTİK alert (hırsızlık!)
```

**Örnek Uyarılar**:
```
🔴 KRİTİK: "Oda 201 boş ama tüketim var!"
   → Durum: Boş, Tüketim: 15 ürün (son 24 saat)
   → Önerilen Aksiyon: ACİL güvenlik kontrolü, hırsızlık olabilir

🟡 ORTA: "Oda 405 dolu ama tüketim yok"
   → Durum: Dolu (3 gün), Tüketim: 0 ürün
   → Önerilen Aksiyon: Minibar kontrolü, misafir tercihi?
```

---

### PHASE 3: Gelişmiş Analiz (Orta Vade - 2 Hafta)

#### 3.1 Ürün Popülaritesi ve Trend Analizi
**Metrikler**:
- En çok/az tüketilen ürünler
- Trend analizi (artış/azalış)
- Sezonsal paternler
- Ürün kombinasyonları

**Örnek Uyarılar**:
```
🟠 YÜKSEK: "Coca Cola tüketimi %60 düştü"
   → Bu ay: 200 adet, Geçen ay: 500 adet
   → Önerilen Aksiyon: Rakip ürün analizi, fiyat kontrolü
```

---

#### 3.2 Müşteri Segmentasyonu
**Metrikler**:
- Oda tipi bazlı tüketim profilleri
- VIP vs standart oda karşılaştırması
- Misafir davranış analizi
- Tekrar eden misafir tüketimi

**Örnek Uyarılar**:
```
🔵 DÜŞÜK: "Suite odalar tüketimi %30 düşük"
   → Ortalama: 25 ürün/gün, Beklenen: 35 ürün/gün
   → Önerilen Aksiyon: Ürün çeşitliliği artırılabilir
```

---

#### 3.3 Tahminsel Bakım
**Metrikler**:
- Ekipman performans düşüşü
- Personel yorgunluk tahmini
- Stok sipariş optimizasyonu
- Talep tahmini

**Örnek Uyarılar**:
```
🟡 ORTA: "Ahmet Yılmaz performans düşüşü tahmini"
   → Son 7 gün trend: Yavaşlama
   → Önerilen Aksiyon: Dinlenme günü planla
```

---

### PHASE 4: Optimizasyon (Uzun Vade - 1 Ay)

#### 4.1 Fiyat Optimizasyonu
- Dinamik fiyatlandırma önerileri
- Talep-fiyat elastikiyeti
- Rakip analizi

#### 4.2 Tedarikçi Performansı
- Teslimat süreleri
- Kalite analizi
- Maliyet optimizasyonu

#### 4.3 Maliyet Analizi
- Ürün bazlı karlılık
- Stok tutma maliyeti
- Operasyonel verimlilik

---

## 📈 BEKLENEN FAYDALAR

### Phase 2 Sonrası
- ✅ Gelir kayıplarını %40 azaltma
- ✅ Fire oranını %50 düşürme
- ✅ Hırsızlık tespiti %90+ doğruluk
- ✅ Personel verimliliği %25 artış

### Phase 3 Sonrası
- ✅ Stok optimizasyonu %30 iyileşme
- ✅ Müşteri memnuniyeti artışı
- ✅ Tahminsel bakım ile kesinti %60 azalma

### Phase 4 Sonrası
- ✅ Toplam karlılık %35+ artış
- ✅ Operasyonel maliyet %25 düşüş
- ✅ Tam otomatik optimizasyon

---

## 🛠️ UYGULAMA ADIMLARI

### Phase 2 İçin (Şimdi Başlayabiliriz!)

1. **Models.py Güncelleme**
   ```bash
   # Yeni enum değerleri ekle
   - GELIR_ODA, GELIR_URUN, KARLILIK_ODA
   - ZIMMET_KULLANIM, ZIMMET_FIRE
   - DOLULUK_ORAN, BOSTA_TUKETIM
   ```

2. **DataCollector Genişletme**
   ```bash
   # Yeni collector fonksiyonları
   - collect_revenue_metrics()
   - collect_zimmet_metrics()
   - collect_occupancy_metrics()
   ```

3. **AnomalyDetector Genişletme**
   ```bash
   # Yeni detector fonksiyonları
   - detect_revenue_anomalies()
   - detect_zimmet_anomalies()
   - detect_occupancy_anomalies()
   ```

4. **Dashboard Güncelleme**
   ```bash
   # Yeni kartlar ve grafikler
   - Gelir trendi grafiği
   - Zimmet performans tablosu
   - Doluluk-tüketim korelasyon grafiği
   ```

5. **Test ve Deploy**
   ```bash
   python test_ml_system_v2.py
   ```

---

## 💡 ÖNERİLER

1. **Veri Kalitesi**: Fiyat bilgilerinin doğru girilmesi kritik
2. **Eğitim**: Personele yeni metrikler hakkında bilgilendirme
3. **Geri Bildirim**: İlk 2 hafta yoğun geri bildirim toplama
4. **Optimizasyon**: Threshold değerlerini gerçek veriye göre ayarlama

---

**Hazırlayan**: ML Sistem Ekibi  
**Tarih**: 9 Kasım 2025  
**Versiyon**: 2.0 Genişletme Planı
