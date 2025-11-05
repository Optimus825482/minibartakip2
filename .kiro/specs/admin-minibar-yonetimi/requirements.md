# Requirements Document

## Introduction

Bu özellik, admin paneline minibar stok yönetimi ve görüntüleme yetenekleri ekler. Admin kullanıcıları, tüm minibar stoklarını depo ve oda bazında görüntüleyebilecek, ayrıca gerektiğinde tüm minibar stoklarını güvenli bir şekilde sıfırlayabilecektir. Sistem, kritik işlemler için admin şifresi doğrulaması gerektirecektir.

## Glossary

- **Admin Panel**: Sistem yöneticisi ve admin rolündeki kullanıcıların erişebildiği yönetim arayüzü
- **Minibar Stok**: Odalarda bulunan ürünlerin mevcut durumu (başlangıç stok, bitiş stok, tüketim)
- **Depo Stok**: Ana depoda bulunan ürünlerin toplam miktarı
- **Stok Sıfırlama**: Minibar stoklarının 0'a çekilmesi işlemi (ana depoya eklenmeden)
- **Admin Şifre Doğrulaması**: Kritik işlemler için kullanıcının şifresini yeniden girmesi
- **Sidebar Menü**: Sol taraftaki navigasyon menüsü
- **MinibarIslem**: Minibar işlemlerinin kaydedildiği tablo
- **MinibarIslemDetay**: Minibar işlem detaylarının (ürün bazında) kaydedildiği tablo

## Requirements

### Requirement 1

**User Story:** Admin kullanıcısı olarak, tüm minibar stoklarını depo bazında görüntülemek istiyorum, böylece hangi üründen ne kadar depoda olduğunu takip edebilirim.

#### Acceptance Criteria

1. WHEN admin kullanıcısı sidebar menüsünden "Depo Stokları" seçeneğine tıkladığında, THE Sistem SHALL tüm ürünlerin depo stok miktarlarını tablo formatında gösterecek
2. THE Sistem SHALL her ürün için ürün adı, grup, birim, mevcut stok miktarı ve kritik stok seviyesi bilgilerini gösterecek
3. THE Sistem SHALL kritik stok seviyesinin altındaki ürünleri kırmızı renkte vurgulayacak
4. THE Sistem SHALL stok verilerini ürün grubuna göre filtreleme imkanı sunacak
5. THE Sistem SHALL stok verilerini Excel formatında dışa aktarma özelliği sağlayacak

### Requirement 2

**User Story:** Admin kullanıcısı olarak, tüm minibar stoklarını oda bazında görüntülemek istiyorum, böylece hangi odada hangi ürünlerden ne kadar olduğunu görebilirim.

#### Acceptance Criteria

1. WHEN admin kullanıcısı sidebar menüsünden "Oda Minibar Stokları" seçeneğine tıkladığında, THE Sistem SHALL tüm odaların minibar stok durumlarını gösterecek
2. THE Sistem SHALL her oda için oda numarası, kat bilgisi ve son işlem tarihini gösterecek
3. WHEN admin kullanıcısı bir odanın detayına tıkladığında, THE Sistem SHALL o odadaki tüm ürünlerin başlangıç stok, bitiş stok, tüketim ve eklenen miktar bilgilerini gösterecek
4. THE Sistem SHALL oda listesini kat numarasına göre filtreleme imkanı sunacak
5. THE Sistem SHALL boş (hiç işlem yapılmamış) odaları ayrı bir bölümde gösterecek

### Requirement 3

**User Story:** Admin kullanıcısı olarak, sidebar menüsünden minibar yönetim sayfalarına kolayca erişmek istiyorum, böylece hızlı bir şekilde istediğim bilgiye ulaşabilirim.

#### Acceptance Criteria

1. THE Sistem SHALL admin paneli sidebar menüsüne "Minibar Yönetimi" ana menü öğesi ekleyecek
2. THE Sistem SHALL "Minibar Yönetimi" altında "Depo Stokları" alt menü öğesi gösterecek
3. THE Sistem SHALL "Minibar Yönetimi" altında "Oda Minibar Stokları" alt menü öğesi gösterecek
4. THE Sistem SHALL "Minibar Yönetimi" altında "Minibarları Sıfırla" alt menü öğesi gösterecek
5. WHEN kullanıcı bir menü öğesine tıkladığında, THE Sistem SHALL ilgili sayfaya yönlendirecek

### Requirement 4

**User Story:** Admin kullanıcısı olarak, tüm minibar stoklarını güvenli bir şekilde sıfırlamak istiyorum, böylece yeni dönem başında veya gerektiğinde tüm odaların stoklarını temizleyebilirim.

#### Acceptance Criteria

1. WHEN admin kullanıcısı "Minibarları Sıfırla" sayfasına eriştiğinde, THE Sistem SHALL işlemin risklerini açıklayan bir uyarı mesajı gösterecek
2. THE Sistem SHALL sıfırlama işlemi öncesinde mevcut toplam minibar stok miktarını özet olarak gösterecek
3. WHEN admin kullanıcısı "Sıfırla" butonuna tıkladığında, THE Sistem SHALL bir modal pencere açarak admin şifresi talep edecek
4. THE Sistem SHALL girilen şifrenin doğru olup olmadığını kontrol edecek
5. IF şifre yanlış ise, THEN THE Sistem SHALL hata mesajı gösterecek ve işlemi iptal edecek

### Requirement 5

**User Story:** Admin kullanıcısı olarak, minibar sıfırlama işleminin ana depoya etki etmemesini istiyorum, böylece sadece oda stoklarını temizleyip depo stoklarını koruyabilirim.

#### Acceptance Criteria

1. WHEN admin şifresi doğrulandığında, THE Sistem SHALL tüm MinibarIslemDetay kayıtlarındaki bitis_stok değerlerini 0 yapacak
2. THE Sistem SHALL sıfırlama işlemi sırasında StokHareket tablosuna herhangi bir kayıt eklemeyecek
3. THE Sistem SHALL sıfırlama işlemini AuditLog tablosuna kaydedecek
4. THE Sistem SHALL sıfırlama işlemini SistemLog tablosuna kaydedecek
5. WHEN sıfırlama işlemi tamamlandığında, THE Sistem SHALL başarı mesajı gösterecek ve kaç odanın etkilendiğini bildirecek

### Requirement 6

**User Story:** Admin kullanıcısı olarak, minibar sıfırlama işleminin loglarını görmek istiyorum, böylece kim tarafından ne zaman yapıldığını takip edebilirim.

#### Acceptance Criteria

1. THE Sistem SHALL her sıfırlama işlemi için kullanıcı adı, tarih, saat ve etkilenen oda sayısı bilgilerini kaydedecek
2. THE Sistem SHALL sıfırlama işlemlerini audit trail sistemine kaydedecek
3. WHEN admin kullanıcısı sistem loglarını görüntülediğinde, THE Sistem SHALL minibar sıfırlama işlemlerini ayrı bir kategori olarak filtreleme imkanı sunacak
4. THE Sistem SHALL her log kaydında işlem öncesi toplam stok miktarını saklayacak
5. THE Sistem SHALL başarısız sıfırlama denemelerini (yanlış şifre) de loglayacak
