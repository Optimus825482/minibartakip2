#!/usr/bin/env python3
"""
Railway ML Metrics Entity Type Fix
Tarih: 2025-11-09
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect

def fix_railway_ml_metrics():
    """Railway'de ML Metrics tablosunu düzelt"""
    try:
        # Railway DATABASE_URL
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL bulunamadı!")
            return False
        
        # postgresql:// -> postgresql+psycopg2://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql+psycopg2://', 1)
        elif database_url.startswith('postgresql://'):
            database_url = database_url.replace('postgresql://', 'postgresql+psycopg2://', 1)
        
        print("🚂 Railway veritabanına bağlanılıyor...")
        engine = create_engine(database_url)
        
        print("🔍 ML Metrics tablosu kontrol ediliyor...")
        inspector = inspect(engine)
        
        if 'ml_metrics' not in inspector.get_table_names():
            print("❌ ml_metrics tablosu bulunamadı!")
            return False
        
        columns = [col['name'] for col in inspector.get_columns('ml_metrics')]
        print(f"📋 Mevcut kolonlar: {columns}")
        
        if 'entity_type' not in columns:
            print("✅ entity_type kolonu zaten yok. İşlem gerekmiyor.")
            return True
        
        print("🔧 entity_type kolonu kaldırılıyor...")
        
        with engine.connect() as conn:
            # entity_type kolonunu kaldır
            conn.execute(text("""
                ALTER TABLE ml_metrics 
                DROP COLUMN IF EXISTS entity_type CASCADE;
            """))
            conn.commit()
            
            print("✅ entity_type kolonu kaldırıldı!")
            
            # Index'i güncelle
            print("🔧 Index güncelleniyor...")
            conn.execute(text("""
                DROP INDEX IF EXISTS idx_ml_metrics_entity;
                CREATE INDEX IF NOT EXISTS idx_ml_metrics_entity ON ml_metrics(entity_id);
            """))
            conn.commit()
            
            print("✅ Index güncellendi!")
        
        # Kontrol
        inspector = inspect(engine)
        columns_after = [col['name'] for col in inspector.get_columns('ml_metrics')]
        print(f"📋 Güncel kolonlar: {columns_after}")
        
        if 'entity_type' in columns_after:
            print("❌ entity_type kolonu hala var!")
            return False
        
        print("\n✅ ML Metrics tablosu başarıyla düzeltildi!")
        return True
        
    except Exception as e:
        print(f"❌ HATA: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("RAILWAY ML METRICS ENTITY TYPE FIX")
    print("=" * 60)
    
    success = fix_railway_ml_metrics()
    
    if success:
        print("\n✅ İşlem tamamlandı!")
        sys.exit(0)
    else:
        print("\n❌ İşlem başarısız!")
        sys.exit(1)
