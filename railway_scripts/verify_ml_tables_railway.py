"""
Railway ML tablolarının model ile uyumunu kontrol et
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv('.env.railway')

DATABASE_URL = os.getenv('RAILWAY_DATABASE_URL')
engine = create_engine(DATABASE_URL)

print("🔍 ML Tablolarını Kontrol Ediyorum...\n")

# Beklenen tablo yapıları
expected_structures = {
    'ml_metrics': [
        'id', 'metric_type', 'otel_id', 'urun_id', 'tarih', 
        'deger', 'tahmin_degeri', 'anomali_skoru', 'is_anomali', 
        'metadata', 'olusturulma_tarihi'
    ],
    'ml_models': [
        'id', 'model_adi', 'model_tipi', 'versiyon', 'dosya_yolu',
        'otel_id', 'egitim_tarihi', 'performans_metrikleri', 
        'aktif', 'aciklama', 'olusturulma_tarihi'
    ],
    'ml_alerts': [
        'id', 'alert_type', 'severity', 'entity_type', 'entity_id',
        'metric_value', 'expected_value', 'deviation_percent', 
        'message', 'suggested_action', 'created_at', 'is_read',
        'is_false_positive', 'resolved_at', 'resolved_by_id'
    ],
    'ml_training_logs': [
        'id', 'model_id', 'baslangic_zamani', 'bitis_zamani',
        'durum', 'veri_sayisi', 'egitim_suresi_sn', 'hata_mesaji',
        'metrikler', 'olusturulma_tarihi'
    ]
}

problems = []

with engine.connect() as conn:
    for table_name, expected_cols in expected_structures.items():
        result = conn.execute(text(f"""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position
        """))
        
        actual_cols = [row[0] for row in result]
        
        missing = set(expected_cols) - set(actual_cols)
        extra = set(actual_cols) - set(expected_cols)
        
        if missing or extra:
            problems.append(table_name)
            print(f"⚠️  {table_name}:")
            if missing:
                print(f"   Eksik kolonlar: {', '.join(missing)}")
            if extra:
                print(f"   Fazla kolonlar: {', '.join(extra)}")
            print()
        else:
            print(f"✅ {table_name}: Uyumlu")

if not problems:
    print("\n🎉 Tüm ML tabloları model ile uyumlu!")
else:
    print(f"\n⚠️  {len(problems)} tabloda sorun var: {', '.join(problems)}")
