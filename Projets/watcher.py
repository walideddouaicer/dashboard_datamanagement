#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de surveillance ETL - watcher.py
Surveille le dossier Excel et la base de données source,
déclenche automatiquement l'ETL en cas de changement.
"""

import os
import sys
import time
import threading
import subprocess
import hashlib
from datetime import datetime
from pathlib import Path

# Forcer l'encodage UTF-8 pour la console Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import psycopg2
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ==================== CONFIGURATION ====================

# Connexion base source PostgreSQL
SOURCE_DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'Universite',
    'user': 'postgres',
    'password': 'postgres'
}

# Configuration
DOSSIER_EXCEL = './excel_files'
CHEMIN_ETL = 'etl_datawarehouse.py'
INTERVALLE_VERIFICATION_DB = 30  # secondes
ATTENTE_AVANT_ETL = 3  # secondes d'attente après détection

# Tables à surveiller
TABLES_A_SURVEILLER = [
    'professeurs',
    'etudiants',
    'modules',
    'enseigne',
    'salles',
    'reservations_salles',
    'evenements',
    'reclamations'
]

# Variables globales pour le verrou ETL
etl_en_cours = False
etl_lock = threading.Lock()

# ==================== FONCTIONS UTILITAIRES ====================

def get_timestamp():
    """Retourne un timestamp formaté sans emojis pour compatibilité"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def print_info(msg):
    """Affiche un message d'information"""
    print(f"[{get_timestamp()}] {msg}")

def print_success(msg):
    """Affiche un message de succès"""
    print(f"[{get_timestamp()}] [OK] {msg}")

def print_warning(msg):
    """Affiche un message d'avertissement"""
    print(f"[{get_timestamp()}] [WARN] {msg}")

def print_error(msg):
    """Affiche un message d'erreur"""
    print(f"[{get_timestamp()}] [ERROR] {msg}")

def print_separator(char='=', length=70):
    """Affiche une ligne de séparation"""
    print(char * length)

def get_db_connection():
    """Crée une connexion PostgreSQL"""
    try:
        conn = psycopg2.connect(**SOURCE_DB_CONFIG)
        return conn
    except Exception as e:
        print_error(f"Erreur de connexion DB: {e}")
        return None

def get_table_counts():
    """Récupère le nombre de lignes pour chaque table surveillée"""
    conn = get_db_connection()
    if not conn:
        return None
    
    counts = {}
    cursor = conn.cursor()
    
    for table in TABLES_A_SURVEILLER:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            counts[table] = cursor.fetchone()[0]
        except Exception as e:
            print_error(f"Erreur lecture table {table}: {e}")
            counts[table] = -1
    
    cursor.close()
    conn.close()
    return counts

def run_etl(trigger_source, details=""):
    """Exécute le script ETL avec un verrou pour éviter les exécutions simultanées"""
    global etl_en_cours, etl_lock
    
    with etl_lock:
        if etl_en_cours:
            print_warning(f"ETL deja en cours, declenchement ignore (source: {trigger_source})")
            return False
        
        etl_en_cours = True
    
    try:
        print_separator()
        print_info(f"DECLENCHEMENT ETL")
        print_info(f"  Source: {trigger_source}")
        if details:
            print_info(f"  Details: {details}")
        print_separator()
        
        # Exécution du script ETL
        # Utiliser chcp 65001 pour UTF-8 sur Windows
        if sys.platform == 'win32':
            command = f'chcp 65001 > nul && {sys.executable} "{CHEMIN_ETL}"'
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                shell=True
            )
        else:
            result = subprocess.run(
                [sys.executable, CHEMIN_ETL],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
        
        if result.returncode == 0:
            print_success(f"ETL termine avec succes")
            # Afficher les dernières lignes de la sortie
            if result.stdout:
                lignes = result.stdout.strip().split('\n')
                for ligne in lignes[-5:]:  # Dernières 5 lignes
                    if 'OK' in ligne or 'succes' in ligne.lower() or 'fait' in ligne:
                        print(f"   {ligne[:100]}")
        else:
            print_error(f"ETL echoue (code {result.returncode})")
            if result.stderr:
                # Afficher les premières lignes d'erreur
                erreur_lignes = result.stderr.strip().split('\n')
                for ligne in erreur_lignes[:10]:
                    print(f"   {ligne[:150]}")
        
        return result.returncode == 0
        
    except FileNotFoundError:
        print_error(f"Script ETL non trouve: {CHEMIN_ETL}")
        return False
    except Exception as e:
        print_error(f"Erreur execution ETL: {e}")
        return False
    finally:
        with etl_lock:
            etl_en_cours = False

# ==================== SURVEILLANCE DOSSIER EXCEL ====================

class ExcelFileHandler(FileSystemEventHandler):
    """Gestionnaire d'événements pour les fichiers Excel"""
    
    def __init__(self):
        self.pending_files = set()
        self.timer = None
    
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.xlsx'):
            self.handle_new_file(event.src_path)
    
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.xlsx'):
            self.handle_new_file(event.src_path)
    
    def handle_new_file(self, filepath):
        filename = os.path.basename(filepath)
        
        # Ajouter le fichier à la liste des fichiers en attente
        self.pending_files.add(filename)
        print_info(f"Nouveau fichier detecte: {filename}")
        
        # Réinitialiser le timer
        if self.timer:
            self.timer.cancel()
        
        # Planifier l'exécution après 3 secondes
        self.timer = threading.Timer(ATTENTE_AVANT_ETL, self.trigger_etl)
        self.timer.start()
    
    def trigger_etl(self):
        if self.pending_files:
            details = f"{len(self.pending_files)} nouveau(x) fichier(s): {', '.join(self.pending_files)}"
            run_etl("Dossier Excel", details)
            self.pending_files.clear()

def start_excel_watcher():
    """Démarre la surveillance du dossier Excel"""
    # Créer le dossier s'il n'existe pas
    if not os.path.exists(DOSSIER_EXCEL):
        os.makedirs(DOSSIER_EXCEL)
        print_info(f"Dossier cree: {os.path.abspath(DOSSIER_EXCEL)}")
    
    event_handler = ExcelFileHandler()
    observer = Observer()
    observer.schedule(event_handler, DOSSIER_EXCEL, recursive=False)
    observer.start()
    
    print_info(f"Surveillance dossier Excel demarree: {os.path.abspath(DOSSIER_EXCEL)}")
    return observer

# ==================== SURVEILLANCE BASE DE DONNÉES ====================

class DatabaseWatcher:
    """Surveille les changements dans la base de données"""
    
    def __init__(self, intervalle=INTERVALLE_VERIFICATION_DB):
        self.intervalle = intervalle
        self.counts_precedents = {}
        self.running = True
    
    def initialize_counts(self):
        """Initialise les compteurs au démarrage"""
        print_info(f"Initialisation des compteurs base de donnees...")
        
        counts = get_table_counts()
        if counts:
            self.counts_precedents = counts.copy()
            print_info(f"Compteurs initiaux:")
            for table, count in self.counts_precedents.items():
                if count >= 0:
                    print(f"     - {table}: {count} enregistrements")
            return True
        return False
    
    def check_and_trigger(self):
        """Vérifie les changements et déclenche l'ETL si nécessaire"""
        if not self.running:
            return
        
        current_counts = get_table_counts()
        if not current_counts:
            return
        
        changes = []
        for table in TABLES_A_SURVEILLER:
            if table in self.counts_precedents and table in current_counts:
                old_count = self.counts_precedents[table]
                new_count = current_counts[table]
                if old_count != new_count and old_count >= 0 and new_count >= 0:
                    diff = new_count - old_count
                    changes.append(f"{table}: {old_count} -> {new_count} ({diff:+d})")
        
        if changes:
            print_info(f"Changements detectes dans la base:")
            for change in changes:
                print(f"     - {change}")
            
            # Mettre à jour les compteurs avant d'exécuter l'ETL
            self.counts_precedents = current_counts.copy()
            
            # Déclencher l'ETL
            run_etl("Base de donnees", f"Tables modifiees: {len(changes)}")
        else:
            # Mise à jour silencieuse des compteurs (pas de changement)
            self.counts_precedents = current_counts.copy()
    
    def run(self):
        """Boucle principale de surveillance"""
        print_info(f"Surveillance base de donnees demarree (intervalle: {self.intervalle}s)")
        
        while self.running:
            time.sleep(self.intervalle)
            if self.running:
                self.check_and_trigger()
    
    def stop(self):
        """Arrête la surveillance"""
        self.running = False

# ==================== FONCTION PRINCIPALE ====================

def main():
    """Fonction principale"""
    # Forcer l'encodage UTF-8 pour la console Windows
    if sys.platform == 'win32':
        os.system('chcp 65001 > nul')
    
    print_separator()
    print_info("DEMARRAGE DU SYSTEME DE SURVEILLANCE")
    print_separator()
    print_info(f"Dossier Excel surveille: {os.path.abspath(DOSSIER_EXCEL)}")
    print_info(f"Base source: {SOURCE_DB_CONFIG['dbname']}")
    print_info(f"Intervalle DB: {INTERVALLE_VERIFICATION_DB}s")
    print_info(f"Attente avant ETL: {ATTENTE_AVANT_ETL}s")
    print_separator()
    
    # Vérifier que le script ETL existe
    if not os.path.exists(CHEMIN_ETL):
        print_error(f"Script ETL '{CHEMIN_ETL}' non trouve!")
        print_info(f"Verifiez que le fichier est dans le meme dossier que watcher.py")
        print_info(f"Dossier courant: {os.getcwd()}")
        sys.exit(1)
    
    # Démarrer la surveillance du dossier Excel
    excel_observer = start_excel_watcher()
    
    # Démarrer la surveillance de la base de données
    db_watcher = DatabaseWatcher()
    
    if not db_watcher.initialize_counts():
        print_warning(f"Impossible d'initialiser les compteurs DB")
        print_info(f"Verifiez que PostgreSQL est demarre et que la base '{SOURCE_DB_CONFIG['dbname']}' existe")
    
    # Démarrer la surveillance DB dans un thread séparé
    db_thread = threading.Thread(target=db_watcher.run, daemon=True)
    db_thread.start()
    
    print_info(f"Surveillance active")
    print_info(f"Appuyez sur Ctrl+C pour arreter\n")
    
    try:
        # Attendre indéfiniment
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print_info(f"Arret demande...")
    finally:
        # Arrêt propre
        print_info(f"Arret de la surveillance...")
        
        # Arrêter la surveillance DB
        db_watcher.stop()
        
        # Arrêter la surveillance Excel
        excel_observer.stop()
        excel_observer.join()
        
        # Attendre que le thread DB se termine
        db_thread.join(timeout=5)
        
        print_info(f"Surveillance arretee")

if __name__ == "__main__":
    main()