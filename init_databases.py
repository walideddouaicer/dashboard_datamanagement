#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Temporary script: create Universite and datawarehouse databases, run SQL schemas."""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

PG_CONFIG = dict(host='localhost', user='postgres', password='postgres', port=5432)

def create_database(db_name):
    conn = psycopg2.connect(**PG_CONFIG, dbname='postgres')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
    if not cur.fetchone():
        cur.execute(f'CREATE DATABASE "{db_name}"')
        print(f"[OK] Database '{db_name}' created")
    else:
        print(f"[OK] Database '{db_name}' already exists")
    cur.close()
    conn.close()

def strip_comments(stmt):
    """Remove full-line SQL comments, preserve statement content."""
    lines = []
    for line in stmt.splitlines():
        stripped = line.strip()
        if not stripped.startswith('--'):
            lines.append(line)
    return '\n'.join(lines).strip()

def execute_sql_file(db_name, filepath):
    print(f"\n[INFO] Executing {filepath} on '{db_name}'...")
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        sql_content = f.read()

    raw_statements = sql_content.split(';')

    conn = psycopg2.connect(**PG_CONFIG, dbname=db_name)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    ok = skip = errors = 0

    for raw in raw_statements:
        stmt = strip_comments(raw)
        if not stmt:
            skip += 1
            continue
        try:
            cur.execute(stmt)
            try:
                cur.fetchall()
            except Exception:
                pass
            ok += 1
        except Exception as e:
            err_msg = str(e).strip()
            if any(x in err_msg.lower() for x in ['already exists', 'duplicate']):
                skip += 1
            else:
                first_line = stmt.splitlines()[0][:80] if stmt else ''
                print(f"  [WARN] {first_line!r}: {err_msg[:100]}")
                errors += 1

    cur.close()
    conn.close()
    print(f"[OK] {ok} statements executed, {skip} skipped/empty, {errors} errors")

def verify_counts(db_name, tables):
    conn = psycopg2.connect(**PG_CONFIG, dbname=db_name)
    cur = conn.cursor()
    for t in tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {t}")
            n = cur.fetchone()[0]
            print(f"  {db_name}.{t}: {n} rows")
        except Exception as e:
            print(f"  {db_name}.{t}: ERROR - {e}")
            conn.rollback()
    cur.close()
    conn.close()

def main():
    print("=" * 60)
    print("DATABASE INITIALIZATION")
    print("=" * 60)

    create_database('Universite')
    execute_sql_file('Universite', r'C:\Users\PC\Desktop\ensa s8\datamanagement\base direction.sql')

    create_database('datawarehouse')
    execute_sql_file('datawarehouse', r'C:\Users\PC\Desktop\ensa s8\datamanagement\datawehouse.sql')

    print("\n[INFO] Verifying table counts...")
    verify_counts('Universite', ['etudiants', 'modules', 'professeurs', 'reclamations'])
    verify_counts('datawarehouse', ['dim_etudiant', 'dim_module', 'dim_temps', 'dim_type_eval', 'fait_notes'])

    print("\n[DONE] Database initialization complete.")

if __name__ == '__main__':
    main()
