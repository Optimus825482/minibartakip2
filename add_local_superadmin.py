"""
Local MySQL'e Superadmin Kullanıcısı Ekleme Script'i
Kullanıcı: superadmin
Şifre: 518518Erkan
Rol: sistem_yoneticisi
"""

import pymysql
from werkzeug.security import generate_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

def add_superadmin():
    """Local MySQL'e superadmin kullanıcısı ekle"""
    
    # Kullanıcı bilgileri
    kullanici_adi = "superadmin"
    sifre = "518518Erkan"
    ad = "Super"
    soyad = "Admin"
    email = "admin@minibar.local"
    rol = "sistem_yoneticisi"
    
    # MySQL bağlantı bilgileri (.env'den)
    mysql_host = os.getenv('MYSQL_HOST', 'localhost')
    mysql_user = os.getenv('MYSQL_USER', 'root')
    mysql_password = os.getenv('MYSQL_PASSWORD', '')
    mysql_db = os.getenv('MYSQL_DB', 'minibar_takip')
    mysql_port = int(os.getenv('MYSQL_PORT', 3306))
    
    print("=" * 60)
    print("SUPERADMIN KULLANICI EKLEME")
    print("=" * 60)
    print()
    print(f"📡 MySQL Bağlantı Bilgileri:")
    print(f"   Host: {mysql_host}")
    print(f"   Port: {mysql_port}")
    print(f"   Database: {mysql_db}")
    print(f"   User: {mysql_user}")
    print()
    
    try:
        # MySQL'e bağlan
        print("🔌 MySQL'e bağlanılıyor...")
        connection = pymysql.connect(
            host=mysql_host,
            port=mysql_port,
            user=mysql_user,
            password=mysql_password,
            database=mysql_db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        cursor = connection.cursor()
        print("✅ Bağlantı başarılı!")
        print()
        
        # Kullanıcı var mı kontrol et
        print(f"🔍 '{kullanici_adi}' kullanıcısı kontrol ediliyor...")
        cursor.execute(
            "SELECT id, kullanici_adi, rol, aktif FROM kullanicilar WHERE kullanici_adi = %s",
            (kullanici_adi,)
        )
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"⚠️  Kullanıcı zaten mevcut!")
            print(f"   ID: {existing_user['id']}")
            print(f"   Kullanıcı Adı: {existing_user['kullanici_adi']}")
            print(f"   Rol: {existing_user['rol']}")
            print(f"   Aktif: {'Evet' if existing_user['aktif'] else 'Hayır'}")
            print()
            
            # Şifre güncelleme seçeneği
            cevap = input("❓ Şifreyi güncellemek ister misin? (e/h): ").lower()
            
            if cevap == 'e':
                sifre_hash = generate_password_hash(sifre)
                cursor.execute(
                    "UPDATE kullanicilar SET sifre_hash = %s, aktif = 1 WHERE id = %s",
                    (sifre_hash, existing_user['id'])
                )
                connection.commit()
                print("✅ Şifre güncellendi ve kullanıcı aktif edildi!")
            else:
                print("ℹ️  İşlem iptal edildi.")
            
        else:
            # Yeni kullanıcı ekle
            print(f"➕ Yeni kullanıcı ekleniyor...")
            
            # Şifreyi hashle
            sifre_hash = generate_password_hash(sifre)
            
            # SQL sorgusu
            sql = """
                INSERT INTO kullanicilar 
                (kullanici_adi, sifre_hash, ad, soyad, email, rol, aktif, olusturma_tarihi)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(sql, (
                kullanici_adi,
                sifre_hash,
                ad,
                soyad,
                email,
                rol,
                True,
                datetime.now()
            ))
            
            connection.commit()
            
            # Eklenen kullanıcıyı göster
            cursor.execute(
                "SELECT id, kullanici_adi, ad, soyad, email, rol FROM kullanicilar WHERE kullanici_adi = %s",
                (kullanici_adi,)
            )
            new_user = cursor.fetchone()
            
            print()
            print("=" * 60)
            print("✅ KULLANICI BAŞARIYLA EKLENDİ!")
            print("=" * 60)
            print()
            print(f"📋 Kullanıcı Bilgileri:")
            print(f"   ID: {new_user['id']}")
            print(f"   Kullanıcı Adı: {new_user['kullanici_adi']}")
            print(f"   Ad Soyad: {new_user['ad']} {new_user['soyad']}")
            print(f"   Email: {new_user['email']}")
            print(f"   Rol: {new_user['rol']}")
            print()
            print(f"🔐 Giriş Bilgileri:")
            print(f"   Kullanıcı Adı: {kullanici_adi}")
            print(f"   Şifre: {sifre}")
            print()
            print(f"🌐 Giriş URL: http://localhost:5014/login")
            print()
        
        cursor.close()
        connection.close()
        
        return True
        
    except pymysql.Error as e:
        print(f"❌ MySQL Hatası: {e}")
        print()
        print("🔧 Kontrol Listesi:")
        print("   ✓ MySQL servisi çalışıyor mu?")
        print("   ✓ .env dosyasındaki bilgiler doğru mu?")
        print("   ✓ Veritabanı oluşturulmuş mu? (python init_db.py)")
        print("   ✓ kullanicilar tablosu var mı?")
        return False
        
    except Exception as e:
        print(f"❌ Beklenmeyen Hata: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print()
    success = add_superadmin()
    print()
    
    if success:
        print("🎉 İşlem tamamlandı!")
    else:
        print("⚠️  İşlem başarısız oldu.")
    
    print()
    exit(0 if success else 1)
