# Requirements Document

## Introduction

Bu özellik, sistemdeki tüm sayfalarda bulunan header (üst navigasyon) yapısını iyileştirmeyi amaçlamaktadır. Mevcut durumda header'da otel logosu küçük kalıyor, her sayfada "Panel" yazısı görünüyor ve sayfa başlıkları bir alta kayıyor. Bu durum hem mantıksız hem yer kaplayan hem de kullanıcı deneyimi açısından olumsuz bir durum yaratıyor. Yeni tasarımda, her sayfanın kendi başlığı header'a taşınacak ve varsa ekleme butonları sayfa içeriğine indirilecek.

## Glossary

- **Header**: Sayfanın en üstünde bulunan, otel logosu, sayfa başlığı ve kullanıcı işlemlerini (tema değiştirme, çıkış) içeren navigasyon alanı
- **Base Template**: Tüm sayfalarda ortak kullanılan ana şablon dosyası (templates/base.html)
- **Page Title Block**: Her sayfanın kendi başlığını tanımladığı Jinja2 block yapısı
- **Action Buttons**: Sayfalarda bulunan "Yeni Ekle", "Kaydet" gibi işlem butonları
- **Kullanici_Otel**: Kullanıcının bağlı olduğu otel bilgisini içeren context değişkeni

## Requirements

### Requirement 1

**User Story:** Sistem yöneticisi olarak, her sayfada o sayfaya özel başlığı header'da görmek istiyorum, böylece hangi sayfada olduğumu net bir şekilde anlayabilirim.

#### Acceptance Criteria

1. WHEN bir kullanıcı herhangi bir sayfayı açtığında, THE Header SHALL o sayfanın başlığını görünür şekilde göstermelidir
2. THE Header SHALL "Panel" yazısını sadece dashboard sayfasında göstermelidir
3. WHEN bir kullanıcı otel listesi sayfasını açtığında, THE Header SHALL "Otel Listesi" başlığını göstermelidir
4. WHEN bir kullanıcı kat yönetimi sayfasını açtığında, THE Header SHALL "Kat Yönetimi" başlığını göstermelidir
5. THE Header SHALL her sayfanın mevcut başlığını (h2 elementindeki) header'a taşımalıdır

### Requirement 2

**User Story:** Sistem yöneticisi olarak, otel logosunun header'da daha görünür olmasını istiyorum, böylece hangi otelin panelinde olduğumu kolayca anlayabilirim.

#### Acceptance Criteria

1. WHEN kullanici_otel bilgisi mevcutsa, THE Header SHALL otel logosunu daha büyük boyutta göstermelidir
2. THE Header SHALL otel logosunu minimum 48px yüksekliğinde göstermelidir
3. WHEN ekran genişliği 640px'den küçükse, THE Header SHALL otel logosunu 32px yüksekliğinde göstermelidir
4. THE Header SHALL otel logosunun yanında otel adını küçük bir etiket olarak göstermelidir
5. WHEN otel logosu yoksa, THE Header SHALL sadece otel adını göstermelidir

### Requirement 3

**User Story:** Sistem yöneticisi olarak, sayfa başlıklarının altındaki açıklama metnini header'da görmek istiyorum, böylece sayfanın amacını hızlıca anlayabilirim.

#### Acceptance Criteria

1. WHEN bir sayfa başlığının altında açıklama metni varsa, THE Header SHALL bu açıklama metnini başlığın altında küçük punto ile göstermelidir
2. THE Header SHALL açıklama metnini text-slate-600 renk tonunda göstermelidir
3. WHEN ekran genişliği 768px'den küçükse, THE Header SHALL açıklama metnini gizlemelidir
4. THE Header SHALL açıklama metnini truncate ile tek satırda göstermelidir

### Requirement 4

**User Story:** Sistem yöneticisi olarak, sayfalardaki işlem butonlarının (Yeni Ekle, vb.) header'dan sayfa içeriğine taşınmasını istiyorum, böylece header daha temiz görünür ve sayfa içeriği daha organize olur.

#### Acceptance Criteria

1. WHEN bir sayfada "Yeni Ekle" butonu varsa, THE System SHALL bu butonu sayfa içeriğinin üst kısmına taşımalıdır
2. THE System SHALL işlem butonlarını sayfa başlığının sağ tarafına hizalı olarak yerleştirmelidir
3. WHEN ekran genişliği 640px'den küçükse, THE System SHALL işlem butonlarını sayfa başlığının altına tam genişlikte yerleştirmelidir
4. THE System SHALL işlem butonlarını header'dan kaldırmalıdır

### Requirement 5

**User Story:** Sistem yöneticisi olarak, header'ın daha az yer kaplamasını istiyorum, böylece sayfa içeriği için daha fazla alan kalır.

#### Acceptance Criteria

1. THE Header SHALL maksimum 64px yüksekliğinde olmalıdır (desktop)
2. THE Header SHALL maksimum 56px yüksekliğinde olmalıdır (mobile)
3. THE Header SHALL gereksiz padding ve margin değerlerini minimize etmelidir
4. THE Header SHALL içerik yoğunluğunu artırarak daha kompakt bir görünüm sağlamalıdır
5. WHEN sidebar açıksa, THE Header SHALL sidebar genişliğini hesaba katarak content alanını optimize etmelidir
