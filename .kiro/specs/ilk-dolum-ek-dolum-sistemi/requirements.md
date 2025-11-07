# İlk Dolum ve Ek Dolum Sistemi - Gereksinimler

## Genel Bakış
Minibar ürünleri için ilk dolum, yeniden dolum ve ek dolum işlemlerinin yönetimi.

## Temel Kurallar

### 1. İlk Dolum İşlemi
- **Ne Zaman**: Bir ürün minibar'a ilk kez eklendiğinde
- **Kısıtlama**: Her oda için her ürün sadece 1 kez ilk dolum yapılabilir
- **Tüketim Kaydı**: İlk dolum tüketim olarak kaydedilmez
- **Stok Hareketi**: Kat sorumlusunun zimmetinden düşer

**Örnek**:
```
Ürün: Efes Bira
İlk Dolum: 5 adet
Minibar Stok: 0 → 5
Tüketim: 0
Kat Sorumlusu Zimmet: -5
```

### 2. Yeniden Dolum İşlemi (Oda Kontrol)
- **Ne Zaman**: İlk dolum yapılmış ürünün kontrolü/doldurulması
- **Tüketim Hesaplama**: Son stok - Gerçek mevcut stok = Tüketim
- **Stok Güncelleme**: Gerçek mevcut + Eklenen = Yeni stok
- **Tüketim Kaydı**: Hesaplanan tüketim minibar tüketimine eklenir

**Örnek 1 - İlk Kontrol**:
```
Ürün: Efes Bira
Son Stok: 5 adet
Gerçek Mevcut: 3 adet (misafir 2 adet tüketti)
Tüketim: 5 - 3 = 2 adet ✅
Eklenen: 2 adet
Yeni Stok: 3 + 2 = 5 adet
Kat Sorumlusu Zimmet: -2
```

**Örnek 2 - İkinci Kontrol**:
```
Ürün: Efes Bira
Son Stok: 5 adet
Gerçek Mevcut: 4 adet (misafir 1 adet tüketti)
Tüketim: 5 - 4 = 1 adet ✅
Eklenen: 1 adet
Yeni Stok: 4 + 1 = 5 adet
Kat Sorumlusu Zimmet: -1
```

### 3. Ek Dolum İşlemi
- **Ne Zaman**: Misafir minibar'da daha fazla ürün istemesi
- **Kısıtlama**: Sadece ilk dolum yapılmış ürünlere uygulanır
- **Tüketim Kaydı**: Ek dolum tüketim olarak kaydedilmez ❌
- **Stok Güncelleme**: Mevcut stok + Ek dolum = Yeni stok
- **Onay Gerekli**: Kat sorumlusu onaylamalı

**Örnek**:
```
Ürün: Efes Bira
Minibar Mevcut: 5 adet
Misafir İsteği: 2 adet daha
Ek Dolum: 2 adet
Yeni Stok: 5 + 2 = 7 adet
Tüketim: 0 (ek dolum tüketim değil) ❌
Kat Sorumlusu Zimmet: -2
İşlem Tipi: "ek_dolum"
```

## İşlem Akışları

### İlk Dolum Akışı
1. Kat sorumlusu "İlk Dolum" sayfasına gider
2. QR veya manuel oda seçer
3. Ürün grubu ve ürün seçer
4. Miktar girer
5. Sistem kontrol eder:
   - Bu ürüne daha önce ilk dolum yapılmış mı?
   - Evet → Ek dolum önerisi göster
   - Hayır → İlk dolum işlemine devam et
6. Zimmet kontrolü yapılır
7. İşlem kaydedilir (islem_tipi: 'ilk_dolum')

### Ek Dolum Akışı
1. Kat sorumlusu "İlk Dolum" sayfasından ürün seçer
2. Sistem kontrol eder: Bu ürüne ilk dolum yapılmış mı?
3. Evet → Uyarı modal açılır:
   ```
   ⚠️ Bu ürüne daha önce ilk dolum yapılmıştır!
   
   Ek dolum yapmak ister misiniz?
   (Ek dolum tüketim olarak kaydedilmez)
   ```
4. Kat sorumlusu onaylarsa modal açılır:
   - Ürün bilgisi
   - Kat sorumlusu zimmet miktarı
   - Minibar'daki mevcut miktar
   - Ek dolum miktarı input
5. Kaydet → İşlem kaydedilir (islem_tipi: 'ek_dolum')

### Yeniden Dolum Akışı (Oda Kontrol)
1. Kat sorumlusu "Oda Kontrol" sayfasına gider
2. Oda seçer
3. Minibar içeriği listelenir
4. Ürün seçer → Modal açılır:
   - Son kayıtlı stok
   - Gerçek mevcut stok input (sayım)
   - Eklenecek miktar input
5. Sistem hesaplar:
   - Tüketim = Son stok - Gerçek mevcut
   - Yeni stok = Gerçek mevcut + Eklenen
6. Onay modal gösterir
7. Kaydet → İşlem kaydedilir (islem_tipi: 'doldurma')

## Veritabanı Değişiklikleri

### MinibarIslem Tablosu
```python
islem_tipi = Enum('ilk_dolum', 'kontrol', 'doldurma', 'ek_dolum')  # 'ek_dolum' eklendi
```

### MinibarIslemDetay Tablosu
Mevcut alanlar yeterli:
- baslangic_stok: İşlem öncesi stok
- bitis_stok: İşlem sonrası stok
- tuketim: Hesaplanan tüketim (ek_dolum'da 0)
- eklenen_miktar: Eklenen miktar

## API Endpoint'leri

### 1. İlk Dolum Kontrolü
```
GET /api/kat-sorumlusu/ilk-dolum-kontrol/<oda_id>/<urun_id>
Response: {
    "success": true,
    "ilk_dolum_yapilmis": true/false,
    "mevcut_stok": 5
}
```

### 2. Ek Dolum İşlemi
```
POST /api/kat-sorumlusu/ek-dolum
Body: {
    "oda_id": 1,
    "urun_id": 5,
    "ek_miktar": 2
}
Response: {
    "success": true,
    "message": "Ek dolum başarıyla kaydedildi",
    "yeni_stok": 7
}
```

### 3. İlk Dolum İşlemi (Güncellenmiş)
```
POST /api/kat-sorumlusu/ilk-dolum
Body: {
    "oda_id": 1,
    "urunler": [
        {"urun_id": 5, "miktar": 5}
    ]
}
```

## Audit Trail

Tüm işlemler audit_trail tablosuna kaydedilmeli:

```python
audit_create(
    tablo_adi='minibar_islemleri',
    kayit_id=minibar_islem.id,
    yeni_deger={
        'islem_tipi': 'ek_dolum',
        'oda_id': 1,
        'urun_id': 5,
        'miktar': 2,
        'personel_id': session['kullanici_id']
    },
    aciklama='Ek dolum işlemi - Misafir talebi'
)
```

## Raporlama

Admin panelinde görüntülenebilmeli:
- İlk dolum işlemleri
- Ek dolum işlemleri
- Yeniden dolum işlemleri
- Tüketim raporları (ek dolum hariç)

## Güvenlik

- Tüm işlemler @login_required ve @role_required ile korunmalı
- Zimmet kontrolü yapılmalı
- CSRF token kontrolü yapılmalı
- Rate limiting uygulanmalı
