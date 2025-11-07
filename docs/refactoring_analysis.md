# App.py Refactoring Analiz Raporu

**Oluşturulma Tarihi:** 07.11.2025 21:54:27

## Özet

- **Toplam Route Sayısı:** 99
- **Kullanılan Route Sayısı:** 59
- **Kullanılmayan Route Sayısı:** 40
- **Template'lerde Kullanılan Endpoint:** 65
- **JS'de Kullanılan API Endpoint:** 5

## Kullanılan Route'lar

| Path | Methods | Function | Kullanıldığı Yerler |
|------|---------|----------|---------------------|
| `/admin/depo-stoklari` | GET | `admin_depo_stoklari` | components\admin_sidebar.html, base.html, sistem_yoneticisi\depo_stoklari.html |
| `/admin/minibar-durumlari` | GET | `admin_minibar_durumlari` | sistem_yoneticisi\admin_minibar_durumlari.html, components\admin_sidebar.html |
| `/admin/minibar-islemleri` | GET | `admin_minibar_islemleri` | components\admin_sidebar.html, sistem_yoneticisi\admin_minibar_islemleri.html |
| `/admin/minibar-sifirla` | GET, POST | `admin_minibar_sifirla` | components\admin_sidebar.html, base.html, sistem_yoneticisi\minibar_sifirla.html |
| `/admin/oda-minibar-detay/<int:oda_id>` | GET | `admin_oda_minibar_detay` | sistem_yoneticisi\admin_minibar_durumlari.html, sistem_yoneticisi\oda_minibar_stoklari.html |
| `/admin/oda-minibar-stoklari` | GET | `admin_oda_minibar_stoklari` | sistem_yoneticisi\oda_minibar_stoklari.html, sistem_yoneticisi\oda_minibar_detay.html, components\admin_sidebar.html (+1 daha) |
| `/admin/personel-zimmetleri` | GET | `admin_personel_zimmetleri` | components\admin_sidebar.html, sistem_yoneticisi\admin_zimmet_detay.html, sistem_yoneticisi\admin_personel_zimmetleri.html |
| `/admin/stok-giris` | GET, POST | `admin_stok_giris` | sistem_yoneticisi\admin_stok_giris.html |
| `/admin/stok-hareketleri` | GET | `admin_stok_hareketleri` | sistem_yoneticisi\admin_stok_giris.html, components\admin_sidebar.html, sistem_yoneticisi\admin_stok_hareketleri.html |
| `/admin/zimmet-detay/<int:zimmet_id>` | GET | `admin_zimmet_detay` | sistem_yoneticisi\admin_personel_zimmetleri.html |
| `/admin/zimmet-iade/<int:zimmet_id>` | POST | `admin_zimmet_iade` | sistem_yoneticisi\admin_zimmet_detay.html |
| `/api/kat-sorumlusu/minibar-urunler` | POST | `api_minibar_urunler` | js\oda_kontrol.js |
| `/api/kat-sorumlusu/yeniden-dolum` | POST | `api_yeniden_dolum` | js\oda_kontrol.js |
| `/api/odalar` | GET | `api_odalar` | js\admin_qr.js |
| `/depo-raporlar` | GET | `depo_raporlar` | base.html, depo_sorumlusu\dashboard.html, depo_sorumlusu\raporlar.html |
| `/dolum-talepleri` | GET | `dolum_talepleri` | base.html |
| `/excel-export/<rapor_tipi>` | GET | `excel_export` | kat_sorumlusu\raporlar.html, depo_sorumlusu\raporlar.html |
| `/grup-aktif-yap/<int:grup_id>` | POST | `grup_aktif_yap` | admin\urun_gruplari.html |
| `/grup-duzenle/<int:grup_id>` | GET, POST | `grup_duzenle` | admin\urun_gruplari.html |
| `/grup-pasif-yap/<int:grup_id>` | POST | `grup_pasif_yap` | admin\urun_gruplari.html |
| `/kat-bazli-rapor` | GET | `kat_bazli_rapor` | base.html |
| `/kat-duzenle/<int:kat_id>` | GET, POST | `kat_duzenle` | sistem_yoneticisi\kat_tanimla.html |
| `/kat-raporlar` | GET | `kat_raporlar` | kat_sorumlusu\raporlar.html, base.html |
| `/kat-sil/<int:kat_id>` | POST | `kat_sil` | sistem_yoneticisi\kat_tanimla.html |
| `/kat-sorumlusu/ilk-dolum` | GET, POST | `ilk_dolum` | base.html, kat_sorumlusu\dashboard.html |
| `/kat-sorumlusu/kritik-stoklar` | GET | `kat_sorumlusu_kritik_stoklar` | base.html, kat_sorumlusu\dashboard.html, kat_sorumlusu\siparis_hazirla.html |
| `/kat-sorumlusu/oda-kontrol` | GET | `oda_kontrol` | base.html, kat_sorumlusu\dashboard.html |
| `/kat-sorumlusu/siparis-hazirla` | GET, POST | `kat_sorumlusu_siparis_hazirla` | kat_sorumlusu\siparis_hazirla.html, base.html, kat_sorumlusu\dashboard.html (+1 daha) |
| `/kat-sorumlusu/zimmet-export` | GET | `kat_sorumlusu_zimmet_export` | kat_sorumlusu\zimmet_stoklarim.html |
| `/kat-sorumlusu/zimmet-stoklarim` | GET | `kat_sorumlusu_zimmet_stoklarim` | base.html, kat_sorumlusu\dashboard.html, kat_sorumlusu\urun_gecmisi.html |
| `/kat-tanimla` | GET, POST | `kat_tanimla` | sistem_yoneticisi\dashboard_old.html, base.html, sistem_yoneticisi\dashboard.html (+2 daha) |
| `/minibar-durumlari` | GET | `minibar_durumlari` | depo_sorumlusu\minibar_durumlari.html, base.html |
| `/oda-sil/<int:oda_id>` | POST | `oda_sil` | sistem_yoneticisi\oda_tanimla.html |
| `/oda-tanimla` | GET, POST | `oda_tanimla` | sistem_yoneticisi\dashboard_old.html, sistem_yoneticisi\oda_duzenle.html, base.html (+2 daha) |
| `/otel-tanimla` | GET, POST | `otel_tanimla` | sistem_yoneticisi\dashboard.html, components\admin_sidebar.html, base.html (+1 daha) |
| `/pdf-export/<rapor_tipi>` | GET | `pdf_export` | kat_sorumlusu\raporlar.html, depo_sorumlusu\raporlar.html |
| `/personel-aktif-yap/<int:personel_id>` | POST | `personel_aktif_yap` | admin\personel_tanimla.html |
| `/personel-duzenle/<int:personel_id>` | GET, POST | `personel_duzenle` | admin\personel_tanimla.html |
| `/personel-pasif-yap/<int:personel_id>` | POST | `personel_pasif_yap` | admin\personel_tanimla.html |
| `/personel-tanimla` | GET, POST | `personel_tanimla` | admin\dashboard.html, sistem_yoneticisi\dashboard_old.html, sistem_yoneticisi\dashboard.html (+3 daha) |
| `/personel-zimmet` | GET, POST | `personel_zimmet` | depo_sorumlusu\zimmet_detay.html, base.html, depo_sorumlusu\dashboard.html |
| `/railwaysync` | GET | `railway_sync_page` | system_backup.html |
| `/resetsystem` | GET, POST | `reset_system` | reset_system.html |
| `/sistem-loglari` | GET | `sistem_loglari` | components\admin_sidebar.html, sistem_yoneticisi\sistem_loglari.html |
| `/sistem-yoneticisi/audit-trail` | GET | `audit_trail` | components\admin_sidebar.html, base.html, sistem_yoneticisi\audit_trail.html |
| `/sistem-yoneticisi/dolum-talepleri` | GET | `admin_dolum_talepleri` | components\admin_sidebar.html, base.html |
| `/stok-duzenle/<int:hareket_id>` | GET, POST | `stok_duzenle` | depo_sorumlusu\stok_duzenle.html, depo_sorumlusu\stok_giris.html, depo_sorumlusu\dashboard.html |
| `/stok-giris` | GET, POST | `stok_giris` | depo_sorumlusu\stok_duzenle.html, base.html, depo_sorumlusu\dashboard.html |
| `/stok-sil/<int:hareket_id>` | POST | `stok_sil` | depo_sorumlusu\stok_giris.html |
| `/systembackupsuperadmin` | GET, POST | `system_backup_login` | super_admin_login.html |
| `/systembackupsuperadmin/download` | POST | `system_backup_download` | system_backup.html |
| `/systembackupsuperadmin/panel` | GET | `system_backup_panel` | railway_sync.html |
| `/toplu-oda-doldurma` | GET | `toplu_oda_doldurma` | base.html |
| `/urun-aktif-yap/<int:urun_id>` | POST | `urun_aktif_yap` | admin\urunler.html |
| `/urun-duzenle/<int:urun_id>` | GET, POST | `urun_duzenle` | admin\urunler.html |
| `/urun-gruplari` | GET, POST | `urun_gruplari` | admin\dashboard.html, sistem_yoneticisi\dashboard_old.html, base.html (+2 daha) |
| `/urun-pasif-yap/<int:urun_id>` | POST | `urun_pasif_yap` | admin\urunler.html |
| `/urunler` | GET, POST | `urunler` | admin\dashboard.html, sistem_yoneticisi\dashboard_old.html, admin\urun_duzenle.html (+3 daha) |
| `/zimmet-detay/<int:zimmet_id>` | GET | `zimmet_detay` | depo_sorumlusu\personel_zimmet.html, depo_sorumlusu\raporlar.html |

## ⚠️ Kullanılmayan Route'lar

**DİKKAT:** Bu route'lar template veya JS dosyalarında tespit edilemedi.
Silmeden önce log kayıtlarını kontrol edin!

| Path | Methods | Function | Satır |
|------|---------|----------|-------|
| `/admin/minibar-islem-sil/<int:islem_id>` | DELETE, POST | `admin_minibar_islem_sil` | 919 |
| `/admin/stok-hareket-duzenle/<int:hareket_id>` | GET, POST | `admin_stok_hareket_duzenle` | 484 |
| `/admin/stok-hareket-sil/<int:hareket_id>` | POST | `admin_stok_hareket_sil` | 541 |
| `/admin/zimmet-iptal/<int:zimmet_id>` | POST | `admin_zimmet_iptal` | 736 |
| `/api/admin/verify-password` | POST | `api_admin_verify_password` | 323 |
| `/api/kat-rapor-veri` | GET | `api_kat_rapor_veri` | 3791 |
| `/api/kat-sorumlusu/kritik-seviye-guncelle` | POST | `api_kat_sorumlusu_kritik_seviye_guncelle` | 5703 |
| `/api/kat-sorumlusu/siparis-kaydet` | POST | `api_kat_sorumlusu_siparis_kaydet` | 5737 |
| `/api/minibar-doldur` | POST | `api_minibar_doldur` | 3401 |
| `/api/minibar-icerigi/<int:oda_id>` | GET | `api_minibar_icerigi` | 3357 |
| `/api/minibar-ilk-dolum` | POST | `api_minibar_ilk_dolum` | 2344 |
| `/api/minibar-ilk-dolum-kontrol/<int:oda_id>` | GET | `api_minibar_ilk_dolum_kontrol` | 2486 |
| `/api/minibar-islem-detay/<int:islem_id>` | GET | `api_minibar_islem_detay` | 868 |
| `/api/minibar-islem-kaydet` | POST | `api_minibar_islem_kaydet` | 2255 |
| `/api/odalar-by-kat/<int:kat_id>` | GET | `odalar_by_kat` | 2105 |
| `/api/son-aktiviteler` | GET | `api_son_aktiviteler` | 4562 |
| `/api/stok-giris` | POST | `api_stok_giris` | 2196 |
| `/api/toplu-oda-doldur` | POST | `api_toplu_oda_doldur` | 3607 |
| `/api/toplu-oda-mevcut-durum` | POST | `api_toplu_oda_mevcut_durum` | 3552 |
| `/api/tuketim-trendleri` | GET | `api_tuketim_trendleri` | 4631 |
| `/api/urun-gruplari` | GET | `api_urun_gruplari` | 2117 |
| `/api/urun-stok/<int:urun_id>` | GET | `urun_stok` | 2525 |
| `/api/urunler` | GET | `api_urunler` | 2129 |
| `/api/urunler-by-grup/<int:grup_id>` | GET | `urunler_by_grup` | 2163 |
| `/api/zimmetim` | GET | `api_zimmetim` | 2555 |
| `/grup-sil/<int:grup_id>` | POST | `grup_sil` | 1591 |
| `/kat-odalari` | GET | `kat_odalari` | 3296 |
| `/kat-sorumlusu/urun-gecmisi/<int:urun_id>` | GET | `kat_sorumlusu_urun_gecmisi` | 5628 |
| `/minibar-kontrol` | GET, POST | `minibar_kontrol` | 3123 |
| `/minibar-urun-gecmis/<int:oda_id>/<int:urun_id>` | GET | `minibar_urun_gecmis` | 2799 |
| `/minibar-urunler` | GET | `minibar_urunler` | 3319 |
| `/oda-duzenle/<int:oda_id>` | GET, POST | `oda_duzenle` | 1247 |
| `/railwaysync/check` | POST | `railway_sync_check` | 5097 |
| `/railwaysync/sync` | POST | `railway_sync_execute` | 5182 |
| `/sistem-yoneticisi/audit-trail/<int:log_id>` | GET | `audit_trail_detail` | 4776 |
| `/sistem-yoneticisi/audit-trail/export` | GET | `audit_trail_export` | 4808 |
| `/urun-sil/<int:urun_id>` | POST | `urun_sil` | 1776 |
| `/zimmet-iade/<int:detay_id>` | POST | `zimmet_iade` | 2642 |
| `/zimmet-iptal/<int:zimmet_id>` | POST | `zimmet_iptal` | 2593 |
| `/zimmetim` | GET | `zimmetim` | 3889 |

## Route Gruplandırma Önerisi

### Sistem Yöneticisi (4 route)

- `/sistem-loglari` → `sistem_loglari`
- `/otel-tanimla` → `otel_tanimla`
- `/kat-tanimla` → `kat_tanimla`
- `/oda-tanimla` → `oda_tanimla`

### Admin (3 route)

- `/personel-tanimla` → `personel_tanimla`
- `/urun-gruplari` → `urun_gruplari`
- `/urunler` → `urunler`

### Admin Minibar (7 route)

- `/admin/depo-stoklari` → `admin_depo_stoklari`
- `/admin/oda-minibar-stoklari` → `admin_oda_minibar_stoklari`
- `/admin/oda-minibar-detay/<int:oda_id>` → `admin_oda_minibar_detay`
- `/admin/minibar-sifirla` → `admin_minibar_sifirla`
- `/admin/minibar-islemleri` → `admin_minibar_islemleri`
- `/admin/minibar-islem-sil/<int:islem_id>` → `admin_minibar_islem_sil`
- `/admin/minibar-durumlari` → `admin_minibar_durumlari`

### Admin Stok (4 route)

- `/admin/stok-giris` → `admin_stok_giris`
- `/admin/stok-hareketleri` → `admin_stok_hareketleri`
- `/admin/stok-hareket-duzenle/<int:hareket_id>` → `admin_stok_hareket_duzenle`
- `/admin/stok-hareket-sil/<int:hareket_id>` → `admin_stok_hareket_sil`

### Admin Zimmet (4 route)

- `/admin/personel-zimmetleri` → `admin_personel_zimmetleri`
- `/admin/zimmet-detay/<int:zimmet_id>` → `admin_zimmet_detay`
- `/admin/zimmet-iade/<int:zimmet_id>` → `admin_zimmet_iade`
- `/admin/zimmet-iptal/<int:zimmet_id>` → `admin_zimmet_iptal`

### Depo (3 route)

- `/stok-giris` → `stok_giris`
- `/stok-duzenle/<int:hareket_id>` → `stok_duzenle`
- `/stok-sil/<int:hareket_id>` → `stok_sil`

### Kat Sorumlusu (11 route)

- `/kat-sorumlusu/zimmet-stoklarim` → `kat_sorumlusu_zimmet_stoklarim`
- `/kat-sorumlusu/kritik-stoklar` → `kat_sorumlusu_kritik_stoklar`
- `/kat-sorumlusu/siparis-hazirla` → `kat_sorumlusu_siparis_hazirla`
- `/kat-sorumlusu/urun-gecmisi/<int:urun_id>` → `kat_sorumlusu_urun_gecmisi`
- `/kat-sorumlusu/zimmet-export` → `kat_sorumlusu_zimmet_export`
- `/api/kat-sorumlusu/kritik-seviye-guncelle` → `api_kat_sorumlusu_kritik_seviye_guncelle`
- `/api/kat-sorumlusu/siparis-kaydet` → `api_kat_sorumlusu_siparis_kaydet`
- `/kat-sorumlusu/ilk-dolum` → `ilk_dolum`
- `/kat-sorumlusu/oda-kontrol` → `oda_kontrol`
- `/api/kat-sorumlusu/minibar-urunler` → `api_minibar_urunler`
- `/api/kat-sorumlusu/yeniden-dolum` → `api_yeniden_dolum`

### API (20 route)

- `/api/admin/verify-password` → `api_admin_verify_password`
- `/api/minibar-islem-detay/<int:islem_id>` → `api_minibar_islem_detay`
- `/api/odalar` → `api_odalar`
- `/api/odalar-by-kat/<int:kat_id>` → `odalar_by_kat`
- `/api/urun-gruplari` → `api_urun_gruplari`
- `/api/urunler` → `api_urunler`
- `/api/urunler-by-grup/<int:grup_id>` → `urunler_by_grup`
- `/api/stok-giris` → `api_stok_giris`
- `/api/minibar-islem-kaydet` → `api_minibar_islem_kaydet`
- `/api/minibar-ilk-dolum` → `api_minibar_ilk_dolum`
- `/api/minibar-ilk-dolum-kontrol/<int:oda_id>` → `api_minibar_ilk_dolum_kontrol`
- `/api/urun-stok/<int:urun_id>` → `urun_stok`
- `/api/zimmetim` → `api_zimmetim`
- `/api/minibar-icerigi/<int:oda_id>` → `api_minibar_icerigi`
- `/api/minibar-doldur` → `api_minibar_doldur`
- `/api/toplu-oda-mevcut-durum` → `api_toplu_oda_mevcut_durum`
- `/api/toplu-oda-doldur` → `api_toplu_oda_doldur`
- `/api/kat-rapor-veri` → `api_kat_rapor_veri`
- `/api/son-aktiviteler` → `api_son_aktiviteler`
- `/api/tuketim-trendleri` → `api_tuketim_trendleri`

### Diğer (43 route)

- `/kat-duzenle/<int:kat_id>` → `kat_duzenle`
- `/kat-sil/<int:kat_id>` → `kat_sil`
- `/oda-duzenle/<int:oda_id>` → `oda_duzenle`
- `/oda-sil/<int:oda_id>` → `oda_sil`
- `/personel-duzenle/<int:personel_id>` → `personel_duzenle`
- `/personel-pasif-yap/<int:personel_id>` → `personel_pasif_yap`
- `/personel-aktif-yap/<int:personel_id>` → `personel_aktif_yap`
- `/grup-duzenle/<int:grup_id>` → `grup_duzenle`
- `/grup-sil/<int:grup_id>` → `grup_sil`
- `/grup-pasif-yap/<int:grup_id>` → `grup_pasif_yap`
- `/grup-aktif-yap/<int:grup_id>` → `grup_aktif_yap`
- `/urun-duzenle/<int:urun_id>` → `urun_duzenle`
- `/urun-sil/<int:urun_id>` → `urun_sil`
- `/urun-pasif-yap/<int:urun_id>` → `urun_pasif_yap`
- `/urun-aktif-yap/<int:urun_id>` → `urun_aktif_yap`
- `/personel-zimmet` → `personel_zimmet`
- `/zimmet-detay/<int:zimmet_id>` → `zimmet_detay`
- `/zimmet-iptal/<int:zimmet_id>` → `zimmet_iptal`
- `/zimmet-iade/<int:detay_id>` → `zimmet_iade`
- `/minibar-durumlari` → `minibar_durumlari`
- `/minibar-urun-gecmis/<int:oda_id>/<int:urun_id>` → `minibar_urun_gecmis`
- `/depo-raporlar` → `depo_raporlar`
- `/dolum-talepleri` → `dolum_talepleri`
- `/sistem-yoneticisi/dolum-talepleri` → `admin_dolum_talepleri`
- `/minibar-kontrol` → `minibar_kontrol`
- `/kat-odalari` → `kat_odalari`
- `/minibar-urunler` → `minibar_urunler`
- `/toplu-oda-doldurma` → `toplu_oda_doldurma`
- `/kat-bazli-rapor` → `kat_bazli_rapor`
- `/zimmetim` → `zimmetim`
- `/kat-raporlar` → `kat_raporlar`
- `/excel-export/<rapor_tipi>` → `excel_export`
- `/pdf-export/<rapor_tipi>` → `pdf_export`
- `/sistem-yoneticisi/audit-trail` → `audit_trail`
- `/sistem-yoneticisi/audit-trail/<int:log_id>` → `audit_trail_detail`
- `/sistem-yoneticisi/audit-trail/export` → `audit_trail_export`
- `/resetsystem` → `reset_system`
- `/railwaysync` → `railway_sync_page`
- `/railwaysync/check` → `railway_sync_check`
- `/railwaysync/sync` → `railway_sync_execute`
- `/systembackupsuperadmin` → `system_backup_login`
- `/systembackupsuperadmin/panel` → `system_backup_panel`
- `/systembackupsuperadmin/download` → `system_backup_download`
