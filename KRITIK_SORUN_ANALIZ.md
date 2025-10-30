# 🔥 KRİTİK SORUN TESPİTİ - MİNİBAR STOK HESAPLAMA
## Tarih: 30 Ekim 2025

---

## ❌ ASIL SORUN

### Senaryonuz:
```
1. İlk Dolum: 2 adet
2. (Müşteri 1 adet tüketti - simülasyon)
3. Doldurma: 1 adet ekle
4. Görünen: 3 adet ❌ YANLIŞ!
5. Olması Gereken: 2 adet ✅
```

### Neden Yanlış Çalışıyor?

**PROBLEM 1:** `bitis_stok` yanlış hesaplanıyor
```python
# api_minibar_doldur - Satır 2047
baslangic_stok = son_detay.bitis_stok  # ❌ 2 (son işlemin bitişi)

# Satır 2109
bitis_stok = baslangic_stok + miktar  # 2 + 1 = 3 ❌ YANLIŞ!
```

**PROBLEM 2:** Gerçek mevcut stok hesaplanmıyor

Doldurma işlemi yaparken:
- `baslangic_stok` = son işlemin `bitis_stok` alınıyor
- AMA eğer arada tüketim olduysa, bu yanlış!

**DOĞRU MANTIK:**
```
İlk Dolum: 2 adet → bitis_stok = 2
Müşteri tüketti: 1 adet → GERÇEK MEVCUT = 2 - 1 = 1 adet
Doldurma: 1 adet ekle
→ baslangic_stok = 1 (gerçek mevcut)
→ bitis_stok = 1 + 1 = 2 ✅ DOĞRU
```

---

## 🎯 ÇÖZÜM STRATEJİSİ

### Strateji 1: Her Doldurma Öncesi Gerçek Stok Hesapla

```python
# MEVCUT GERÇEK STOK HESAPLAMA:
# İlk dolumdan beri:
# gerçek_stok = toplam_eklenen - toplam_tuketilen

# Toplam eklenen = ilk_dolum + tüm_doldurma_işlemleri
# Toplam tüketilen = ???
```

**SORUN:** Tüketimi nasıl bilelim?

### Strateji 2: Kontrol İşlemi Zorunlu Yapma ❌

Klavuzda kontrol işlemi sadece görüntüleme için. Bu değiştirilemez.

### Strateji 3: Gerçek Envanter Takibi ✅ ÖNERİLEN

**YENİ YAKLAŞIM:**

Doldurma işleminde kullanıcıdan **MEVCUT STOK** bilgisi alınmalı!

```
Modal Açıldığında:
1. "Minibar'da şu an kaç adet var?"
2. Kullanıcı girer: 1 adet (gerçek sayım)
3. "Kaç adet eklemek istiyorsunuz?"
4. Kullanıcı girer: 1 adet

Hesaplama:
- baslangic_stok = 1 (gerçek sayım)
- eklenen = 1
- bitis_stok = 1 + 1 = 2
- tuketim = son_bitis_stok - baslangic_stok = 2 - 1 = 1
```

---

## 🛠️ DÜZELTMEalter

### Frontend Değişikliği Gerekli!