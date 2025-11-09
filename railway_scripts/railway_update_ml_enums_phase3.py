"""
Railway ML Enum Güncelleme - Phase 3
QR ve Talep sistemi metriklerini ekler
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
print("🔧 RAILWAY ML ENUM GÜNCELLEMESİ - PHASE 3")
print("=" * 60)
print()
print("🔗 Railway veritabanına bağlanılıyor...")
print("   Host: shinkansen.proxy.rlwy.net:27699")
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
        print(f"\n   Mevcut ml_metric_type: {len(existing_metrics)} değer")
        
        # Mevcut ml_alert_type değerlerini kontrol et
        result = conn.execute(text("""
            SELECT e.enumlabel 
            FROM pg_enum e
            JOIN pg_type t ON e.enumtypid = t.oid
            WHERE t.typname = 'ml_alert_type'
            ORDER BY e.enumlabel
        """))
        existing_alerts = [row[0] for row in result]
        print(f"   Mevcut ml_alert_type: {len(existing_alerts)} değer")
        
        print("\n🚀 Phase 3: QR & Talep metrikleri ekleniyor...")
        
        # ml_metric_type enum'una yeni değerler ekle
        new_metrics = [
            ('talep_yanit_sure', 'Talep yanıt süresi'),
            ('talep_yogunluk', 'Oda/kat bazlı talep sayısı'),
            ('qr_okutma_siklik', 'Personel QR okutma sıklığı')
        ]
        
        for metric, description in new_metrics:
            if metric not in existing_metrics:
                try:
                    conn.execute(text(f"ALTER TYPE ml_metric_type ADD VALUE '{metric}'"))
                    conn.commit()
                    print(f"   ✅ ml_metric_type: {metric} eklendi - {description}")
                except Exception as e:
                    if "already exists" in str(e):
                        print(f"   ⚠️  ml_metric_type: {metric} zaten mevcut")
                    else:
                        raise
            else:
                print(f"   ⏭️  ml_metric_type: {metric} zaten mevcut")
        
        # ml_alert_type enum'una yeni değerler ekle
        new_alerts = [
            ('talep_yanitlanmadi', 'Uzun süre yanıtlanmayan talep'),
            ('talep_yogunluk_yuksek', 'Aşırı talep yoğunluğu'),
            ('qr_kullanim_dusuk', 'QR sistemi az kullanılıyor')
        ]
        
        for alert, description in new_alerts:
            if alert not in existing_alerts:
                try:
                    conn.execute(text(f"ALTER TYPE ml_alert_type ADD VALUE '{alert}'"))
                    conn.commit()
                    print(f"   ✅ ml_alert_type: {alert} eklendi - {description}")
                except Exception as e:
                    if "already exists" in str(e):
                        print(f"   ⚠️  ml_alert_type: {alert} zaten mevcut")
                    else:
                        raise
            else:
                print(f"   ⏭️  ml_alert_type: {alert} zaten mevcut")
        
        print()
        print("=" * 60)
        print("✅ PHASE 3 ENUM GÜNCELLEMESİ TAMAMLANDI!")
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
        
        print("📊 Güncel Toplam Enum Değerleri:")
        print()
        print(f"ml_metric_type: {len(all_metrics)} değer")
        for i, metric in enumerate(all_metrics, 1):
            marker = "🆕" if metric in [m[0] for m in new_metrics] else "  "
            print(f"   {marker} {i:2}. {metric}")
        
        print()
        print(f"ml_alert_type: {len(all_alerts)} değer")
        for i, alert in enumerate(all_alerts, 1):
            marker = "🆕" if alert in [a[0] for a in new_alerts] else "  "
            print(f"   {marker} {i:2}. {alert}")
        
        print()
        print("=" * 60)
        print("🎯 QR & TALEP SİSTEMİ ML METRİKLERİ HAZIR!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ HATA: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        exit(1)
