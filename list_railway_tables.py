"""
Railway veritabanındaki tüm tabloları listele
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv('.env.railway')

DATABASE_URL = os.getenv('RAILWAY_DATABASE_URL')
engine = create_engine(DATABASE_URL)

print("📋 Railway Veritabanı Tabloları:\n")

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT 
            table_name,
            (SELECT COUNT(*) 
             FROM information_schema.columns 
             WHERE table_schema = 'public' 
             AND table_name = t.table_name) as column_count
        FROM information_schema.tables t
        WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """))
    
    tables = list(result)
    print(f"Toplam {len(tables)} tablo bulundu:\n")
    
    for idx, row in enumerate(tables, 1):
        print(f"{idx:2}. {row[0]:30} ({row[1]} kolon)")

print("\n✅ Listeleme tamamlandı!")
