"""
Railway Deployment Durum Kontrolü
Tüm sistemin detaylı kontrolü
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv('.env.railway')

DATABASE_URL = os.getenv('RAILWAY_DATABASE_URL')
engine = create_engine(DATABASE_URL)

print("=" * 70)
print("🔍 RAILWAY DEPLOYMENT DURUM KONTROLÜ")
print("=" * 70)
print()

with engine.connect() as conn:
    try:
        # 1. Veritabanı Bilgileri
        print("1️⃣  VERİTABANI BİLGİLERİ")
        result = conn.execute(text("SELECT version()"))
        version = result.fetchone()[0]
        print(f"   PostgreSQL: {version.split(',')[0]}")
        
        result = conn.execute(text("SELECT pg_database_size(current_database())"))
        db_size = result.fetchone()[0]
        print(f"   Database Size: {db_size / 1024 / 1024:.2f} MB")
        
        result = conn.execute(text("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        table_count = result.fetchone()[0]
        print(f"   Toplam Tablo: {table_count}")
        print()
        
        # 2. ML Tabloları Detay
        print("2️⃣  ML TABLOLARI DETAY")
        ml_tables = {
            'ml_metrics': 'Metrik Verileri',
            'ml_models': 'ML Modelleri',
            'ml_alerts': 'Uyarılar',
            'ml_training_logs': 'Eğitim Logları'
        }
        
        for table, desc in ml_tables.items():
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = result.fetchone()[0]
            
            result = conn.execute(text(f"""
                SELECT COUNT(*) 
                FROM information_schema.columns
                WHERE table_name = '{table}'
            """))
            col_count = result.fetchone()[0]
            
            print(f"   ✅ {table:20} - {desc:20} ({col_count} kolon, {count} kayıt)")
        print()
        
        # 3. Enum Değerleri Detaylı
        print("3️⃣  ML ENUM DEĞERLERİ (DETAYLI)")
        
        # ml_metric_type
        result = conn.execute(text("""
            SELECT e.enumlabel 
            FROM pg_enum e
            JOIN pg_type t ON e.enumtypid = t.oid
            WHERE t.typname = 'ml_metric_type'
            ORDER BY e.enumlabel
        """))
        metrics = [row[0] for row in result]
        print(f"\n   ml_metric_type ({len(metrics)} değer):")
        for i, metric in enumerate(metrics, 1):
            print(f"      {i:2}. {metric}")
        
        # ml_alert_type
        result = conn.execute(text("""
            SELECT e.enumlabel 
            FROM pg_enum e
            JOIN pg_type t ON e.enumtypid = t.oid
            WHERE t.typname = 'ml_alert_type'
            ORDER BY e.enumlabel
        """))
        alerts = [row[0] for row in result]
        print(f"\n   ml_alert_type ({len(alerts)} değer):")
        for i, alert in enumerate(alerts, 1):
            print(f"      {i:2}. {alert}")
        
        # ml_alert_severity
        result = conn.execute(text("""
            SELECT e.enumlabel 
            FROM pg_enum e
            JOIN pg_type t ON e.enumtypid = t.oid
            WHERE t.typname = 'ml_alert_severity'
            ORDER BY e.enumlabel
        """))
        severities = [row[0] for row in result]
        print(f"\n   ml_alert_severity ({len(severities)} değer):")
        for i, severity in enumerate(severities, 1):
            print(f"      {i:2}. {severity}")
        print()
        
        # 4. Index Kontrolü
        print("4️⃣  INDEX'LER")
        result = conn.execute(text("""
            SELECT 
                tablename,
                COUNT(*) as index_count
            FROM pg_indexes
            WHERE schemaname = 'public'
            AND tablename LIKE 'ml_%'
            GROUP BY tablename
            ORDER BY tablename
        """))
        
        total_indexes = 0
        for row in result:
            print(f"   {row[0]:25} {row[1]} index")
            total_indexes += row[1]
        print(f"\n   Toplam ML Index: {total_indexes}")
        print()
        
        # 5. Foreign Key Kontrolü
        print("5️⃣  FOREIGN KEY İLİŞKİLERİ")
        result = conn.execute(text("""
            SELECT 
                tc.table_name,
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
            AND tc.table_name LIKE 'ml_%'
            ORDER BY tc.table_name, kcu.column_name
        """))
        
        fk_count = 0
        for row in result:
            print(f"   {row[0]}.{row[1]:20} → {row[2]}.{row[3]}")
            fk_count += 1
        print(f"\n   Toplam FK: {fk_count}")
        print()
        
        # 6. Diğer Önemli Tablolar
        print("6️⃣  DİĞER ÖNEMLİ TABLOLAR")
        important_tables = [
            'oteller', 'kullanicilar', 'urunler', 'odalar', 
            'minibar_islemleri', 'stok_hareketleri'
        ]
        
        for table in important_tables:
            try:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.fetchone()[0]
                print(f"   {table:25} {count:5} kayıt")
            except:
                print(f"   {table:25} HATA!")
        print()
        
        # 7. Son Aktivite
        print("7️⃣  SON AKTİVİTE")
        
        # Son işlem
        result = conn.execute(text("""
            SELECT MAX(islem_tarihi)
            FROM minibar_islemleri
        """))
        last_islem = result.fetchone()[0]
        print(f"   Son Minibar İşlemi: {last_islem or 'Henüz yok'}")
        
        # Son log
        result = conn.execute(text("""
            SELECT MAX(tarih)
            FROM sistem_loglari
        """))
        last_log = result.fetchone()[0]
        print(f"   Son Sistem Logu: {last_log or 'Henüz yok'}")
        print()
        
        # 8. Genel Değerlendirme
        print("=" * 70)
        print("📊 GENEL DEĞERLENDİRME")
        print("=" * 70)
        
        issues = []
        
        if len(metrics) < 12:
            issues.append(f"⚠️  ml_metric_type eksik ({len(metrics)}/12)")
        else:
            print(f"✅ ml_metric_type: {len(metrics)}/12 değer")
            
        if len(alerts) < 12:
            issues.append(f"⚠️  ml_alert_type eksik ({len(alerts)}/12)")
        else:
            print(f"✅ ml_alert_type: {len(alerts)}/12 değer")
            
        if len(severities) < 4:
            issues.append(f"⚠️  ml_alert_severity eksik ({len(severities)}/4)")
        else:
            print(f"✅ ml_alert_severity: {len(severities)}/4 değer")
            
        if total_indexes < 15:
            issues.append(f"⚠️  Index eksik ({total_indexes}/15)")
        else:
            print(f"✅ Index'ler: {total_indexes}/15")
            
        if fk_count < 5:
            issues.append(f"⚠️  Foreign Key eksik ({fk_count}/5)")
        else:
            print(f"✅ Foreign Key'ler: {fk_count}/5")
        
        print()
        
        if issues:
            print("⚠️  SORUNLAR:")
            for issue in issues:
                print(f"   {issue}")
        else:
            print("🎉 HİÇBİR SORUN YOK - SİSTEM HAZIR!")
            
        print()
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ HATA: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
