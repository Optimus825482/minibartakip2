"""
ML Enum Güncelleme - Phase 3
QR ve Talep sistemi metriklerini ekler
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db

print("=" * 60)
print("🔧 ML ENUM GÜNCELLEMESİ - PHASE 3 (QR & TALEP)")
print("=" * 60)
print()

with app.app_context():
    try:
        print("📝 Enum'lar güncelleniyor...")
        
        # ml_metric_type enum'una yeni değerler ekle
        db.session.execute(db.text("""
            ALTER TYPE ml_metric_type ADD VALUE IF NOT EXISTS 'talep_yanit_sure';
            ALTER TYPE ml_metric_type ADD VALUE IF NOT EXISTS 'talep_yogunluk';
            ALTER TYPE ml_metric_type ADD VALUE IF NOT EXISTS 'qr_okutma_siklik';
        """))
        
        print("   ✅ ml_metric_type güncellendi")
        
        # ml_alert_type enum'una yeni değerler ekle
        db.session.execute(db.text("""
            ALTER TYPE ml_alert_type ADD VALUE IF NOT EXISTS 'talep_yanitlanmadi';
            ALTER TYPE ml_alert_type ADD VALUE IF NOT EXISTS 'talep_yogunluk_yuksek';
            ALTER TYPE ml_alert_type ADD VALUE IF NOT EXISTS 'qr_kullanim_dusuk';
        """))
        
        print("   ✅ ml_alert_type güncellendi")
        
        db.session.commit()
        
        print()
        print("=" * 60)
        print("✅ ENUM GÜNCELLEMESİ TAMAMLANDI!")
        print("=" * 60)
        print()
        print("Yeni Metrik Tipleri:")
        print("   - talep_yanit_sure (Talep yanıt süresi)")
        print("   - talep_yogunluk (Oda/kat bazlı talep sayısı)")
        print("   - qr_okutma_siklik (Personel QR okutma sıklığı)")
        print()
        print("Yeni Alert Tipleri:")
        print("   - talep_yanitlanmadi (Uzun süre yanıtlanmayan talep)")
        print("   - talep_yogunluk_yuksek (Aşırı talep yoğunluğu)")
        print("   - qr_kullanim_dusuk (QR sistemi az kullanılıyor)")
        print()
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ HATA: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        sys.exit(1)
