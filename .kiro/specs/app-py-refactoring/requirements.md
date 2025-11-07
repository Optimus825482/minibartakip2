# Requirements Document

## Introduction

Bu proje, mevcut monolitik app.py dosyasının (6746 satır) daha küçük, yönetilebilir modüllere bölünmesini ve routes dizinine organize edilmesini amaçlamaktadır. Ayrıca kullanılmayan endpoint'lerin ve fonksiyonların tespit edilerek temizlenmesi hedeflenmektedir.

## Glossary

- **Sistem**: Minibar takip ve yönetim uygulaması
- **app.py**: Ana Flask uygulama dosyası (6746 satır)
- **routes dizini**: Flask route'larının organize edildiği modül dizini
- **endpoint**: HTTP isteklerini karşılayan Flask route fonksiyonları
- **Blueprint**: Flask'ta route'ları gruplamak için kullanılan yapı
- **template**: HTML şablon dosyaları
- **static**: CSS, JS ve diğer statik dosyalar
- **kullanılmayan kod**: Template veya diğer kodlar tarafından referans edilmeyen fonksiyonlar/endpoint'ler

## Requirements

### Requirement 1: Kod Analizi ve Envanter Çıkarma

**User Story:** Sistem yöneticisi olarak, mevcut app.py dosyasındaki tüm endpoint'lerin ve fonksiyonların envanterini çıkarmak istiyorum, böylece hangi kodların kullanıldığını ve hangilerinin kullanılmadığını görebilirim.

#### Acceptance Criteria

1. WHEN Sistem app.py dosyasını analiz ettiğinde, THE Sistem SHALL tüm @app.route dekoratörlü fonksiyonları listeleyecek
2. WHEN Sistem template dosyalarını taradığında, THE Sistem SHALL tüm url_for çağrılarını tespit edecek
3. WHEN Sistem static dosyaları (JS) taradığında, THE Sistem SHALL tüm API endpoint çağrılarını tespit edecek
4. THE Sistem SHALL her endpoint için kullanım durumunu (kullanılıyor/kullanılmıyor) belirleyecek
5. THE Sistem SHALL analiz sonuçlarını bir rapor dosyasına kaydetmek

### Requirement 2: Yedekleme ve Güvenlik

**User Story:** Geliştirici olarak, refactoring işlemi öncesinde mevcut app.py dosyasının yedeğini almak istiyorum, böylece bir sorun olduğunda geri dönebilirim.

#### Acceptance Criteria

1. WHEN refactoring başlamadan önce, THE Sistem SHALL app.py dosyasının tam yedeğini oluşturacak
2. THE Sistem SHALL yedek dosyasını tarih-saat damgası ile adlandıracak (örn: app_backup_20241107_143000.py)
3. THE Sistem SHALL yedek dosyasını proje kök dizinine kaydetmek
4. THE Sistem SHALL yedekleme işleminin başarılı olduğunu doğrulayacak

### Requirement 3: Blueprint Yapısı Oluşturma

**User Story:** Geliştirici olarak, endpoint'leri mantıksal gruplara ayırmak için Blueprint yapısı oluşturmak istiyorum, böylece kod daha organize ve yönetilebilir olur.

#### Acceptance Criteria

1. THE Sistem SHALL routes dizininde aşağıdaki Blueprint modüllerini oluşturacak:
   - auth_routes.py (login, logout, setup)
   - sistem_yoneticisi_routes.py (sistem yöneticisi endpoint'leri)
   - admin_routes.py (admin endpoint'leri)
   - depo_routes.py (depo sorumlusu endpoint'leri)
   - kat_sorumlusu_routes.py (kat sorumlusu endpoint'leri)
   - api_routes.py (API endpoint'leri)
2. WHEN her Blueprint modülü oluşturulduğunda, THE Sistem SHALL gerekli import'ları ekleyecek
3. THE Sistem SHALL her Blueprint'i app.py'de register edecek
4. THE Sistem SHALL mevcut routes dizinindeki dosyalarla uyumlu çalışacak

### Requirement 4: Endpoint'lerin Taşınması

**User Story:** Geliştirici olarak, app.py'deki endpoint'leri ilgili Blueprint modüllerine taşımak istiyorum, böylece her modül kendi sorumluluğundaki route'ları içerir.

#### Acceptance Criteria

1. WHEN bir endpoint taşınırken, THE Sistem SHALL endpoint fonksiyonunu ve tüm bağımlılıklarını kopyalayacak
2. THE Sistem SHALL @app.route dekoratörünü @blueprint.route olarak değiştirecek
3. THE Sistem SHALL decorator'ları (@login_required, @role_required vb.) koruyacak
4. THE Sistem SHALL taşınan endpoint'i app.py'den silmeyecek (önce test edilmeli)
5. THE Sistem SHALL her taşıma işlemini log'layacak

### Requirement 5: Kullanılmayan Kod Tespiti

**User Story:** Geliştirici olarak, hiçbir template veya kod tarafından kullanılmayan endpoint'leri tespit etmek istiyorum, böylece gereksiz kodu temizleyebilirim.

#### Acceptance Criteria

1. WHEN Sistem kullanılmayan kod analizi yaptığında, THE Sistem SHALL template'lerde referans edilmeyen endpoint'leri listeleyecek
2. THE Sistem SHALL static JS dosyalarında çağrılmayan API endpoint'lerini listeleyecek
3. THE Sistem SHALL diğer Python modüllerinde import edilmeyen fonksiyonları listeleyecek
4. THE Sistem SHALL kullanılmayan kod listesini bir rapor dosyasına kaydetmek
5. IF bir endpoint son 90 gün içinde log'larda görünmüyorsa, THEN THE Sistem SHALL bunu "potansiyel kullanılmayan" olarak işaretleyecek

### Requirement 6: Test ve Doğrulama

**User Story:** Geliştirici olarak, refactoring sonrası uygulamanın düzgün çalıştığını doğrulamak istiyorum, böylece hiçbir fonksiyonalite bozulmadığından emin olabilirim.

#### Acceptance Criteria

1. WHEN refactoring tamamlandığında, THE Sistem SHALL Flask uygulamasını başlatabilecek
2. THE Sistem SHALL tüm Blueprint'lerin doğru register edildiğini doğrulayacak
3. THE Sistem SHALL her endpoint'in erişilebilir olduğunu kontrol edecek
4. THE Sistem SHALL import hatalarını tespit edecek
5. THE Sistem SHALL test sonuçlarını bir rapor dosyasına kaydetmek

### Requirement 7: Dokümantasyon

**User Story:** Geliştirici olarak, refactoring işleminin detaylı dokümantasyonunu görmek istiyorum, böylece yapılan değişiklikleri anlayabilir ve gelecekte referans alabilirim.

#### Acceptance Criteria

1. THE Sistem SHALL her Blueprint modülünün sorumluluklarını dokümante edecek
2. THE Sistem SHALL taşınan endpoint'lerin listesini oluşturacak
3. THE Sistem SHALL silinen/kullanılmayan kodların listesini oluşturacak
4. THE Sistem SHALL yeni dizin yapısını dokümante edecek
5. THE Sistem SHALL tüm dokümantasyonu Türkçe olarak hazırlayacak

### Requirement 8: Kademeli Geçiş

**User Story:** Geliştirici olarak, refactoring işlemini kademeli olarak yapmak istiyorum, böylece her adımda test edebilir ve sorun çıkarsa geri dönebilirim.

#### Acceptance Criteria

1. THE Sistem SHALL refactoring'i aşamalara bölerek ilerleyecek
2. WHEN her aşama tamamlandığında, THE Sistem SHALL o aşamanın test edilmesini bekleyecek
3. THE Sistem SHALL her aşamada app.py'nin çalışır durumda kalmasını sağlayacak
4. THE Sistem SHALL her aşama için ayrı commit önerisi sunacak
5. IF bir aşamada hata tespit edilirse, THEN THE Sistem SHALL o aşamayı geri alabilecek
