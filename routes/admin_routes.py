"""
Admin Route'ları

Bu modül admin rolü ile ilgili endpoint'leri içerir.

Endpoint'ler:
- /personel-tanimla - Personel tanımlama ve listeleme
- /personel-duzenle/<int:personel_id> - Personel düzenleme
- /personel-pasif-yap/<int:personel_id> - Personel pasif yapma
- /personel-aktif-yap/<int:personel_id> - Personel aktif yapma
- /urun-gruplari - Ürün grupları tanımlama ve listeleme
- /grup-duzenle/<int:grup_id> - Ürün grubu düzenleme
- /grup-sil/<int:grup_id> - Ürün grubu silme
- /grup-pasif-yap/<int:grup_id> - Ürün grubu pasif yapma
- /grup-aktif-yap/<int:grup_id> - Ürün grubu aktif yapma
- /urunler - Ürün tanımlama ve listeleme
- /urun-duzenle/<int:urun_id> - Ürün düzenleme
- /urun-sil/<int:urun_id> - Ürün silme
- /urun-pasif-yap/<int:urun_id> - Ürün pasif yapma
- /urun-aktif-yap/<int:urun_id> - Ürün aktif yapma

Roller:
- sistem_yoneticisi
- admin
"""

from flask import render_template, request, redirect, url_for, flash, session
from models import db, Kullanici, UrunGrup, Urun, StokHareket
from utils.decorators import login_required, role_required
from utils.helpers import log_islem, log_hata
from utils.audit import audit_create, audit_update, audit_delete, serialize_model


def register_admin_routes(app):
    """Admin route'larını kaydet"""
    
    # ============================================================================
    # PERSONEL YÖNETİMİ
    # ============================================================================
    
    @app.route('/personel-tanimla', methods=['GET', 'POST'])
    @login_required
    @role_required('sistem_yoneticisi', 'admin')
    def personel_tanimla():
        """Personel tanımlama ve listeleme"""
        from forms import PersonelForm
        from sqlalchemy.exc import IntegrityError

        form = PersonelForm()

        if form.validate_on_submit():
            try:
                personel = Kullanici(
                    kullanici_adi=form.kullanici_adi.data,
                    ad=form.ad.data,
                    soyad=form.soyad.data,
                    email=form.email.data or '',
                    telefon=form.telefon.data or '',
                    rol=form.rol.data
                )
                personel.sifre_belirle(form.sifre.data)
                db.session.add(personel)
                db.session.commit()

                # Audit Trail
                audit_create('kullanici', personel.id, personel)

                flash('Kullanıcı başarıyla eklendi.', 'success')
                return redirect(url_for('personel_tanimla'))

            except IntegrityError as e:
                db.session.rollback()
                error_msg = str(e)

                # Kullanıcı dostu hata mesajları
                if 'kullanici_adi' in error_msg:
                    flash('Bu kullanıcı adı zaten kullanılıyor. Lütfen farklı bir kullanıcı adı seçin.', 'danger')
                elif 'email' in error_msg:
                    flash('Bu e-posta adresi zaten kullanılıyor. Lütfen farklı bir e-posta adresi seçin.', 'danger')
                else:
                    flash('Kayıt sırasında bir hata oluştu.', 'danger')
                log_hata(e, modul='personel_tanimla')

            except Exception as e:
                db.session.rollback()
                flash('Beklenmeyen bir hata oluştu. Lütfen sistem yöneticisine başvurun.', 'danger')
                log_hata(e, modul='personel_tanimla')

        personeller = Kullanici.query.filter(
            Kullanici.rol.in_(['admin', 'depo_sorumlusu', 'kat_sorumlusu']),
            Kullanici.aktif.is_(True)
        ).order_by(Kullanici.olusturma_tarihi.desc()).all()
        return render_template('admin/personel_tanimla.html', form=form, personeller=personeller)

    @app.route('/personel-duzenle/<int:personel_id>', methods=['GET', 'POST'])
    @login_required
    @role_required('sistem_yoneticisi', 'admin')
    def personel_duzenle(personel_id):
        """Personel düzenleme"""
        from forms import PersonelDuzenleForm
        from sqlalchemy.exc import IntegrityError

        personel = Kullanici.query.get_or_404(personel_id)
        form = PersonelDuzenleForm(obj=personel)

        if form.validate_on_submit():
            try:
                # Eski değerleri kaydet
                eski_deger = serialize_model(personel)

                personel.kullanici_adi = form.kullanici_adi.data
                personel.ad = form.ad.data
                personel.soyad = form.soyad.data
                personel.email = form.email.data or ''
                personel.telefon = form.telefon.data or ''
                personel.rol = form.rol.data

                # Şifre değiştirilmişse
                if form.yeni_sifre.data:
                    personel.sifre_belirle(form.yeni_sifre.data)

                db.session.commit()

                # Audit Trail
                audit_update('kullanici', personel.id, eski_deger, personel)

                flash('Kullanıcı başarıyla güncellendi.', 'success')
                return redirect(url_for('personel_tanimla'))

            except IntegrityError as e:
                db.session.rollback()
                error_msg = str(e)

                # Kullanıcı dostu hata mesajları
                if 'kullanici_adi' in error_msg:
                    flash('Bu kullanıcı adı zaten kullanılıyor. Lütfen farklı bir kullanıcı adı seçin.', 'danger')
                elif 'email' in error_msg:
                    flash('Bu e-posta adresi zaten kullanılıyor. Lütfen farklı bir e-posta adresi seçin.', 'danger')
                else:
                    flash('Güncelleme sırasında bir hata oluştu.', 'danger')
                log_hata(e, modul='personel_duzenle')

            except Exception as e:
                db.session.rollback()
                flash('Beklenmeyen bir hata oluştu. Lütfen sistem yöneticisine başvurun.', 'danger')
                log_hata(e, modul='personel_duzenle')

        return render_template('admin/personel_duzenle.html', form=form, personel=personel)

    @app.route('/personel-pasif-yap/<int:personel_id>', methods=['POST'])
    @login_required
    @role_required('sistem_yoneticisi', 'admin')
    def personel_pasif_yap(personel_id):
        """Personel pasif yapma"""
        try:
            personel = Kullanici.query.get_or_404(personel_id)
            eski_deger = serialize_model(personel)
            personel.aktif = False
            db.session.commit()
            
            # Audit Trail
            audit_update('kullanici', personel.id, eski_deger, personel)
            
            flash('Kullanıcı başarıyla pasif yapıldı.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Hata oluştu: {str(e)}', 'danger')
        
        return redirect(url_for('personel_tanimla'))

    @app.route('/personel-aktif-yap/<int:personel_id>', methods=['POST'])
    @login_required
    @role_required('sistem_yoneticisi', 'admin')
    def personel_aktif_yap(personel_id):
        """Personel aktif yapma"""
        try:
            personel = Kullanici.query.get_or_404(personel_id)
            eski_deger = serialize_model(personel)
            personel.aktif = True
            db.session.commit()
            
            # Audit Trail
            audit_update('kullanici', personel.id, eski_deger, personel)
            
            flash('Kullanıcı başarıyla aktif yapıldı.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Hata oluştu: {str(e)}', 'danger')
        
        return redirect(url_for('personel_tanimla'))

    # ============================================================================
    # ÜRÜN GRUBU YÖNETİMİ
    # ============================================================================

    @app.route('/urun-gruplari', methods=['GET', 'POST'])
    @login_required
    @role_required('sistem_yoneticisi', 'admin')
    def urun_gruplari():
        """Ürün grupları tanımlama ve listeleme"""
        from forms import UrunGrupForm
        from sqlalchemy.exc import IntegrityError

        form = UrunGrupForm()

        if form.validate_on_submit():
            try:
                grup = UrunGrup(
                    grup_adi=form.grup_adi.data,
                    aciklama=form.aciklama.data or ''
                )
                db.session.add(grup)
                db.session.commit()

                # Audit Trail
                audit_create('urun_grup', grup.id, grup)

                flash('Ürün grubu başarıyla eklendi.', 'success')
                return redirect(url_for('urun_gruplari'))

            except IntegrityError as e:
                db.session.rollback()
                flash('Bu grup adı zaten kullanılıyor. Lütfen farklı bir ad girin.', 'danger')
                log_hata(e, modul='urun_gruplari')

            except Exception as e:
                db.session.rollback()
                flash('Beklenmeyen bir hata oluştu. Lütfen sistem yöneticisine başvurun.', 'danger')
                log_hata(e, modul='urun_gruplari')

        gruplar = UrunGrup.query.filter_by(aktif=True).order_by(UrunGrup.grup_adi).all()
        return render_template('admin/urun_gruplari.html', form=form, gruplar=gruplar)

    @app.route('/grup-duzenle/<int:grup_id>', methods=['GET', 'POST'])
    @login_required
    @role_required('sistem_yoneticisi', 'admin')
    def grup_duzenle(grup_id):
        """Ürün grubu düzenleme"""
        from forms import UrunGrupForm
        from sqlalchemy.exc import IntegrityError

        grup = UrunGrup.query.get_or_404(grup_id)
        form = UrunGrupForm(obj=grup)

        if form.validate_on_submit():
            try:
                eski_deger = serialize_model(grup)
                grup.grup_adi = form.grup_adi.data
                grup.aciklama = form.aciklama.data or ''
                db.session.commit()

                # Audit Trail
                audit_update('urun_grup', grup.id, eski_deger, grup)

                flash('Ürün grubu başarıyla güncellendi.', 'success')
                return redirect(url_for('urun_gruplari'))

            except IntegrityError as e:
                db.session.rollback()
                flash('Bu grup adı zaten kullanılıyor. Lütfen farklı bir ad girin.', 'danger')
                log_hata(e, modul='grup_duzenle')

            except Exception as e:
                db.session.rollback()
                flash('Beklenmeyen bir hata oluştu. Lütfen sistem yöneticisine başvurun.', 'danger')
                log_hata(e, modul='grup_duzenle')

        return render_template('admin/grup_duzenle.html', form=form, grup=grup)

    @app.route('/grup-sil/<int:grup_id>', methods=['POST'])
    @login_required
    @role_required('sistem_yoneticisi', 'admin')
    def grup_sil(grup_id):
        """Ürün grubu silme"""
        try:
            grup = UrunGrup.query.get_or_404(grup_id)
            
            # Gruba ait ürün var mı kontrol et
            urun_sayisi = Urun.query.filter_by(grup_id=grup_id).count()
            if urun_sayisi > 0:
                flash(f'Bu gruba ait {urun_sayisi} ürün bulunmaktadır. Önce ürünleri silin veya başka gruba taşıyın.', 'danger')
                return redirect(url_for('urun_gruplari'))
            
            eski_deger = serialize_model(grup)
            db.session.delete(grup)
            db.session.commit()
            
            # Audit Trail
            audit_delete('urun_grup', grup_id, eski_deger)
            
            flash('Ürün grubu başarıyla silindi.', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash(f'Hata oluştu: {str(e)}', 'danger')
        
        return redirect(url_for('urun_gruplari'))

    @app.route('/grup-pasif-yap/<int:grup_id>', methods=['POST'])
    @login_required
    @role_required('sistem_yoneticisi', 'admin')
    def grup_pasif_yap(grup_id):
        """Ürün grubu pasif yapma"""
        try:
            grup = UrunGrup.query.get_or_404(grup_id)
            eski_deger = serialize_model(grup)
            grup.aktif = False
            db.session.commit()
            
            # Audit Trail
            audit_update('urun_grup', grup.id, eski_deger, grup)
            
            flash('Ürün grubu başarıyla pasif yapıldı.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Hata oluştu: {str(e)}', 'danger')
        
        return redirect(url_for('urun_gruplari'))

    @app.route('/grup-aktif-yap/<int:grup_id>', methods=['POST'])
    @login_required
    @role_required('sistem_yoneticisi', 'admin')
    def grup_aktif_yap(grup_id):
        """Ürün grubu aktif yapma"""
        try:
            grup = UrunGrup.query.get_or_404(grup_id)
            eski_deger = serialize_model(grup)
            grup.aktif = True
            db.session.commit()
            
            # Audit Trail
            audit_update('urun_grup', grup.id, eski_deger, grup)
            
            flash('Ürün grubu başarıyla aktif yapıldı.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Hata oluştu: {str(e)}', 'danger')
        
        return redirect(url_for('urun_gruplari'))

    # ============================================================================
    # ÜRÜN YÖNETİMİ
    # ============================================================================

    @app.route('/urunler', methods=['GET', 'POST'])
    @login_required
    @role_required('sistem_yoneticisi', 'admin')
    def urunler():
        """Ürün tanımlama ve listeleme"""
        from forms import UrunForm
        from sqlalchemy.exc import IntegrityError

        # Grup seçeneklerini doldur (form oluşturmadan önce)
        gruplar = UrunGrup.query.filter_by(aktif=True).order_by(UrunGrup.grup_adi).all()
        grup_choices = [(g.id, g.grup_adi) for g in gruplar]
        
        form = UrunForm()
        form.grup_id.choices = grup_choices

        if form.validate_on_submit():
            try:
                urun = Urun(
                    grup_id=form.grup_id.data,
                    urun_adi=form.urun_adi.data,
                    barkod=form.barkod.data or None,
                    birim=form.birim.data or 'Adet',
                    kritik_stok_seviyesi=form.kritik_stok_seviyesi.data or 10
                )
                db.session.add(urun)
                db.session.commit()

                # Audit Trail
                audit_create('urun', urun.id, urun)

                # Log kaydı
                log_islem('ekleme', 'urun', {
                    'urun_adi': urun.urun_adi,
                    'barkod': urun.barkod,
                    'grup_id': urun.grup_id,
                    'birim': urun.birim
                })

                flash('Ürün başarıyla eklendi.', 'success')
                return redirect(url_for('urunler'))

            except IntegrityError as e:
                db.session.rollback()
                error_msg = str(e)
                if 'barkod' in error_msg:
                    flash('Bu barkod numarası zaten kullanılıyor. Lütfen farklı bir barkod girin veya boş bırakın.', 'danger')
                else:
                    flash('Kayıt sırasında bir hata oluştu.', 'danger')
                log_hata(e, modul='urunler')

            except Exception as e:
                db.session.rollback()
                flash('Beklenmeyen bir hata oluştu. Lütfen sistem yöneticisine başvurun.', 'danger')
                log_hata(e, modul='urunler')

        # Tüm ürünleri getir (aktif ve pasif)
        urunler = Urun.query.order_by(Urun.aktif.desc(), Urun.urun_adi).all()
        return render_template('admin/urunler.html', form=form, gruplar=gruplar, urunler=urunler)

    @app.route('/urun-duzenle/<int:urun_id>', methods=['GET', 'POST'])
    @login_required
    @role_required('sistem_yoneticisi', 'admin')
    def urun_duzenle(urun_id):
        """Ürün düzenleme"""
        from forms import UrunForm
        from sqlalchemy.exc import IntegrityError

        urun = Urun.query.get_or_404(urun_id)
        gruplar = UrunGrup.query.filter_by(aktif=True).order_by(UrunGrup.grup_adi).all()
        grup_choices = [(g.id, g.grup_adi) for g in gruplar]

        form = UrunForm(obj=urun)
        form.grup_id.choices = grup_choices

        if form.validate_on_submit():
            try:
                # Eski değerleri kaydet
                eski_deger = serialize_model(urun)
                eski_urun_adi = urun.urun_adi

                urun.urun_adi = form.urun_adi.data
                urun.grup_id = form.grup_id.data
                urun.barkod = form.barkod.data or None
                urun.birim = form.birim.data or 'Adet'
                urun.kritik_stok_seviyesi = form.kritik_stok_seviyesi.data or 10

                db.session.commit()

                # Audit Trail
                audit_update('urun', urun.id, eski_deger, urun)

                # Log kaydı
                log_islem('guncelleme', 'urun', {
                    'urun_id': urun.id,
                    'eski_urun_adi': eski_urun_adi,
                    'yeni_urun_adi': urun.urun_adi,
                    'barkod': urun.barkod
                })

                flash('Ürün başarıyla güncellendi.', 'success')
                return redirect(url_for('urunler'))

            except IntegrityError as e:
                db.session.rollback()
                error_msg = str(e)
                if 'barkod' in error_msg:
                    flash('Bu barkod numarası zaten kullanılıyor. Lütfen farklı bir barkod girin veya boş bırakın.', 'danger')
                else:
                    flash('Güncelleme sırasında bir hata oluştu.', 'danger')
                log_hata(e, modul='urun_duzenle')

            except Exception as e:
                db.session.rollback()
                flash('Beklenmeyen bir hata oluştu. Lütfen sistem yöneticisine başvurun.', 'danger')
                log_hata(e, modul='urun_duzenle')

        return render_template('admin/urun_duzenle.html', form=form, urun=urun, gruplar=gruplar)

    @app.route('/urun-sil/<int:urun_id>', methods=['POST'])
    @login_required
    @role_required('sistem_yoneticisi', 'admin')
    def urun_sil(urun_id):
        """Ürün silme"""
        try:
            urun = Urun.query.get_or_404(urun_id)
            urun_adi = urun.urun_adi
            
            # Ürüne ait stok hareketi var mı kontrol et
            stok_hareketi = StokHareket.query.filter_by(urun_id=urun_id).first()
            if stok_hareketi:
                flash('Bu ürüne ait stok hareketi bulunmaktadır. Ürün silinemez.', 'danger')
                return redirect(url_for('urunler'))
            
            # Eski değerleri kaydet (silme öncesi)
            eski_deger = serialize_model(urun)
            
            db.session.delete(urun)
            db.session.commit()
            
            # Audit Trail
            audit_delete('urun', urun_id, eski_deger)
            
            # Log kaydı
            log_islem('silme', 'urun', {
                'urun_id': urun_id,
                'urun_adi': urun_adi
            })
            
            flash('Ürün başarıyla silindi.', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash(f'Hata oluştu: {str(e)}', 'danger')
        
        return redirect(url_for('urunler'))

    @app.route('/urun-pasif-yap/<int:urun_id>', methods=['POST'])
    @login_required
    @role_required('sistem_yoneticisi', 'admin')
    def urun_pasif_yap(urun_id):
        """Ürün pasif yapma"""
        try:
            urun = Urun.query.get_or_404(urun_id)
            eski_deger = serialize_model(urun)
            urun.aktif = False
            db.session.commit()
            
            # Audit Trail
            audit_update('urun', urun.id, eski_deger, urun)
            
            flash('Ürün başarıyla pasif yapıldı.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Hata oluştu: {str(e)}', 'danger')
        
        return redirect(url_for('urunler'))

    @app.route('/urun-aktif-yap/<int:urun_id>', methods=['POST'])
    @login_required
    @role_required('sistem_yoneticisi', 'admin')
    def urun_aktif_yap(urun_id):
        """Ürün aktif yapma"""
        try:
            urun = Urun.query.get_or_404(urun_id)
            eski_deger = serialize_model(urun)
            urun.aktif = True
            db.session.commit()
            
            # Audit Trail
            audit_update('urun', urun.id, eski_deger, urun)
            
            flash('Ürün başarıyla aktif yapıldı.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Hata oluştu: {str(e)}', 'danger')
        
        return redirect(url_for('urunler'))
