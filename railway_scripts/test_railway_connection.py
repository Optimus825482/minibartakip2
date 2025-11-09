"""
Railway veritabanı bağlantısını test et
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv('.env.railway')

DATABASE_URL = os.getenv('RAILWAY_DATABASE_URL')
engine = create_engine(DATABASE_URL)

print("🔗 Railway Bağlantı Testi\n")

try:
    with engine.connect() as conn:
        # Basit test sorgusu
        result = conn.execute(text("SELECT version()"))
        version = result.fetchone()[0]
        print(f"✅ Bağlantı başarılı!")
        print(f"   PostgreSQL: {version.split(',')[0]}\n")
        
        # ML tablolarını kontrol et
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE 'ml_%'
            ORDER BY table_name
        """))
        
        tables = [row[0] for row in result]
        print(f"📊 ML Tabloları ({len(tables)} adet):")
        for table in tables:
            # Her tablodaki kayıt sayısını al
            count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = count_result.fetchone()[0]
            print(f"   ✓ {table:25} ({count} kayıt)")
        
        # Test sorgusu - ml_alerts
        print("\n🧪 Test Sorgusu (ml_alerts):")
        result = conn.execute(text("""
            SELECT COUNT(*) 
            FROM ml_alerts 
            WHERE is_read = false 
            AND is_false_positive = false
        """))
        count = result.fetchone()[0]
        print(f"   Okunmamış uyarılar: {count}")
        
        print("\n✅ Tüm testler başarılı!")
        
except Exception as e:
    print(f"❌ Hata: {e}")
    import traceback
    traceback.print_exc()
