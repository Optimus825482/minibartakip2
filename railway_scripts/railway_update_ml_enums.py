"""
Railway ML Enum Güncelleme
Yeni metrik ve alert tiplerini ekler
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Railway .env dosyasını yükle
load_dotenv('.env.railway')

DATABASE_URL = os.getenv('RAILWAY_DATABASE_URL')

if not DATABASE_URL:
    print("❌ RAILWAY_DATABASE_URL bulunamadı!")
    exit(1)

engine = create_engine(DATABASE_URL)

print("=" * 60)
print("🔧 RAILWAY ML ENUM GÜNCELLEMESİ")
print("=" * 60)
print()
print(f"🔗 Railway veritabanına bağlanılıyor...")
print(f"   Host: shinkansen.proxy.rlwy.net:27699")
print()

with engine.connect() as conn:
    try:
        print("📝 Mevcut enum değerleri kontrol ediliyor...")
        
        # Mevcut ml_metric_type değerlerini kontrol et
        result = conn.execute(text("""
            SELECT e.enumlabel 
            FROM pg_enum e
            JOIN pg_type t ON e.enumtypid = t.oid
            WHERE t.typname = 'ml_metric_type'
            ORDER BY e.enumlabel
        """))
        existing_metrics = [row[0] for row in result]
        print(f"\n   Mevcut ml_metric_type değerleri: {', '.join(existing_metrics)}")
        
        # Mevcut ml_alert_type değerlerini kontrol et
        result = conn.execute(text("""
            SELECT e.enumlabel 
            FROM pg_enum e
            JOIN pg_type t ON e.enumtypid = t.oid
            WHERE t.typname = 'ml_alert_type'
            ORDER BY e.enumlabel
        """))
        existing_alerts = [row[0] for row in result]
        print(f"   Mevcut ml_alert_type değerleri: {', '.join(existing_alerts)}")
        
        print("\n🚀 Yeni enum değerleri ekleniyor...")
        
        # ml_metric_type enum'una yeni değerler ekle
        new_metrics = [
            'zimmet_kullanim',
            'zimmet_fire', 
            'doluluk_oran',
            'bosta_tuketim'
        ]
        
        for metric in new_metrics:
            if metric not in existing_metrics:
                try:
                    conn.execute(text(f"ALTER TYPE ml_metric_type ADD VALUE '{metric}'"))
                    conn.commit()  # Her ADD VALUE sonrası commit gerekli
                    print(f"   ✅ ml_metric_type: {metric} eklendi")
                except Exception as e:
                    if "already exists" in str(e):
                        print(f"   ⚠️  ml_metric_type: {metric} zaten mevcut")
                    else:
                        raise
            else:
                print(f"   ⏭️  ml_metric_type: {metric} zaten mevcut")
        
        # ml_alert_type enum'una yeni değerler ekle
        new_alerts = [
            'zimmet_fire_yuksek',
            'zimmet_kullanim_dusuk',
            'bosta_tuketim_var',
            'doluda_tuketim_yok'
        ]
        
        for alert in new_alerts:
            if alert not in existing_alerts:
                try:
                    conn.execute(text(f"ALTER TYPE ml_alert_type ADD VALUE '{alert}'"))
                    conn.commit()  # Her ADD VALUE sonrası commit gerekli
                    print(f"   ✅ ml_alert_type: {alert} eklendi")
                except Exception as e:
                    if "already exists" in str(e):
                        print(f"   ⚠️  ml_alert_type: {alert} zaten mevcut")
                    else:
                        raise
            else:
                print(f"   ⏭️  ml_alert_type: {alert} zaten mevcut")
        
        print()
        print("=" * 60)
        print("✅ ENUM GÜNCELLEMESİ TAMAMLANDI!")
        print("=" * 60)
        print()
        
        # Güncel enum değerlerini göster
        result = conn.execute(text("""
            SELECT e.enumlabel 
            FROM pg_enum e
            JOIN pg_type t ON e.enumtypid = t.oid
            WHERE t.typname = 'ml_metric_type'
            ORDER BY e.enumlabel
        """))
        all_metrics = [row[0] for row in result]
        
        result = conn.execute(text("""
            SELECT e.enumlabel 
            FROM pg_enum e
            JOIN pg_type t ON e.enumtypid = t.oid
            WHERE t.typname = 'ml_alert_type'
            ORDER BY e.enumlabel
        """))
        all_alerts = [row[0] for row in result]
        
        print("📊 Güncel Enum Değerleri:")
        print()
        print(f"ml_metric_type ({len(all_metrics)} değer):")
        for metric in all_metrics:
            print(f"   - {metric}")
        
        print()
        print(f"ml_alert_type ({len(all_alerts)} değer):")
        for alert in all_alerts:
            print(f"   - {alert}")
        
        print()
        
    except Exception as e:
        print(f"\n❌ HATA: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        exit(1)
