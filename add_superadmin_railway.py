#!/usr/bin/env python3
"""Railway MySQL'e superadmin kullanıcısı ekle - TEMPOrary script"""

import pymysql
from werkzeug.security import generate_password_hash

# Railway MySQL bağlantı bilgileri
RAILWAY_CONFIG = {
    'host': 'yamabiko.proxy.rlwy.net',
    'port': 10782,
    'user': 'root',
    'password': 'xAxDAxNfgHyzgnUMVBjjQSUqYUrgBJhq',
    'database': 'railway',  # Railway default database
    'charset': 'utf8mb4'
}

# Yeni kullanıcı bilgileri
NEW_USER = {
    'kullanici_adi': 'superadmin',
    'sifre': '518518Erkan',
    'ad': 'Erkan',
    'soyad': 'ERDEM',
    'email': 'erkan@erkanerdem.net',
    'telefon': '05305288254',
    'rol': 'sistem_yoneticisi',
    'aktif': 1
}

def add_superadmin():
    """Railway MySQL'e superadmin kullanıcısı ekle"""
    print("=" * 60)
    print("🔐 Railway MySQL - Superadmin Kullanıcı Ekleme")
    print("=" * 60)
    
    try:
        # Bağlantı oluştur
        print("\n📡 Railway MySQL'e bağlanılıyor...")
        conn = pymysql.connect(**RAILWAY_CONFIG)
        cursor = conn.cursor()
        print("✅ Bağlantı başarılı!")
        
        # Şifreyi hash'le
        print("\n🔒 Şifre hash'leniyor...")
        password_hash = generate_password_hash(NEW_USER['sifre'])
        print(f"✅ Hash oluşturuldu: {password_hash[:50]}...")
        
        # Kullanıcı var mı kontrol et
        print(f"\n🔍 '{NEW_USER['kullanici_adi']}' kullanıcısı kontrol ediliyor...")
        cursor.execute(
            "SELECT id, kullanici_adi FROM kullanicilar WHERE kullanici_adi = %s",
            (NEW_USER['kullanici_adi'],)
        )
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"⚠️  Kullanıcı zaten mevcut! (ID: {existing_user[0]})")
            print("\n🔄 Mevcut kullanıcı güncelleniyor...")
            
            # Mevcut kullanıcıyı güncelle
            cursor.execute("""
                UPDATE kullanicilar 
                SET sifre_hash = %s,
                    ad = %s,
                    soyad = %s,
                    email = %s,
                    telefon = %s,
                    rol = %s,
                    aktif = %s
                WHERE kullanici_adi = %s
            """, (
                password_hash,
                NEW_USER['ad'],
                NEW_USER['soyad'],
                NEW_USER['email'],
                NEW_USER['telefon'],
                NEW_USER['rol'],
                NEW_USER['aktif'],
                NEW_USER['kullanici_adi']
            ))
            conn.commit()
            print("✅ Kullanıcı güncellendi!")
        else:
            print("✅ Kullanıcı mevcut değil, yeni kayıt ekleniyor...")
            
            # Yeni kullanıcı ekle
            cursor.execute("""
                INSERT INTO kullanicilar 
                (kullanici_adi, sifre_hash, ad, soyad, email, telefon, rol, aktif, olusturma_tarihi)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """, (
                NEW_USER['kullanici_adi'],
                password_hash,
                NEW_USER['ad'],
                NEW_USER['soyad'],
                NEW_USER['email'],
                NEW_USER['telefon'],
                NEW_USER['rol'],
                NEW_USER['aktif']
            ))
            conn.commit()
            print("✅ Yeni kullanıcı eklendi!")
        
        # Eklenen kullanıcıyı doğrula
        print("\n📋 Kullanıcı bilgileri:")
        cursor.execute("""
            SELECT id, kullanici_adi, ad, soyad, email, telefon, rol, aktif, olusturma_tarihi
            FROM kullanicilar 
            WHERE kullanici_adi = %s
        """, (NEW_USER['kullanici_adi'],))
        
        result = cursor.fetchone()
        if result:
            print("-" * 60)
            print(f"  ID             : {result[0]}")
            print(f"  Kullanıcı Adı  : {result[1]}")
            print(f"  Ad Soyad       : {result[2]} {result[3]}")
            print(f"  Email          : {result[4]}")
            print(f"  Telefon        : {result[5]}")
            print(f"  Rol            : {result[6]}")
            print(f"  Aktif          : {'Evet' if result[7] == 1 else 'Hayır'}")
            print(f"  Oluşturma      : {result[8]}")
            print("-" * 60)
        
        # Bağlantıyı kapat
        cursor.close()
        conn.close()
        
        print("\n🎉 İşlem başarıyla tamamlandı!")
        print(f"\n🔑 Giriş Bilgileri:")
        print(f"   Kullanıcı: {NEW_USER['kullanici_adi']}")
        print(f"   Şifre    : {NEW_USER['sifre']}")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ HATA: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    add_superadmin()
