#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Route Analiz Aracı

Bu script app.py dosyasındaki tüm route'ları analiz eder ve
template'lerde kullanılan endpoint'leri tespit eder.
"""

import re
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def analyze_app_routes(app_file='app.py'):
    """app.py'deki tüm route'ları analiz et"""
    routes = []
    
    if not os.path.exists(app_file):
        print(f"❌ {app_file} bulunamadı!")
        return routes
    
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
        
        # @app.route pattern'ini bul
        route_pattern = r"@app\.route\(['\"]([^'\"]+)['\"](?:,\s*methods=\[([^\]]+)\])?\)"
        
        for i, line in enumerate(lines):
            match = re.search(route_pattern, line)
            if match:
                path = match.group(1)
                methods = match.group(2) if match.group(2) else 'GET'
                
                # Fonksiyon ismini bul (bir sonraki satırda)
                func_name = None
                if i + 1 < len(lines):
                    # Decorator'ları atla
                    j = i + 1
                    while j < len(lines) and lines[j].strip().startswith('@'):
                        j += 1
                    
                    if j < len(lines):
                        func_match = re.search(r'def\s+(\w+)\s*\(', lines[j])
                        if func_match:
                            func_name = func_match.group(1)
                
                routes.append({
                    'path': path,
                    'methods': methods.replace("'", "").replace('"', ''),
                    'function': func_name,
                    'line': i + 1
                })
    
    return routes


def analyze_template_usage(template_dir='templates'):
    """Template'lerde kullanılan url_for çağrılarını analiz et"""
    used_endpoints = defaultdict(list)
    
    if not os.path.exists(template_dir):
        print(f"❌ {template_dir} dizini bulunamadı!")
        return used_endpoints
    
    template_path = Path(template_dir)
    
    for template_file in template_path.rglob('*.html'):
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # url_for pattern'ini bul
                pattern = r"url_for\(['\"]([^'\"]+)['\"]"
                matches = re.finditer(pattern, content)
                
                for match in matches:
                    endpoint = match.group(1)
                    relative_path = template_file.relative_to(template_path)
                    used_endpoints[endpoint].append(str(relative_path))
        except Exception as e:
            print(f"⚠️  {template_file} okunamadı: {e}")
    
    return used_endpoints


def analyze_static_api_calls(static_dir='static'):
    """Static JS dosyalarındaki API çağrılarını analiz et"""
    api_calls = defaultdict(list)
    
    if not os.path.exists(static_dir):
        print(f"❌ {static_dir} dizini bulunamadı!")
        return api_calls
    
    static_path = Path(static_dir)
    
    # API endpoint pattern'leri
    patterns = [
        r"fetch\(['\"]([^'\"]+)['\"]",
        r"\$\.ajax\(\{[^}]*url:\s*['\"]([^'\"]+)['\"]",
        r"\$\.get\(['\"]([^'\"]+)['\"]",
        r"\$\.post\(['\"]([^'\"]+)['\"]",
        r"axios\.(get|post|put|delete)\(['\"]([^'\"]+)['\"]"
    ]
    
    for js_file in static_path.rglob('*.js'):
        try:
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                for pattern in patterns:
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        # axios için grup 2, diğerleri için grup 1
                        url = match.group(2) if 'axios' in pattern else match.group(1)
                        
                        # Sadece /api/ ile başlayanları al
                        if url.startswith('/api/') or url.startswith('/admin/'):
                            relative_path = js_file.relative_to(static_path)
                            api_calls[url].append(str(relative_path))
        except Exception as e:
            print(f"⚠️  {js_file} okunamadı: {e}")
    
    return api_calls


def find_unused_routes(all_routes, used_endpoints, api_calls):
    """Kullanılmayan route'ları bul"""
    unused = []
    used = []
    
    # Kullanılan endpoint isimlerini set'e çevir
    used_endpoint_names = set(used_endpoints.keys())
    
    # API çağrılarını path'e göre kontrol et
    used_api_paths = set(api_calls.keys())
    
    for route in all_routes:
        is_used = False
        usage_info = []
        
        # Fonksiyon ismi ile kontrol
        if route['function'] in used_endpoint_names:
            is_used = True
            usage_info.extend(used_endpoints[route['function']])
        
        # Path ile kontrol (API endpoint'leri için)
        if route['path'] in used_api_paths:
            is_used = True
            usage_info.extend(api_calls[route['path']])
        
        # Dinamik path'leri kontrol et (örn: /admin/oda/<int:oda_id>)
        for api_path in used_api_paths:
            # Basit pattern matching
            if '<' in route['path']:
                # /admin/oda/<int:oda_id> -> /admin/oda/
                base_path = re.sub(r'<[^>]+>', '', route['path'])
                if api_path.startswith(base_path.rstrip('/')):
                    is_used = True
                    usage_info.extend(api_calls[api_path])
                    break
        
        if is_used:
            used.append({
                **route,
                'used_in': list(set(usage_info))
            })
        else:
            unused.append(route)
    
    return unused, used


def generate_report(all_routes, unused_routes, used_routes, used_endpoints, api_calls):
    """Analiz raporunu oluştur"""
    report = []
    
    report.append("# App.py Refactoring Analiz Raporu")
    report.append(f"\n**Oluşturulma Tarihi:** {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
    
    # Özet
    report.append("## Özet\n")
    report.append(f"- **Toplam Route Sayısı:** {len(all_routes)}")
    report.append(f"- **Kullanılan Route Sayısı:** {len(used_routes)}")
    report.append(f"- **Kullanılmayan Route Sayısı:** {len(unused_routes)}")
    report.append(f"- **Template'lerde Kullanılan Endpoint:** {len(used_endpoints)}")
    report.append(f"- **JS'de Kullanılan API Endpoint:** {len(api_calls)}\n")
    
    # Kullanılan Route'lar
    report.append("## Kullanılan Route'lar\n")
    report.append("| Path | Methods | Function | Kullanıldığı Yerler |")
    report.append("|------|---------|----------|---------------------|")
    
    for route in sorted(used_routes, key=lambda x: x['path']):
        used_in = ', '.join(route['used_in'][:3])  # İlk 3 kullanım
        if len(route['used_in']) > 3:
            used_in += f" (+{len(route['used_in']) - 3} daha)"
        
        report.append(f"| `{route['path']}` | {route['methods']} | `{route['function']}` | {used_in} |")
    
    report.append("")
    
    # Kullanılmayan Route'lar
    if unused_routes:
        report.append("## ⚠️ Kullanılmayan Route'lar\n")
        report.append("**DİKKAT:** Bu route'lar template veya JS dosyalarında tespit edilemedi.")
        report.append("Silmeden önce log kayıtlarını kontrol edin!\n")
        report.append("| Path | Methods | Function | Satır |")
        report.append("|------|---------|----------|-------|")
        
        for route in sorted(unused_routes, key=lambda x: x['path']):
            report.append(f"| `{route['path']}` | {route['methods']} | `{route['function']}` | {route['line']} |")
        
        report.append("")
    
    # Route Gruplandırma Önerisi
    report.append("## Route Gruplandırma Önerisi\n")
    
    groups = {
        'Auth': [],
        'Dashboard': [],
        'Sistem Yöneticisi': [],
        'Admin': [],
        'Admin Minibar': [],
        'Admin Stok': [],
        'Admin Zimmet': [],
        'Depo': [],
        'Kat Sorumlusu': [],
        'API': [],
        'Diğer': []
    }
    
    for route in all_routes:
        path = route['path']
        
        if path in ['/', '/setup', '/login', '/logout']:
            groups['Auth'].append(route)
        elif 'dashboard' in path or path in ['/sistem-yoneticisi', '/depo', '/kat-sorumlusu']:
            groups['Dashboard'].append(route)
        elif path.startswith('/admin/minibar') or path.startswith('/admin/oda-minibar') or path.startswith('/admin/depo-stok'):
            groups['Admin Minibar'].append(route)
        elif path.startswith('/admin/stok'):
            groups['Admin Stok'].append(route)
        elif path.startswith('/admin/zimmet') or path.startswith('/admin/personel-zimmet'):
            groups['Admin Zimmet'].append(route)
        elif path.startswith('/admin/') or path in ['/personel-tanimla', '/personel-duzenle', '/urun-gruplari', '/urunler']:
            groups['Admin'].append(route)
        elif path in ['/otel-tanimla', '/kat-tanimla', '/kat-duzenle', '/kat-sil', '/oda-tanimla', '/oda-duzenle', '/oda-sil', '/sistem-loglari']:
            groups['Sistem Yöneticisi'].append(route)
        elif path.startswith('/stok-'):
            groups['Depo'].append(route)
        elif 'kat-sorumlusu' in path.lower():
            groups['Kat Sorumlusu'].append(route)
        elif path.startswith('/api/'):
            groups['API'].append(route)
        else:
            groups['Diğer'].append(route)
    
    for group_name, routes in groups.items():
        if routes:
            report.append(f"### {group_name} ({len(routes)} route)\n")
            for route in routes:
                report.append(f"- `{route['path']}` → `{route['function']}`")
            report.append("")
    
    return '\n'.join(report)


def main():
    """Ana fonksiyon"""
    print("🔍 App.py Route Analizi Başlıyor...\n")
    
    # Route'ları analiz et
    print("📝 app.py analiz ediliyor...")
    all_routes = analyze_app_routes()
    print(f"   ✅ {len(all_routes)} route bulundu\n")
    
    # Template kullanımını analiz et
    print("📄 Template dosyaları analiz ediliyor...")
    used_endpoints = analyze_template_usage()
    print(f"   ✅ {len(used_endpoints)} endpoint kullanımı bulundu\n")
    
    # Static JS kullanımını analiz et
    print("📜 JavaScript dosyaları analiz ediliyor...")
    api_calls = analyze_static_api_calls()
    print(f"   ✅ {len(api_calls)} API çağrısı bulundu\n")
    
    # Kullanılmayan route'ları bul
    print("🔎 Kullanılmayan route'lar tespit ediliyor...")
    unused_routes, used_routes = find_unused_routes(all_routes, used_endpoints, api_calls)
    print(f"   ✅ {len(unused_routes)} kullanılmayan route bulundu\n")
    
    # Rapor oluştur
    print("📊 Rapor oluşturuluyor...")
    report = generate_report(all_routes, unused_routes, used_routes, used_endpoints, api_calls)
    
    # Raporu kaydet
    os.makedirs('docs', exist_ok=True)
    report_file = 'docs/refactoring_analysis.md'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"   ✅ Rapor kaydedildi: {report_file}\n")
    
    # Özet
    print("=" * 60)
    print("📈 ANALİZ ÖZETİ")
    print("=" * 60)
    print(f"Toplam Route       : {len(all_routes)}")
    print(f"Kullanılan         : {len(used_routes)}")
    print(f"Kullanılmayan      : {len(unused_routes)}")
    print(f"Template Endpoint  : {len(used_endpoints)}")
    print(f"API Çağrısı        : {len(api_calls)}")
    print("=" * 60)
    print(f"\n✅ Detaylı rapor için: {report_file}")


if __name__ == '__main__':
    main()
