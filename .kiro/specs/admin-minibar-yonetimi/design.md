# Design Document

## Overview

Admin paneline minibar stok yönetimi özellikleri eklenecektir. Bu özellik, admin kullanıcılarının tüm minibar stoklarını görüntülemesine, depo ve oda bazında raporlama yapmasına ve gerektiğinde tüm minibar stoklarını güvenli bir şekilde sıfırlamasına olanak tanır.

Sistem, mevcut Flask uygulamasına yeni route'lar, template'ler ve yardımcı fonksiyonlar ekleyerek genişletilecektir. Güvenlik için kritik işlemlerde admin şifre doğrulaması yapılacaktır.

## Architecture

### Katmanlı Mimari

```
┌─────────────────────────────────────┐
│     Presentation Layer              │
│  (Templates + JavaScript)           │
│  - depo_stoklari.html              │
│  - oda_minibar_stoklari.html       │
│  - minibar_sifirla.html            │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│     Application Layer               │
│  (Flask Routes + Decorators)        │
│  - @role_required('admin')         │
│  - CSRF Protection                  │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│     Business Logic Layer            │
│  (Helper Functions)                 │
│  - get_depo_stok_durumu()          │
│  - get_oda_minibar_stoklari()      │
│  - sifirla_minibar_stoklari()      │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│     Data Access Layer               │
│  (SQLAlchemy Models)                │
│  - Urun, StokHareket               │
│  - MinibarIslem, MinibarIslemDetay │
│  - AuditLog, SistemLog             │
└─────────────────────────────────────┘
```

### Güvenlik Katmanı

- **Authentication**: Session-based (mevcut sistem)
- **Authorization**: Role-based (@role_required decorator)
- **CSRF Protection**: Flask-WTF CSRFProtect (mevcut)
- **Password Verification**: Kritik işlemler için re-authentication
- **Audit Trail**: Tüm işlemler loglanır

## Components and Interfaces

### 1. Backend Components

#### 1.1 Flask Routes (app.py)

**Depo Stokları Route**
```python
@app.route('/admin/depo-stoklari')
@login_required
@role_required('sistem_yoneticisi', 'admin')
def admin_depo_stoklari():
    """
    Depo stok durumlarını gösterir
    Query Parameters:
    - grup_id: Ürün grubu filtresi (optional)
    - format: 'excel' ise Excel export yapar
    """
```

**Oda Minibar Stokları Route**
```python
@app.route('/admin/oda-minibar-stoklari')
@login_required
@role_required('sistem_yoneticisi', 'admin')
def admin_oda_minibar_stoklari():
    """
    Tüm odaların minibar stok durumlarını listeler
    Query Parameters:
    - kat_id: Kat filtresi (optional)
    """
```

**Oda Minibar Detay Route**
```python
@app.route('/admin/oda-minibar-detay/<int:oda_id>')
@login_required
@role_required('sistem_yoneticisi', 'admin')
def admin_oda_minibar_detay(oda_id):
    """
    Belirli bir odanın minibar detaylarını gösterir
    """
```

**Minibar Sıfırlama Route**
```python
@app.route('/admin/minibar-sifirla', methods=['GET', 'POST'])
@login_required
@role_required('sistem_yoneticisi', 'admin')
def admin_minibar_sifirla():
    """
    GET: Sıfırlama sayfasını gösterir
    POST: Admin şifresi doğrular ve sıfırlama yapar
    """
```

**Şifre Doğrulama API Route**
```python
@app.route('/api/admin/verify-password', methods=['POST'])
@login_required
@role_required('sistem_yoneticisi', 'admin')
def api_admin_verify_password():
    """
    AJAX ile admin şifresini doğrular
    Request Body: {"password": "admin_sifre"}
    Response: {"success": true/false, "message": "..."}
    """
```

#### 1.2 Helper Functions (utils/helpers.py)

**Depo Stok Durumu**
```python
def get_depo_stok_durumu(grup_id=None):
    """
    Depo stok durumlarını hesaplar
    
    Args:
        grup_id (int, optional): Ürün grubu filtresi
    
    Returns:
        list: [
            {
                'urun_id': int,
                'urun_adi': str,
                'grup_adi': str,
                'birim': str,
                'mevcut_stok': int,
                'kritik_stok': int,
                'durum': 'kritik'|'normal'
            },
            ...
        ]
    """
```

**Oda Minibar Stokları**
```python
def get_oda_minibar_stoklari(kat_id=None):
    """
    Tüm odaların minibar stok durumlarını getirir
    
    Args:
        kat_id (int, optional): Kat filtresi
    
    Returns:
        list: [
            {
                'oda_id': int,
                'oda_no': str,
                'kat_adi': str,
                'son_islem_tarihi': datetime,
                'toplam_urun_sayisi': int,
                'bos_mu': bool
            },
            ...
        ]
    """
```

**Oda Minibar Detay**
```python
def get_oda_minibar_detay(oda_id):
    """
    Belirli bir odanın minibar detaylarını getirir
    
    Args:
        oda_id (int): Oda ID
    
    Returns:
        dict: {
            'oda': Oda object,
            'son_islem': MinibarIslem object,
            'urunler': [
                {
                    'urun_adi': str,
                    'baslangic_stok': int,
                    'bitis_stok': int,
                    'tuketim': int,
                    'eklenen_miktar': int
                },
                ...
            ]
        }
    """
```

**Minibar Sıfırlama**
```python
def sifirla_minibar_stoklari(kullanici_id):
    """
    Tüm minibar stoklarını sıfırlar (ana depoya eklenmeden)
    
    Args:
        kullanici_id (int): İşlemi yapan kullanıcı ID
    
    Returns:
        dict: {
            'success': bool,
            'etkilenen_oda_sayisi': int,
            'toplam_sifirlanan_stok': int,
            'message': str
        }
    
    Process:
        1. Tüm MinibarIslemDetay kayıtlarını getir
        2. bitis_stok değerlerini 0 yap
        3. AuditLog'a kaydet
        4. SistemLog'a kaydet
        5. Transaction commit
    """
```

**Minibar Sıfırlama Özeti**
```python
def get_minibar_sifirlama_ozeti():
    """
    Sıfırlama öncesi özet bilgileri getirir
    
    Returns:
        dict: {
            'toplam_oda_sayisi': int,
            'dolu_oda_sayisi': int,
            'toplam_urun_adedi': int,
            'urun_dagilimi': [
                {'urun_adi': str, 'toplam': int},
                ...
            ]
        }
    """
```

#### 1.3 Excel Export Fonksiyonu

```python
def export_depo_stok_excel(stok_listesi):
    """
    Depo stok listesini Excel formatında export eder
    
    Args:
        stok_listesi (list): get_depo_stok_durumu() çıktısı
    
    Returns:
        BytesIO: Excel dosyası buffer
    
    Excel Yapısı:
        - Sheet: "Depo Stokları"
        - Columns: Ürün Adı, Grup, Birim, Mevcut Stok, Kritik Stok, Durum
        - Styling: Kritik stoklar kırmızı highlight
    """
```

### 2. Frontend Components

#### 2.1 Sidebar Menü Güncellemesi (base.html)

Mevcut sidebar'a yeni menü öğeleri eklenecek:

```html
<!-- Minibar Yönetimi -->
<div class="px-4 py-2 mt-4">
    <h3 class="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
        Minibar Yönetimi
    </h3>
</div>
<a href="{{ url_for('admin_depo_stoklari') }}"
   class="flex items-center px-4 py-2 text-slate-700 dark:text-slate-200 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700">
    <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <!-- Icon: Warehouse/Storage -->
    </svg>
    Depo Stokları
</a>
<a href="{{ url_for('admin_oda_minibar_stoklari') }}"
   class="flex items-center px-4 py-2 text-slate-700 dark:text-slate-200 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700">
    <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <!-- Icon: Room/Door -->
    </svg>
    Oda Minibar Stokları
</a>
<a href="{{ url_for('admin_minibar_sifirla') }}"
   class="flex items-center px-4 py-2 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20">
    <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <!-- Icon: Trash/Reset -->
    </svg>
    Minibarları Sıfırla
</a>
```

#### 2.2 Template: depo_stoklari.html

**Yapı:**
- Sayfa başlığı ve açıklama
- Filtre bölümü (Ürün grubu dropdown)
- Excel export butonu
- Stok tablosu (responsive)
- Kritik stok uyarıları

**Tablo Kolonları:**
1. Ürün Adı
2. Grup
3. Birim
4. Mevcut Stok
5. Kritik Stok Seviyesi
6. Durum (Badge: Kritik/Normal)

**JavaScript:**
- Tablo filtreleme
- Excel export trigger
- Responsive tablo scroll indicator

#### 2.3 Template: oda_minibar_stoklari.html

**Yapı:**
- Sayfa başlığı ve açıklama
- Filtre bölümü (Kat dropdown)
- İstatistik kartları (Toplam oda, Dolu oda, Boş oda)
- Oda listesi tablosu
- Boş odalar bölümü (collapsible)

**Tablo Kolonları:**
1. Oda No
2. Kat
3. Son İşlem Tarihi
4. Toplam Ürün
5. Durum (Badge: Dolu/Boş)
6. Aksiyon (Detay butonu)

**JavaScript:**
- Kat filtresi
- Boş odalar toggle
- Detay modal/sayfa açma

#### 2.4 Template: oda_minibar_detay.html

**Yapı:**
- Oda bilgileri (Oda no, Kat, Son işlem tarihi)
- Geri butonu
- Ürün detay tablosu

**Tablo Kolonları:**
1. Ürün Adı
2. Başlangıç Stok
3. Bitiş Stok
4. Tüketim
5. Eklenen Miktar

#### 2.5 Template: minibar_sifirla.html

**Yapı:**
- Uyarı mesajı (Tehlike badge)
- Sıfırlama özeti kartları
  - Toplam oda sayısı
  - Dolu oda sayısı
  - Toplam ürün adedi
- Ürün dağılımı tablosu
- Sıfırla butonu (Kırmızı, büyük)

**Modal: Şifre Doğrulama**
```html
<div id="password-modal" class="hidden">
    <div class="modal-overlay"></div>
    <div class="modal-content">
        <h3>Admin Şifresi Gerekli</h3>
        <p>Bu işlemi onaylamak için şifrenizi girin:</p>
        <input type="password" id="admin-password" />
        <div class="modal-actions">
            <button id="cancel-btn">İptal</button>
            <button id="confirm-btn">Onayla ve Sıfırla</button>
        </div>
        <div id="error-message" class="hidden"></div>
    </div>
</div>
```

**JavaScript:**
- Modal açma/kapama
- AJAX şifre doğrulama
- Sıfırlama işlemi
- Loading state
- Success/Error notification

## Data Models

Mevcut modeller kullanılacak, yeni model eklenmeyecek:

### Kullanılan Modeller

**Urun**
- id, urun_adi, grup_id, birim, kritik_stok_seviyesi

**UrunGrup**
- id, grup_adi

**StokHareket**
- id, urun_id, hareket_tipi, miktar, islem_tarihi

**Oda**
- id, oda_no, kat_id

**Kat**
- id, kat_adi, kat_no

**MinibarIslem**
- id, oda_id, personel_id, islem_tipi, islem_tarihi

**MinibarIslemDetay**
- id, islem_id, urun_id, baslangic_stok, bitis_stok, tuketim, eklenen_miktar

**AuditLog**
- id, kullanici_id, islem_tipi, tablo_adi, kayit_id, eski_deger, yeni_deger, islem_tarihi

**SistemLog**
- id, kullanici_id, islem_tipi, modul, islem_detay, islem_tarihi

### Veri İlişkileri

```
Urun ─┬─ StokHareket (1:N)
      └─ MinibarIslemDetay (1:N)

Oda ─── MinibarIslem (1:N)

MinibarIslem ─── MinibarIslemDetay (1:N)

Kullanici ─┬─ AuditLog (1:N)
           └─ SistemLog (1:N)
```

## Error Handling

### 1. Route Level Error Handling

```python
try:
    # İşlem kodu
    db.session.commit()
    flash('İşlem başarılı', 'success')
except OperationalError as e:
    db.session.rollback()
    flash('Veritabanı bağlantı hatası', 'danger')
    log_hata(e, modul='admin_minibar')
except Exception as e:
    db.session.rollback()
    flash('Beklenmeyen hata', 'danger')
    log_hata(e, modul='admin_minibar')
```

### 2. AJAX Error Handling

```javascript
fetch('/api/admin/verify-password', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({password: password})
})
.then(response => {
    if (!response.ok) throw new Error('Network error');
    return response.json();
})
.then(data => {
    if (data.success) {
        // Başarılı
    } else {
        // Hata mesajı göster
    }
})
.catch(error => {
    // Genel hata
});
```

### 3. Validation Errors

- **Boş şifre**: "Şifre alanı boş bırakılamaz"
- **Yanlış şifre**: "Şifre hatalı, lütfen tekrar deneyin"
- **Yetkisiz erişim**: 403 Forbidden + redirect
- **Geçersiz oda ID**: 404 Not Found

### 4. Transaction Rollback

Sıfırlama işlemi sırasında hata oluşursa:
1. db.session.rollback() çağrılır
2. Hata loglanır (HataLog tablosu)
3. Kullanıcıya hata mesajı gösterilir
4. Hiçbir veri değişmez (atomicity)

## Testing Strategy

### 1. Unit Tests

**Test: get_depo_stok_durumu()**
- Boş veritabanı durumu
- Tek ürün durumu
- Kritik stok kontrolü
- Grup filtresi

**Test: get_oda_minibar_stoklari()**
- Boş oda listesi
- Dolu/boş oda ayrımı
- Kat filtresi
- Son işlem tarihi sıralaması

**Test: sifirla_minibar_stoklari()**
- Başarılı sıfırlama
- Transaction rollback
- Audit log kaydı
- Etkilenen oda sayısı hesaplama

### 2. Integration Tests

**Test: Depo Stokları Sayfası**
- Sayfa yükleme (200 OK)
- Grup filtresi çalışması
- Excel export
- Kritik stok vurgulaması

**Test: Oda Minibar Stokları**
- Sayfa yükleme
- Kat filtresi
- Detay sayfasına geçiş
- Boş oda listesi

**Test: Minibar Sıfırlama**
- Sayfa yükleme
- Özet bilgileri doğruluğu
- Şifre doğrulama (doğru/yanlış)
- Sıfırlama işlemi
- Log kaydı

### 3. Security Tests

- **Authorization**: Admin olmayan kullanıcı erişimi
- **CSRF**: Token olmadan POST request
- **Password**: Brute force koruması (rate limiting)
- **SQL Injection**: Parametreli sorgular
- **XSS**: Template escaping

### 4. UI/UX Tests

- **Responsive**: Mobil, tablet, desktop görünüm
- **Dark Mode**: Tüm sayfalar dark mode uyumlu
- **Loading States**: Spinner/skeleton gösterimi
- **Error Messages**: Kullanıcı dostu mesajlar
- **Accessibility**: Keyboard navigation, ARIA labels

### 5. Performance Tests

- **Depo Stokları**: 1000+ ürün ile yükleme süresi
- **Oda Listesi**: 500+ oda ile yükleme süresi
- **Sıfırlama**: 10000+ detay kaydı ile işlem süresi
- **Excel Export**: Büyük veri seti export süresi

## Security Considerations

### 1. Authentication & Authorization

- Tüm route'lar `@login_required` decorator ile korunur
- Admin route'ları `@role_required('sistem_yoneticisi', 'admin')` ile kısıtlanır
- Session timeout: 30 dakika (mevcut ayar)

### 2. CSRF Protection

- Tüm POST/PUT/DELETE request'lerde CSRF token zorunlu
- Flask-WTF CSRFProtect kullanılır (mevcut)
- AJAX request'lerde X-CSRFToken header

### 3. Password Verification

- Kritik işlemler için re-authentication
- Werkzeug check_password_hash kullanılır
- Şifre plain text olarak loglanmaz

### 4. Audit Trail

- Tüm sıfırlama işlemleri AuditLog'a kaydedilir
- Başarısız şifre denemeleri loglanır
- IP adresi ve user agent kaydedilir

### 5. Input Validation

- Tüm kullanıcı girdileri sanitize edilir
- SQL Injection: Parametreli sorgular (SQLAlchemy ORM)
- XSS: Jinja2 auto-escaping (mevcut)

### 6. Rate Limiting

Sıfırlama işlemi için rate limit:
- 5 deneme / 15 dakika
- IP bazlı kısıtlama
- Başarısız denemeler loglanır

## UI/UX Design

### 1. Renk Paleti

**Durum Renkleri:**
- Kritik Stok: `bg-red-100 text-red-800` (Light), `bg-red-900/20 text-red-400` (Dark)
- Normal Stok: `bg-green-100 text-green-800` (Light), `bg-green-900/20 text-green-400` (Dark)
- Boş Oda: `bg-slate-100 text-slate-600` (Light), `bg-slate-800 text-slate-400` (Dark)
- Dolu Oda: `bg-blue-100 text-blue-800` (Light), `bg-blue-900/20 text-blue-400` (Dark)

**Aksiyon Renkleri:**
- Sıfırla Butonu: `bg-red-600 hover:bg-red-700 text-white`
- Excel Export: `bg-green-600 hover:bg-green-700 text-white`
- Detay Butonu: `bg-blue-600 hover:bg-blue-700 text-white`

### 2. İkonlar (Heroicons)

- Depo: `<path d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"/>`
- Oda: `<path d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"/>`
- Sıfırla: `<path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>`
- Uyarı: `<path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>`

### 3. Responsive Breakpoints

- Mobile: < 640px (sm)
- Tablet: 640px - 1024px (md, lg)
- Desktop: > 1024px (xl)

**Tablo Davranışı:**
- Mobile: Horizontal scroll + scroll indicator
- Tablet/Desktop: Full width, no scroll

### 4. Loading States

**Skeleton Loader:**
```html
<div class="animate-pulse">
    <div class="h-4 bg-slate-200 rounded w-3/4 mb-2"></div>
    <div class="h-4 bg-slate-200 rounded w-1/2"></div>
</div>
```

**Spinner:**
```html
<svg class="animate-spin h-5 w-5 text-white" viewBox="0 0 24 24">
    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
</svg>
```

### 5. Notifications

**Toast Notification (Mevcut sistem kullanılacak):**
- Success: Yeşil arka plan, check icon
- Error: Kırmızı arka plan, X icon
- Warning: Sarı arka plan, exclamation icon
- Auto-dismiss: 5 saniye

## Implementation Notes

### 1. Kod Organizasyonu

**Yeni Dosyalar:**
- `templates/sistem_yoneticisi/depo_stoklari.html`
- `templates/sistem_yoneticisi/oda_minibar_stoklari.html`
- `templates/sistem_yoneticisi/oda_minibar_detay.html`
- `templates/sistem_yoneticisi/minibar_sifirla.html`

**Güncellenecek Dosyalar:**
- `app.py`: Yeni route'lar eklenecek
- `utils/helpers.py`: Yeni helper fonksiyonlar eklenecek
- `templates/base.html`: Sidebar menü güncellenecek

### 2. Veritabanı İşlemleri

**Performans Optimizasyonu:**
- Eager loading: `joinedload()` kullanımı
- Index'ler: Mevcut index'ler yeterli
- Pagination: Büyük listeler için sayfalama (optional)

**Query Örnekleri:**
```python
# Depo stok hesaplama
giris = db.session.query(func.sum(StokHareket.miktar)).filter(
    StokHareket.urun_id == urun_id,
    StokHareket.hareket_tipi == 'giris'
).scalar() or 0

cikis = db.session.query(func.sum(StokHareket.miktar)).filter(
    StokHareket.urun_id == urun_id,
    StokHareket.hareket_tipi == 'cikis'
).scalar() or 0

mevcut_stok = giris - cikis
```

### 3. Excel Export

**Kütüphane:** openpyxl (mevcut)

**Stil Özellikleri:**
- Header: Bold, mavi arka plan
- Kritik stok: Kırmızı arka plan
- Freeze panes: İlk satır sabit
- Auto-width: Kolon genişlikleri otomatik

### 4. JavaScript Best Practices

- Vanilla JS kullanımı (jQuery yok)
- Event delegation
- Debounce/throttle (filtreleme için)
- Error boundary
- Progressive enhancement

### 5. Accessibility

- ARIA labels: Tüm interaktif elementler
- Keyboard navigation: Tab order
- Focus indicators: Visible focus states
- Screen reader: Semantic HTML
- Color contrast: WCAG AA uyumlu

## Deployment Considerations

### 1. Veritabanı Migration

Yeni tablo/kolon eklenmediği için migration gerekmez.

### 2. Backward Compatibility

Mevcut özellikler etkilenmez, sadece yeni özellikler eklenir.

### 3. Rollback Plan

Hata durumunda:
1. Yeni route'ları devre dışı bırak (comment out)
2. Sidebar menüsünü eski haline döndür
3. Template dosyalarını sil

### 4. Monitoring

- Sıfırlama işlemi süresi (performance)
- Başarısız şifre denemeleri (security)
- Excel export hataları (error rate)
- Sayfa yükleme süreleri (UX)

### 5. Documentation

- README güncelleme: Yeni özellikler
- API documentation: Yeni endpoint'ler
- User guide: Admin kullanım kılavuzu
- Changelog: Versiyon notları
