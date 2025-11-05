# Implementation Plan

- [x] 1. Helper fonksiyonları oluştur


  - `utils/helpers.py` dosyasına yeni fonksiyonlar ekle
  - Depo stok durumu hesaplama fonksiyonu yaz
  - Oda minibar stokları listeleme fonksiyonu yaz
  - Oda minibar detay fonksiyonu yaz
  - Minibar sıfırlama fonksiyonu yaz
  - Minibar sıfırlama özeti fonksiyonu yaz
  - Excel export fonksiyonu yaz
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4, 5.1, 5.2, 6.4_

- [x] 2. Backend route'ları ekle


  - `app.py` dosyasına yeni route'lar ekle
  - Depo stokları route'u oluştur (GET)
  - Oda minibar stokları route'u oluştur (GET)
  - Oda minibar detay route'u oluştur (GET)
  - Minibar sıfırlama route'u oluştur (GET, POST)
  - Şifre doğrulama API route'u oluştur (POST)
  - Tüm route'lara @login_required ve @role_required decorator'ları ekle
  - CSRF protection kontrolü yap
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4, 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 3. Sidebar menüsünü güncelle


  - `templates/base.html` dosyasını düzenle
  - "Minibar Yönetimi" ana menü başlığı ekle
  - "Depo Stokları" menü öğesi ekle
  - "Oda Minibar Stokları" menü öğesi ekle
  - "Minibarları Sıfırla" menü öğesi ekle (kırmızı renk)
  - İkonları ekle (Heroicons)
  - Dark mode uyumluluğunu kontrol et
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 4. Depo stokları sayfasını oluştur


  - `templates/sistem_yoneticisi/depo_stoklari.html` dosyası oluştur
  - Sayfa başlığı ve açıklama ekle
  - Ürün grubu filtre dropdown'u ekle
  - Excel export butonu ekle
  - Responsive stok tablosu oluştur
  - Kritik stok vurgulama (kırmızı badge) ekle
  - JavaScript filtreleme fonksiyonu yaz
  - Excel export trigger JavaScript'i yaz
  - Dark mode stilleri ekle
  - Mobile scroll indicator ekle
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [x] 5. Oda minibar stokları sayfasını oluştur


  - `templates/sistem_yoneticisi/oda_minibar_stoklari.html` dosyası oluştur
  - Sayfa başlığı ve açıklama ekle
  - İstatistik kartları ekle (Toplam oda, Dolu oda, Boş oda)
  - Kat filtre dropdown'u ekle
  - Oda listesi tablosu oluştur
  - Boş odalar collapsible bölümü ekle
  - Detay butonu ekle
  - JavaScript kat filtresi yaz
  - JavaScript boş odalar toggle yaz
  - Dark mode stilleri ekle
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [x] 6. Oda minibar detay sayfasını oluştur


  - `templates/sistem_yoneticisi/oda_minibar_detay.html` dosyası oluştur
  - Oda bilgileri kartı ekle (Oda no, Kat, Son işlem tarihi)
  - Geri butonu ekle
  - Ürün detay tablosu oluştur
  - Responsive tablo yapısı ekle
  - Dark mode stilleri ekle
  - _Requirements: 2.3_

- [x] 7. Minibar sıfırlama sayfasını oluştur


  - `templates/sistem_yoneticisi/minibar_sifirla.html` dosyası oluştur
  - Tehlike uyarı mesajı ekle (kırmızı banner)
  - Sıfırlama özeti kartları ekle
  - Ürün dağılımı tablosu ekle
  - Sıfırla butonu ekle (kırmızı, büyük)
  - Şifre doğrulama modal'ı oluştur
  - Modal açma/kapama JavaScript'i yaz
  - AJAX şifre doğrulama fonksiyonu yaz
  - Sıfırlama işlemi JavaScript'i yaz
  - Loading state gösterimi ekle
  - Success/Error notification gösterimi ekle
  - Dark mode stilleri ekle
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 8. Audit ve log kayıtlarını ekle

  - Sıfırlama işleminde AuditLog kaydı ekle
  - Sıfırlama işleminde SistemLog kaydı ekle
  - Başarısız şifre denemelerini logla
  - İşlem öncesi toplam stok miktarını kaydet
  - Etkilenen oda sayısını kaydet
  - _Requirements: 5.3, 5.4, 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 9. Error handling ve validation ekle

  - Route'larda try-catch blokları ekle
  - OperationalError handling ekle
  - Generic Exception handling ekle
  - AJAX error handling ekle
  - Boş şifre validation ekle
  - Yanlış şifre mesajı ekle
  - Yetkisiz erişim kontrolü ekle
  - Geçersiz oda ID kontrolü ekle
  - Transaction rollback mekanizması ekle
  - _Requirements: 4.5, 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 10. Excel export fonksiyonalitesini tamamla

  - openpyxl ile Excel dosyası oluştur
  - Sheet yapısını oluştur (Depo Stokları)
  - Kolonları ekle (Ürün Adı, Grup, Birim, Mevcut Stok, Kritik Stok, Durum)
  - Header stilini uygula (Bold, mavi arka plan)
  - Kritik stok satırlarını kırmızı highlight yap
  - Freeze panes uygula (İlk satır sabit)
  - Auto-width kolon genişliği ayarla
  - BytesIO buffer döndür
  - Route'da send_file ile dosyayı gönder
  - _Requirements: 1.5_

- [x] 11. UI/UX iyileştirmeleri ve responsive tasarım

  - Tüm sayfaların mobile responsive olduğunu kontrol et
  - Tablet görünümünü test et
  - Desktop görünümünü test et
  - Dark mode tüm sayfalarda çalıştığını kontrol et
  - Loading state'leri ekle (skeleton loader, spinner)
  - Toast notification'ları test et
  - Keyboard navigation ekle
  - ARIA labels ekle
  - Focus indicators ekle
  - Color contrast kontrolü yap (WCAG AA)
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4, 2.5, 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 12. Güvenlik kontrollerini tamamla

  - Tüm route'larda @login_required decorator'ı kontrol et
  - @role_required('sistem_yoneticisi', 'admin') decorator'ı kontrol et
  - CSRF token'ların tüm POST request'lerde olduğunu kontrol et
  - AJAX request'lerde X-CSRFToken header'ı kontrol et
  - Password verification fonksiyonunu test et
  - Şifre plain text olarak loglanmadığını kontrol et
  - SQL Injection koruması kontrol et (parametreli sorgular)
  - XSS koruması kontrol et (Jinja2 auto-escaping)
  - Rate limiting ekle (sıfırlama işlemi için)
  - _Requirements: 4.3, 4.4, 4.5, 6.5_

- [x] 13. Test senaryolarını çalıştır


  - Helper fonksiyonları için unit test yaz
  - Route'lar için integration test yaz
  - Şifre doğrulama için security test yaz
  - Excel export için test yaz
  - Responsive tasarım için UI test yap
  - Dark mode için UI test yap
  - Loading states için UI test yap
  - Error messages için UI test yap
  - Performance test yap (1000+ ürün, 500+ oda)
  - _Requirements: Tüm requirements_

- [x] 14. Dokümantasyon güncelle



  - README dosyasına yeni özellikler ekle
  - API documentation oluştur (yeni endpoint'ler)
  - User guide oluştur (Admin kullanım kılavuzu)
  - Changelog güncelle (versiyon notları)
  - Deployment guide güncelle
  - _Requirements: Tüm requirements_
