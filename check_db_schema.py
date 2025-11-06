"""
Veritabanı şema karşılaştırma scripti
"""
import os
from sqlalchemy import create_engine, inspect

# Railway DB
railway_url = "mysql+pymysql://root:xAxDAxNfgHyzgnUMVBjjQSUqYUrgBJhq@yamabiko.proxy.rlwy.net:10782/railway?charset=utf8mb4"

# Local DB
local_host = os.getenv('DB_HOST', 'localhost')
local_user = os.getenv('DB_USER', 'root')
local_pass = os.getenv('DB_PASSWORD', '')
local_db = os.getenv('DB_NAME', 'minibar_takip')
local_url = f"mysql+pymysql://{local_user}:{local_pass}@{local_host}:3306/{local_db}?charset=utf8mb4"

def get_schema(engine_url, db_name):
    """Veritabanı şemasını al"""
    try:
        engine = create_engine(engine_url)
        inspector = inspect(engine)
        
        schema = {}
        for table_name in inspector.get_table_names():
            columns = {}
            for col in inspector.get_columns(table_name):
                columns[col['name']] = str(col['type'])
            schema[table_name] = columns
        
        engine.dispose()
        return schema
    except Exception as e:
        print(f"❌ {db_name} bağlantı hatası: {e}")
        return None

print("=" * 80)
print("VERITABANI ŞEMA KARŞILAŞTIRMA")
print("=" * 80)

# Railway şeması
print("\n📡 Railway veritabanı kontrol ediliyor...")
railway_schema = get_schema(railway_url, "Railway")

# Local şeması
print("💻 Local veritabanı kontrol ediliyor...")
local_schema = get_schema(local_url, "Local")

if not railway_schema or not local_schema:
    print("\n❌ Veritabanlarına bağlanılamadı!")
    exit(1)

# Tablo karşılaştırması
print("\n" + "=" * 80)
print("TABLO KARŞILAŞTIRMASI")
print("=" * 80)

railway_tables = set(railway_schema.keys())
local_tables = set(local_schema.keys())

# Sadece Railway'de olan tablolar
only_railway = railway_tables - local_tables
if only_railway:
    print(f"\n⚠️  Sadece Railway'de olan tablolar: {only_railway}")

# Sadece Local'de olan tablolar
only_local = local_tables - railway_tables
if only_local:
    print(f"\n⚠️  Sadece Local'de olan tablolar: {only_local}")

# Ortak tablolar
common_tables = railway_tables & local_tables
print(f"\n✅ Ortak tablolar ({len(common_tables)} adet)")

# Kolon karşılaştırması
print("\n" + "=" * 80)
print("KOLON FARKLILIKLARI")
print("=" * 80)

for table in sorted(common_tables):
    railway_cols = set(railway_schema[table].keys())
    local_cols = set(local_schema[table].keys())
    
    only_railway_cols = railway_cols - local_cols
    only_local_cols = local_cols - railway_cols
    
    if only_railway_cols or only_local_cols:
        print(f"\n📋 {table}:")
        
        if only_railway_cols:
            print(f"   ⚠️  Sadece Railway'de: {only_railway_cols}")
            for col in only_railway_cols:
                print(f"      - {col}: {railway_schema[table][col]}")
        
        if only_local_cols:
            print(f"   ⚠️  Sadece Local'de: {only_local_cols}")
            for col in only_local_cols:
                print(f"      - {col}: {local_schema[table][col]}")

print("\n" + "=" * 80)
print("ÖZET")
print("=" * 80)
print(f"Railway Tablo Sayısı: {len(railway_tables)}")
print(f"Local Tablo Sayısı: {len(local_tables)}")
print(f"Ortak Tablo Sayısı: {len(common_tables)}")

if only_railway or only_local:
    print("\n⚠️  TABLO FARKLILIKLARI VAR!")
else:
    print("\n✅ Tüm tablolar her iki veritabanında da mevcut")

print("\n" + "=" * 80)
