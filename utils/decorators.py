from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """Giriş yapmış kullanıcı kontrolü"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'kullanici_id' not in session:
            flash('Bu sayfaya erişmek için giriş yapmalısınız.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles):
    """Belirli rollere sahip kullanıcı kontrolü"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'kullanici_id' not in session:
                flash('Bu sayfaya erişmek için giriş yapmalısınız.', 'warning')
                return redirect(url_for('login'))
            
            if 'rol' not in session or session['rol'] not in roles:
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
        
        setup_tamamlandi = SistemAyar.query.filter_by(anahtar='setup_tamamlandi').first()
        
        if not setup_tamamlandi or setup_tamamlandi.deger != '1':
            return redirect(url_for('setup'))
        
        return f(*args, **kwargs)
    return decorated_function


def setup_not_completed(f):
    """Setup tamamlandıysa ana sayfaya yönlendir"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from models import SistemAyar
        
        setup_tamamlandi = SistemAyar.query.filter_by(anahtar='setup_tamamlandi').first()
        
        if setup_tamamlandi and setup_tamamlandi.deger == '1':
            flash('Setup zaten tamamlanmış.', 'info')
            return redirect(url_for('login'))
        
        return f(*args, **kwargs)
    return decorated_function

