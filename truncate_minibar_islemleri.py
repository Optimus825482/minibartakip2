#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Railway veritabanındaki minibar_islemleri tablosunu truncate eden script
Kullanım: python truncate_minibar_islemleri.py
"""

import mysql.connector
from mysql.connector import Error
import sys

# Railway veritabanı bağlantı bilgileri
RAILWAY_DATABASE_URL = "mysql://root:xAxDAxNfgHyzgnUMVBjjQSUqYUrgBJhq@yamabiko.proxy.rlwy.net:10782/railway"

def parse_database_url(url):
    """Database URL'ini parse eder"""
    try:
        # mysql://user:password@host:port/database formatını parse et
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

def truncate_minibar_islemleri():
    """minibar_islemleri tablosunu truncate eder"""
    connection = None
    
    try:
        # Database URL'ini parse et
        db_config = parse_database_url(RAILWAY_DATABASE_URL)
        if not db_config:
            return False
        
        print("🔄 Railway veritabanına bağlanılıyor...")
        print(f"   Host: {db_config['host']}:{db_config['port']}")
        print(f"   Database: {db_config['database']}")
        
        # Veritabanına bağlan
        connection = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        
        if connection.is_connected():
            print("✅ Veritabanı bağlantısı başarılı!")
            
            cursor = connection.cursor()
            
            # Önce kayıt sayısını kontrol et
            cursor.execute("SELECT COUNT(*) FROM minibar_islemleri")
            count = cursor.fetchone()[0]
            print(f"\n📊 Mevcut kayıt sayısı: {count}")
            
            if count == 0:
                print("ℹ️  Tablo zaten boş, truncate işlemine gerek yok.")
                return True
            
            # Kullanıcıdan onay al
            print(f"\n⚠️  DİKKAT: {count} adet kayıt silinecek!")
            onay = input("Devam etmek istiyor musun? (EVET/hayır): ")
            
            if onay.upper() != "EVET":
                print("❌ İşlem iptal edildi.")
                return False
            
            # Foreign key kontrollerini geçici olarak kapat
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            # Truncate işlemini gerçekleştir
            print("\n🔄 Truncate işlemi başlatılıyor...")
            cursor.execute("TRUNCATE TABLE minibar_islemleri")
            
            # Foreign key kontrollerini tekrar aç
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            
            connection.commit()
            
            # Kontrol et
            cursor.execute("SELECT COUNT(*) FROM minibar_islemleri")
            new_count = cursor.fetchone()[0]
            
            if new_count == 0:
                print("✅ Truncate işlemi başarılı!")
                print(f"   Silinen kayıt sayısı: {count}")
                print(f"   Kalan kayıt sayısı: {new_count}")
                return True
            else:
                print(f"⚠️  Beklenmeyen durum: Hala {new_count} kayıt var!")
                return False
                
    except Error as e:
        print(f"❌ MySQL Hatası: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Genel Hata: {e}")
        return False
        
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("\n🔌 Veritabanı bağlantısı kapatıldı.")

if __name__ == "__main__":
    print("=" * 60)
    print("  RAILWAY MINIBAR İŞLEMLERİ TRUNCATE SCRIPT")
    print("=" * 60)
    print()
    
    success = truncate_minibar_islemleri()
    
    print()
    print("=" * 60)
    
    sys.exit(0 if success else 1)
