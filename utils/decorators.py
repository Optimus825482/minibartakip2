from functools import wraps
from flask import session, redirect, url_for, flash
from sqlalchemy.exc import OperationalError, TimeoutError
import time
import logging

logger = logging.getLogger(__name__)

def db_query_with_retry(query_func, max_retries=3, retry_delay=1):
    """
    Database query'lerini retry mekanizması ile çalıştır
    Railway timeout sorunlarını çözer
    """
    for attempt in range(max_retries):
        try:
            return query_func()
        except (OperationalError, TimeoutError) as e:
            logger.warning(f"⚠️ DB Query timeout (Deneme {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 1.5  # Exponential backoff
            else:
                logger.error(f"❌ DB Query {max_retries} denemeden sonra başarısız!")
                raise
        except Exception as e:
            logger.error(f"❌ DB Query beklenmeyen hata: {str(e)}")
            raise
    return None

def login_required(f):
    """Giriş yapmış kullanıcı kontrolü"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request, jsonify
        
        if 'kullanici_id' not in session:
            # API isteği mi kontrol et
            if request.path.startswith('/api/') or request.is_json:
                return jsonify({'success': False, 'error': 'Giriş yapmalısınız'}), 401
            flash('Bu sayfaya erişmek için giriş yapmalısınız.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def role_required(*allowed_roles):
    """Belirli rollere sahip kullanıcı kontrolü
    
    Kullanım:
        @role_required('admin')  # Tek rol
        @role_required('admin', 'sistem_yoneticisi')  # Çoklu rol
        @role_required(['admin', 'sistem_yoneticisi'])  # Liste olarak da olabilir
    """
    # Eğer tek parametre ve liste/tuple ise, onu düzleştir
    if len(allowed_roles) == 1 and isinstance(allowed_roles[0], (list, tuple)):
        allowed_roles = allowed_roles[0]
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request, jsonify
            
            if 'kullanici_id' not in session:
                # API isteği mi kontrol et
                if request.path.startswith('/api/') or request.is_json:
                    return jsonify({'success': False, 'error': 'Giriş yapmalısınız'}), 401
                flash('Bu sayfaya erişmek için giriş yapmalısınız.', 'warning')
                return redirect(url_for('login'))
            
            # Rol kontrolü
            if 'rol' not in session or session['rol'] not in allowed_roles:
                # API isteği mi kontrol et
                if request.path.startswith('/api/') or request.is_json:
                    # Debug için ekstra bilgi
                    error_msg = f"Bu işlem için yetkiniz yok (Gerekli: {', '.join(allowed_roles)}, Mevcut: {session.get('rol', 'Yok')})"
                    return jsonify({'success': False, 'error': error_msg}), 403
                flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
                return redirect(url_for('dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def setup_required(f):
    """Setup tamamlanmamışsa setup sayfasına yönlendir"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from models import SistemAyar
        
        try:
            # Retry mekanizması ile query çalıştır
            setup_tamamlandi = db_query_with_retry(
                lambda: SistemAyar.query.filter_by(anahtar='setup_tamamlandi').first()
            )
            
            if not setup_tamamlandi or setup_tamamlandi.deger != '1':
                return redirect(url_for('setup'))
        except Exception as e:
            logger.error(f"❌ Setup kontrolü başarısız: {str(e)}")
            flash('Veritabanı bağlantı hatası. Lütfen tekrar deneyin.', 'danger')
            return redirect(url_for('login'))
        
        return f(*args, **kwargs)
    return decorated_function


def setup_not_completed(f):
    """Setup tamamlandıysa ana sayfaya yönlendir"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from models import SistemAyar
        
        try:
            # Retry mekanizması ile query çalıştır
            setup_tamamlandi = db_query_with_retry(
                lambda: SistemAyar.query.filter_by(anahtar='setup_tamamlandi').first()
            )
            
            if setup_tamamlandi and setup_tamamlandi.deger == '1':
                flash('Setup zaten tamamlanmış.', 'info')
                return redirect(url_for('login'))
        except Exception as e:
            logger.error(f"❌ Setup kontrolü başarısız: {str(e)}")
            # Setup sayfasına devam et
            pass
        
        return f(*args, **kwargs)
    return decorated_function

