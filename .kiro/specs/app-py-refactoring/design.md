# Design Document

## Overview

Bu tasarım, 6746 satırlık monolitik app.py dosyasının modüler bir yapıya dönüştürülmesini ve kullanılmayan kodların temizlenmesini hedeflemektedir. Mevcut routes dizinindeki yapı korunarak, yeni Blueprint modülleri eklenecek ve tüm endpoint'ler mantıksal gruplara ayrılacaktır.

## Architecture

### Mevcut Durum

```
project/
├── app.py (6746 satır - MONOLİTİK)
├── routes/
│   ├── admin_qr_routes.py (register_admin_qr_routes fonksiyonu)
│   ├── dolum_talebi_routes.py (register_dolum_talebi_routes fonksiyonu)
│   ├── kat_sorumlusu_ilk_dolum_routes.py (register_kat_sorumlusu_ilk_dolum_routes fonksiyonu)
│   ├── kat_sorumlusu_qr_routes.py
│   └── misafir_qr_routes.py
├── templates/
└── static/
```

### Hedef Durum

```
project/
├── app.py (200-300 satır - SADECE BOOTSTRAP)
├── routes/
│   ├── __init__.py (Tüm Blueprint'leri register eden merkezi modül)
│   ├── auth_routes.py (Login, Logout, Setup)
│   ├── dashboard_routes.py (Tüm dashboard'lar)
│   ├── sistem_yoneticisi_routes.py (Otel, Kat, Oda yönetimi)
│   ├── admin_routes.py (Personel, Ürün, Grup yönetimi)
│   ├── admin_minibar_routes.py (Admin minibar işlemleri)
│   ├── admin_stok_routes.py (Admin stok işlemleri)
│   ├── admin_zimmet_routes.py (Admin zimmet işlemleri)
│   ├── admin_qr_routes.py (Mevcut - QR yönetimi)
│   ├── depo_routes.py (Depo sorumlusu işlemleri)
│   ├── kat_sorumlusu_routes.py (Kat sorumlusu işlemleri)
│   ├── kat_sorumlusu_ilk_dolum_routes.py (Mevcut - İlk dolum)
│   ├── kat_sorumlusu_qr_routes.py (Mevcut)
│   ├── dolum_talebi_routes.py (Mevcut - Dolum talepleri)
│   ├── misafir_qr_routes.py (Mevcut)
│   └── api_routes.py (Tüm API endpoint'leri)
├── templates/
└── static/
```

## Components and Interfaces

### 1. Blueprint Registration Pattern

Mevcut routes dizinindeki dosyalar `register_*_routes(app)` pattern'ini kullanıyor. Bu pattern'i koruyarak yeni modüller ekleyeceğiz.

```python
# routes/__init__.py
def register_all_routes(app):
    """Tüm route modüllerini register et"""
    from routes.auth_routes import register_auth_routes
    from routes.dashboard_routes import register_dashboard_routes
    from routes.sistem_yoneticisi_routes import register_sistem_yoneticisi_routes
    # ... diğer import'lar
    
    # Register işlemleri
    register_auth_routes(app)
    register_dashboard_routes(app)
    register_sistem_yoneticisi_routes(app)
    # ... diğer register'lar
```

### 2. Route Modül Yapısı

Her route modülü aşağıdaki yapıyı takip edecek:

```python
"""
[Modül Açıklaması]
"""

from flask import render_template, request, redirect, url_for, flash, session, jsonify
from models import db, [Gerekli Modeller]
from utils.decorators import login_required, role_required
from utils.helpers import log_islem, log_hata, [Diğer helper'lar]
from utils.audit import audit_create, audit_update, audit_delete, serialize_model

def register_[modul_adi]_routes(app):
    """[Modül] route'larını kaydet"""
    
    @app.route('/endpoint-path', methods=['GET', 'POST'])
    @login_required
    @role_required('rol1', 'rol2')
    def endpoint_fonksiyonu():
        """Endpoint açıklaması"""
        try:
            # İşlem mantığı
            pass
        except Exception as e:
            log_hata(e, modul='modul_adi')
            flash('Hata mesajı', 'danger')
            return redirect(url_for('fallback'))
```

### 3. Ana app.py Yapısı

Refactoring sonrası app.py sadece bootstrap kodunu içerecek:

```python
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Flask uygulaması oluştur
app = Flask(__name__)

# Konfigürasyonu yükle
app.config.from_object('config.Config')

# CSRF Koruması
csrf = CSRFProtect(app)

# Veritabanı başlat
from models import db
db.init_app(app)

# Context processors
from utils.helpers import get_current_user

@app.context_processor
def inject_user():
    return dict(current_user=get_current_user())

@app.context_processor
def inject_builtins():
    return dict(min=min, max=max)

# Error handlers
from routes.error_handlers import register_error_handlers
register_error_handlers(app)

# Tüm route'ları register et
from routes import register_all_routes
register_all_routes(app)

if __name__ == '__main__':
    app.run()
```

## Data Models

Mevcut model yapısı korunacak, değişiklik yapılmayacak.

## Error Handling

### Error Handler Modülü

```python
# routes/error_handlers.py
def register_error_handlers(app):
    """Error handler'ları register et"""
    
    @app.errorhandler(429)
    def ratelimit_handler(e):
        """Rate limit hatası"""
        return render_template('errors/429.html', error=e), 429
    
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        """CSRF hatası"""
        log_hata(e, modul='csrf')
        flash('Form doğrulaması başarısız oldu (CSRF).', 'danger')
        return redirect(request.referrer or url_for('index'))
```

## Testing Strategy

### 1. Kod Analizi ve Envanter

**Araç:** Python script ile otomatik analiz

```python
# scripts/analyze_routes.py
import re
import os
from pathlib import Path

def analyze_app_routes():
    """app.py'deki tüm route'ları analiz et"""
    routes = []
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
        # @app.route pattern'ini bul
        pattern = r"@app\.route\(['\"]([^'\"]+)['\"](?:,\s*methods=\[([^\]]+)\])?\)"
        matches = re.finditer(pattern, content)
        for match in matches:
            routes.append({
                'path': match.group(1),
                'methods': match.group(2) if match.group(2) else 'GET'
            })
    return routes

def analyze_template_usage():
    """Template'lerde kullanılan url_for çağrılarını analiz et"""
    used_endpoints = set()
    template_dir = Path('templates')
    for template_file in template_dir.rglob('*.html'):
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # url_for pattern'ini bul
            pattern = r"url_for\(['\"]([^'\"]+)['\"]"
            matches = re.finditer(pattern, content)
            for match in matches:
                used_endpoints.add(match.group(1))
    return used_endpoints

def find_unused_routes():
    """Kullanılmayan route'ları bul"""
    all_routes = analyze_app_routes()
    used_endpoints = analyze_template_usage()
    
    # Route fonksiyon isimlerini çıkar
    unused = []
    for route in all_routes:
        # Fonksiyon ismini bul (route path'inden tahmin et)
        if route['path'] not in used_endpoints:
            unused.append(route)
    
    return unused
```

### 2. Yedekleme Stratejisi

```python
# scripts/backup_app.py
import shutil
from datetime import datetime

def backup_app_py():
    """app.py'nin yedeğini al"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f'app_backup_{timestamp}.py'
    shutil.copy2('app.py', backup_name)
    print(f'✅ Yedek oluşturuldu: {backup_name}')
    return backup_name
```

### 3. Kademeli Test Stratejisi

Her aşamada:
1. Yedek al
2. Değişikliği yap
3. Flask uygulamasını başlat
4. Import hatalarını kontrol et
5. Endpoint'lerin erişilebilir olduğunu doğrula
6. Manuel test yap
7. Commit yap

## Refactoring Aşamaları

### Aşama 1: Hazırlık ve Analiz
- app.py yedeğini al
- Tüm endpoint'leri listele
- Template'lerde kullanılan endpoint'leri tespit et
- Kullanılmayan endpoint'leri belirle
- Analiz raporunu oluştur

### Aşama 2: Error Handlers
- `routes/error_handlers.py` oluştur
- Error handler'ları taşı
- app.py'de register et
- Test et

### Aşama 3: Auth Routes
- `routes/auth_routes.py` oluştur
- Login, logout, setup endpoint'lerini taşı
- Test et

### Aşama 4: Dashboard Routes
- `routes/dashboard_routes.py` oluştur
- Tüm dashboard endpoint'lerini taşı
- Test et

### Aşama 5: Sistem Yöneticisi Routes
- `routes/sistem_yoneticisi_routes.py` oluştur
- Otel, Kat, Oda yönetim endpoint'lerini taşı
- Test et

### Aşama 6: Admin Routes (Temel)
- `routes/admin_routes.py` oluştur
- Personel, Ürün Grup, Ürün yönetim endpoint'lerini taşı
- Test et

### Aşama 7: Admin Minibar Routes
- `routes/admin_minibar_routes.py` oluştur
- Admin minibar işlem endpoint'lerini taşı
- Test et

### Aşama 8: Admin Stok Routes
- `routes/admin_stok_routes.py` oluştur
- Admin stok işlem endpoint'lerini taşı
- Test et

### Aşama 9: Admin Zimmet Routes
- `routes/admin_zimmet_routes.py` oluştur
- Admin zimmet işlem endpoint'lerini taşı
- Test et

### Aşama 10: Depo Routes
- `routes/depo_routes.py` oluştur
- Depo sorumlusu endpoint'lerini taşı
- Test et

### Aşama 11: Kat Sorumlusu Routes
- `routes/kat_sorumlusu_routes.py` oluştur
- Kat sorumlusu endpoint'lerini taşı (ilk dolum hariç - zaten ayrı modülde)
- Test et

### Aşama 12: API Routes
- `routes/api_routes.py` oluştur
- Kalan API endpoint'lerini taşı
- Test et

### Aşama 13: Merkezi Register
- `routes/__init__.py` oluştur
- `register_all_routes()` fonksiyonunu implement et
- app.py'yi temizle ve sadece bootstrap kodunu bırak
- Test et

### Aşama 14: Kullanılmayan Kod Temizliği
- Kullanılmayan endpoint'leri sil
- Kullanılmayan import'ları temizle
- Test et

### Aşama 15: Dokümantasyon
- Her modülün sorumluluklarını dokümante et
- Taşınan endpoint listesini oluştur
- Silinen kod listesini oluştur
- README güncelle

## Endpoint Gruplandırması

### Auth Routes (routes/auth_routes.py)
- `/` - index (yönlendirme)
- `/setup` - İlk kurulum
- `/login` - Giriş
- `/logout` - Çıkış

### Dashboard Routes (routes/dashboard_routes.py)
- `/dashboard` - Rol bazlı yönlendirme
- `/sistem-yoneticisi` - Sistem yöneticisi dashboard
- `/depo` - Depo sorumlusu dashboard
- `/kat-sorumlusu` - Kat sorumlusu dashboard
- `/kat-sorumlusu/dashboard` - Kat sorumlusu dashboard (alternatif)

### Sistem Yöneticisi Routes (routes/sistem_yoneticisi_routes.py)
- `/otel-tanimla` - Otel tanımlama
- `/kat-tanimla` - Kat tanımlama
- `/kat-duzenle/<int:kat_id>` - Kat düzenleme
- `/kat-sil/<int:kat_id>` - Kat silme
- `/oda-tanimla` - Oda tanımlama
- `/oda-duzenle/<int:oda_id>` - Oda düzenleme
- `/oda-sil/<int:oda_id>` - Oda silme
- `/sistem-loglari` - Sistem logları

### Admin Routes (routes/admin_routes.py)
- `/personel-tanimla` - Personel tanımlama
- `/personel-duzenle/<int:personel_id>` - Personel düzenleme
- `/personel-pasif-yap/<int:personel_id>` - Personel pasif yapma
- `/personel-aktif-yap/<int:personel_id>` - Personel aktif yapma
- `/urun-gruplari` - Ürün grupları
- `/grup-duzenle/<int:grup_id>` - Grup düzenleme
- `/grup-sil/<int:grup_id>` - Grup silme
- `/grup-pasif-yap/<int:grup_id>` - Grup pasif yapma
- `/grup-aktif-yap/<int:grup_id>` - Grup aktif yapma
- `/urunler` - Ürünler
- `/urun-duzenle/<int:urun_id>` - Ürün düzenleme
- `/urun-sil/<int:urun_id>` - Ürün silme
- `/urun-pasif-yap/<int:urun_id>` - Ürün pasif yapma
- `/urun-aktif-yap/<int:urun_id>` - Ürün aktif yapma

### Admin Minibar Routes (routes/admin_minibar_routes.py)
- `/admin/depo-stoklari` - Depo stokları
- `/admin/oda-minibar-stoklari` - Oda minibar stokları
- `/admin/oda-minibar-detay/<int:oda_id>` - Oda minibar detay
- `/admin/minibar-sifirla` - Minibar sıfırlama
- `/admin/minibar-islemleri` - Minibar işlemleri
- `/admin/minibar-islem-sil/<int:islem_id>` - Minibar işlem silme
- `/admin/minibar-durumlari` - Minibar durumları
- `/api/minibar-islem-detay/<int:islem_id>` - Minibar işlem detay API
- `/api/admin/verify-password` - Şifre doğrulama API

### Admin Stok Routes (routes/admin_stok_routes.py)
- `/admin/stok-giris` - Admin stok girişi
- `/admin/stok-hareketleri` - Stok hareketleri
- `/admin/stok-hareket-duzenle/<int:hareket_id>` - Stok hareket düzenleme
- `/admin/stok-hareket-sil/<int:hareket_id>` - Stok hareket silme

### Admin Zimmet Routes (routes/admin_zimmet_routes.py)
- `/admin/personel-zimmetleri` - Personel zimmetleri
- `/admin/zimmet-detay/<int:zimmet_id>` - Zimmet detay
- `/admin/zimmet-iade/<int:zimmet_id>` - Zimmet iade
- `/admin/zimmet-iptal/<int:zimmet_id>` - Zimmet iptal

### Depo Routes (routes/depo_routes.py)
- `/stok-giris` - Stok girişi
- `/stok-duzenle/<int:hareket_id>` - Stok düzenleme
- (Diğer depo endpoint'leri - app.py'den tespit edilecek)

### Admin QR Routes (routes/admin_qr_routes.py) - MEVCUT
- `/admin/oda-qr-olustur/<int:oda_id>` - QR oluştur
- `/admin/toplu-qr-olustur` - Toplu QR oluştur
- `/admin/oda-qr-goruntule/<int:oda_id>` - QR görüntüle
- `/admin/oda-qr-indir/<int:oda_id>` - QR indir
- `/admin/toplu-qr-indir` - Toplu QR indir
- `/admin/oda-misafir-mesaji/<int:oda_id>` - Misafir mesajı

### Kat Sorumlusu İlk Dolum Routes (routes/kat_sorumlusu_ilk_dolum_routes.py) - MEVCUT
- `/api/kat-sorumlusu/ilk-dolum-kontrol/<int:oda_id>/<int:urun_id>` - İlk dolum kontrol
- `/api/kat-sorumlusu/ek-dolum` - Ek dolum
- `/api/kat-sorumlusu/ilk-dolum` - İlk dolum

### Dolum Talebi Routes (routes/dolum_talebi_routes.py) - MEVCUT
- `/api/dolum-talepleri` - Dolum talepleri listesi
- `/api/dolum-talebi-tamamla/<int:talep_id>` - Talep tamamla
- `/api/dolum-talebi-iptal/<int:talep_id>` - Talep iptal
- `/api/dolum-talepleri-admin` - Admin dolum talepleri
- `/api/dolum-talepleri-istatistik` - Dolum talepleri istatistik

### Kat Sorumlusu QR Routes (routes/kat_sorumlusu_qr_routes.py) - MEVCUT
(İçeriği kontrol edilecek)

### Misafir QR Routes (routes/misafir_qr_routes.py) - MEVCUT
(İçeriği kontrol edilecek)

## Migration Strategy

### Güvenli Geçiş Adımları

1. **Yedekleme**: Her aşamada app.py yedeği al
2. **Kademeli Taşıma**: Bir modül taşı, test et, commit yap
3. **Paralel Çalışma**: Taşınan kod app.py'den hemen silinmeyecek
4. **Doğrulama**: Her aşamada Flask uygulaması başlatılıp test edilecek
5. **Geri Alma**: Sorun çıkarsa yedekten geri dön

### Rollback Planı

```bash
# Sorun çıkarsa en son yedeğe dön
cp app_backup_YYYYMMDD_HHMMSS.py app.py

# Veya git ile geri al
git checkout HEAD -- app.py
```

## Performance Considerations

- Blueprint kullanımı performansı etkilemez
- Import süreleri minimal artış gösterebilir
- Lazy loading gerekirse uygulanabilir
- Modüler yapı cache stratejilerini kolaylaştırır

## Security Considerations

- Tüm decorator'lar (@login_required, @role_required) korunacak
- CSRF koruması devam edecek
- Audit trail sistemi korunacak
- Log sistemi korunacak

## Maintenance and Extensibility

### Yeni Endpoint Ekleme

```python
# İlgili routes modülüne ekle
@app.route('/yeni-endpoint')
@login_required
@role_required('rol')
def yeni_endpoint():
    """Yeni endpoint"""
    pass
```

### Yeni Modül Ekleme

1. `routes/yeni_modul_routes.py` oluştur
2. `register_yeni_modul_routes(app)` fonksiyonu ekle
3. `routes/__init__.py`'de import ve register et

## Documentation

Her modül şu dokümantasyonu içerecek:

```python
"""
[Modül Adı] Route'ları

Bu modül [açıklama] ile ilgili endpoint'leri içerir.

Endpoint'ler:
- /endpoint1 - Açıklama
- /endpoint2 - Açıklama

Roller:
- sistem_yoneticisi
- admin
- depo_sorumlusu
- kat_sorumlusu
"""
```

## Success Criteria

1. ✅ app.py 300 satırın altına indirildi
2. ✅ Tüm endpoint'ler çalışıyor
3. ✅ Import hataları yok
4. ✅ Test coverage korundu
5. ✅ Performans düşüşü yok
6. ✅ Dokümantasyon tamamlandı
7. ✅ Kullanılmayan kod temizlendi
8. ✅ Git commit geçmişi temiz
