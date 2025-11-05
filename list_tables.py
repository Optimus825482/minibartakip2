#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Railway veritabanındaki tüm tabloları ve kayıt sayılarını listeler
"""

import mysql.connector
from mysql.connector import Error

# Railway veritabanı bağlantı bilgileri
RAILWAY_DATABASE_URL = "mysql://root:xAxDAxNfgHyzgnUMVBjjQSUqYUrgBJhq@yamabiko.proxy.rlwy.net:10782/railway"

def parse_database_url(url):
    """Database URL'ini parse eder"""
    try:
        url = url.replace("mysql://", "")
        auth, location = url.split("@")
        user, password = auth.split(":")
        host_port, database = location.split("/")
        host, port = host_port.split(":")
        
        return {
            'user': user,
            'password': password,
            'host': host,
            'port': int(port),
            'database': database
        }
    except Exception as e:
        print(f"❌ URL parse hatası: {e}")
        return None

def list_all_tables():
    """Tüm tabloları ve kayıt sayılarını listeler"""
    connection = None
    
    try:
        db_config = parse_database_url(RAILWAY_DATABASE_URL)
        if not db_config:
            return
        
        print("🔄 Railway veritabanına bağlanılıyor...")
        print(f"   Host: {db_config['host']}:{db_config['port']}")
        print(f"   Database: {db_config['database']}\n")
        
        connection = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        
        if connection.is_connected():
            print("✅ Veritabanı bağlantısı başarılı!\n")
            
            cursor = connection.cursor()
            
            # Tüm tabloları al
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if not tables:
                print("ℹ️  Veritabanında tablo bulunamadı.")
                return
            
            print("=" * 70)
            print(f"{'TABLO ADI':<40} {'KAYIT SAYISI':>15} {'DURUM':>10}")
            print("=" * 70)
            
            total_records = 0
            table_data = []
            
            # Her tablo için kayıt sayısını al
            for (table_name,) in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                    count = cursor.fetchone()[0]
                    table_data.append((table_name, count))
                    total_records += count
                except Error as e:
                    table_data.append((table_name, f"Hata: {e}"))
            
            # Kayıt sayısına göre sırala (büyükten küçüğe)
            table_data.sort(key=lambda x: x[1] if isinstance(x[1], int) else 0, reverse=True)
            
            # Tabloları yazdır - HEPSİNİ GÖSTER
            for i, (table_name, count) in enumerate(table_data, 1):
                if isinstance(count, int):
                    status = "✅" if count > 0 else "⚪"
                    print(f"{i:>2}. {table_name:<37} {count:>15,} {status:>10}")
                else:
                    print(f"{i:>2}. {table_name:<37} {str(count):>15} {'❌':>10}")
            
            print("=" * 70)
            print(f"{'TOPLAM':<40} {total_records:>15,}")
            print("=" * 70)
            print(f"\n📊 Toplam {len(tables)} tablo bulundu.")
            print(f"📈 Toplam {total_records:,} kayıt var.\n")
                
    except Error as e:
        print(f"❌ MySQL Hatası: {e}")
        
    except Exception as e:
        print(f"❌ Genel Hata: {e}")
        
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Veritabanı bağlantısı kapatıldı.")

if __name__ == "__main__":
    print("=" * 70)
    print("  RAILWAY VERİTABANI TABLO LİSTESİ")
    print("=" * 70)
    print()
    
    list_all_tables()
