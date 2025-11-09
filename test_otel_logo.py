#!/usr/bin/env python3
"""
Otel logo kontrolü ve test
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

print("🔍 OTEL LOGO KONTROLÜ")
print("=" * 80)

with engine.connect() as conn:
    # Otelleri ve logolarını kontrol et
    result = conn.execute(text("""
        SELECT 
            o.id,
            o.ad,
            LENGTH(o.logo) as logo_uzunlugu,
            CASE 
                WHEN o.logo IS NULL THEN 'YOK'
                WHEN LENGTH(o.logo) = 0 THEN 'BOŞ'
                WHEN o.logo LIKE 'iVBOR%' THEN 'PNG (Base64)'
                WHEN o.logo LIKE '/9j/%' THEN 'JPG (Base64)'
                WHEN o.logo LIKE 'data:image%' THEN 'Data URL'
                ELSE 'BİLİNMEYEN FORMAT'
            END as logo_durumu,
            (SELECT COUNT(*) FROM katlar k WHERE k.otel_id = o.id) as kat_sayisi,
            (SELECT COUNT(*) FROM odalar od 
             JOIN katlar k2 ON od.kat_id = k2.id 
             WHERE k2.otel_id = o.id) as oda_sayisi
        FROM oteller o
        ORDER BY o.id
    """))
    
    print("\n📊 OTEL LOGO DURUMU")
    print("-" * 80)
    
    oteller = list(result)
    if not oteller:
        print("❌ Hiç otel bulunamadı!")
    else:
        for row in oteller:
            print(f"\n🏨 Otel: {row[1]} (ID: {row[0]})")
            print(f"   Logo Durumu: {row[3]}")
            if row[2]:
                print(f"   Logo Boyutu: {row[2]:,} karakter")
            print(f"   Kat Sayısı: {row[4]}")
            print(f"   Oda Sayısı: {row[5]}")
            
            if row[3] == 'YOK' or row[3] == 'BOŞ':
                print(f"   ⚠️  UYARI: Logo bulunamadı!")
    
    # Detaylı oda-kat-otel ilişkisi kontrolü
    print("\n\n🔍 ODA-KAT-OTEL İLİŞKİSİ KONTROLÜ")
    print("-" * 80)
    
    result = conn.execute(text("""
        SELECT 
            od.id as oda_id,
            od.oda_no,
            k.id as kat_id,
            k.kat_adi,
            o.id as otel_id,
            o.ad as otel_adi,
            CASE 
                WHEN o.logo IS NULL THEN 'YOK'
                WHEN LENGTH(o.logo) = 0 THEN 'BOŞ'
                ELSE 'VAR (' || LENGTH(o.logo) || ' karakter)'
            END as logo_durumu
        FROM odalar od
        LEFT JOIN katlar k ON od.kat_id = k.id
        LEFT JOIN oteller o ON k.otel_id = o.id
        ORDER BY od.oda_no
        LIMIT 10
    """))
    
    odalar = list(result)
    if not odalar:
        print("❌ Hiç oda bulunamadı!")
    else:
        print(f"\nİlk 10 oda:")
        for row in odalar:
            status = "✅" if row[6] and 'VAR' in row[6] else "❌"
            print(f"{status} Oda {row[1]} → Kat: {row[3] or 'YOK'} → Otel: {row[5] or 'YOK'} → Logo: {row[6]}")
    
    # QR Token örneği kontrol
    print("\n\n🔍 QR TOKEN KONTROLÜ")
    print("-" * 80)
    
    result = conn.execute(text("""
        SELECT 
            od.id,
            od.oda_no,
            od.qr_kod_token,
            o.ad as otel_adi,
            o.logo IS NOT NULL as logo_var
        FROM odalar od
        LEFT JOIN katlar k ON od.kat_id = k.id
        LEFT JOIN oteller o ON k.otel_id = o.id
        WHERE od.qr_kod_token IS NOT NULL
        LIMIT 5
    """))
    
    tokens = list(result)
    if not tokens:
        print("❌ QR token'lı oda bulunamadı!")
    else:
        print(f"\n{len(tokens)} oda QR token'ına sahip:")
        for row in tokens:
            logo_status = "✅ Logo var" if row[4] else "❌ Logo yok"
            print(f"\nOda {row[1]} - {row[3]}")
            print(f"  Token: {row[2][:20]}...")
            print(f"  {logo_status}")
            print(f"  Test URL: http://localhost:5000/misafir/dolum-talebi/{row[2]}")

print("\n" + "=" * 80)
print("✅ KONTROL TAMAMLANDI!")
