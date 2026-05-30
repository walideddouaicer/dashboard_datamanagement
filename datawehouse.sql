
DROP TABLE IF EXISTS FAIT_RECLAMATIONS CASCADE;
DROP TABLE IF EXISTS FAIT_TRAVAUX CASCADE;
DROP TABLE IF EXISTS FAIT_ABSENCES CASCADE;
DROP TABLE IF EXISTS FAIT_NOTES CASCADE;
DROP TABLE IF EXISTS DIM_TYPE_EVAL CASCADE;
DROP TABLE IF EXISTS DIM_TEMPS CASCADE;
DROP TABLE IF EXISTS DIM_PROF CASCADE;
DROP TABLE IF EXISTS DIM_MODULE CASCADE;
DROP TABLE IF EXISTS DIM_ETUDIANT CASCADE;

-- =====================================================
-- DIMENSIONS
-- =====================================================

-- 1. DIM_ETUDIANT
CREATE TABLE DIM_ETUDIANT (
    num_apogee INTEGER PRIMARY KEY,
    nom VARCHAR(50),
    prenom VARCHAR(50),
    email VARCHAR(100),
    annee_etude VARCHAR(20)
);

-- 2. DIM_MODULE
CREATE TABLE DIM_MODULE (
    code_module VARCHAR(20) PRIMARY KEY,
    intitule VARCHAR(100),
    semestre VARCHAR(5),
    annee_etude VARCHAR(20),
    coef_ep NUMERIC(4,2),
    coef_cc NUMERIC(4,2),
    coef_td NUMERIC(4,2),
    coef_examen NUMERIC(4,2)
);

-- 3. DIM_PROF
CREATE TABLE DIM_PROF (
    id_prof SERIAL PRIMARY KEY,
    nom VARCHAR(50),
    prenom VARCHAR(50),
    email VARCHAR(100)
);

-- 4. DIM_TEMPS
CREATE TABLE DIM_TEMPS (
    id_temps SERIAL PRIMARY KEY,
    annee_scolaire VARCHAR(10),
    semestre VARCHAR(5)
);

-- 5. DIM_TYPE_EVAL
CREATE TABLE DIM_TYPE_EVAL (
    id_type_eval SERIAL PRIMARY KEY,
    libelle VARCHAR(20)
);

-- =====================================================
-- INSERTION UNIQUEMENT DANS DIM_TYPE_EVAL
-- =====================================================
INSERT INTO DIM_TYPE_EVAL (libelle) VALUES
('EP'),
('CC'),
('TD'),
('Examen');

-- =====================================================
-- TABLES DE FAITS
-- =====================================================

-- 6. FAIT_NOTES
CREATE TABLE FAIT_NOTES (
    id_fait_note SERIAL PRIMARY KEY,
    num_apogee INTEGER REFERENCES DIM_ETUDIANT(num_apogee) ON DELETE RESTRICT,
    code_module VARCHAR(20) REFERENCES DIM_MODULE(code_module) ON DELETE RESTRICT,
    id_temps INTEGER REFERENCES DIM_TEMPS(id_temps) ON DELETE RESTRICT,
    id_type_eval INTEGER REFERENCES DIM_TYPE_EVAL(id_type_eval) ON DELETE RESTRICT,
    note_ep NUMERIC(5,2) NULL,
    note_cc NUMERIC(5,2) NULL,
    note_td NUMERIC(5,2) NULL,
    note_examen NUMERIC(5,2) NULL,
    evaluations_passees VARCHAR(30),
    moyenne NUMERIC(5,2),
    classement INTEGER,
    ecart_moyenne_classe NUMERIC(5,2),
    statut_validation VARCHAR(20)
);

-- 7. FAIT_ABSENCES
CREATE TABLE FAIT_ABSENCES (
    id_fait_absence SERIAL PRIMARY KEY,
    num_apogee INTEGER REFERENCES DIM_ETUDIANT(num_apogee) ON DELETE RESTRICT,
    code_module VARCHAR(20) REFERENCES DIM_MODULE(code_module) ON DELETE RESTRICT,
    id_temps INTEGER REFERENCES DIM_TEMPS(id_temps) ON DELETE RESTRICT,
    date_seance DATE,
    seance VARCHAR(20),
    justifiee CHAR(1) CHECK (justifiee IN ('O', 'N')),
    nb_absences_total INTEGER,
    taux_absence NUMERIC(5,2),
    seuil_depasse CHAR(1) CHECK (seuil_depasse IN ('O', 'N'))
);

-- 8. FAIT_TRAVAUX
CREATE TABLE FAIT_TRAVAUX (
    id_fait_travail SERIAL PRIMARY KEY,
    num_apogee INTEGER REFERENCES DIM_ETUDIANT(num_apogee) ON DELETE RESTRICT,
    code_module VARCHAR(20) REFERENCES DIM_MODULE(code_module) ON DELETE RESTRICT,
    id_temps INTEGER REFERENCES DIM_TEMPS(id_temps) ON DELETE RESTRICT,
    rendu CHAR(1) CHECK (rendu IN ('O', 'N')),
    date_rendu DATE NULL,
    date_limite DATE,
    retard_jours INTEGER
);

-- 9. FAIT_RECLAMATIONS
CREATE TABLE FAIT_RECLAMATIONS (
    id_fait_reclam SERIAL PRIMARY KEY,
    num_apogee INTEGER REFERENCES DIM_ETUDIANT(num_apogee) ON DELETE RESTRICT,
    id_prof INTEGER REFERENCES DIM_PROF(id_prof) ON DELETE RESTRICT,
    code_module VARCHAR(20) REFERENCES DIM_MODULE(code_module) ON DELETE RESTRICT,
    id_temps INTEGER REFERENCES DIM_TEMPS(id_temps) ON DELETE RESTRICT,
    type_reclamation VARCHAR(30),
    statut VARCHAR(20),
    date_depot DATE,
    date_reponse DATE NULL,
    delai_traitement INTEGER
);

ALTER TABLE FAIT_TRAVAUX 
ADD COLUMN id_travail INTEGER;
ALTER TABLE FAIT_ABSENCES 
ADD COLUMN nb_seances_total INTEGER;

ALTER TABLE DIM_MODULE 
RENAME COLUMN coef_ep TO coef_tp;
ALTER TABLE DIM_MODULE 
RENAME COLUMN coef_td TO coef_projet;
ALTER TABLE FAIT_NOTES 
RENAME COLUMN note_ep TO note_tp;
ALTER TABLE FAIT_NOTES 
RENAME COLUMN note_td TO note_projet;


SELECT * FROM FAIT_NOTES ;


-- 1. Supprimer l'ancienne table FAIT_NOTES
DROP TABLE IF EXISTS FAIT_NOTES CASCADE;

-- 2. Recréer FAIT_NOTES avec les bonnes colonnes
CREATE TABLE FAIT_NOTES (
    id_fait_note SERIAL PRIMARY KEY,
    num_apogee INTEGER REFERENCES DIM_ETUDIANT(num_apogee) ON DELETE RESTRICT,
    code_module VARCHAR(20) REFERENCES DIM_MODULE(code_module) ON DELETE RESTRICT,
    id_temps INTEGER REFERENCES DIM_TEMPS(id_temps) ON DELETE RESTRICT,
    id_type_eval INTEGER REFERENCES DIM_TYPE_EVAL(id_type_eval) ON DELETE RESTRICT,
    note_tp NUMERIC(5,2) NULL,
    note_cc NUMERIC(5,2) NULL,
    note_projet NUMERIC(5,2) NULL,
    note_examen NUMERIC(5,2) NULL,
    evaluations_passees VARCHAR(30),
    moyenne NUMERIC(5,2),
    classement INTEGER,
    ecart_moyenne_classe NUMERIC(5,2),
    statut_validation VARCHAR(20)
);

-- 3. Vérifier la structure
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'fait_notes' 
ORDER BY ordinal_position;

-- 1. Supprimer l'ancienne table FAIT_NOTES
DROP TABLE IF EXISTS FAIT_NOTES CASCADE;

-- 2. Recréer FAIT_NOTES avec les bonnes colonnes
CREATE TABLE FAIT_NOTES (
    id_fait_note SERIAL PRIMARY KEY,
    num_apogee INTEGER REFERENCES DIM_ETUDIANT(num_apogee) ON DELETE RESTRICT,
    code_module VARCHAR(20) REFERENCES DIM_MODULE(code_module) ON DELETE RESTRICT,
    id_temps INTEGER REFERENCES DIM_TEMPS(id_temps) ON DELETE RESTRICT,
    id_type_eval INTEGER REFERENCES DIM_TYPE_EVAL(id_type_eval) ON DELETE RESTRICT,
    note_tp NUMERIC(5,2) NULL,
    note_cc NUMERIC(5,2) NULL,
    note_projet NUMERIC(5,2) NULL,
    note_examen NUMERIC(5,2) NULL,
    evaluations_passees VARCHAR(30),
    moyenne NUMERIC(5,2),
    classement INTEGER,
    ecart_moyenne_classe NUMERIC(5,2),
    statut_validation VARCHAR(20)
);

-- 3. Vérifier la structure
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'fait_notes' 
ORDER BY ordinal_position;
TRUNCATE TABLE
FAIT_RECLAMATIONS,
FAIT_TRAVAUX,
FAIT_ABSENCES,
FAIT_NOTES,
DIM_ETUDIANT,
DIM_MODULE,
DIM_PROF,
DIM_TEMPS,
DIM_TYPE_EVAL
RESTART IDENTITY CASCADE;


-- Restructurer DIM_TEMPS
TRUNCATE TABLE DIM_TEMPS RESTART IDENTITY CASCADE;

ALTER TABLE DIM_TEMPS 
ADD COLUMN IF NOT EXISTS annee_fichier INTEGER;

-- Ajouter contrainte d'unicité
ALTER TABLE DIM_TEMPS 
ADD CONSTRAINT unique_semestre_annee 
UNIQUE (semestre, annee_scolaire);

select * from  FAIT_NOTES where id_temps = 13 ;
select * from DIM_TEMPS;

SELECT *
FROM DIM_MODULE ;