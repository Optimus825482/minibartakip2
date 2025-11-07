"""
Railway Veritabanı Migration Script'i
Railway'deki veritabanına eksik kolonları ekler
"""

import pymysql
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

def get_railway_connection():
    """Railway veritabanı bağlantısı oluştur"""
    
    # Railway bağlantı bilgileri
    config = {
        'host': os.getenv('RAILWAY_MYSQL_HOST', 'yamabiko.proxy.rlwy.net'),
        'port': int(os.getenv('RAILWAY_MYSQL_PORT', '10782')),
        'user': os.getenv('RAILWAY_MYSQL_USER', 'root'),
        'password': os.getenv('RAILWAY_MYSQL_PASSWORD', 'xAxDAxNfgHyzgnUMVBjjQSUqYUrgBJhq'),
        'database': os.getenv('RAILWAY_MYSQL_DATABASE', 'railway'),
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }
    
    return pymysql.connect(**config)

def check_column_exists(cursor, table_name, column_name):
    """Kolonun var olup olmadığını kontrol et"""
    
    cursor.execute(f"""
        SELECT COUNT(*) as count
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = '{table_name}'
        AND COLUMN_NAME = '{column_name}'
    """)
    
    result = cursor.fetchone()
    return result['count'] > 0

def run_migration():
    """Migration çalıştır"""
    
    print("=" * 70)
    print("RAILWAY VERİTABANI MİGRATION")
    print("=" * 70)
    print()
    
    try:
        # Railway'e bağlan
        print("📡 Railway veritabanına bağlanılıyor...")
        connection = get_railway_connection()
        cursor = connection.cursor()
        
        print(f"✅ Bağlantı başarılı: {connection.get_server_info()}")
        print()
        
        migrations_applied = []
        migrations_skipped = []
        
        # ODALAR tablosu için migration
        print("📋 ODALAR tablosu kontrol ediliyor...")
        
        qr_columns = {
            'qr_kod_token': "VARCHAR(64) NULL",
            'qr_kod_gorsel': "TEXT NULL",
            'qr_kod_olusturma_tarihi': "DATETIME NULL",
            'misafir_mesaji': "VARCHAR(500) NULL"
        }
        
        for col_name, col_type in qr_columns.items():
            if not check_column_exists(cursor, 'odalar', col_name):
                print(f"   ➕ {col_name} kolonu ekleniyor...")
                cursor.execute(f"ALTER TABLE odalar ADD COLUMN {col_name} {col_type}")
                migrations_applied.append(f"odalar.{col_name}")
                print(f"   ✅ {col_name} eklendi")
            else:
                migrations_skipped.append(f"odalar.{col_name}")
                print(f"   ⏭️  {col_name} zaten mevcut")
        
        print()
        
        # PERSONEL_ZIMMET_DETAY tablosu için migration
        print("📋 PERSONEL_ZIMMET_DETAY tablosu kontrol ediliyor...")
        
        if not check_column_exists(cursor, 'personel_zimmet_detay', 'kritik_stok_seviyesi'):
            print("   ➕ kritik_stok_seviyesi kolonu ekleniyor...")
            cursor.execute("ALTER TABLE personel_zimmet_detay ADD COLUMN kritik_stok_seviyesi INTEGER NULL DEFAULT 0")
            migrations_applied.append("personel_zimmet_detay.kritik_stok_seviyesi")
            print("   ✅ kritik_stok_seviyesi eklendi")
        else:
            migrations_skipped.append("personel_zimmet_detay.kritik_stok_seviyesi")
            print("   ⏭️  kritik_stok_seviyesi zaten mevcut")
        
        # Değişiklikleri kaydet
        connection.commit()
        
        print()
        print("=" * 70)
        print("MİGRATION SONUÇLARI")
        print("=" * 70)
        
        if migrations_applied:
            print(f"\n✅ Eklenen kolonlar ({len(migrations_applied)} adet):")
            for migration in migrations_applied:
                print(f"   ✓ {migration}")
        
        if migrations_skipped:
            print(f"\n⏭️  Atlanan kolonlar ({len(migrations_skipped)} adet):")
            for migration in migrations_skipped:
                print(f"   - {migration}")
        
        if not migrations_applied:
            print("\nℹ️  Hiçbir migration uygulanmadı - tüm kolonlar zaten mevcut")
        else:
            print(f"\n🎉 {len(migrations_applied)} kolon başarıyla eklendi!")
        
        print()
        
        # Bağlantıyı kapat
        cursor.close()
        connection.close()
        
        return True
        
    except pymysql.Error as e:
        print(f"\n❌ MySQL Hatası: {e}")
        print(f"   Hata Kodu: {e.args[0]}")
        print(f"   Mesaj: {e.args[1]}")
        return False
        
    except Exception as e:
        print(f"\n❌ Beklenmeyen Hata: {e}")
        return False

def verify_migration():
    """Migration'ın başarılı olduğunu doğrula"""
    
    print()
    print("🔍 Migration doğrulanıyor...")
    
    try:
        connection = get_railway_connection()
        cursor = connection.cursor()
        
        # Tüm kolonları kontrol et
        required_columns = {
            'odalar': ['qr_kod_token', 'qr_kod_gorsel', 'qr_kod_olusturma_tarihi', 'misafir_mesaji'],
            'personel_zimmet_detay': ['kritik_stok_seviyesi']
        }
        
        all_ok = True
        
        for table_name, columns in required_columns.items():
            for col_name in columns:
                if not check_column_exists(cursor, table_name, col_name):
                    print(f"❌ {table_name}.{col_name} eksik!")
                    all_ok = False
        
        cursor.close()
        connection.close()
        
        if all_ok:
            print("✅ Tüm kolonlar başarıyla eklendi!")
            return True
        else:
            print("⚠️  Bazı kolonlar eksik!")
            return False
            
    except Exception as e:
        print(f"❌ Doğrulama hatası: {e}")
        return False

if __name__ == '__main__':
    print()
    
    # Migration çalıştır
    if run_migration():
        # Doğrula
        verify_migration()
        print()
        print("=" * 70)
        print("✅ RAILWAY MİGRATION TAMAMLANDI!")
        print("=" * 70)
        print()
        exit(0)
    else:
        print()
        print("=" * 70)
        print("❌ RAILWAY MİGRATION BAŞARISIZ!")
        print("=" * 70)
        print()
        exit(1)
