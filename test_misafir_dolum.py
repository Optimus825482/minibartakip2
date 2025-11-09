#!/usr/bin/env python3
"""
Misafir dolum talebi sayfası test scripti
QR token ile sayfayı test et
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Railway bağlantısı
load_dotenv('.env.railway')

railway_url = os.getenv('RAILWAY_DATABASE_URL')
if railway_url:
    railway_url = railway_url.replace('postgresql://', 'postgresql+psycopg2://')

engine = create_engine(railway_url)

print("🧪 MİSAFİR DOLUM TALEBİ TEST")
print("=" * 80)

with engine.connect() as conn:
    # QR token'lı odaları al
    result = conn.execute(text("""
        SELECT 
            od.id,
            od.oda_no,
            od.qr_kod_token,
            k.kat_adi,
            o.ad as otel_adi,
            LENGTH(o.logo) as logo_boyutu
        FROM odalar od
        JOIN katlar k ON od.kat_id = k.id
        JOIN oteller o ON k.otel_id = o.id
        WHERE od.qr_kod_token IS NOT NULL
        AND o.logo IS NOT NULL
        ORDER BY od.oda_no
        LIMIT 5
    """))
    
    odalar = list(result)
    
    if not odalar:
        print("❌ QR token'lı oda bulunamadı!")
        print("\n🔧 Oda için QR token oluşturuluyor...")
        
        # İlk odaya token ekle
        result = conn.execute(text("""
            SELECT od.id, od.oda_no
            FROM odalar od
            JOIN katlar k ON od.kat_id = k.id
            JOIN oteller o ON k.otel_id = o.id
            WHERE o.logo IS NOT NULL
            LIMIT 1
        """))
        
        oda = result.fetchone()
        if oda:
            import secrets
            token = secrets.token_urlsafe(32)
            
            conn.execute(text("""
                UPDATE odalar 
                SET qr_kod_token = :token
                WHERE id = :oda_id
            """), {"token": token, "oda_id": oda[0]})
            conn.commit()
            
            print(f"✅ Oda {oda[1]} için token oluşturuldu!")
            
            # Tekrar sorgula
            result = conn.execute(text("""
                SELECT 
                    od.id,
                    od.oda_no,
                    od.qr_kod_token,
                    k.kat_adi,
                    o.ad as otel_adi,
                    LENGTH(o.logo) as logo_boyutu
                FROM odalar od
                JOIN katlar k ON od.kat_id = k.id
                JOIN oteller o ON k.otel_id = o.id
                WHERE od.id = :oda_id
            """), {"oda_id": oda[0]})
            
            odalar = list(result)
    
    if odalar:
        print("\n✅ TEST İÇİN HAZIR ODALAR")
        print("-" * 80)
        
        for i, row in enumerate(odalar, 1):
            print(f"\n{i}. Oda {row[1]} - {row[3]} - {row[4]}")
            print(f"   Logo Boyutu: {row[5]:,} karakter")
            print(f"   Token: {row[2][:30]}...")
            
            # URL'leri göster
            print(f"\n   🌐 TEST URL'LERİ:")
            print(f"   Lokal:   http://localhost:5000/misafir/dolum-talebi/{row[2]}")
            print(f"   Railway: https://minibartakip2-production.up.railway.app/misafir/dolum-talebi/{row[2]}")
            
            if i == 1:
                print(f"\n   📱 QR KOD İÇİN:")
                print(f"   https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=https://minibartakip2-production.up.railway.app/misafir/dolum-talebi/{row[2]}")

print("\n" + "=" * 80)
print("✅ TEST BİLGİLERİ HAZIR!")
print("\n📝 TEST ADIMLARI:")
print("1. Yukarıdaki URL'lerden birini tarayıcıda aç")
print("2. Otel logosunun görüntülendiğini kontrol et")
print("3. Dolum talebi formu çalışıyor mu test et")
print("4. QR kod üret ve mobil cihazdan tara")
