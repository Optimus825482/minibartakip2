"""
ML Sistemi Detaylı Test - Phase 2
Zimmet ve Doluluk analizlerini test eder
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("🧪 ML SİSTEMİ DETAYLI TEST - PHASE 2")
print("=" * 70)
print()

from app import app, db

with app.app_context():
    from models import (
        MLMetric, MLAlert, Kullanici, PersonelZimmet, 
        PersonelZimmetDetay, Oda, MisafirKayit
    )
    
    # 1. Zimmet Durumu Analizi
    print("1️⃣ ZİMMET DURUMU ANALİZİ")
    print("-" * 70)
    
    kat_sorumlulari = Kullanici.query.filter_by(
        rol='kat_sorumlusu',
        aktif=True
    ).all()
    
    print(f"   Toplam Kat Sorumlusu: {len(kat_sorumlulari)}")
    print()
    
    for personel in kat_sorumlulari:
        print(f"   👤 {personel.ad} {personel.soyad}")
        
        # Aktif zimmetler
        aktif_zimmetler = PersonelZimmet.query.filter_by(
            personel_id=personel.id,
            durum='aktif'
        ).all()
        
        if aktif_zimmetler:
            toplam_zimmet = 0
            toplam_kullanim = 0
            toplam_kalan = 0
            
            for zimmet in aktif_zimmetler:
                for detay in zimmet.detaylar:
                    toplam_zimmet += detay.miktar
                    toplam_kullanim += detay.kullanilan_miktar
                    toplam_kalan += (detay.kalan_miktar or 0)
            
            fire = toplam_zimmet - toplam_kullanim - toplam_kalan
            kullanim_oran = (toplam_kullanim / toplam_zimmet * 100) if toplam_zimmet > 0 else 0
            fire_oran = (fire / toplam_zimmet * 100) if toplam_zimmet > 0 else 0
            
            print(f"      Zimmet: {toplam_zimmet} ürün")
            print(f"      Kullanılan: {toplam_kullanim} ürün ({kullanim_oran:.1f}%)")
            print(f"      Kalan: {toplam_kalan} ürün")
            print(f"      Fire: {fire} ürün ({fire_oran:.1f}%)")
            
            # Uyarı kontrolü
            if fire_oran >= 20:
                print(f"      ⚠️  UYARI: Yüksek fire oranı!")
            elif kullanim_oran < 30:
                print(f"      ⚠️  UYARI: Düşük kullanım oranı!")
            else:
                print(f"      ✅ Normal")
        else:
            print(f"      ℹ️  Aktif zimmet yok")
        print()
    
    # 2. Oda Doluluk Durumu
    print("2️⃣ ODA DOLULUK DURUMU")
    print("-" * 70)
    
    from datetime import datetime, timezone, timedelta
    son_24_saat = datetime.now(timezone.utc) - timedelta(hours=24)
    
    odalar = Oda.query.filter_by(aktif=True).limit(10).all()
    
    print(f"   Toplam Oda (ilk 10): {len(odalar)}")
    print()
    
    bos_oda_tuketim = 0
    dolu_oda_tuketim_yok = 0
    
    bugun = datetime.now(timezone.utc).date()
    
    for oda in odalar:
        # Bugün bu odada misafir var mı?
        misafir = MisafirKayit.query.filter(
            MisafirKayit.oda_id == oda.id,
            MisafirKayit.giris_tarihi <= bugun,
            MisafirKayit.cikis_tarihi >= bugun
        ).first()
        
        oda_dolu = misafir is not None
        
        # Tüketim kontrolü
        from sqlalchemy import func
        from models import MinibarIslem, MinibarIslemDetay
        
        tuketim = db.session.query(
            func.coalesce(func.sum(MinibarIslemDetay.tuketim), 0)
        ).join(
            MinibarIslem
        ).filter(
            MinibarIslem.oda_id == oda.id,
            MinibarIslem.islem_tarihi >= son_24_saat
        ).scalar()
        
        durum = "🟢 DOLU" if oda_dolu else "⚪ BOŞ"
        tuketim_str = f"{int(tuketim)} ürün" if tuketim > 0 else "Yok"
        
        print(f"   Oda {oda.oda_no}: {durum} | Tüketim: {tuketim_str}")
        
        # Anomali kontrolü
        if not oda_dolu and tuketim > 0:
            print(f"      🔴 KRİTİK: Boş oda ama tüketim var! (Hırsızlık olabilir)")
            bos_oda_tuketim += 1
        elif oda_dolu and tuketim == 0:
            print(f"      🟡 UYARI: Dolu oda ama tüketim yok")
            dolu_oda_tuketim_yok += 1
    
    print()
    print(f"   Anomali Özeti:")
    print(f"      Boş oda + tüketim: {bos_oda_tuketim} oda")
    print(f"      Dolu oda + tüketim yok: {dolu_oda_tuketim_yok} oda")
    print()
    
    # 3. ML Metrik İstatistikleri
    print("3️⃣ ML METRİK İSTATİSTİKLERİ")
    print("-" * 70)
    
    metrik_tipleri = [
        ('stok_seviye', 'Stok Seviyeleri'),
        ('tuketim_miktar', 'Tüketim Miktarları'),
        ('dolum_sure', 'Dolum Süreleri'),
        ('zimmet_kullanim', 'Zimmet Kullanım'),
        ('zimmet_fire', 'Zimmet Fire'),
        ('bosta_tuketim', 'Boş Oda Tüketim')
    ]
    
    for tip, isim in metrik_tipleri:
        try:
            count = MLMetric.query.filter_by(metric_type=tip).count()
            son_metrik = MLMetric.query.filter_by(metric_type=tip).order_by(
                MLMetric.timestamp.desc()
            ).first()
            
            if son_metrik:
                print(f"   {isim}: {count} kayıt (Son: {son_metrik.metric_value:.1f})")
            else:
                print(f"   {isim}: {count} kayıt")
        except Exception as e:
            print(f"   {isim}: Hata - {str(e)}")
    
    print()
    
    # 4. ML Alert İstatistikleri
    print("4️⃣ ML ALERT İSTATİSTİKLERİ")
    print("-" * 70)
    
    alert_tipleri = [
        ('stok_anomali', 'Stok Anomalisi'),
        ('tuketim_anomali', 'Tüketim Anomalisi'),
        ('dolum_gecikme', 'Dolum Gecikmesi'),
        ('stok_bitis_uyari', 'Stok Bitiş Uyarısı'),
        ('zimmet_fire_yuksek', 'Yüksek Fire'),
        ('zimmet_kullanim_dusuk', 'Düşük Kullanım'),
        ('bosta_tuketim_var', 'Boş Oda Tüketim')
    ]
    
    toplam_alert = 0
    aktif_alert = 0
    
    for tip, isim in alert_tipleri:
        try:
            count = MLAlert.query.filter_by(alert_type=tip).count()
            aktif = MLAlert.query.filter_by(
                alert_type=tip,
                is_read=False,
                is_false_positive=False
            ).count()
            
            if count > 0:
                print(f"   {isim}: {count} toplam ({aktif} aktif)")
                toplam_alert += count
                aktif_alert += aktif
        except Exception as e:
            pass
    
    print()
    print(f"   TOPLAM: {toplam_alert} alert ({aktif_alert} aktif)")
    print()
    
    # 5. Sistem Sağlık Kontrolü
    print("5️⃣ SİSTEM SAĞLIK KONTROLÜ")
    print("-" * 70)
    
    # Son 1 saatte veri toplandı mı?
    son_1_saat = datetime.now(timezone.utc) - timedelta(hours=1)
    son_metrik = MLMetric.query.filter(
        MLMetric.timestamp >= son_1_saat
    ).count()
    
    if son_metrik > 0:
        print(f"   ✅ Veri Toplama: Aktif (Son 1 saat: {son_metrik} metrik)")
    else:
        print(f"   ⚠️  Veri Toplama: Son 1 saatte veri yok")
    
    # Model durumu
    from models import MLModel
    model_count = MLModel.query.filter_by(is_active=True).count()
    
    if model_count > 0:
        print(f"   ✅ ML Modelleri: {model_count} aktif model")
    else:
        print(f"   ⚠️  ML Modelleri: Henüz eğitilmemiş")
    
    # Alert sistemi
    if aktif_alert > 0:
        print(f"   ⚠️  Alert Sistemi: {aktif_alert} aktif uyarı var")
    else:
        print(f"   ✅ Alert Sistemi: Aktif uyarı yok")
    
    print()

print("=" * 70)
print("✅ DETAYLI TEST TAMAMLANDI!")
print("=" * 70)
print()
print("📊 Dashboard'u görüntülemek için:")
print("   http://localhost:5000/ml/dashboard")
print()
