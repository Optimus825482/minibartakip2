"""
Railway veritabanına ML tablolarını ekle
"""
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import text
from flask import Flask
from models import db

# .env.railway dosyasını yükle
load_dotenv('.env.railway')

# Railway DATABASE_URL'i kullan
DATABASE_URL = os.getenv('RAILWAY_DATABASE_URL')

if not DATABASE_URL:
    print("❌ RAILWAY_DATABASE_URL bulunamadı!")
    sys.exit(1)

print("🔗 Railway veritabanına bağlanılıyor...")
print("   Host: shinkansen.proxy.rlwy.net:27699")

# Flask uygulaması oluştur
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')

db.init_app(app)

def upgrade():
    """ML tablolarını oluştur"""
    with app.app_context():
        try:
            print("\n🚀 ML tabloları oluşturuluyor...")
            
            # Tüm tabloları oluştur (sadece yeni olanlar oluşturulur)
            db.create_all()
            
            print("\n✅ ML tabloları başarıyla oluşturuldu!")
            print("   - ml_metrics")
            print("   - ml_models")
            print("   - ml_alerts")
            print("   - ml_training_logs")
            print("   - Index'ler oluşturuldu")
            
            # Tabloların varlığını kontrol et
            print("\n🔍 Tablolar kontrol ediliyor...")
            result = db.session.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name LIKE 'ml_%'
                ORDER BY table_name
            """))
            
            tables = [row[0] for row in result]
            if tables:
                print("   Oluşturulan ML tabloları:")
                for table in tables:
                    print(f"   ✓ {table}")
            else:
                print("   ⚠️  ML tablosu bulunamadı!")
            
        except Exception as e:
            print(f"\n❌ Hata: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

if __name__ == '__main__':
    upgrade()
