#!/usr/bin/env python3
"""
Eksik index'leri oluştur
"""
import os
import psycopg2

def create_indexes():
    """Eksik index'leri oluştur"""
    
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL environment variable bulunamadı!")
        return False
    
    # Oluşturulacak index'ler
    indexes = [
        # Kullanıcılar
        "CREATE INDEX IF NOT EXISTS idx_kullanicilar_rol ON kullanicilar(rol);",
        "CREATE INDEX IF NOT EXISTS idx_kullanicilar_aktif ON kullanicilar(aktif);",
        
        # Stok Hareketleri (EN ÖNEMLİ!)
        "CREATE INDEX IF NOT EXISTS idx_stok_hareketleri_urun_id ON stok_hareketleri(urun_id);",
        "CREATE INDEX IF NOT EXISTS idx_stok_hareketleri_hareket_tipi ON stok_hareketleri(hareket_tipi);",
        "CREATE INDEX IF NOT EXISTS idx_stok_hareketleri_islem_tarihi ON stok_hareketleri(islem_tarihi);",
        "CREATE INDEX IF NOT EXISTS idx_stok_hareketleri_urun_tarih ON stok_hareketleri(urun_id, islem_tarihi);",
        
        # Minibar İşlemleri (ÇOK ÖNEMLİ!)
        "CREATE INDEX IF NOT EXISTS idx_minibar_islemleri_oda_id ON minibar_islemleri(oda_id);",
        "CREATE INDEX IF NOT EXISTS idx_minibar_islemleri_personel_id ON minibar_islemleri(personel_id);",
        "CREATE INDEX IF NOT EXISTS idx_minibar_islemleri_islem_tarihi ON minibar_islemleri(islem_tarihi);",
        "CREATE INDEX IF NOT EXISTS idx_minibar_islemleri_islem_tipi ON minibar_islemleri(islem_tipi);",
        
        # Minibar İşlem Detayları
        "CREATE INDEX IF NOT EXISTS idx_minibar_islem_detay_islem_id ON minibar_islem_detay(islem_id);",
        "CREATE INDEX IF NOT EXISTS idx_minibar_islem_detay_urun_id ON minibar_islem_detay(urun_id);",
        
        # Odalar
        "CREATE INDEX IF NOT EXISTS idx_odalar_kat_id ON odalar(kat_id);",
        "CREATE INDEX IF NOT EXISTS idx_odalar_aktif ON odalar(aktif);",
        
        # Katlar
        "CREATE INDEX IF NOT EXISTS idx_katlar_aktif ON katlar(aktif);",
        
        # Ürünler
        "CREATE INDEX IF NOT EXISTS idx_urunler_grup_id ON urunler(grup_id);",
        "CREATE INDEX IF NOT EXISTS idx_urunler_aktif ON urunler(aktif);",
        
        # Personel Zimmet
        "CREATE INDEX IF NOT EXISTS idx_personel_zimmet_personel_id ON personel_zimmet(personel_id);",
        "CREATE INDEX IF NOT EXISTS idx_personel_zimmet_durum ON personel_zimmet(durum);",
        "CREATE INDEX IF NOT EXISTS idx_personel_zimmet_zimmet_tarihi ON personel_zimmet(zimmet_tarihi);",
        
        # Dolum Talepleri
        "CREATE INDEX IF NOT EXISTS idx_minibar_dolum_talepleri_oda_id ON minibar_dolum_talepleri(oda_id);",
        "CREATE INDEX IF NOT EXISTS idx_minibar_dolum_talepleri_durum ON minibar_dolum_talepleri(durum);",
        "CREATE INDEX IF NOT EXISTS idx_minibar_dolum_talepleri_talep_tarihi ON minibar_dolum_talepleri(talep_tarihi);",
        
        # Audit Logs
        "CREATE INDEX IF NOT EXISTS idx_audit_logs_kullanici_id ON audit_logs(kullanici_id);",
        "CREATE INDEX IF NOT EXISTS idx_audit_logs_islem_tarihi ON audit_logs(islem_tarihi);",
        "CREATE INDEX IF NOT EXISTS idx_audit_logs_islem_tipi ON audit_logs(islem_tipi);",
        "CREATE INDEX IF NOT EXISTS idx_audit_logs_tablo_adi ON audit_logs(tablo_adi);",
        
        # Sistem Logları
        "CREATE INDEX IF NOT EXISTS idx_sistem_loglari_log_seviyesi ON sistem_loglari(log_seviyesi);",
        "CREATE INDEX IF NOT EXISTS idx_sistem_loglari_olusturma_tarihi ON sistem_loglari(olusturma_tarihi);",
        
        # Hata Logları
        "CREATE INDEX IF NOT EXISTS idx_hata_loglari_olusturma_tarihi ON hata_loglari(olusturma_tarihi);",
    ]
    
    try:
        conn = psycopg2.connect(database_url)
        conn.autocommit = True
        cur = conn.cursor()
        
        print("=" * 80)
        print("RAILWAY POSTGRESQL INDEX OLUŞTURMA")
        print("=" * 80)
        print(f"\n📝 {len(indexes)} index oluşturulacak...\n")
        
        success_count = 0
        error_count = 0
        
        for i, index_sql in enumerate(indexes, 1):
            try:
                # Index adını çıkar
                index_name = index_sql.split("idx_")[1].split(" ")[0]
                
                print(f"[{i}/{len(indexes)}] Oluşturuluyor: idx_{index_name}...", end=" ")
                
                cur.execute(index_sql)
                
                print("✅")
                success_count += 1
                
            except Exception as e:
                print(f"❌ Hata: {e}")
                error_count += 1
        
        print("\n" + "=" * 80)
        print(f"✅ Başarılı: {success_count}")
        print(f"❌ Hatalı: {error_count}")
        print("=" * 80)
        
        # Index'leri kontrol et
        print("\n📊 Oluşturulan index'ler kontrol ediliyor...\n")
        
        cur.execute("""
            SELECT 
                schemaname,
                tablename,
                indexname,
                pg_size_pretty(pg_relation_size(indexname::regclass)) as index_size
            FROM pg_indexes
            WHERE schemaname = 'public'
            AND indexname LIKE 'idx_%'
            ORDER BY tablename, indexname;
        """)
        
        for schema, table, index_name, size in cur.fetchall():
            print(f"   ✅ {table}.{index_name} ({size})")
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("\n⚠️  DİKKAT: Bu işlem birkaç dakika sürebilir!\n")
    
    if create_indexes():
        print("\n✅ Tüm index'ler başarıyla oluşturuldu!")
        print("\n💡 Uygulama artık çok daha hızlı çalışacak!")
    else:
        print("\n❌ Index oluşturma başarısız!")
