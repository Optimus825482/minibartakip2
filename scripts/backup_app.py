#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
App.py Yedekleme Aracı

Bu script app.py dosyasının tarih-saat damgalı yedeğini oluşturur.
"""

import shutil
import os
from datetime import datetime
from pathlib import Path


def backup_app_py(source_file='app.py', backup_dir='.'):
    """
    app.py'nin yedeğini al
    
    Args:
        source_file: Yedeklenecek dosya
        backup_dir: Yedeklerin kaydedileceği dizin
    
    Returns:
        tuple: (başarılı mı, yedek dosya adı, hata mesajı)
    """
    try:
        # Kaynak dosya kontrolü
        if not os.path.exists(source_file):
            return False, None, f"❌ {source_file} bulunamadı!"
        
        # Yedek dizini oluştur
        backup_path = Path(backup_dir)
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # Tarih-saat damgası
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Yedek dosya adı
        source_name = Path(source_file).stem  # 'app'
        source_ext = Path(source_file).suffix  # '.py'
        backup_name = f'{source_name}_backup_{timestamp}{source_ext}'
        backup_file = backup_path / backup_name
        
        # Dosyayı kopyala
        shutil.copy2(source_file, backup_file)
        
        # Dosya boyutunu kontrol et
        source_size = os.path.getsize(source_file)
        backup_size = os.path.getsize(backup_file)
        
        if source_size != backup_size:
            return False, str(backup_file), "⚠️  Yedek dosya boyutu kaynak dosya ile eşleşmiyor!"
        
        return True, str(backup_file), None
        
    except Exception as e:
        return False, None, f"❌ Yedekleme hatası: {str(e)}"


def list_backups(backup_dir='.', pattern='app_backup_*.py'):
    """
    Mevcut yedekleri listele
    
    Args:
        backup_dir: Yedeklerin bulunduğu dizin
        pattern: Yedek dosya pattern'i
    
    Returns:
        list: Yedek dosyaların listesi (tarih sıralı)
    """
    backup_path = Path(backup_dir)
    
    if not backup_path.exists():
        return []
    
    backups = list(backup_path.glob(pattern))
    
    # Tarihe göre sırala (en yeni önce)
    backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    return backups


def restore_backup(backup_file, target_file='app.py'):
    """
    Yedekten geri yükle
    
    Args:
        backup_file: Geri yüklenecek yedek dosya
        target_file: Hedef dosya
    
    Returns:
        tuple: (başarılı mı, hata mesajı)
    """
    try:
        if not os.path.exists(backup_file):
            return False, f"❌ Yedek dosya bulunamadı: {backup_file}"
        
        # Mevcut dosyanın yedeğini al
        if os.path.exists(target_file):
            temp_backup = f"{target_file}.before_restore"
            shutil.copy2(target_file, temp_backup)
            print(f"ℹ️  Mevcut dosya yedeklendi: {temp_backup}")
        
        # Yedekten geri yükle
        shutil.copy2(backup_file, target_file)
        
        return True, None
        
    except Exception as e:
        return False, f"❌ Geri yükleme hatası: {str(e)}"


def main():
    """Ana fonksiyon"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'list':
            # Yedekleri listele
            print("📋 Mevcut Yedekler:\n")
            backups = list_backups()
            
            if not backups:
                print("   Yedek bulunamadı.")
            else:
                for i, backup in enumerate(backups, 1):
                    size_mb = backup.stat().st_size / (1024 * 1024)
                    mtime = datetime.fromtimestamp(backup.stat().st_mtime)
                    print(f"   {i}. {backup.name}")
                    print(f"      Tarih: {mtime.strftime('%d.%m.%Y %H:%M:%S')}")
                    print(f"      Boyut: {size_mb:.2f} MB\n")
        
        elif command == 'restore':
            # Geri yükle
            if len(sys.argv) < 3:
                print("❌ Kullanım: python backup_app.py restore <yedek_dosya>")
                sys.exit(1)
            
            backup_file = sys.argv[2]
            
            print(f"⚠️  DİKKAT: {backup_file} dosyasından geri yükleme yapılacak!")
            confirm = input("Devam etmek istiyor musunuz? (evet/hayır): ")
            
            if confirm.lower() in ['evet', 'e', 'yes', 'y']:
                success, error = restore_backup(backup_file)
                
                if success:
                    print(f"✅ Geri yükleme başarılı: app.py")
                else:
                    print(error)
                    sys.exit(1)
            else:
                print("❌ İşlem iptal edildi.")
                sys.exit(0)
        
        else:
            print(f"❌ Bilinmeyen komut: {command}")
            print("Kullanım:")
            print("  python backup_app.py          - Yedek oluştur")
            print("  python backup_app.py list     - Yedekleri listele")
            print("  python backup_app.py restore <dosya> - Geri yükle")
            sys.exit(1)
    
    else:
        # Yedek oluştur
        print("💾 App.py Yedekleme Başlıyor...\n")
        
        success, backup_file, error = backup_app_py()
        
        if success:
            print(f"✅ Yedek başarıyla oluşturuldu!")
            print(f"   Dosya: {backup_file}")
            
            # Dosya bilgileri
            size_mb = os.path.getsize(backup_file) / (1024 * 1024)
            print(f"   Boyut: {size_mb:.2f} MB")
            
            # Satır sayısı
            with open(backup_file, 'r', encoding='utf-8') as f:
                line_count = sum(1 for _ in f)
            print(f"   Satır: {line_count:,}")
            
        else:
            print(error)
            sys.exit(1)


if __name__ == '__main__':
    main()
