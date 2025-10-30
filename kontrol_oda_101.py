"""Oda 101 minibar işlemlerini kontrol et"""

from app import app, db
from models import MinibarIslem, MinibarIslemDetay, Urun, Oda

with app.app_context():
    # 101 nolu odayı bul
    oda = Oda.query.filter_by(oda_no='101').first()
    
    if not oda:
        print("❌ Oda 101 bulunamadı!")
        exit()
    
    print(f"\n🏨 Oda: {oda.oda_no} (ID: {oda.id})")
    print("=" * 80)
    
    # Bu odaya yapılan tüm işlemleri getir
    islemler = MinibarIslem.query.filter_by(oda_id=oda.id).order_by(MinibarIslem.id).all()
    
    print(f"\n📋 Toplam İşlem Sayısı: {len(islemler)}\n")
    
    for islem in islemler:
        print(f"İşlem #{islem.id}")
        print(f"  Tip: {islem.islem_tipi}")
        print(f"  Tarih: {islem.islem_tarihi.strftime('%d.%m.%Y %H:%M')}")
        print(f"  Açıklama: {islem.aciklama}")
        print(f"  Detay Sayısı: {len(islem.detaylar)}")
        print(f"  Ürünler:")
        
        for detay in islem.detaylar:
            urun = Urun.query.get(detay.urun_id)
            print(f"    • {urun.urun_adi if urun else 'Bilinmeyen'}")
            print(f"      - Başlangıç: {detay.baslangic_stok}")
            print(f"      - Eklenen: {detay.eklenen_miktar}")
            print(f"      - Tüketim: {detay.tuketim}")
            print(f"      - Bitiş: {detay.bitis_stok}")
        
        print("-" * 80)
    
    # Son işlemi özel olarak göster
    print("\n🎯 SON İŞLEM (API'nin döndüreceği):")
    son_islem = MinibarIslem.query.filter_by(oda_id=oda.id).order_by(MinibarIslem.id.desc()).first()
    
    if son_islem:
        print(f"İşlem ID: {son_islem.id}")
        print(f"Tip: {son_islem.islem_tipi}")
        print(f"Detay Sayısı: {len(son_islem.detaylar)}")
        print(f"\nÜrün Listesi (API'de görünecekler):")
        for detay in son_islem.detaylar:
            urun = Urun.query.get(detay.urun_id)
            mevcut_stok = detay.bitis_stok if detay.bitis_stok is not None else (
                (detay.baslangic_stok or 0) + (detay.eklenen_miktar or 0) - (detay.tuketim or 0)
            )
            print(f"  • {urun.urun_adi if urun else 'Bilinmeyen'}: {mevcut_stok} adet")
