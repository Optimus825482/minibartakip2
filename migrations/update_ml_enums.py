"""
ML Enum Güncelleme - Phase 2
Yeni metrik ve alert tiplerini ekler
"""

import sys
import os

# Parent directory'yi path'e ekle
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db

print("=" * 60)
print("🔧 ML ENUM GÜNCELLEMESİ - PHASE 2")
print("=" * 60)
print()

with app.app_context():
    try:
        # PostgreSQL enum'larını güncelle
        print("📝 Enum'lar güncelleniyor...")
        
        # ml_metric_type enum'una yeni değerler ekle
        db.session.execute(db.text("""
            ALTER TYPE ml_metric_type ADD VALUE IF NOT EXISTS 'zimmet_kullanim';
            ALTER TYPE ml_metric_type ADD VALUE IF NOT EXISTS 'zimmet_fire';
            ALTER TYPE ml_metric_type ADD VALUE IF NOT EXISTS 'doluluk_oran';
            ALTER TYPE ml_metric_type ADD VALUE IF NOT EXISTS 'bosta_tuketim';
        """))
        
        print("   ✅ ml_metric_type güncellendi")
        
        # ml_alert_type enum'una yeni değerler ekle
        db.session.execute(db.text("""
            ALTER TYPE ml_alert_type ADD VALUE IF NOT EXISTS 'zimmet_fire_yuksek';
            ALTER TYPE ml_alert_type ADD VALUE IF NOT EXISTS 'zimmet_kullanim_dusuk';
            ALTER TYPE ml_alert_type ADD VALUE IF NOT EXISTS 'bosta_tuketim_var';
            ALTER TYPE ml_alert_type ADD VALUE IF NOT EXISTS 'doluda_tuketim_yok';
        """))
        
        print("   ✅ ml_alert_type güncellendi")
        
        db.session.commit()
        
        print()
        print("=" * 60)
        print("✅ ENUM GÜNCELLEMESİ TAMAMLANDI!")
        print("=" * 60)
        print()
        print("Yeni Metrik Tipleri:")
        print("   - zimmet_kullanim")
        print("   - zimmet_fire")
        print("   - doluluk_oran")
        print("   - bosta_tuketim")
        print()
        print("Yeni Alert Tipleri:")
        print("   - zimmet_fire_yuksek")
        print("   - zimmet_kullanim_dusuk")
        print("   - bosta_tuketim_var")
        print("   - doluda_tuketim_yok")
        print()
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ HATA: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        sys.exit(1)
