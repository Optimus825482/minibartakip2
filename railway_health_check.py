#!/usr/bin/env python3
"""
Railway Health Check Script
Database bağlantısını kontrol eder ve sorunları tespit eder
"""

import os
import sys
import time
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, TimeoutError

# Logging ayarla
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_database_url():
    """Database URL'ini environment variable'lardan al"""
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        # Heroku postgres:// -> postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://')
        return database_url
    
    # Railway internal variables
    pghost = os.getenv('PGHOST')
    pguser = os.getenv('PGUSER')
    pgpassword = os.getenv('PGPASSWORD')
    pgdatabase = os.getenv('PGDATABASE')
    pgport = os.getenv('PGPORT', '5432')
    
    if pghost and pguser:
        return f'postgresql+psycopg2://{pguser}:{pgpassword}@{pghost}:{pgport}/{pgdatabase}'
    
    logger.error("❌ Database URL bulunamadı!")
    return None

def test_connection(max_retries=5, retry_delay=2):
    """Database bağlantısını test et"""
    database_url = get_database_url()
    
    if not database_url:
        return False
    
    logger.info(f"🔍 Database bağlantısı test ediliyor...")
    logger.info(f"📍 Host: {os.getenv('PGHOST', 'N/A')}")
    logger.info(f"📍 Port: {os.getenv('PGPORT', 'N/A')}")
    logger.info(f"📍 Database: {os.getenv('PGDATABASE', 'N/A')}")
    
    for attempt in range(max_retries):
        try:
            # Engine oluştur - Railway için optimize edilmiş ayarlar
            engine = create_engine(
                database_url,
                pool_size=2,
                max_overflow=3,
                pool_timeout=60,
                pool_recycle=1800,
                pool_pre_ping=True,
                connect_args={
                    'connect_timeout': 30,
                    'keepalives': 1,
                    'keepalives_idle': 60,
                    'keepalives_interval': 10,
                    'keepalives_count': 5,
                }
            )
            
            # Bağlantıyı test et
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                result.fetchone()
                
            logger.info(f"✅ Database bağlantısı başarılı! (Deneme {attempt + 1}/{max_retries})")
            engine.dispose()
            return True
            
        except (OperationalError, TimeoutError) as e:
            logger.warning(f"⚠️ Bağlantı hatası (Deneme {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"🔄 {retry_delay} saniye sonra tekrar denenecek...")
                time.sleep(retry_delay)
                retry_delay *= 1.5  # Exponential backoff
            else:
                logger.error(f"❌ Database bağlantısı {max_retries} denemeden sonra başarısız!")
                return False
                
        except Exception as e:
            logger.error(f"❌ Beklenmeyen hata: {str(e)}")
            return False
    
    return False

def main():
    """Ana fonksiyon"""
    logger.info("=" * 60)
    logger.info("🚀 Railway Database Health Check")
    logger.info("=" * 60)
    
    success = test_connection()
    
    if success:
        logger.info("=" * 60)
        logger.info("✅ Health Check BAŞARILI!")
        logger.info("=" * 60)
        sys.exit(0)
    else:
        logger.error("=" * 60)
        logger.error("❌ Health Check BAŞARISIZ!")
        logger.error("=" * 60)
        sys.exit(1)

if __name__ == '__main__':
    main()
