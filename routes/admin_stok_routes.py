"""
Admin Stok Route'ları

Bu modül admin stok yönetimi ile ilgili endpoint'leri içerir.

Endpoint'ler:
- /admin/stok-giris - Admin stok girişi
- /admin/stok-hareketleri - Stok hareketleri listesi
- /admin/stok-hareket-duzenle/<int:hareket_id> - Stok hareket düzenleme
- /admin/stok-hareket-sil/<int:hareket_id> - Stok hareket silme

Roller:
- sistem_yoneticisi
- admin
"""

from flask import render_template, request, redirect, url_for, flash, session, jsonify
from models import db, StokHareket, Urun
from utils.decorators import login_required, role_required
from utils.helpers import log_islem, log_hata
from utils.audit import audit_create, audit_update, audit_delete, serialize_model


def register_admin_stok_routes(app):
    """Admin stok route'larını kaydet"""
    
    @app.route('/admin/stok-giris', methods=['GET', 'POST'])
    @login_required
    @role_required('sistem_yoneticisi', 'admin')
    def admin_stok_giris():
        """Admin için stok giriş sayfası"""
        from forms import StokGirisForm
        
        form = StokGirisForm()
        
        if form.validate_on_submit():
            try:
                # Stok hareketi oluştur
                hareket = StokHareket(
                    urun_id=form.urun_id.data,
                    hareket_tipi='giris',
                    miktar=form.miktar.data,
                    aciklama=form.aciklama.data,
                    islem_yapan_id=session['kullanici_id']
                )
                db.session.add(hareket)
                db.session.commit()
                
                # Audit log
                audit_create(
                    tablo_adi='stok_hareketleri',
                    kayit_id=hareket.id,
                    yeni_deger=serialize_model(hareket),
                    aciklama='Admin stok girişi'
                )
                
                # Log kaydı
                log_islem('ekleme', 'stok_giris', {
                    'urun_id': hareket.urun_id,
                    'miktar': hareket.miktar,
                    'aciklama': hareket.aciklama
                })
                
                flash('Stok girişi başarıyla kaydedildi.', 'success')
                return redirect(url_for('admin_stok_giris'))
                
            except Exception as e:
                db.session.rollback()
                log_hata(e, modul='admin_stok_giris')
                flash('Stok girişi sırasında hata oluştu.', 'danger')
        
        # Ürünleri getir
        urunler = Urun.query.filter_by(aktif=True).order_by(Urun.urun_adi).all()
        
        return render_template('sistem_yoneticisi/admin_stok_giris.html',
                             form=form,
                             urunler=urunler)

    @app.route('/admin/stok-hareketleri')
    @login_required
    @role_required('sistem_yoneticisi', 'admin')
    def admin_stok_hareketleri():
        """Tüm stok hareketlerini listele"""
        try:
            # Filtreler
            urun_id = request.args.get('urun_id', type=int)
            hareket_tipi = request.args.get('hareket_tipi', '')
            baslangic_tarih = request.args.get('baslangic_tarih', '')
            bitis_tarih = request.args.get('bitis_tarih', '')
            
            # Sayfalama
            sayfa = request.args.get('sayfa', 1, type=int)
            per_page = 50
            
            # Sorgu oluştur
            query = StokHareket.query.options(
                db.joinedload(StokHareket.urun),
                db.joinedload(StokHareket.islem_yapan)
            )
            
            if urun_id:
                query = query.filter(StokHareket.urun_id == urun_id)
            if hareket_tipi:
                query = query.filter(StokHareket.hareket_tipi == hareket_tipi)
            if baslangic_tarih:
                query = query.filter(StokHareket.islem_tarihi >= baslangic_tarih)
            if bitis_tarih:
                query = query.filter(StokHareket.islem_tarihi <= bitis_tarih)
            
            # Sayfalama
            hareketler = query.order_by(StokHareket.islem_tarihi.desc()).paginate(
                page=sayfa, per_page=per_page, error_out=False
            )
            
            # Ürünler (filtre için)
            urunler = Urun.query.filter_by(aktif=True).order_by(Urun.urun_adi).all()
            
            # Log kaydı
            log_islem('goruntuleme', 'stok_hareketleri', {
                'sayfa': sayfa,
                'kayit_sayisi': hareketler.total
            })
            
            return render_template('sistem_yoneticisi/admin_stok_hareketleri.html',
                                 hareketler=hareketler,
                                 urunler=urunler,
                                 urun_id=urun_id,
                                 hareket_tipi=hareket_tipi,
                                 baslangic_tarih=baslangic_tarih,
                                 bitis_tarih=bitis_tarih)
            
        except Exception as e:
            log_hata(e, modul='admin_stok_hareketleri')
            flash('Stok hareketleri yüklenirken hata oluştu.', 'danger')
            return redirect(url_for('sistem_yoneticisi_dashboard'))

    @app.route('/admin/stok-hareket-duzenle/<int:hareket_id>', methods=['GET', 'POST'])
    @login_required
    @role_required('sistem_yoneticisi', 'admin')
    def admin_stok_hareket_duzenle(hareket_id):
        """Stok hareket kaydını düzenle"""
        from forms import StokGirisForm
        
        hareket = db.session.get(StokHareket, hareket_id)
        if not hareket:
            flash('Stok hareketi bulunamadı.', 'danger')
            return redirect(url_for('admin_stok_hareketleri'))
        
        # Eski değeri sakla
        eski_deger = serialize_model(hareket)
        
        form = StokGirisForm(obj=hareket)
        
        if form.validate_on_submit():
            try:
                hareket.urun_id = form.urun_id.data
                hareket.miktar = form.miktar.data
                hareket.aciklama = form.aciklama.data
                
                db.session.commit()
                
                # Audit log
                audit_update(
                    tablo_adi='stok_hareketleri',
                    kayit_id=hareket.id,
                    eski_deger=eski_deger,
                    yeni_deger=serialize_model(hareket),
                    aciklama='Admin stok hareket düzenleme'
                )
                
                # Log kaydı
                log_islem('guncelleme', 'stok_hareketi', {
                    'hareket_id': hareket.id,
                    'urun_id': hareket.urun_id
                })
                
                flash('Stok hareketi başarıyla güncellendi.', 'success')
                return redirect(url_for('admin_stok_hareketleri'))
                
            except Exception as e:
                db.session.rollback()
                log_hata(e, modul='admin_stok_hareket_duzenle')
                flash('Güncelleme sırasında hata oluştu.', 'danger')
        
        urunler = Urun.query.filter_by(aktif=True).order_by(Urun.urun_adi).all()
        
        return render_template('sistem_yoneticisi/admin_stok_hareket_duzenle.html',
                             form=form,
                             hareket=hareket,
                             urunler=urunler)

    @app.route('/admin/stok-hareket-sil/<int:hareket_id>', methods=['POST'])
    @login_required
    @role_required('sistem_yoneticisi', 'admin')
    def admin_stok_hareket_sil(hareket_id):
        """Stok hareket kaydını sil"""
        try:
            hareket = db.session.get(StokHareket, hareket_id)
            if not hareket:
                return jsonify({'success': False, 'message': 'Stok hareketi bulunamadı'}), 404
            
            # Eski değeri sakla
            eski_deger = serialize_model(hareket)
            
            # Sil
            db.session.delete(hareket)
            db.session.commit()
            
            # Audit log
            audit_delete(
                tablo_adi='stok_hareketleri',
                kayit_id=hareket_id,
                eski_deger=eski_deger,
                aciklama='Admin stok hareket silme'
            )
            
            # Log kaydı
            log_islem('silme', 'stok_hareketi', {
                'hareket_id': hareket_id,
                'urun_id': hareket.urun_id
            })
            
            flash('Stok hareketi başarıyla silindi.', 'success')
            return jsonify({'success': True, 'message': 'Stok hareketi silindi'})
            
        except Exception as e:
            db.session.rollback()
            log_hata(e, modul='admin_stok_hareket_sil')
            return jsonify({'success': False, 'message': 'Silme işlemi başarısız'}), 500
