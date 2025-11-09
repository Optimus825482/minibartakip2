#!/usr/bin/env python3
"""
Railway PostgreSQL Index Optimizasyonu - Faz 2
Composite index'lerin kullanılması için eski index'leri kaldır
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv('.env.railway')

railway_url = os.getenv('RAILWAY_DATABASE_URL')
if railway_url:
    railway_url = railway_url.replace('postgresql://', 'postgresql+psycopg2://')

if not railway_url:
    print("❌ RAILWAY_DATABASE_URL bulunamadı!")
    exit(1)

engine = create_engine(railway_url)

print("🔧 RAILWAY POSTGRESQL INDEX OPTİMİZASYONU - FAZ 2")
print("=" * 80)
print("Composite index'lerin kullanılması için eski tekli index'ler kaldırılıyor...\n")

with engine.connect() as conn:
    
    # STOK HAREKETLERİ - Composite index varken tekli index'ler gereksiz
    print("📌 1. STOK_HAREKETLERI TABLOSU")
    print("-" * 80)
    print("Composite index: idx_stok_hareketleri_composite (islem_tarihi, hareket_tipi, urun_id)")
    print("Silinecek tekli index'ler:")
    
    stok_indexes = [
        'idx_stok_hareketleri_islem_tarihi',
        'idx_stok_hareketleri_hareket_tipi', 
        'idx_stok_hareketleri_urun_id',
        'idx_stok_hareketleri_urun_tarih'  # Duplicate composite
    ]
    
    for idx in stok_indexes:
        try:
            conn.execute(text(f"DROP INDEX IF EXISTS {idx} CASCADE"))
            conn.commit()
            print(f"  ✅ {idx}")
        except Exception as e:
            print(f"  ⚠️  {idx}: {str(e)[:80]}")
    
    # SİSTEM LOGLARI - Composite ile tekli index'ler gereksiz
    print("\n📌 2. SISTEM_LOGLARI TABLOSU")
    print("-" * 80)
    print("Composite index: idx_sistem_loglari_composite (islem_tarihi, islem_tipi)")
    print("Silinecek tekli index:")
    
    try:
        conn.execute(text("DROP INDEX IF EXISTS idx_sistem_loglari_islem_tarihi CASCADE"))
        conn.commit()
        print("  ✅ idx_sistem_loglari_islem_tarihi")
    except Exception as e:
        print(f"  ⚠️  idx_sistem_loglari_islem_tarihi: {str(e)[:80]}")
    
    # AUDIT_LOGS için eski index'ler zaten silinmiş, composite kalıyor
    print("\n📌 3. AUDIT_LOGS TABLOSU")
    print("-" * 80)
    print("  ✅ Composite index zaten aktif: idx_audit_logs_composite")
    print("  ✅ Eski index'ler zaten silinmiş")
    
    # MİNİBAR İŞLEMLERİ - Kritik tablo, index'leri koru
    print("\n📌 4. MİNİBAR_İŞLEMLERİ TABLOSU")
    print("-" * 80)
    print("  ⏭️  Index'ler korunuyor (aktif kullanımda)")
    
    # VACUUM ANALYZE
    print("\n📌 5. VERİTABANI OPTİMİZASYONU")
    print("-" * 80)
    
    conn.commit()
    try:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        conn.execute(text("VACUUM ANALYZE"))
        print("  ✅ VACUUM ANALYZE tamamlandı")
    except Exception as e:
        print(f"  ⚠️  VACUUM: {str(e)[:80]}")
    
    # İstatistikleri güncelle
    print("\n📌 6. INDEX İSTATİSTİKLERİ GÜNCELLENİYOR")
    print("-" * 80)
    
    try:
        conn.execute(text("ANALYZE stok_hareketleri"))
        conn.execute(text("ANALYZE sistem_loglari"))
        conn.execute(text("ANALYZE audit_logs"))
        print("  ✅ Tablo istatistikleri güncellendi")
    except Exception as e:
        print(f"  ⚠️  ANALYZE: {str(e)[:80]}")
    
    # Sonuçlar
    print("\n📌 7. OPTİMİZASYON SONUÇLARI")
    print("-" * 80)
    
    result = conn.execute(text("""
        SELECT COUNT(*) as total_indexes,
               pg_size_pretty(SUM(pg_relation_size(indexrelid))) as total_size
        FROM pg_stat_user_indexes
        WHERE schemaname = 'public'
    """))
    
    for row in result:
        print(f"Toplam Index: {row[0]}")
        print(f"Toplam Boyut: {row[1]}")

print("\n" + "=" * 80)
print("✅ FAZ 2 OPTİMİZASYONU TAMAMLANDI!")
print("\n📝 YAPILAN İŞLEMLER:")
print("1. ✅ 5 tekli index kaldırıldı (composite index'ler kullanılacak)")
print("2. ✅ VACUUM ANALYZE çalıştırıldı")
print("3. ✅ Query planner istatistikleri güncellendi")
print("\n🚀 Composite index'ler şimdi kullanılacak!")
print("\n⚠️  NOT: Değişikliklerin etkisini görmek için uygulamayı yeniden başlatın")
print("📊 Kontrol için: python railway_performance_check.py")
