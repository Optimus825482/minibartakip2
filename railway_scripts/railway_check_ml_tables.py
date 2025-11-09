"""
Railway ML Tabloları Kontrol ve Oluşturma
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect

# Railway .env dosyasını yükle
load_dotenv('.env.railway')

DATABASE_URL = os.getenv('RAILWAY_DATABASE_URL')

if not DATABASE_URL:
    print("❌ RAILWAY_DATABASE_URL bulunamadı!")
    exit(1)

engine = create_engine(DATABASE_URL)

print("=" * 60)
print("🤖 RAILWAY ML TABLO KONTROLÜ")
print("=" * 60)
print()
print("🔗 Railway veritabanına bağlanılıyor...")
print("   Host: shinkansen.proxy.rlwy.net:27699")
print()

with engine.connect() as conn:
    try:
        # Mevcut tabloları kontrol et
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        print("📋 Mevcut Toplam Tablo Sayısı:", len(existing_tables))
        print()
        
        # ML tablolarını kontrol et
        ml_tables = ['ml_metrics', 'ml_models', 'ml_alerts', 'ml_training_logs']
        
        print("🔍 ML Tabloları Kontrolü:")
        all_exist = True
        for table in ml_tables:
            if table in existing_tables:
                # Kayıt sayısını al
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.fetchone()[0]
                
                # Kolon sayısını al
                result = conn.execute(text(f"""
                    SELECT COUNT(*) 
                    FROM information_schema.columns
                    WHERE table_name = '{table}'
                """))
                col_count = result.fetchone()[0]
                
                print(f"   ✅ {table:25} ({col_count} kolon, {count} kayıt)")
            else:
                print(f"   ❌ {table:25} (YOK!)")
                all_exist = False
        
        print()
        
        if all_exist:
            print("✅ Tüm ML tabloları mevcut!")
            print()
            
            # Index'leri kontrol et
            print("📑 ML Tablo Index'leri:")
            for table in ml_tables:
                indexes = inspector.get_indexes(table)
                print(f"\n   {table}:")
                if indexes:
                    for idx in indexes:
                        cols = ', '.join(idx['column_names'])
                        unique = " (UNIQUE)" if idx.get('unique') else ""
                        print(f"      - {idx['name']:35} ({cols}){unique}")
                else:
                    print("      (Index yok)")
            
            print()
            
            # Enum'ları kontrol et
            print("📊 ML Enum Tipleri:")
            
            result = conn.execute(text("""
                SELECT t.typname, COUNT(e.enumlabel) as value_count
                FROM pg_type t
                LEFT JOIN pg_enum e ON t.oid = e.enumtypid
                WHERE t.typname LIKE 'ml_%'
                GROUP BY t.typname
                ORDER BY t.typname
            """))
            
            for row in result:
                print(f"   - {row[0]:30} ({row[1]} değer)")
            
            print()
            print("=" * 60)
            print("✅ KONTROL TAMAMLANDI - HER ŞEY HAZIR!")
            print("=" * 60)
            
        else:
            print("⚠️  Eksik tablolar var! Lütfen migration'ı çalıştırın.")
            
    except Exception as e:
        print(f"\n❌ HATA: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
