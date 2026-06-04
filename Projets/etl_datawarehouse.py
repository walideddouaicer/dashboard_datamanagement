
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime, timedelta
import os
import re
import glob
import sys
import warnings
warnings.filterwarnings('ignore')

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# ==================== CONFIGURATION ====================

SOURCE_DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'Universite',
    'user': 'postgres',
    'password': 'postgres'
}

DWH_DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'datawarehouse',
    'user': 'postgres',
    'password': 'postgres'
}

NB_SEANCES_TOTAL = 14
DOSSIER_EXCEL = 'excel_files'

# Explicit aliases: Excel module names that differ from the source DB intitulé by
# extra/missing words (so neither exact nor underscore-normalisation matches).
# Each maps the Excel module name -> source code_module. Reviewed 1:1 mapping.
MODULE_ALIASES = {
    'Competences_Numeriques_Programmation': 'INFO201',  # Programmation
    'Complexes_structures_donnees':         'INFO101',  # Structures donnees
    'Electromagnetisme_Electrocinetique':   'P101',     # Electromagnetisme
    'Electronique_analogique_numerique':    'ELEC101',  # Electronique
    'Fonctions_variables_reelles':          'M202',     # Fonctions reelles
    'Mecanique_solide_systemes':            'MEC101',   # Mecanique solide
    'Modelisation_simulation_numerique':    'SIM101',   # Modelisation
    'Optimisation_systemes_industriels':    'OPT101',   # Optimisation
    'Optique_geometrique_instrumentale':    'P102',     # Optique geometrique
    'Optique_physique_lasers':              'P203',     # Optique physique
    'Reseaux_locaux_protocoles':            'RES101',   # Reseaux protocoles
    'Securite_des_donnees':                 'SECU101',  # Securite donnees
    'Statistique_inferentielle':            'STAT101',  # Statistique
    'Traitement_de_signal':                 'SIG101',   # Traitement signal
}

# ==================== FONCTIONS DE BASE ====================

def get_db_connection(config):
    try:
        return psycopg2.connect(**config)
    except Exception as e:
        print(f"[ERROR] Connexion impossible: {e}")
        raise

def normalize_string(s):
    """Normalise une chaine pour la comparaison (minuscules, sans underscores)"""
    if s is None:
        return ""
    return re.sub(r'[_]+', ' ', str(s)).strip().lower()

def find_code_module(conn_source, intitule_module):
    """
    Trouve le code_module a partir de l'intitule du module.
    Priorite a la correspondance EXACTE (respect de la casse).
    Si non trouve, cherche avec normalisation.
    """
    cursor = conn_source.cursor()
    cursor.execute("SELECT code_module, intitule FROM modules")
    modules = cursor.fetchall()
    cursor.close()
    
    # 1. RECHERCHE EXACTE (respect de la casse)
    for code_module, intitule in modules:
        if intitule == intitule_module:
            return code_module
    
    # 2. RECHERCHE NORMALISEE (insensible a la casse)
    normalized_input = normalize_string(intitule_module)
    for code_module, intitule in modules:
        if normalize_string(intitule) == normalized_input:
            print(f"    [INFO] Module trouve avec normalisation: '{intitule_module}' -> '{intitule}'")
            return code_module

    # 3. ALIAS EXPLICITE (noms Excel differents de l'intitule source)
    if intitule_module in MODULE_ALIASES:
        code_module = MODULE_ALIASES[intitule_module]
        if any(cm == code_module for cm, _ in modules):
            print(f"    [INFO] Module trouve via alias: '{intitule_module}' -> {code_module}")
            return code_module

    print(f"    [WARN] Module '{intitule_module}' non trouve dans la base source")
    return None

def get_semestre_for_module(conn_source, code_module):
    """Recupere le semestre a partir du code_module"""
    cursor = conn_source.cursor()
    cursor.execute("SELECT semestre FROM modules WHERE code_module = %s", (code_module,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def convert_date_excel(date_str):
    if pd.isna(date_str) or date_str == '':
        return None
    try:
        if isinstance(date_str, str):
            return datetime.strptime(date_str, '%d/%m/%Y').date()
        elif isinstance(date_str, (datetime, pd.Timestamp)):
            return date_str.date()
    except:
        return None
    return None

def safe_float_conversion(value):
    if pd.isna(value) or value is None or value == '':
        return None
    try:
        return float(value)
    except:
        return None

def safe_int_conversion(value, default=None):
    if pd.isna(value) or value is None:
        return default
    try:
        return int(float(value))
    except:
        return default

# ==================== GESTION DIM_TEMPS ====================

def get_or_create_id_temps(conn_dwh, annee_fichier, semestre):
    annee_scolaire = f"{annee_fichier}-{annee_fichier + 1}"
    
    cursor = conn_dwh.cursor()
    cursor.execute("""
        SELECT id_temps FROM DIM_TEMPS 
        WHERE semestre = %s AND annee_scolaire = %s
    """, (semestre, annee_scolaire))
    result = cursor.fetchone()
    
    if result:
        cursor.close()
        return result[0]
    
    cursor.execute("""
        INSERT INTO DIM_TEMPS (annee_scolaire, semestre, annee_fichier) 
        VALUES (%s, %s, %s) RETURNING id_temps
    """, (annee_scolaire, semestre, annee_fichier))
    id_temps = cursor.fetchone()[0]
    conn_dwh.commit()
    cursor.close()
    return id_temps

# ==================== PHASE 1 - DIMENSIONS ====================

def load_dim_etudiant(conn_source, conn_dwh):
    print("\n[INFO] Chargement DIM_ETUDIANT...")
    df = pd.read_sql("SELECT num_apogee, nom, prenom, email, annee_etude FROM etudiants", conn_source)
    cursor = conn_dwh.cursor()
    execute_values(cursor, """
        INSERT INTO DIM_ETUDIANT (num_apogee, nom, prenom, email, annee_etude)
        VALUES %s ON CONFLICT (num_apogee) DO NOTHING
    """, [tuple(row) for row in df.values])
    conn_dwh.commit()
    cursor.close()
    print(f"[OK] {len(df)} etudiants charges")

def load_dim_prof(conn_source, conn_dwh):
    print("\n[INFO] Chargement DIM_PROF...")
    df = pd.read_sql("SELECT id_prof, nom, prenom, email FROM professeurs", conn_source)
    cursor = conn_dwh.cursor()
    execute_values(cursor, """
        INSERT INTO DIM_PROF (id_prof, nom, prenom, email)
        VALUES %s ON CONFLICT (id_prof) DO NOTHING
    """, [tuple(row) for row in df.values])
    conn_dwh.commit()
    cursor.close()
    print(f"[OK] {len(df)} professeurs charges")

def load_dim_module(conn_source, conn_dwh):
    print("\n[INFO] Chargement DIM_MODULE...")
    df = pd.read_sql("""
        SELECT code_module, intitule, semestre, annee_etude,
               coeff_tp, coeff_cc, coeff_projet, coeff_examen
        FROM modules
    """, conn_source)
    cursor = conn_dwh.cursor()
    execute_values(cursor, """
        INSERT INTO DIM_MODULE (code_module, intitule, semestre, annee_etude,
                                coef_tp, coef_cc, coef_projet, coef_examen)
        VALUES %s ON CONFLICT (code_module) DO NOTHING
    """, [tuple(row) for row in df.values])
    conn_dwh.commit()
    cursor.close()
    print(f"[OK] {len(df)} modules charges")

def init_dim_type_eval(conn_dwh):
    cursor = conn_dwh.cursor()
    cursor.execute("SELECT COUNT(*) FROM DIM_TYPE_EVAL")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO DIM_TYPE_EVAL (libelle) VALUES ('TP'), ('CC'), ('Projet'), ('Examen')")
        conn_dwh.commit()
        print("[OK] DIM_TYPE_EVAL initialise")
    cursor.close()

# ==================== PHASE 2 - NOTES ====================

def process_fait_notes(conn_dwh, conn_source, code_module, module_name, filepath, annee_fichier, semestre):
    print(f"\n  [NOTES] Annee {annee_fichier}...")
    
    try:
        df = pd.read_excel(filepath)
        print(f"    Fichier: {len(df)} lignes")
    except Exception as e:
        print(f"    [ERROR] {e}")
        return 0
    
    cursor = conn_dwh.cursor()
    cursor.execute("""
        SELECT coef_tp, coef_cc, coef_projet, coef_examen 
        FROM DIM_MODULE WHERE code_module = %s
    """, (code_module,))
    coefs = cursor.fetchone()
    cursor.close()
    
    if not coefs:
        print(f"    [WARN] Coefficients non trouves")
        return 0
    
    coef_tp, coef_cc, coef_projet, coef_examen = float(coefs[0]), float(coefs[1]), float(coefs[2]), float(coefs[3])
    
    id_temps = get_or_create_id_temps(conn_dwh, annee_fichier, semestre)
    
    cursor = conn_dwh.cursor()
    cursor.execute("SELECT num_apogee, annee_etude FROM DIM_ETUDIANT")
    etudiant_annee = {row[0]: row[1] for row in cursor.fetchall()}
    cursor.close()
    
    notes_data = []
    
    for _, row in df.iterrows():
        num_apogee = row.get('num_apogee')
        if pd.isna(num_apogee) or num_apogee not in etudiant_annee:
            continue
        
        note_tp = safe_float_conversion(row.get('EP'))
        note_cc = safe_float_conversion(row.get('CC'))
        note_projet = safe_float_conversion(row.get('TD'))
        note_examen = safe_float_conversion(row.get('examen'))
        
        total_weight = 0
        weighted_sum = 0
        
        if note_tp is not None and coef_tp > 0:
            weighted_sum += note_tp * coef_tp
            total_weight += coef_tp
        if note_cc is not None and coef_cc > 0:
            weighted_sum += note_cc * coef_cc
            total_weight += coef_cc
        if note_projet is not None and coef_projet > 0:
            weighted_sum += note_projet * coef_projet
            total_weight += coef_projet
        if note_examen is not None and coef_examen > 0:
            weighted_sum += note_examen * coef_examen
            total_weight += coef_examen
        
        if total_weight == 0:
            continue
        
        moyenne = round(weighted_sum / total_weight, 2)
        
        evaluations = []
        if note_tp is not None:
            evaluations.append('TP')
        if note_cc is not None:
            evaluations.append('CC')
        if note_projet is not None:
            evaluations.append('Projet')
        if note_examen is not None:
            evaluations.append('Examen')
        eval_str = '+'.join(evaluations) if evaluations else None
        
        annee_etude = etudiant_annee[num_apogee]
        if '1ere' in annee_etude or '2eme' in annee_etude:
            statut = 'Valide' if moyenne >= 10 else 'Non valide'
        else:
            statut = 'Valide' if moyenne >= 12 else 'Non valide'
        
        notes_data.append({
            'num_apogee': num_apogee,
            'note_tp': note_tp,
            'note_cc': note_cc,
            'note_projet': note_projet,
            'note_examen': note_examen,
            'moyenne': moyenne,
            'evaluations': eval_str,
            'statut': statut
        })
    
    if not notes_data:
        print(f"    Aucune donnee valide")
        return 0
    
    df_notes = pd.DataFrame(notes_data)
    
    if len(df_notes) > 1:
        df_notes['classement'] = df_notes['moyenne'].rank(ascending=False, method='min').astype(int)
        moyenne_classe = df_notes['moyenne'].mean()
        df_notes['ecart'] = (df_notes['moyenne'] - moyenne_classe).round(2)
    else:
        df_notes['classement'] = 1
        df_notes['ecart'] = 0.0
    
    cursor = conn_dwh.cursor()
    inserted = 0
    
    for _, row in df_notes.iterrows():
        if pd.notna(row['note_tp']):
            eval_type = 1
        elif pd.notna(row['note_cc']):
            eval_type = 2
        elif pd.notna(row['note_projet']):
            eval_type = 3
        elif pd.notna(row['note_examen']):
            eval_type = 4
        else:
            eval_type = 2
        
        try:
            cursor.execute("""
                INSERT INTO FAIT_NOTES 
                (num_apogee, code_module, id_temps, id_type_eval, 
                 note_tp, note_cc, note_projet, note_examen, 
                 evaluations_passees, moyenne, classement, 
                 ecart_moyenne_classe, statut_validation)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['num_apogee'], code_module, id_temps, eval_type,
                row['note_tp'], row['note_cc'], row['note_projet'], row['note_examen'],
                row['evaluations'], row['moyenne'], row['classement'],
                row['ecart'], row['statut']
            ))
            inserted += 1
        except Exception as e:
            pass
    
    conn_dwh.commit()
    cursor.close()
    
    print(f"    [OK] {inserted} notes inserees, moyenne: {df_notes['moyenne'].mean():.2f}")
    return inserted

# ==================== PHASE 2 - ABSENCES ====================

def process_fait_absences(conn_dwh, conn_source, code_module, filepath, annee_fichier, semestre):
    print(f"\n  [ABSENCES] Annee {annee_fichier}...")
    
    try:
        df = pd.read_excel(filepath)
        print(f"    Fichier: {len(df)} lignes")
    except Exception as e:
        print(f"    [ERROR] {e}")
        return 0
    
    if 'date' not in df.columns:
        print(f"    [WARN] Colonne 'date' manquante")
        return 0
    
    id_temps = get_or_create_id_temps(conn_dwh, annee_fichier, semestre)
    
    df['date'] = df['date'].apply(convert_date_excel)
    df = df.dropna(subset=['num_apogee', 'date'])
    
    if df.empty:
        return 0
    
    if 'justifiee' not in df.columns:
        df['justifiee'] = 'N'
    
    aggs = df.groupby('num_apogee').agg(
        nb_absences_total=('num_apogee', 'count'),
        nb_non_justifiees=('justifiee', lambda x: (x == 'N').sum())
    ).reset_index()
    
    aggs['taux_absence'] = (aggs['nb_absences_total'] / NB_SEANCES_TOTAL * 100).round(2)
    aggs['seuil_depasse'] = aggs['nb_non_justifiees'].apply(lambda x: 'O' if x > 3 else 'N')
    
    df = df.merge(aggs[['num_apogee', 'nb_absences_total', 'taux_absence', 'seuil_depasse']], on='num_apogee', how='left')
    df['nb_seances_total'] = NB_SEANCES_TOTAL
    
    cursor = conn_dwh.cursor()
    data = []
    for _, row in df.iterrows():
        data.append((
            row['num_apogee'], code_module, id_temps,
            row['date'], row.get('seance'), row['justifiee'],
            row['nb_absences_total'], row['nb_seances_total'],
            row['taux_absence'], row['seuil_depasse']
        ))
    
    execute_values(cursor, """
        INSERT INTO FAIT_ABSENCES 
        (num_apogee, code_module, id_temps, date_seance, seance, justifiee,
         nb_absences_total, nb_seances_total, taux_absence, seuil_depasse)
        VALUES %s
    """, data)
    
    conn_dwh.commit()
    cursor.close()
    
    print(f"    [OK] {len(df)} absences inserees")
    return len(df)

# ==================== PHASE 2 - TRAVAUX ====================

def process_fait_travaux(conn_dwh, conn_source, code_module, filepath, annee_fichier, semestre):
    print(f"\n  [TRAVAUX] Annee {annee_fichier}...")
    
    try:
        df = pd.read_excel(filepath)
        print(f"    Fichier: {len(df)} lignes")
    except Exception as e:
        print(f"    [ERROR] {e}")
        return 0
    
    if 'date_rendu' not in df.columns or 'date_limite' not in df.columns:
        print(f"    [WARN] Colonnes dates manquantes")
        return 0
    
    id_temps = get_or_create_id_temps(conn_dwh, annee_fichier, semestre)
    
    df['date_rendu'] = df['date_rendu'].apply(convert_date_excel)
    df['date_limite'] = df['date_limite'].apply(convert_date_excel)
    
    if 'rendu' not in df.columns:
        df['rendu'] = 'N'
    
    def calc_retard(row):
        if row.get('rendu') == 'O' and row.get('date_rendu') and row.get('date_limite'):
            delta = row['date_rendu'] - row['date_limite']
            return max(delta.days, 0) if delta.days > 0 else 0
        return None
    
    df['retard_jours'] = df.apply(calc_retard, axis=1)
    
    cursor = conn_dwh.cursor()
    data = []
    for idx, row in df.iterrows():
        num_apogee = row.get('num_apogee')
        if pd.isna(num_apogee):
            continue
        
        id_travail = safe_int_conversion(row.get('id_travail'), idx + 1)
        rendu = row.get('rendu', 'N')
        retard = safe_int_conversion(row.get('retard_jours'))
        
        data.append((
            num_apogee, code_module, id_temps,
            id_travail, rendu,
            row.get('date_rendu'), row.get('date_limite'),
            retard
        ))
    
    if data:
        execute_values(cursor, """
            INSERT INTO FAIT_TRAVAUX 
            (num_apogee, code_module, id_temps, id_travail, rendu, 
             date_rendu, date_limite, retard_jours)
            VALUES %s
        """, data)
        conn_dwh.commit()
    
    cursor.close()
    print(f"    [OK] {len(data)} travaux inseres")
    return len(data)

# ==================== PHASE 3 - RECLAMATIONS ====================

def process_fait_reclamations(conn_source, conn_dwh):
    print("\n[INFO] Traitement des reclamations...")
    
    try:
        query = """
            SELECT id_reclamation, emetteur_id, destinataire_id, code_module,
                   date_reclamation, type_reclamation, statut
            FROM reclamations
            WHERE role_emetteur = 'etudiant' AND role_destinataire = 'professeur'
        """
        
        df = pd.read_sql(query, conn_source)
        print(f"  {len(df)} reclamations recuperees")
        
        if df.empty:
            print("  Aucune reclamation a traiter")
            return 0
        
        cursor = conn_dwh.cursor()
        inserted = 0
        
        for _, row in df.iterrows():
            num_apogee = row['emetteur_id']
            id_prof = row['destinataire_id']
            code_module = row['code_module']
            date_depot = row['date_reclamation']
            type_reclam = row['type_reclamation']
            statut = row['statut']
            
            cursor.execute("SELECT semestre FROM DIM_MODULE WHERE code_module = %s", (code_module,))
            semestre = cursor.fetchone()
            semestre = semestre[0] if semestre else None
            
            annee_fichier = date_depot.year
            id_temps = get_or_create_id_temps(conn_dwh, annee_fichier, semestre)
            
            date_reponse = None
            delai = None
            if statut == 'traitee':
                delai = 1
                date_reponse = date_depot + timedelta(days=1)
            
            cursor.execute("""
                INSERT INTO FAIT_RECLAMATIONS 
                (num_apogee, id_prof, code_module, id_temps, type_reclamation, 
                 statut, date_depot, date_reponse, delai_traitement)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (num_apogee, id_prof, code_module, id_temps, type_reclam,
                  statut, date_depot, date_reponse, delai))
            inserted += 1
        
        conn_dwh.commit()
        cursor.close()
        
        print(f"[OK] {inserted} reclamations chargees")
        return inserted
    except Exception as e:
        print(f"  [ERROR] Erreur traitement reclamations: {e}")
        return 0

# ==================== SCAN DES FICHIERS ====================

def parse_filename(filename):
    pattern = r'^(notes|absences|travaux)_(.+?)_(\d{4})\.xlsx$'
    match = re.match(pattern, filename)
    if match:
        return match.group(1), match.group(2), int(match.group(3))
    return None, None, None

def scan_excel_files(dossier):
    """Scanne le dossier et groupe les fichiers par module (garde le nom exact)"""
    modules = {}
    
    if not os.path.exists(dossier):
        os.makedirs(dossier)
        return modules
    
    for filepath in glob.glob(os.path.join(dossier, "*.xlsx")):
        filename = os.path.basename(filepath)
        file_type, module_name, annee = parse_filename(filename)
        
        if file_type and module_name and annee:
            if module_name not in modules:
                modules[module_name] = {}
            if annee not in modules[module_name]:
                modules[module_name][annee] = {}
            modules[module_name][annee][file_type] = filepath
    
    return modules

# ==================== RAPPORT FINAL ====================

def generate_final_report(conn_dwh):
    print("\n" + "="*70)
    print("RAPPORT FINAL")
    print("="*70)
    
    cursor = conn_dwh.cursor()
    
    print("\nDIMENSIONS:")
    for table in ['DIM_ETUDIANT', 'DIM_PROF', 'DIM_MODULE', 'DIM_TEMPS', 'DIM_TYPE_EVAL']:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"  {table}: {cursor.fetchone()[0]}")
    
    print("\nFAITS:")
    for table in ['FAIT_NOTES', 'FAIT_ABSENCES', 'FAIT_TRAVAUX', 'FAIT_RECLAMATIONS']:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"  {table}: {cursor.fetchone()[0]}")
    
    print("\nDIM_TEMPS:")
    cursor.execute("SELECT id_temps, annee_scolaire, semestre, annee_fichier FROM DIM_TEMPS ORDER BY annee_scolaire")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} ({row[2]}) <- fichier {row[3]}")
    
    cursor.execute("SELECT COUNT(DISTINCT num_apogee), ROUND(AVG(moyenne),2) FROM FAIT_NOTES WHERE moyenne IS NOT NULL")
    nb, moy = cursor.fetchone()
    if nb:
        print(f"\nNOTES: {nb} etudiants, moyenne generale: {moy}/20")
    
    cursor.close()

# ==================== MAIN ====================

def main():
    print("="*70)
    print("ETL DATA WAREHOUSE UNIVERSITAIRE")
    print("="*70)
    
    conn_source = None
    conn_dwh = None
    
    try:
        print(f"\nDossier Excel: {DOSSIER_EXCEL}")
        print("\n[1] Connexion aux bases...")
        conn_source = get_db_connection(SOURCE_DB_CONFIG)
        conn_dwh = get_db_connection(DWH_DB_CONFIG)
        print("[OK] Connexions etablies")
        
        init_dim_type_eval(conn_dwh)
        
        print("\n" + "="*50)
        print("PHASE 1 - CHARGEMENT DES DIMENSIONS")
        print("="*50)
        load_dim_etudiant(conn_source, conn_dwh)
        load_dim_prof(conn_source, conn_dwh)
        load_dim_module(conn_source, conn_dwh)
        
        print("\n" + "="*50)
        print("PHASE 2 - FICHIERS EXCEL")
        print("="*50)
        
        modules = scan_excel_files(DOSSIER_EXCEL)
        
        if not modules:
            print(f"[WARN] Aucun fichier dans {DOSSIER_EXCEL}")
        else:
            print(f"\nModules trouves: {len(modules)}")
            
            for module_name, annees_data in modules.items():
                print(f"\n{'='*50}")
                print(f"Module Excel: {module_name}")
                print(f"Annees: {sorted(annees_data.keys())}")
                print(f"{'='*50}")
                
                # Chercher le code_module dans la base
                code_module = find_code_module(conn_source, module_name)
                if not code_module:
                    print(f"  Module ignore (non trouve dans la base)")
                    continue
                
                # Recuperer le semestre depuis la base
                semestre = get_semestre_for_module(conn_source, code_module)
                print(f"Code module: {code_module} (Semestre: {semestre})")
                
                for annee in sorted(annees_data.keys()):
                    files = annees_data[annee]
                    print(f"\n  --- Annee {annee} ---")
                    
                    if 'notes' in files:
                        process_fait_notes(conn_dwh, conn_source, code_module, module_name, files['notes'], annee, semestre)
                    if 'absences' in files:
                        process_fait_absences(conn_dwh, conn_source, code_module, files['absences'], annee, semestre)
                    if 'travaux' in files:
                        process_fait_travaux(conn_dwh, conn_source, code_module, files['travaux'], annee, semestre)
        
        print("\n" + "="*50)
        print("PHASE 3 - RECLAMATIONS")
        print("="*50)
        process_fait_reclamations(conn_source, conn_dwh)
        
        generate_final_report(conn_dwh)
        
        print("\n" + "="*70)
        print("ETL TERMINE")
        print("="*70)
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        if conn_source:
            conn_source.close()
        if conn_dwh:
            conn_dwh.close()
        print("\nConnexions fermees")

if __name__ == "__main__":
    main()