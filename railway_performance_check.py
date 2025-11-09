#!/usr/bin/env python3
"""
Railway PostgreSQL Performans ve Index Analizi
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from tabulate import tabulate

load_dotenv('.env.railway')

railway_url = os.getenv('RAILWAY_DATABASE_URL')
if railway_url:
    railway_url = railway_url.replace('postgresql://', 'postgresql+psycopg2://')

if not railway_url:
    print("❌ RAILWAY_DATABASE_URL bulunamadı!")
    exit(1)

engine = create_engine(railway_url)

print("🔍 RAILWAY POSTGRESQL PERFORMANS ANALİZİ")
print("=" * 80)

with engine.connect() as conn:
    
    # 1. MEVCUT INDEX'LERI LİSTELE
    print("\n📊 1. MEVCUT INDEX'LER")
    print("-" * 80)
    result = conn.execute(text("""
        SELECT 
            schemaname,
            tablename,
            indexname,
            indexdef,
            pg_size_pretty(pg_relation_size(indexname::regclass)) as index_size
        FROM pg_indexes 
        WHERE schemaname = 'public'
        ORDER BY tablename, indexname
    """))
    
    indexes = []
    for row in result:
        indexes.append([row[0], row[1], row[2], row[3][:60] + '...', row[4]])
    
    print(tabulate(indexes, headers=['Schema', 'Tablo', 'Index Adı', 'Tanım', 'Boyut'], tablefmt='grid'))
    print(f"\n✅ Toplam {len(indexes)} index bulundu")
    
    # 2. KULLANILMAYAN INDEX'LER
    print("\n🚨 2. KULLANILMAYAN INDEX'LER (Index Scan = 0)")
    print("-" * 80)
    result = conn.execute(text("""
        SELECT 
            schemaname,
            relname as tablename,
            indexrelname as indexname,
            idx_scan as index_scans,
            pg_size_pretty(pg_relation_size(indexrelid)) as index_size
        FROM pg_stat_user_indexes
        WHERE schemaname = 'public'
        AND idx_scan = 0
        AND indexrelname NOT LIKE '%_pkey'
        ORDER BY pg_relation_size(indexrelid) DESC
    """))
    
    unused = []
    for row in result:
        unused.append([row[0], row[1], row[2], row[3], row[4]])
    
    if unused:
        print(tabulate(unused, headers=['Schema', 'Tablo', 'Index', 'Scan Sayısı', 'Boyut'], tablefmt='grid'))
        print(f"\n⚠️  {len(unused)} kullanılmayan index bulundu - bunlar silinebilir!")
    else:
        print("✅ Kullanılmayan index yok")
    
    # 3. DUPLICATE/REDUNDANT INDEX'LER
    print("\n🔄 3. DUPLICATE INDEX'LER")
    print("-" * 80)
    result = conn.execute(text("""
        SELECT 
            pg_size_pretty(SUM(pg_relation_size(idx))::BIGINT) as total_size,
            (array_agg(idx))[1] as idx1,
            (array_agg(idx))[2] as idx2,
            (array_agg(idx))[3] as idx3,
            (array_agg(idx))[4] as idx4
        FROM (
            SELECT 
                indexrelid::regclass as idx,
                (indrelid::text ||E'\n'|| indclass::text ||E'\n'|| indkey::text ||E'\n'||
                COALESCE(indexprs::text,'')||E'\n' || COALESCE(indpred::text,'')) as key
            FROM pg_index
        ) sub
        GROUP BY key 
        HAVING COUNT(*) > 1
        ORDER BY SUM(pg_relation_size(idx)) DESC
    """))
    
    duplicates = list(result)
    if duplicates:
        for dup in duplicates:
            print(f"Toplam Boyut: {dup[0]}")
            print(f"  Index'ler: {', '.join([str(x) for x in dup[1:] if x])}")
            print()
        print(f"⚠️  {len(duplicates)} grup duplicate index bulundu!")
    else:
        print("✅ Duplicate index yok")
    
    # 4. TABLO BOYUTLARI VE İSTATİSTİKLER
    print("\n📦 4. TABLO BOYUTLARI VE SATIR SAYILARI")
    print("-" * 80)
    result = conn.execute(text("""
        SELECT 
            schemaname,
            relname as tablename,
            pg_size_pretty(pg_total_relation_size(relid)) as total_size,
            pg_size_pretty(pg_relation_size(relid)) as table_size,
            pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) as indexes_size,
            n_live_tup as row_count
        FROM pg_stat_user_tables
        WHERE schemaname = 'public'
        ORDER BY pg_total_relation_size(relid) DESC
    """))
    
    tables = []
    for row in result:
        tables.append([row[0], row[1], row[2], row[3], row[4], f"{row[5]:,}"])
    
    print(tabulate(tables, headers=['Schema', 'Tablo', 'Toplam', 'Tablo', 'Index', 'Satır'], tablefmt='grid'))
    
    # 5. EKSİK INDEX ÖNERİLERİ (Sequential Scan'ler)
    print("\n🔍 5. EKSİK INDEX ÖNERİLERİ (Çok Sequential Scan Yapılan Tablolar)")
    print("-" * 80)
    result = conn.execute(text("""
        SELECT 
            schemaname,
            relname as tablename,
            seq_scan,
            seq_tup_read,
            idx_scan,
            n_live_tup as row_count,
            CASE 
                WHEN seq_scan > 0 
                THEN ROUND(100.0 * idx_scan / (seq_scan + idx_scan), 2)
                ELSE 0 
            END as index_usage_percent
        FROM pg_stat_user_tables
        WHERE schemaname = 'public'
        AND n_live_tup > 100
        ORDER BY seq_scan DESC
        LIMIT 20
    """))
    
    seq_scans = []
    for row in result:
        usage = row[6] if row[6] else 0
        status = "❌" if usage < 50 else "⚠️" if usage < 80 else "✅"
        seq_scans.append([status, row[1], row[2], row[4], f"{usage}%", f"{row[5]:,}"])
    
    print(tabulate(seq_scans, headers=['Durum', 'Tablo', 'Seq Scan', 'Index Scan', 'Index Kullanım %', 'Satır'], tablefmt='grid'))
    print("\n❌ = Index eksik olabilir (<50%)")
    print("⚠️  = Index optimizasyonu gerekebilir (50-80%)")
    print("✅ = İyi durumda (>80%)")
    
    # 6. CACHE HIT RATIO
    print("\n💾 6. CACHE HIT RATIO (Veritabanı Bellek Performansı)")
    print("-" * 80)
    result = conn.execute(text("""
        SELECT 
            sum(heap_blks_read) as heap_read,
            sum(heap_blks_hit) as heap_hit,
            CASE 
                WHEN (sum(heap_blks_hit) + sum(heap_blks_read)) > 0 
                THEN sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) * 100
                ELSE 100
            END as cache_hit_ratio
        FROM pg_statio_user_tables
    """))
    
    for row in result:
        if row[0] is not None or row[1] is not None:
            heap_read = row[0] or 0
            heap_hit = row[1] or 0
            ratio = row[2] or 100
            status = "✅" if ratio > 99 else "⚠️" if ratio > 90 else "❌"
            print(f"{status} Cache Hit Ratio: {ratio:.2f}%")
            print(f"   Disk'ten okunan: {heap_read:,}")
            print(f"   Cache'den okunan: {heap_hit:,}")
            if ratio < 99 and (heap_read + heap_hit) > 0:
                print("   ⚠️  Cache hit ratio düşük - shared_buffers artırılmalı!")
        else:
            print("✅ Henüz yeterli veri yok (veritabanı yeni oluşturuldu veya temizlendi)")
    
    # 7. VERİTABANI BOYUTU
    print("\n💿 7. VERİTABANI TOPLAM BOYUTU")
    print("-" * 80)
    result = conn.execute(text("""
        SELECT 
            pg_database.datname,
            pg_size_pretty(pg_database_size(pg_database.datname)) AS size
        FROM pg_database
        WHERE datname = current_database()
    """))
    
    for row in result:
        print(f"Veritabanı: {row[0]}")
        print(f"Toplam Boyut: {row[1]}")
    
    # 8. BAĞLANTI SAYISI
    print("\n🔌 8. AKTİF BAĞLANTILAR")
    print("-" * 80)
    result = conn.execute(text("""
        SELECT 
            count(*) as total_connections,
            count(*) FILTER (WHERE state = 'active') as active,
            count(*) FILTER (WHERE state = 'idle') as idle,
            count(*) FILTER (WHERE state = 'idle in transaction') as idle_in_transaction
        FROM pg_stat_activity
        WHERE datname = current_database()
    """))
    
    for row in result:
        print(f"Toplam Bağlantı: {row[0]}")
        print(f"Aktif: {row[1]}")
        print(f"Boşta: {row[2]}")
        print(f"Transaction'da Boşta: {row[3]}")
        if row[3] > 5:
            print("⚠️  Çok fazla 'idle in transaction' - connection leak olabilir!")
    
    # 9. LONG RUNNING QUERIES
    print("\n⏱️  9. UZUN SÜREN SORULAR (>1 saniye)")
    print("-" * 80)
    result = conn.execute(text("""
        SELECT 
            pid,
            now() - query_start as duration,
            state,
            left(query, 100) as query
        FROM pg_stat_activity
        WHERE state != 'idle'
        AND query NOT LIKE '%pg_stat_activity%'
        AND now() - query_start > interval '1 second'
        ORDER BY duration DESC
        LIMIT 10
    """))
    
    long_queries = []
    for row in result:
        long_queries.append([row[0], str(row[1]), row[2], row[3]])
    
    if long_queries:
        print(tabulate(long_queries, headers=['PID', 'Süre', 'Durum', 'Sorgu'], tablefmt='grid'))
        print(f"\n⚠️  {len(long_queries)} uzun süren sorgu bulundu!")
    else:
        print("✅ Uzun süren sorgu yok")

print("\n" + "=" * 80)
print("✅ ANALİZ TAMAMLANDI!")
print("\n📝 ÖNERİLER:")
print("1. Kullanılmayan index'leri silin (Bölüm 2)")
print("2. Duplicate index'leri kaldırın (Bölüm 3)")
print("3. Sequential scan'i yüksek tablolara index ekleyin (Bölüm 5)")
print("4. Cache hit ratio düşükse shared_buffers artırın (Bölüm 6)")
print("5. Uzun süren sorguları optimize edin (Bölüm 9)")
