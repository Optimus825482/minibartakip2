#!/usr/bin/env python3
"""
Startup ML Fix - Railway deployment sonrası otomatik çalışır
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect

def fix_ml_models_columns(engine):
    """ML Models tablosundaki Türkçe kolon isimlerini İngilizce'ye çevir"""
    try:
        inspector = inspect(engine)
        
        if 'ml_models' not in inspector.get_table_names():
            print("⚠️  ml_models tablosu yok")
            return True
        
        columns = [col['name'] for col in inspector.get_columns('ml_models')]
        print(f"📋 ml_models kolonları: {columns}")
        
        # Türkçe kolon isimleri varsa değiştir
        renames = {
            'model_tipi': 'model_type',
            'metrik_tipi': 'metric_type',
            'model_verisi': 'model_data',
            'parametreler': 'parameters',
            'egitim_tarihi': 'training_date',
            'dogruluk': 'accuracy',
            'kesinlik': 'precision',
            'duyarlilik': 'recall',
            'aktif': 'is_active'
        }
        
        renamed_count = 0
        with engine.connect() as conn:
            for old_name, new_name in renames.items():
                if old_name in columns:
                    print(f"🔧 {old_name} -> {new_name}")
                    conn.execute(text(f"ALTER TABLE ml_models RENAME COLUMN {old_name} TO {new_name};"))
                    renamed_count += 1
            
            if renamed_count > 0:
                conn.commit()
                print(f"✅ {renamed_count} kolon ismi değiştirildi!")
            else:
                print("✅ ml_models kolonları zaten doğru")
        
        return True
        
    except Exception as e:
        print(f"⚠️  ml_models fix hatası: {str(e)}")
        return True


def fix_ml_metrics_on_startup():
    """Startup'ta ML Metrics tablosunu kontrol et ve düzelt"""
    try:
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("⚠️  DATABASE_URL yok, fix atlanıyor")
            return True
        
        # PostgreSQL URL fix
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql+psycopg2://', 1)
        elif database_url.startswith('postgresql://'):
            database_url = database_url.replace('postgresql://', 'postgresql+psycopg2://', 1)
        
        print("🔧 ML Metrics tablosu kontrol ediliyor...")
        engine = create_engine(database_url)
        inspector = inspect(engine)
        
        if 'ml_metrics' not in inspector.get_table_names():
            print("⚠️  ml_metrics tablosu yok, fix atlanıyor")
            return True
        
        columns = [col['name'] for col in inspector.get_columns('ml_metrics')]
        print(f"📋 Mevcut kolonlar: {columns}")
        
        # entity_id yoksa tabloyu yeniden oluştur
        if 'entity_id' not in columns:
            print("🔧 entity_id kolonu yok, tablo yeniden oluşturuluyor...")
            
            with engine.connect() as conn:
                # Tabloyu sil ve yeniden oluştur
                conn.execute(text("DROP TABLE IF EXISTS ml_metrics CASCADE;"))
                conn.execute(text("""
                    CREATE TABLE ml_metrics (
                        id SERIAL PRIMARY KEY,
                        metric_type VARCHAR(50) NOT NULL,
                        entity_id INTEGER NOT NULL,
                        metric_value DOUBLE PRECISION NOT NULL,
                        timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                        extra_data JSONB
                    );
                """))
                conn.execute(text("CREATE INDEX idx_ml_metrics_type_time ON ml_metrics(metric_type, timestamp);"))
                conn.execute(text("CREATE INDEX idx_ml_metrics_entity ON ml_metrics(entity_id);"))
                conn.commit()
                
            print("✅ ML Metrics tablosu yeniden oluşturuldu!")
            return True
        
        # entity_type varsa kaldır
        if 'entity_type' in columns:
            print("🔧 entity_type kolonu kaldırılıyor...")
            
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE ml_metrics DROP COLUMN IF EXISTS entity_type CASCADE;"))
                conn.execute(text("DROP INDEX IF EXISTS idx_ml_metrics_entity;"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_ml_metrics_entity ON ml_metrics(entity_id);"))
                conn.commit()
            
            print("✅ entity_type kolonu kaldırıldı!")
            return True
        
        print("✅ ML Metrics tablosu doğru yapıda")
        
        # ML Models tablosunu da düzelt
        fix_ml_models_columns(engine)
        
        return True
        
    except Exception as e:
        print(f"⚠️  ML Metrics fix hatası (devam ediliyor): {str(e)}")
        return True  # Hata olsa bile uygulama başlasın

if __name__ == '__main__':
    fix_ml_metrics_on_startup()
