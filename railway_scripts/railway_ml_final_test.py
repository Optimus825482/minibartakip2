"""
Railway ML Sistemi Final Test
Tüm ML bileşenlerinin çalıştığını doğrular
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv('.env.railway')

DATABASE_URL = os.getenv('RAILWAY_DATABASE_URL')
engine = create_engine(DATABASE_URL)

print("=" * 70)
print("🎯 RAILWAY ML SİSTEMİ - FİNAL TEST")
print("=" * 70)
print()

with engine.connect() as conn:
    try:
        # 1. Bağlantı testi
        print("1️⃣  Bağlantı Testi")
        result = conn.execute(text("SELECT version()"))
        version = result.fetchone()[0].split(',')[0]
        print(f"   ✅ {version}")
        print()
        
        # 2. ML Tabloları
        print("2️⃣  ML Tabloları")
        ml_tables = ['ml_metrics', 'ml_models', 'ml_alerts', 'ml_training_logs']
        for table in ml_tables:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = result.fetchone()[0]
            print(f"   ✅ {table:25} Hazır ({count} kayıt)")
        print()
        
        # 3. Enum Değerleri
        print("3️⃣  Enum Değerleri")
        
        result = conn.execute(text("""
            SELECT e.enumlabel 
            FROM pg_enum e
            JOIN pg_type t ON e.enumtypid = t.oid
            WHERE t.typname = 'ml_metric_type'
            ORDER BY e.enumlabel
        """))
        metrics = [row[0] for row in result]
        print(f"   ✅ ml_metric_type: {len(metrics)} değer")
        print(f"      {', '.join(metrics[:3])}...")
        
        result = conn.execute(text("""
            SELECT e.enumlabel 
            FROM pg_enum e
            JOIN pg_type t ON e.enumtypid = t.oid
            WHERE t.typname = 'ml_alert_type'
            ORDER BY e.enumlabel
        """))
        alerts = [row[0] for row in result]
        print(f"   ✅ ml_alert_type: {len(alerts)} değer")
        print(f"      {', '.join(alerts[:3])}...")
        
        result = conn.execute(text("""
            SELECT e.enumlabel 
            FROM pg_enum e
            JOIN pg_type t ON e.enumtypid = t.oid
            WHERE t.typname = 'ml_alert_severity'
            ORDER BY e.enumlabel
        """))
        severities = [row[0] for row in result]
        print(f"   ✅ ml_alert_severity: {len(severities)} değer")
        print(f"      {', '.join(severities)}")
        print()
        
        # 4. Index'ler
        print("4️⃣  Index'ler")
        result = conn.execute(text("""
            SELECT COUNT(*) 
            FROM pg_indexes 
            WHERE schemaname = 'public' 
            AND tablename LIKE 'ml_%'
        """))
        index_count = result.fetchone()[0]
        print(f"   ✅ {index_count} adet index kurulu")
        print()
        
        # 5. Foreign Key'ler
        print("5️⃣  Foreign Key İlişkileri")
        result = conn.execute(text("""
            SELECT 
                tc.table_name,
                kcu.column_name,
                ccu.table_name AS foreign_table_name
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
            AND tc.table_name LIKE 'ml_%'
            ORDER BY tc.table_name
        """))
        
        fk_count = 0
        for row in result:
            print(f"   ✅ {row[0]}.{row[1]} → {row[2]}")
            fk_count += 1
        
        if fk_count == 0:
            print("   ℹ️  Foreign key yok (bazı tablolarda normal)")
        print()
        
        # 6. Test Sorguları
        print("6️⃣  Test Sorguları")
        
        # ml_alerts test
        result = conn.execute(text("""
            SELECT COUNT(*) 
            FROM ml_alerts 
            WHERE is_read = false
        """))
        print(f"   ✅ Okunmamış uyarılar sorgusu çalışıyor")
        
        # ml_metrics test
        result = conn.execute(text("""
            SELECT COUNT(*) 
            FROM ml_metrics 
            WHERE is_anomali = true
        """))
        print(f"   ✅ Anomali sorgusu çalışıyor")
        
        # ml_models test
        result = conn.execute(text("""
            SELECT COUNT(*) 
            FROM ml_models 
            WHERE aktif = true
        """))
        print(f"   ✅ Aktif model sorgusu çalışıyor")
        
        print()
        print("=" * 70)
        print("🎉 TÜM TESTLER BAŞARILI - RAILWAY ML SİSTEMİ HAZIR!")
        print("=" * 70)
        print()
        print("📌 Sonraki Adımlar:")
        print("   1. Railway Dashboard'dan uygulamayı yeniden başlatın")
        print("   2. ML veri toplama servisi otomatik başlayacak")
        print("   3. Anomali tespiti aktif olacak")
        print("   4. Dashboard'da ML uyarıları görünecek")
        print()
        
    except Exception as e:
        print(f"\n❌ TEST BAŞARISIZ: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
