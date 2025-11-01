# 🏨 OTEL MİNİBAR TAKİP SİSTEMİ 
## BÖLÜM 4: AKIŞ ŞEMALARI VE İŞ AKIŞLARI

**Versiyon:** 1.0  
**Tarih:** 31 Ekim 2025

---

## 1. SİSTEM GENEL AKIŞ ŞEMASI

```mermaid
graph TD
    Start([Sistem Başlangıç]) --> Setup{İlk Kurulum<br/>Yapılmış mı?}
    Setup -->|Hayır| SetupPage[Setup Sayfası]
    SetupPage --> CreateAdmin[Sistem Yöneticisi Oluştur]
    CreateAdmin --> CreateHotel[Otel Bilgileri Gir]
    CreateHotel --> DBInit[Veritabanı Başlangıç]
    DBInit --> Login[Login Sayfası]
    
    Setup -->|Evet| Login
    
    Login --> Auth{Kimlik Doğrulama}
    Auth -->|Başarısız| RateLimit{5 Deneme<br/>Aşıldı mı?}
    RateLimit -->|Evet| Block[Hesap Kilitlendi<br/>1 Saat]
    RateLimit -->|Hayır| Login
    
    Auth -->|Başarılı| RoleCheck{Rol Kontrolü}
    
    RoleCheck -->|Sistem Yöneticisi| SYDashboard[Sistem Yöneticisi<br/>Dashboard]
    RoleCheck -->|Admin| AdminDashboard[Admin<br/>Dashboard]
    RoleCheck -->|Depo Sorumlusu| DepoDashboard[Depo Sorumlusu<br/>Dashboard]
    RoleCheck -->|Kat Sorumlusu| KatDashboard[Kat Sorumlusu<br/>Dashboard]
    
    SYDashboard --> SYOperations[Otel/Kat/Oda/Personel<br/>Yönetimi]
    AdminDashboard --> AdminOperations[Ürün/Grup<br/>Yönetimi]
    DepoDashboard --> DepoOperations[Stok/Zimmet<br/>Yönetimi]
    KatDashboard --> KatOperations[Minibar<br/>Yönetimi]
    
    SYOperations --> Logout[Çıkış]
    AdminOperations --> Logout
    DepoOperations --> Logout
    KatOperations --> Logout
    
    Logout --> Login

    style Start fill:#e1f5ff
    style Login fill:#fff3e0
    style SYDashboard fill:#e8f5e9
    style AdminDashboard fill:#f3e5f5
    style DepoDashboard fill:#fff9c4
    style KatDashboard fill:#ffe0b2
    style Block fill:#ffcdd2
```

---

## 2. KULLANICI KİMLİK DOĞRULAMA AKIŞI

```mermaid
sequenceDiagram
    participant User as Kullanıcı
    participant Browser as Tarayıcı
    participant Flask as Flask App
    participant Limiter as Rate Limiter
    participant DB as Veritabanı
    participant Audit as Audit Log

    User->>Browser: Login sayfasına git
    Browser->>Flask: GET /login
    Flask->>Browser: Login formu (CSRF token)
    
    User->>Browser: Kullanıcı adı & Şifre gir
    Browser->>Flask: POST /login (CSRF token ile)
    
    Flask->>Flask: CSRF token doğrula
    
    Flask->>Limiter: Rate limit kontrolü
    alt Limit aşıldı
        Limiter-->>Flask: 429 Too Many Requests
        Flask-->>Browser: Hata mesajı
        Browser-->>User: "Çok fazla deneme"
    else Limit OK
        Limiter-->>Flask: İzin verildi
        
        Flask->>DB: Kullanıcı sorgula
        DB-->>Flask: Kullanıcı bilgileri
        
        Flask->>Flask: Şifre hash doğrula
        
        alt Şifre yanlış
            Flask->>Audit: Login başarısız kaydet
            Flask-->>Browser: Hata mesajı
            Browser-->>User: "Hatalı bilgiler"
        else Şifre doğru
            Flask->>Flask: Session oluştur
            Flask->>Audit: Login başarılı kaydet
            Flask-->>Browser: Yönlendirme (role dashboard)
            Browser-->>User: Dashboard göster
        end
    end
```

---

## 3. STOK YÖNETİMİ AKIŞI

```mermaid
graph TD
    Start([Stok Yönetimi Başlat]) --> StokMenu{İşlem Seçimi}
    
    StokMenu -->|Stok Giriş| StokGiris[Stok Giriş Formu]
    StokMenu -->|Stok Listesi| StokList[Stok Listesi Görüntüle]
    StokMenu -->|Stok Raporu| StokReport[Stok Raporu Oluştur]
    
    StokGiris --> FormFill[Form Doldur]
    FormFill --> UrunSec[Ürün Seç]
    UrunSec --> MiktarGir[Miktar & Birim Fiyat Gir]
    MiktarGir --> HareketTip[Hareket Tipi Seç<br/>Giriş/Devir/Sayım]
    HareketTip --> Validate{Form Validasyon}
    
    Validate -->|Hata| FormFill
    Validate -->|Başarılı| SaveStok[Stok Hareketi Kaydet]
    
    SaveStok --> CalcStock[Stok Hesapla]
    CalcStock --> CheckCritical{Kritik Seviye<br/>Kontrolü}
    
    CheckCritical -->|Kritik| AlertShow[Kritik Stok Uyarısı]
    CheckCritical -->|Normal| NoAlert[Uyarı Yok]
    
    AlertShow --> LogOp[İşlem Logla]
    NoAlert --> LogOp
    
    LogOp --> AuditCreate[Audit Kaydı Oluştur]
    AuditCreate --> Success[Başarı Mesajı]
    Success --> End([Bitiş])
    
    StokList --> FilterApply{Filtre Var mı?}
    FilterApply -->|Evet| ApplyFilter[Filtre Uygula]
    FilterApply -->|Hayır| ShowAll[Tüm Ürünler]
    ApplyFilter --> DisplayTable[Tablo Göster]
    ShowAll --> DisplayTable
    DisplayTable --> ExportOpt{Export İstendi mi?}
    ExportOpt -->|Excel| ExcelGen[Excel Oluştur]
    ExportOpt -->|PDF| PDFGen[PDF Oluştur]
    ExportOpt -->|Hayır| End
    ExcelGen --> End
    PDFGen --> End
    
    StokReport --> ReportDate[Tarih Aralığı Seç]
    ReportDate --> GenerateRep[Rapor Oluştur]
    GenerateRep --> End

    style Start fill:#e1f5ff
    style SaveStok fill:#c8e6c9
    style AlertShow fill:#ffcdd2
    style Success fill:#a5d6a7
    style End fill:#e1f5ff
```

---

## 4. ZİMMET YÖNETİMİ AKIŞI

```mermaid
graph TD
    Start([Zimmet Yönetimi]) --> ZimmetOp{İşlem Tipi}
    
    ZimmetOp -->|Yeni Zimmet| NewZimmet[Zimmet Atama]
    ZimmetOp -->|Zimmet Görüntüle| ViewZimmet[Zimmet Listesi]
    ZimmetOp -->|Zimmet İade| ReturnZimmet[İade İşlemi]
    ZimmetOp -->|Zimmet İptal| CancelZimmet[İptal İşlemi]
    
    NewZimmet --> SelectPersonel[Personel Seç<br/>Kat Sorumlusu]
    SelectPersonel --> SelectProducts[Ürünler Seç]
    SelectProducts --> EnterQty[Miktar Gir]
    EnterQty --> CheckStock{Stok Yeterli mi?}
    
    CheckStock -->|Hayır| StockError[Yetersiz Stok Hatası]
    StockError --> SelectProducts
    
    CheckStock -->|Evet| CreateZimmet[Zimmet Kaydı Oluştur]
    CreateZimmet --> CreateDetails[Zimmet Detayları Oluştur]
    CreateDetails --> StockExit[Stoktan Çıkış Yap]
    StockExit --> StokHareket[Stok Hareketi Kaydet<br/>Tip: Çıkış]
    StokHareket --> AuditLog[Audit Log Kaydet]
    AuditLog --> NotifyPersonel[Personele Bildirim<br/>Opsiyonel]
    NotifyPersonel --> SuccessMsg[Başarı Mesajı]
    SuccessMsg --> End([Bitiş])
    
    ViewZimmet --> FilterZimmet{Filtre?}
    FilterZimmet -->|Personel| PersonelFilter[Personel Filtresi]
    FilterZimmet -->|Durum| StatusFilter[Durum Filtresi<br/>Aktif/Tamamlandı/İptal]
    FilterZimmet -->|Hayır| AllZimmet[Tüm Zimmetler]
    
    PersonelFilter --> DisplayZimmet[Zimmet Listesi Göster]
    StatusFilter --> DisplayZimmet
    AllZimmet --> DisplayZimmet
    
    DisplayZimmet --> DetailView{Detay Görüntüle?}
    DetailView -->|Evet| ShowDetails[Ürün Detayları<br/>Teslim/Kullanılan/Kalan]
    DetailView -->|Hayır| End
    ShowDetails --> End
    
    ReturnZimmet --> SelectZimmet[Zimmet Seç]
    SelectZimmet --> SelectProduct[Ürün Seç]
    SelectProduct --> EnterReturnQty[İade Miktarı Gir]
    EnterReturnQty --> ValidateReturn{Miktar<br/>Geçerli mi?}
    
    ValidateReturn -->|Hayır| ReturnError[Hata: Kalan miktardan fazla]
    ReturnError --> EnterReturnQty
    
    ValidateReturn -->|Evet| UpdateZimmet[Zimmet Güncelle]
    UpdateZimmet --> StockEntry[Stoka Giriş Yap]
    StockEntry --> LogReturn[İade Logla]
    LogReturn --> CheckComplete{Tüm Ürünler<br/>İade Edildi mi?}
    
    CheckComplete -->|Evet| ZimmetComplete[Durum: Tamamlandı]
    CheckComplete -->|Hayır| ZimmetActive[Durum: Aktif]
    
    ZimmetComplete --> End
    ZimmetActive --> End
    
    CancelZimmet --> ConfirmCancel{Onay?}
    ConfirmCancel -->|Hayır| End
    ConfirmCancel -->|Evet| ReturnAllProducts[Tüm Kalanları İade Et]
    ReturnAllProducts --> UpdateStatus[Durum: İptal]
    UpdateStatus --> End

    style Start fill:#e1f5ff
    style CreateZimmet fill:#c8e6c9
    style StockError fill:#ffcdd2
    style ReturnError fill:#ffcdd2
    style SuccessMsg fill:#a5d6a7
    style End fill:#e1f5ff
```

---

## 5. ZİMMET KULLANIM AKIŞI (FIFO)

```mermaid
graph TD
    Start([Minibar Doldurma<br/>Zimmet Kullanımı]) --> GetProduct[Kullanılacak Ürün & Miktar]
    GetProduct --> FindZimmet[Personelin Aktif Zimmetlerini Bul]
    FindZimmet --> SortByDate[Tarihe Göre Sırala<br/>En Eski → En Yeni]
    
    SortByDate --> LoopStart{Zimmet Listesinde<br/>Sonraki Var mı?}
    
    LoopStart -->|Hayır| InsufficientError[Hata: Yetersiz Zimmet]
    InsufficientError --> End([Bitiş - Hata])
    
    LoopStart -->|Evet| GetZimmet[Sonraki Zimmeti Al]
    GetZimmet --> CheckRemaining{Kalan Miktar > 0?}
    
    CheckRemaining -->|Hayır| LoopStart
    
    CheckRemaining -->|Evet| CalcDeduct[Düşülecek Miktarı Hesapla<br/>MIN Kalan, Gerekli]
    CalcDeduct --> UpdateZimmet[Zimmet Detayını Güncelle<br/>Kullanılan += Düşülen<br/>Kalan -= Düşülen]
    UpdateZimmet --> SubtractNeed[Gerekli -= Düşülen]
    
    SubtractNeed --> CheckComplete{Gerekli = 0?}
    
    CheckComplete -->|Hayır| CheckZimmetDone{Zimmet<br/>Kalan = 0?}
    CheckZimmetDone -->|Evet| MarkComplete[Zimmet Durumu:<br/>Tamamlandı]
    MarkComplete --> LoopStart
    CheckZimmetDone -->|Hayır| LoopStart
    
    CheckComplete -->|Evet| AllDeducted[Tüm Miktar Düşüldü]
    AllDeducted --> LogUsage[Kullanım Logla]
    LogUsage --> Success([Bitiş - Başarılı])

    style Start fill:#e1f5ff
    style UpdateZimmet fill:#fff9c4
    style InsufficientError fill:#ffcdd2
    style Success fill:#a5d6a7
    style End fill:#ffcdd2
```

**FIFO Örnek Senaryo:**
```
Personel Zimmetleri:
1. Zimmet #001: Coca Cola - 100 adet (50 kullanılmış, 50 kalan) [01.10.2025]
2. Zimmet #002: Coca Cola - 200 adet (0 kullanılmış, 200 kalan) [15.10.2025]
3. Zimmet #003: Coca Cola - 150 adet (0 kullanılmış, 150 kalan) [25.10.2025]

Kullanım İsteği: 80 adet Coca Cola

Algoritma:
1. Zimmet #001'den 50 adet düş (kalan 0) → Durum: Tamamlandı
2. Zimmet #002'den 30 adet düş (kalan 170) → Durum: Aktif
3. Toplam düşülen: 80 adet ✓

Sonuç:
- Zimmet #001: 100 kullanılmış, 0 kalan [Tamamlandı]
- Zimmet #002: 30 kullanılmış, 170 kalan [Aktif]
- Zimmet #003: 0 kullanılmış, 150 kalan [Aktif]
```

---

## 6. MİNİBAR İŞLEMLERİ AKIŞI

### 6.1 İlk Dolum Akışı

```mermaid
graph TD
    Start([İlk Dolum Başlat]) --> SelectFloor[Kat Seç]
    SelectFloor --> LoadRooms[Odaları Yükle<br/>AJAX]
    LoadRooms --> SelectRoom[Oda Seç]
    SelectRoom --> CheckFirstFill{İlk Dolum<br/>Yapılmış mı?}
    
    CheckFirstFill -->|Evet| AlreadyFilled[Hata: İlk dolum mevcut]
    AlreadyFilled --> End([Bitiş])
    
    CheckFirstFill -->|Hayır| SelectType[İşlem Tipi: İlk Dolum]
    SelectType --> LoadProducts[Ürünleri Yükle<br/>Grup bazlı]
    LoadProducts --> SelectProducts[Ürün Seç<br/>Çoklu]
    SelectProducts --> EnterQuantities[Her Ürün için<br/>Miktar Gir]
    
    EnterQuantities --> ShowZimmet[Zimmetteki Miktar Göster<br/>Her ürün için]
    ShowZimmet --> ValidateZimmet{Tüm Ürünler için<br/>Zimmet Yeterli mi?}
    
    ValidateZimmet -->|Hayır| ZimmetError[Hata: Yetersiz Zimmet<br/>Detay göster]
    ZimmetError --> EnterQuantities
    
    ValidateZimmet -->|Evet| ConfirmSave{Kaydet Onayı}
    ConfirmSave -->|Hayır| End
    
    ConfirmSave -->|Evet| CreateMinibar[MinibarIslem Oluştur<br/>Tip: ilk_dolum]
    CreateMinibar --> LoopProducts[Her Ürün için]
    
    LoopProducts --> CreateDetail[MinibarIslemDetay Oluştur<br/>baslangic_stok: 0<br/>eklenen: miktar<br/>bitis_stok: miktar<br/>tuketim: 0]
    CreateDetail --> DeductZimmet[Zimmetten Düş<br/>FIFO Algoritması]
    DeductZimmet --> NextProduct{Sonraki Ürün?}
    
    NextProduct -->|Evet| LoopProducts
    NextProduct -->|Hayır| LogOperation[İşlem Logla]
    
    LogOperation --> AuditCreate[Audit Kaydı]
    AuditCreate --> SuccessMsg[Başarı Mesajı<br/>Toast]
    SuccessMsg --> End

    style Start fill:#e1f5ff
    style CreateMinibar fill:#c8e6c9
    style AlreadyFilled fill:#ffcdd2
    style ZimmetError fill:#ffcdd2
    style SuccessMsg fill:#a5d6a7
    style End fill:#e1f5ff
```

### 6.2 Kontrol Akışı

```mermaid
graph TD
    Start([Kontrol Başlat]) --> SelectRoom[Kat & Oda Seç]
    SelectRoom --> SelectType[İşlem Tipi: Kontrol]
    SelectType --> CheckHistory{İlk Dolum<br/>Var mı?}
    
    CheckHistory -->|Hayır| NoHistory[Hata: İlk dolum yapılmamış]
    NoHistory --> End([Bitiş])
    
    CheckHistory -->|Evet| GetLastStatus[Son Minibar Durumunu Al<br/>API Call]
    GetLastStatus --> DisplayProducts[Ürün Listesi Göster<br/>Tablo]
    
    DisplayProducts --> ShowDetails[Her Ürün için:<br/>- Ürün Adı<br/>- Birim<br/>- Mevcut Stok<br/>- Son İşlem Tarihi]
    
    ShowDetails --> LogView[Görüntüleme Logla<br/>SistemLog]
    LogView --> SuccessMsg[Görüntüleme Tamamlandı<br/>Toast]
    SuccessMsg --> End

    style Start fill:#e1f5ff
    style DisplayProducts fill:#fff9c4
    style NoHistory fill:#ffcdd2
    style SuccessMsg fill:#a5d6a7
    style End fill:#e1f5ff
```

### 6.3 Doldurma (Tekli) Akışı

```mermaid
graph TD
    Start([Doldurma Başlat]) --> SelectRoom[Kat & Oda Seç]
    SelectRoom --> SelectType[İşlem Tipi: Doldurma]
    SelectType --> CheckHistory{İlk Dolum<br/>Var mı?}
    
    CheckHistory -->|Hayır| NoHistory[Hata: İlk dolum yapılmamış]
    NoHistory --> End([Bitiş])
    
    CheckHistory -->|Evet| GetLastStatus[Son Minibar Durumunu Al<br/>API]
    GetLastStatus --> LoadProducts[Ürünleri Formlara Yükle<br/>Otomatik]
    
    LoadProducts --> ShowCurrent[Her Ürün için<br/>Mevcut Stok Göster]
    ShowCurrent --> ManualInput[Her Ürün için Girişler:<br/>1. Gerçek Stok Sayımı<br/>2. Eklenecek Miktar]
    
    ManualInput --> CalcConsumption[Tüketim Hesapla<br/>Kayıtlı - Gerçek]
    CalcConsumption --> CalcNew[Yeni Stok Hesapla<br/>Gerçek + Eklenecek]
    CalcNew --> ShowCalc[Hesaplananları Göster<br/>Tüketim & Yeni Stok]
    
    ShowCalc --> ValidateZimmet{Eklenen Miktar için<br/>Zimmet Yeterli mi?}
    
    ValidateZimmet -->|Hayır| ZimmetError[Hata: Yetersiz Zimmet<br/>Detay]
    ZimmetError --> ManualInput
    
    ValidateZimmet -->|Evet| ConfirmSave{Kaydet Onayı}
    ConfirmSave -->|Hayır| End
    
    ConfirmSave -->|Evet| CreateMinibar[MinibarIslem Oluştur<br/>Tip: doldurma]
    CreateMinibar --> CopyOthers[Değişmeyen Ürünleri<br/>Kopyala]
    
    CopyOthers --> LoopChanged[Değişen Her Ürün için]
    LoopChanged --> CreateDetail[MinibarIslemDetay Oluştur<br/>baslangic: gerçek<br/>eklenen: eklenen<br/>bitis: yeni<br/>tuketim: hesaplanan]
    
    CreateDetail --> DeductZimmet[Zimmetten Düş<br/>Sadece Eklenen Miktar<br/>FIFO]
    DeductZimmet --> NextChanged{Sonraki Ürün?}
    
    NextChanged -->|Evet| LoopChanged
    NextChanged -->|Hayır| LogOp[İşlem Logla]
    LogOp --> AuditLog[Audit Kaydı]
    AuditLog --> SuccessMsg[Başarı Mesajı]
    SuccessMsg --> End

    style Start fill:#e1f5ff
    style CreateMinibar fill:#c8e6c9
    style NoHistory fill:#ffcdd2
    style ZimmetError fill:#ffcdd2
    style SuccessMsg fill:#a5d6a7
    style End fill:#e1f5ff
```

### 6.4 Toplu Oda Doldurma Akışı

```mermaid
graph TD
    Start([Toplu Doldurma]) --> SelectFloor[Kat Seç]
    SelectFloor --> LoadRooms[Odaları Yükle<br/>Checkbox List]
    LoadRooms --> SelectRooms[Odalar Seç<br/>Çoklu]
    SelectRooms --> SelectProduct[Ürün Seç<br/>Tek]
    SelectProduct --> EnterQty[Miktar Gir<br/>Tek Değer]
    
    EnterQty --> CalcTotal[Toplam Hesapla<br/>Oda Sayısı × Miktar]
    CalcTotal --> CheckZimmet{Toplam için<br/>Zimmet Yeterli mi?}
    
    CheckZimmet -->|Hayır| ZimmetError[Hata: Yetersiz Zimmet]
    ZimmetError --> EnterQty
    
    CheckZimmet -->|Evet| ShowCurrent{Mevcut Durum<br/>Göster İstendi mi?}
    ShowCurrent -->|Evet| DisplayCurrent[Her Oda için<br/>Mevcut Stok Göster]
    DisplayCurrent --> ConfirmBulk
    ShowCurrent -->|Hayır| ConfirmBulk
    
    ConfirmBulk{Toplu Doldur Onayı} -->|Hayır| End([Bitiş])
    
    ConfirmBulk -->|Evet| InitVars[Değişkenleri Başlat<br/>Başarılı Listesi<br/>Başarısız Listesi]
    InitVars --> LoopRooms[Her Oda için Sırayla]
    
    LoopRooms --> TryBlock{Try Bloğu}
    TryBlock --> GetRoomStatus[Odanın Son<br/>Minibar Durumu Al]
    GetRoomStatus --> CreateOp[MinibarIslem Oluştur]
    CreateOp --> CopyProducts[Diğer Ürünleri<br/>Kopyala]
    
    CopyProducts --> AddNew[Yeni Ürün Detayı Ekle<br/>baslangic: mevcut<br/>eklenen: miktar<br/>bitis: mevcut+miktar<br/>tuketim: 0]
    
    AddNew --> DeductZ[Zimmetten Düş<br/>FIFO]
    DeductZ --> AddSuccess[Başarılı Listesine Ekle<br/>Oda No]
    AddSuccess --> NextRoom
    
    TryBlock -->|Hata| LogError[Hatayı Logla]
    LogError --> AddFail[Başarısız Listesine Ekle<br/>Oda No + Hata Mesajı]
    AddFail --> NextRoom{Sonraki Oda?}
    
    NextRoom -->|Evet| LoopRooms
    NextRoom -->|Hayır| GenerateReport[Sonuç Raporu Oluştur]
    
    GenerateReport --> ShowReport[Rapor Göster:<br/>- Başarılı Oda Sayısı<br/>- Başarısız Oda Sayısı<br/>- Başarılı Odalar<br/>- Başarısız Detaylar<br/>- Kullanılan Zimmet]
    
    ShowReport --> End

    style Start fill:#e1f5ff
    style CreateOp fill:#c8e6c9
    style ZimmetError fill:#ffcdd2
    style LogError fill:#ffcdd2
    style ShowReport fill:#fff9c4
    style End fill:#e1f5ff
```

---

## 7. RAPORLAMA AKIŞI

```mermaid
graph TD
    Start([Rapor Talebi]) --> SelectReport{Rapor Tipi}
    
    SelectReport -->|Stok Raporu| StokRep[Stok Raporu]
    SelectReport -->|Zimmet Raporu| ZimmetRep[Zimmet Raporu]
    SelectReport -->|Minibar Raporu| MinibarRep[Minibar Raporu]
    SelectReport -->|Tüketim Raporu| TuketimRep[Tüketim Raporu]
    SelectReport -->|Kat Bazlı| KatRep[Kat Bazlı Raporu]
    SelectReport -->|Personel Raporu| PersonelRep[Personel Raporu]
    SelectReport -->|Oda Raporu| OdaRep[Oda Raporu]
    
    StokRep --> StokFilters[Filtreler:<br/>- Ürün Grubu<br/>- Kritik Durum]
    ZimmetRep --> ZimmetFilters[Filtreler:<br/>- Personel<br/>- Durum<br/>- Tarih Aralığı]
    MinibarRep --> MinibarFilters[Filtreler:<br/>- Kat<br/>- Oda<br/>- Tarih Aralığı]
    TuketimRep --> TuketimFilters[Filtreler:<br/>- Ürün<br/>- Tarih Aralığı]
    KatRep --> KatFilters[Filtreler:<br/>- Kat<br/>- Tarih Aralığı]
    PersonelRep --> PersonelFilters[Filtreler:<br/>- Personel<br/>- Tarih Aralığı]
    OdaRep --> OdaFilters[Filtreler:<br/>- Oda<br/>- Tarih Aralığı]
    
    StokFilters --> QueryDB[Veritabanı Sorgusu]
    ZimmetFilters --> QueryDB
    MinibarFilters --> QueryDB
    TuketimFilters --> QueryDB
    KatFilters --> QueryDB
    PersonelFilters --> QueryDB
    OdaFilters --> QueryDB
    
    QueryDB --> ProcessData[Veri İşleme<br/>Gruplama & Hesaplama]
    ProcessData --> DisplayWeb[Web'de Göster<br/>Tablo Formatı]
    
    DisplayWeb --> ExportChoice{Export İstendi mi?}
    
    ExportChoice -->|Hayır| End([Bitiş])
    
    ExportChoice -->|Excel| ExcelFlow[Excel Export]
    ExportChoice -->|PDF| PDFFlow[PDF Export]
    
    ExcelFlow --> CreateWB[Workbook Oluştur<br/>OpenPyXL]
    CreateWB --> StyleHeaders[Başlık Stilleri<br/>Font, Renk, Border]
    StyleHeaders --> WriteData[Verileri Yaz<br/>Satır satır]
    WriteData --> AutoWidth[Sütun Genişlik<br/>Otomatik Ayarla]
    AutoWidth --> SaveExcel[Excel Dosyası Kaydet<br/>BytesIO]
    SaveExcel --> SendExcel[Dosya Gönder<br/>send_file]
    SendExcel --> End
    
    PDFFlow --> CreatePDF[PDF Oluştur<br/>ReportLab]
    CreatePDF --> SetupPage[Sayfa Ayarları<br/>A4, Portrait/Landscape]
    SetupPage --> DrawHeader[Başlık Çiz<br/>Otel Adı, Logo]
    DrawHeader --> DrawTable[Tablo Çiz<br/>Table widget]
    DrawTable --> DrawFooter[Altbilgi Çiz<br/>Tarih, Sayfa No]
    DrawFooter --> SavePDF[PDF Dosyası Kaydet<br/>BytesIO]
    SavePDF --> SendPDF[Dosya Gönder<br/>send_file]
    SendPDF --> End

    style Start fill:#e1f5ff
    style QueryDB fill:#fff9c4
    style CreateWB fill:#c8e6c9
    style CreatePDF fill:#c8e6c9
    style End fill:#e1f5ff
```

---

## 8. AUDİT TRAIL AKIŞI

```mermaid
graph TD
    Start([Sistem İşlemi]) --> CheckDecorator{@audit_trail<br/>Dekoratör Var mı?}
    
    CheckDecorator -->|Hayır| DirectOp[Direkt İşlem]
    DirectOp --> End([Bitiş])
    
    CheckDecorator -->|Evet| BeforeOp[İşlem Öncesi<br/>Durum Kaydet]
    BeforeOp --> ExecuteOp[İşlem Yürüt]
    ExecuteOp --> OpSuccess{İşlem<br/>Başarılı mı?}
    
    OpSuccess -->|Hayır| LogError[Hata Logla<br/>HataLog Tablosu]
    LogError --> End
    
    OpSuccess -->|Evet| AfterOp[İşlem Sonrası<br/>Durum Kaydet]
    AfterOp --> DetectChange[Değişiklikleri Tespit Et<br/>Eski vs Yeni]
    
    DetectChange --> HasChange{Değişiklik<br/>Var mı?}
    
    HasChange -->|Hayır| NoAudit[Audit Kaydetme]
    NoAudit --> End
    
    HasChange -->|Evet| SerializeOld[Eski Değerleri<br/>JSON'a Çevir]
    SerializeOld --> SerializeNew[Yeni Değerleri<br/>JSON'a Çevir]
    SerializeNew --> CreateSummary[İnsan Okunabilir<br/>Özet Oluştur]
    
    CreateSummary --> GetContext[Bağlam Bilgileri:<br/>- Kullanıcı ID<br/>- IP Adresi<br/>- User Agent<br/>- Oturum ID]
    
    GetContext --> CreateAudit[AuditLog Kaydı Oluştur:<br/>- Tablo Adı<br/>- İşlem Tipi<br/>- Kayıt ID<br/>- Eski Değerler JSON<br/>- Yeni Değerler JSON<br/>- Değişiklik Özeti<br/>- Kullanıcı<br/>- IP<br/>- Timestamp]
    
    CreateAudit --> SaveAudit[Veritabanına Kaydet]
    SaveAudit --> IndexLog[Full-text Index<br/>Arama için]
    IndexLog --> End

    style Start fill:#e1f5ff
    style CreateAudit fill:#c8e6c9
    style LogError fill:#ffcdd2
    style End fill:#e1f5ff
```

**Audit Trail Örnek Kayıt:**
```json
{
  "tablo_adi": "urunler",
  "islem_tipi": "update",
  "kayit_id": 15,
  "eski_deger": {
    "urun_adi": "Coca Cola",
    "birim_fiyat": 5.50,
    "kritik_seviye": 100
  },
  "yeni_deger": {
    "urun_adi": "Coca Cola",
    "birim_fiyat": 6.00,
    "kritik_seviye": 150
  },
  "degisiklik_ozeti": "Birim fiyat 5.50 TL'den 6.00 TL'ye güncellendi. Kritik seviye 100'den 150'ye yükseltildi.",
  "kullanici_id": 3,
  "ip_adresi": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "oturum_id": "abc123xyz",
  "timestamp": "2025-10-31 14:45:23"
}
```

---

## 9. GÜVENLİK VE RATE LİMİTİNG AKIŞI

```mermaid
graph TD
    Start([HTTP İstek]) --> ParseRequest[İstek Parse Et]
    ParseRequest --> CheckCSRF{POST/PUT/DELETE?}
    
    CheckCSRF -->|Hayır GET| SkipCSRF[CSRF Atla]
    CheckCSRF -->|Evet| ValidateCSRF{CSRF Token<br/>Geçerli mi?}
    
    ValidateCSRF -->|Hayır| CSRFError[400 Bad Request<br/>CSRF Hatası]
    CSRFError --> EndError([Bitiş - Hata])
    
    ValidateCSRF -->|Evet| CheckAuth
    SkipCSRF --> CheckAuth{Kimlik Doğrulama<br/>Gerekli mi?}
    
    CheckAuth -->|Hayır| PublicRoute[Public Route]
    PublicRoute --> RateLimit
    
    CheckAuth -->|Evet| CheckSession{Session<br/>Geçerli mi?}
    
    CheckSession -->|Hayır| AuthError[401 Unauthorized<br/>Login'e Yönlendir]
    AuthError --> EndError
    
    CheckSession -->|Evet| CheckRole{Rol Kontrolü<br/>Gerekli mi?}
    
    CheckRole -->|Hayır| RoleOK[Rol Kontrolü Yok]
    RoleOK --> RateLimit
    
    CheckRole -->|Evet| ValidateRole{Kullanıcı Rolü<br/>Yeterli mi?}
    
    ValidateRole -->|Hayır| RoleError[403 Forbidden<br/>Yetki Hatası]
    RoleError --> EndError
    
    ValidateRole -->|Evet| RateLimit{Rate Limit<br/>Kontrolü}
    
    RateLimit --> CheckLoginLimit{Login Endpoint?}
    
    CheckLoginLimit -->|Evet| LoginLimit{5 İstek/Dakika<br/>Aşıldı mı?}
    LoginLimit -->|Evet| RateLimitError[429 Too Many Requests<br/>1 Saat Block]
    RateLimitError --> EndError
    LoginLimit -->|Hayır| ExecuteRoute
    
    CheckLoginLimit -->|Hayır| GeneralLimit{200 İstek/Gün<br/>Aşıldı mı?}
    GeneralLimit -->|Evet| RateLimitError
    GeneralLimit -->|Hayır| ExecuteRoute[Route Fonksiyonu Çalıştır]
    
    ExecuteRoute --> LogAccess[Erişim Logla<br/>SistemLog]
    LogAccess --> ReturnResponse[Response Dön]
    ReturnResponse --> AddHeaders[Güvenlik Headers Ekle:<br/>- CSP<br/>- X-Frame-Options<br/>- HSTS<br/>- X-Content-Type]
    AddHeaders --> EndSuccess([Bitiş - Başarılı])

    style Start fill:#e1f5ff
    style ExecuteRoute fill:#c8e6c9
    style CSRFError fill:#ffcdd2
    style AuthError fill:#ffcdd2
    style RoleError fill:#ffcdd2
    style RateLimitError fill:#ffcdd2
    style EndSuccess fill:#a5d6a7
    style EndError fill:#ffcdd2
```

---

## 10. HATA YÖNETİMİ AKIŞI

```mermaid
graph TD
    Start([İstek Geldi]) --> TryBlock{Try Bloğu}
    
    TryBlock --> ExecuteLogic[İş Mantığı Çalıştır]
    ExecuteLogic --> Success{Başarılı?}
    
    Success -->|Evet| CommitDB[DB Commit]
    CommitDB --> LogSuccess[Başarı Logla]
    LogSuccess --> ReturnSuccess[Başarı Yanıtı<br/>200/201]
    ReturnSuccess --> End([Bitiş])
    
    Success -->|Hayır Validasyon| ValidationError[Validasyon Hatası]
    ValidationError --> LogValidation[Validasyon Hatası Logla]
    LogValidation --> Return400[400 Bad Request<br/>Hata Detayları]
    Return400 --> End
    
    TryBlock -->|Exception| CatchBlock[Exception Yakalandı]
    CatchBlock --> ErrorType{Hata Tipi?}
    
    ErrorType -->|IntegrityError| DBIntegrity[Veritabanı<br/>Bütünlük Hatası]
    ErrorType -->|SQLAlchemyError| DBError[Veritabanı Hatası]
    ErrorType -->|ValidationError| ValError[Validasyon Hatası]
    ErrorType -->|PermissionError| PermError[Yetki Hatası]
    ErrorType -->|Other| GenericError[Genel Hata]
    
    DBIntegrity --> Rollback[DB Rollback]
    DBError --> Rollback
    ValError --> Rollback
    PermError --> Rollback
    GenericError --> Rollback
    
    Rollback --> LogError[HataLog Tablosuna Kaydet:<br/>- Hata Mesajı<br/>- Traceback<br/>- Kullanıcı<br/>- URL<br/>- Parametreler]
    
    LogError --> NotifyAdmin{Kritik Hata?}
    
    NotifyAdmin -->|Evet| SendAlert[Admin'e Bildirim<br/>Email/SMS Opsiyonel]
    NotifyAdmin -->|Hayır| SkipAlert[Bildirim Yok]
    
    SendAlert --> FormatError[Kullanıcı Dostu<br/>Hata Mesajı Oluştur]
    SkipAlert --> FormatError
    
    FormatError --> ReturnError[Hata Yanıtı:<br/>- 400 Validasyon<br/>- 403 Yetki<br/>- 500 Sistem]
    
    ReturnError --> RenderErrorPage{HTML İstek?}
    
    RenderErrorPage -->|Evet| ErrorTemplate[Hata Sayfası Render<br/>404.html/500.html]
    RenderErrorPage -->|Hayır| ErrorJSON[JSON Hata Yanıtı]
    
    ErrorTemplate --> End
    ErrorJSON --> End

    style Start fill:#e1f5ff
    style Success fill:#c8e6c9
    style CatchBlock fill:#ffcdd2
    style LogError fill:#fff59d
    style End fill:#e1f5ff
```

---

## 11. VERİ AKIŞ DİYAGRAMI

```mermaid
graph LR
    subgraph Kullanıcı Katmanı
        SY[Sistem Yöneticisi]
        AD[Admin]
        DS[Depo Sorumlusu]
        KS[Kat Sorumlusu]
    end
    
    subgraph Uygulama Katmanı
        Flask[Flask App]
        Auth[Authentication]
        Decorators[Security Decorators]
        Forms[WTForms Validation]
        Helpers[Helper Functions]
    end
    
    subgraph Veri Katmanı
        SQLAlchemy[SQLAlchemy ORM]
        DB[(MySQL Database)]
    end
    
    subgraph Dış Sistemler
        Railway[Railway Platform]
        Logs[Log Files]
        Reports[Excel/PDF Reports]
    end
    
    SY -->|HTTP İstek| Flask
    AD -->|HTTP İstek| Flask
    DS -->|HTTP İstek| Flask
    KS -->|HTTP İstek| Flask
    
    Flask --> Auth
    Auth --> Decorators
    Decorators --> Forms
    Forms --> Helpers
    
    Helpers --> SQLAlchemy
    SQLAlchemy --> DB
    
    DB -->|Sorgu Sonucu| SQLAlchemy
    SQLAlchemy -->|Model Nesneleri| Helpers
    Helpers -->|İşlenmiş Veri| Flask
    
    Flask -->|HTML/JSON| SY
    Flask -->|HTML/JSON| AD
    Flask -->|HTML/JSON| DS
    Flask -->|HTML/JSON| KS
    
    Flask -->|Sistem Logları| Logs
    Flask -->|Hata Logları| Logs
    
    Helpers -->|Excel/PDF| Reports
    Reports -->|Download| SY
    Reports -->|Download| DS
    
    Railway -->|ENV Variables| Flask
    Railway -->|Database URL| DB

    style Flask fill:#42a5f5
    style DB fill:#66bb6a
    style Auth fill:#ffa726
    style Reports fill:#ab47bc
```

---

## 12. DEPLOYMENT AKIŞI (RAILWAY)

```mermaid
graph TD
    Start([Deployment Başlat]) --> GitPush[Git Push to Main]
    GitPush --> RailwayDetect[Railway Webhook Tetiklenir]
    RailwayDetect --> CloneRepo[Repository Clone]
    CloneRepo --> DetectRuntime[Runtime Detect<br/>runtime.txt]
    
    DetectRuntime --> InstallPython[Python 3.11 Kurulumu]
    InstallPython --> InstallDeps[Pip Install<br/>requirements.txt]
    InstallDeps --> CheckProcfile[Procfile Oku]
    CheckProcfile --> SetEnv[ENV Variables Ayarla:<br/>- DATABASE_URL<br/>- SECRET_KEY<br/>- FLASK_ENV]
    
    SetEnv --> DBConnection[MySQL Bağlantı Test]
    DBConnection --> DBOk{Bağlantı OK?}
    
    DBOk -->|Hayır| DBError[Deployment Hatası<br/>DB Connection Failed]
    DBError --> NotifyFail[Hata Bildirimi]
    NotifyFail --> EndFail([Deployment Başarısız])
    
    DBOk -->|Evet| RunMigrations[DB Migrations<br/>SQLAlchemy]
    RunMigrations --> CreateTables[Tabloları Oluştur<br/>db.create_all]
    CreateTables --> CheckSetup{Setup Yapılmış mı?}
    
    CheckSetup -->|Hayır| FirstRun[İlk Çalıştırma<br/>Setup Gerekli]
    CheckSetup -->|Evet| StartApp
    
    FirstRun --> StartApp[Gunicorn Start<br/>web: gunicorn app:app]
    StartApp --> HealthCheck[Health Check<br/>/ Endpoint]
    HealthCheck --> HealthOk{200 OK?}
    
    HealthOk -->|Hayır| AppError[App Start Hatası]
    AppError --> NotifyFail
    
    HealthOk -->|Evet| AssignDomain[Domain Ata<br/>*.up.railway.app]
    AssignDomain --> EnableHTTPS[HTTPS Sertifika<br/>Let's Encrypt]
    EnableHTTPS --> NotifySuccess[Deployment Başarılı<br/>Bildirim]
    NotifySuccess --> Monitor[Monitoring Başlat<br/>CPU, RAM, DB]
    Monitor --> EndSuccess([Deployment Başarılı<br/>App Live])

    style Start fill:#e1f5ff
    style StartApp fill:#c8e6c9
    style DBError fill:#ffcdd2
    style AppError fill:#ffcdd2
    style EndSuccess fill:#a5d6a7
    style EndFail fill:#ffcdd2
```

---

## 13. KRİTİK İŞ AKIŞLARI

### 13.1 Günlük İş Akışı - Kat Sorumlusu

```
1. Sabah (08:00)
   └─ Login yap
   └─ Dashboard kontrol et
      ├─ Zimmet durumunu gör
      └─ Son minibar işlemlerini incele

2. Oda Kontrolleri (09:00-12:00)
   └─ Her oda için:
      ├─ Minibar kontrol et (Kontrol işlemi)
      ├─ Tüketim varsa not al
      └─ Sonraki odaya geç

3. Minibar Doldurma (13:00-17:00)
   └─ Her oda için:
      ├─ Gerçek stok say
      ├─ Tüketimi kaydet
      ├─ Eksikleri doldur
      └─ Zimmetten düş

4. Toplu İşlemler (Gerektiğinde)
   └─ Aynı ürün için birden fazla oda
   └─ Toplu oda doldurma kullan

5. Akşam (17:30)
   └─ Zimmet durumunu kontrol et
   └─ Yetersiz zimmet varsa Depo'dan talep et
   └─ Günlük rapor oluştur
   └─ Logout
```

### 13.2 Günlük İş Akışı - Depo Sorumlusu

```
1. Sabah (08:00)
   └─ Login yap
   └─ Dashboard kontrol et
      ├─ Kritik stok uyarıları
      ├─ Zimmet talepleri
      └─ Minibar durumları

2. Stok Kontrolü (09:00-10:00)
   └─ Kritik stok ürünleri tespit et
   └─ Sipariş listesi hazırla
   └─ Satın alma ile iletişim

3. Stok Girişi (10:00-12:00)
   └─ Gelen ürünleri kaydet
   └─ Stok giriş işlemi yap
   └─ Depo yerleşimi

4. Zimmet Yönetimi (13:00-15:00)
   └─ Kat sorumlularından gelen talepler
   └─ Zimmet atama yap
   └─ Stoktan düşüm kontrolü

5. Minibar Takip (15:00-17:00)
   └─ Minibar durumlarını incele
   └─ Anormal tüketim tespit et
   └─ Oda bazlı ürün geçmişi

6. Raporlama (17:00-18:00)
   └─ Günlük stok raporu
   └─ Zimmet özet raporu
   └─ Kritik stok listesi
   └─ Logout
```

---

## 14. PERFORMANS OPTİMİZASYON AKIŞI

```mermaid
graph TD
    Request([HTTP İstek]) --> Cache{Cache Mevcut?}
    
    Cache -->|Evet| ReturnCache[Cache'den Dön<br/>Hızlı]
    ReturnCache --> End([Bitiş])
    
    Cache -->|Hayır| DBQuery[Veritabanı Sorgusu]
    DBQuery --> Optimize{Query Optimize?}
    
    Optimize -->|Evet| UseIndex[Index Kullan<br/>Hızlı Arama]
    Optimize -->|Hayır| FullScan[Full Table Scan<br/>Yavaş]
    
    UseIndex --> Pagination{Sayfalama Gerekli?}
    FullScan --> Pagination
    
    Pagination -->|Evet| LimitOffset[LIMIT & OFFSET<br/>SQL]
    Pagination -->|Hayır| AllData[Tüm Veri]
    
    LimitOffset --> ProcessData[Veri İşle]
    AllData --> ProcessData
    
    ProcessData --> Serialize[JSON Serialize]
    Serialize --> CacheStore{Cache'le?}
    
    CacheStore -->|Evet| StoreCache[Cache'e Kaydet<br/>TTL: 5 dakika]
    CacheStore -->|Hayır| SkipCache[Cache Atla]
    
    StoreCache --> Compress{Sıkıştır?}
    SkipCache --> Compress
    
    Compress -->|Evet Büyük| Gzip[GZip Sıkıştırma]
    Compress -->|Hayır| Normal[Normal Yanıt]
    
    Gzip --> ReturnResponse[Response Dön]
    Normal --> ReturnResponse
    ReturnResponse --> End

    style Request fill:#e1f5ff
    style ReturnCache fill:#c8e6c9
    style UseIndex fill:#fff9c4
    style FullScan fill:#ffcdd2
    style End fill:#e1f5ff
```



