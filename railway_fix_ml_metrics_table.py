"""
Railway ML Metrics Tablosunu Yeniden Oluştur
entity_type kolonunu içeren tam şemayla tabloyu yeniden oluşturur
"""

from flask import Flask
from models import db, MLMetric
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv()

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

def fix_ml_metrics_table():
    """ml_metrics tablosunu düzelt"""
    with app.app_context():
        try:
            print("\n🔧 ML Metrics Tablosu Düzeltiliyor...")
            print("=" * 60)
            
            # 1. Mevcut tablo şemasını kontrol et
            print("\n1️⃣ Mevcut şema kontrol ediliyor...")
            check_query = """
                SELECT column_name, data_type 
                FROM information_schema.columns
                WHERE table_name = 'ml_metrics'
                ORDER BY ordinal_position;
            """
            result = db.session.execute(text(check_query))
            columns = {row[0]: row[1] for row in result.fetchall()}
            
            print(f"   Bulunan kolonlar: {len(columns)}")
            for col, dtype in columns.items():
                mark = "✅" if col in ['id', 'metric_type', 'entity_type', 'entity_id', 'metric_value', 'timestamp', 'extra_data'] else "⚠️"
                print(f"   {mark} {col:<20} : {dtype}")
            
            if 'entity_type' in columns:
                print("\n✅ entity_type kolonu zaten var!")
                print("   Ancak SQLAlchemy görmüyorsa, tablonun DROP+CREATE edilmesi gerekiyor.")
                
                confirm = input("\n❓ Tabloyu silip yeniden oluşturmak istiyor musunuz? (yes/no): ")
                if confirm.lower() != 'yes':
                    print("❌ İşlem iptal edildi.")
                    return False
            
            # 2. Mevcut verileri kontrol et (tablo varsa)
            print("\n2️⃣ Mevcut veriler kontrol ediliyor...")
            try:
                backup_query = """
                    SELECT COUNT(*) as count FROM ml_metrics;
                """
                result = db.session.execute(text(backup_query))
                row_count = result.fetchone()[0]
                
                print(f"   Toplam kayıt: {row_count}")
                
                if row_count > 0:
                    print("   ⚠️  DİKKAT: Tüm ML metrik verileri silinecek!")
                    confirm2 = input("   Devam etmek istiyor musunuz? (yes/no): ")
                    if confirm2.lower() != 'yes':
                        print("❌ İşlem iptal edildi.")
                        return False
            except Exception:
                print("   ℹ️  Tablo bulunamadı, direkt oluşturulacak")
                db.session.rollback()  # Transaction'ı temizle
            
            # 3. Tabloyu ve ENUM tiplerini sil
            print("\n3️⃣ ml_metrics tablosu ve ENUM tipleri siliniyor...")
            db.session.execute(text('DROP TABLE IF EXISTS ml_metrics CASCADE'))
            db.session.execute(text('DROP TYPE IF EXISTS ml_metric_type CASCADE'))
            db.session.commit()
            print("   ✅ Tablo ve ENUM tipleri silindi")
            
            # 4. Tabloyu yeniden oluştur
            print("\n4️⃣ ml_metrics tablosu yeniden oluşturuluyor...")
            
            # SQLAlchemy ile yeni tablo oluştur
            MLMetric.__table__.create(db.engine)
            
            print("   ✅ Tablo oluşturuldu")
            
            # 5. Yeni şemayı doğrula
            print("\n5️⃣ Yeni şema doğrulanıyor...")
            result = db.session.execute(text(check_query))
            new_columns = {row[0]: row[1] for row in result.fetchall()}
            
            print(f"   Yeni kolonlar: {len(new_columns)}")
            for col, dtype in new_columns.items():
                print(f"   ✅ {col:<20} : {dtype}")
            
            # 6. entity_type kolonunu özel olarak kontrol et
            if 'entity_type' in new_columns:
                print("\n✅ entity_type kolonu başarıyla eklendi!")
            else:
                print("\n❌ entity_type kolonu hala eksik!")
                return False
            
            # 7. Test verisi ekle
            print("\n6️⃣ Test verisi ekleniyor...")
            test_insert = """
                INSERT INTO ml_metrics (metric_type, entity_type, entity_id, metric_value, timestamp)
                VALUES ('stok_seviye', 'urun', 1, 100.0, NOW())
                RETURNING id;
            """
            result = db.session.execute(text(test_insert))
            test_id = result.fetchone()[0]
            db.session.commit()
            
            print(f"   ✅ Test kaydı eklendi (ID: {test_id})")
            
            # Test kaydını sil
            db.session.execute(text(f"DELETE FROM ml_metrics WHERE id = {test_id}"))
            db.session.commit()
            print("   🧹 Test kaydı temizlendi")
            
            print("\n" + "=" * 60)
            print("✅ ML METRICS TABLOSU BAŞARIYLA DÜZELTİLDİ!")
            print("=" * 60)
            print("\n📝 Sonraki adımlar:")
            print("   1. Railway'i yeniden başlatın (git push veya redeploy)")
            print("   2. Uygulama loglarını kontrol edin")
            print("   3. ML dashboard'u test edin")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ HATA: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = fix_ml_metrics_table()
    exit(0 if success else 1)
