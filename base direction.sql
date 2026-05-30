-- =====================================================
-- BASE DE DONNÉES UNIVERSITÉ - VERSION SIMPLE
-- SANS NOTES - AVEC COEFFICIENTS DANS LES MODULES
-- =====================================================

-- Suppression des tables
DROP TABLE IF EXISTS reclamations CASCADE;
DROP TABLE IF EXISTS evenements CASCADE;
DROP TABLE IF EXISTS reservations_salles CASCADE;
DROP TABLE IF EXISTS enseigne CASCADE;
DROP TABLE IF EXISTS modules CASCADE;
DROP TABLE IF EXISTS etudiants CASCADE;
DROP TABLE IF EXISTS professeurs CASCADE;
DROP TABLE IF EXISTS salles CASCADE;

-- =====================================================
-- 1. TABLE PROFESSEURS
-- =====================================================
CREATE TABLE professeurs (
    id_prof SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL
);

INSERT INTO professeurs (nom, prenom, email, mot_de_passe) VALUES
('MOUMEN', 'Aniss', 'aniss.moumen@univ.ma', MD5('prof123')),
('BENNANI', 'Mohamed', 'mohamed.bennani@univ.ma', MD5('prof123')),
('ELFASSI', 'Fatima', 'fatima.elfassi@univ.ma', MD5('prof123')),
('TOUATI', 'Karim', 'karim.touati@univ.ma', MD5('prof123')),
('NAJI', 'Sanae', 'sanae.naji@univ.ma', MD5('prof123')),
('BOUSSAID', 'Rachid', 'rachid.boussaid@univ.ma', MD5('prof123')),
('BELKHIR', 'Hassan', 'hassan.belkhir@univ.ma', MD5('prof123')),
('MAGHRIBI', 'Nadia', 'nadia.maghribi@univ.ma', MD5('prof123')),
('SEBTI', 'Youssef', 'youssef.sebti@univ.ma', MD5('prof123')),
('CHAFIK', 'Samira', 'samira.chafik@univ.ma', MD5('prof123')),
('RADI', 'Hamza', 'hamza.radi@univ.ma', MD5('prof123')),
('ALAOUI', 'Imane', 'imane.alaoui@univ.ma', MD5('prof123')),
('BENCHERIF', 'Amine', 'amine.bencherif@univ.ma', MD5('prof123')),
('KETTANI', 'Soukaina', 'soukaina.kettani@univ.ma', MD5('prof123')),
('ZOUHRI', 'Reda', 'reda.zouhri@univ.ma', MD5('prof123')),
('BENZAKOUR', 'Asmae', 'asmae.benzakour@univ.ma', MD5('prof123')),
('YACOUBI', 'Mehdi', 'mehdi.yacoubi@univ.ma', MD5('prof123')),
('SLAOUI', 'Nawal', 'nawal.slaoui@univ.ma', MD5('prof123')),
('MOUDEN', 'Yassine', 'yassine.mouden@univ.ma', MD5('prof123')),
('BOUABID', 'Sara', 'sara.bouabid@univ.ma', MD5('prof123')),
('TABIBI', 'Hicham', 'hicham.tabibi@univ.ma', MD5('prof123')),
('BOUCHTA', 'Latifa', 'latifa.bouchta@univ.ma', MD5('prof123')),
('HADDAD', 'Karima', 'karima.haddad@univ.ma', MD5('prof123')),
('FARES', 'Rachida', 'rachida.fares@univ.ma', MD5('prof123'));

-- =====================================================
-- 2. TABLE ÉTUDIANTS (30 étudiants)
-- =====================================================
CREATE TABLE etudiants (
    num_apogee INTEGER PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    annee_etude VARCHAR(20) NOT NULL
);

INSERT INTO etudiants (num_apogee, nom, prenom, email, mot_de_passe, annee_etude) VALUES
(20220001, 'SABRI', 'Mehdi', 'mehdi.sabri@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220002, 'BENALI', 'Samira', 'samira.benali@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220003, 'TOUATI', 'Amine', 'amine.touati@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220004, 'LAHRICHI', 'Khadija', 'khadija.lahrichi@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220005, 'EL AMRANI', 'Mehdi', 'mehdi.elamrani@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220006, 'NADIR', 'Samira', 'samira.nadir@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220007, 'MOUFID', 'Mehdi', 'mehdi.moufid@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220008, 'KABBAB', 'Leila', 'leila.kabbab@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220009, 'CHERKAOUI', 'Youssef', 'youssef.cherkaoui@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220010, 'EL OMARI', 'Imane', 'imane.elomari@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220011, 'LAHRICHI', 'Anas', 'anas.lahrichi@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220012, 'FIKRI', 'Fatima', 'fatima.fikri@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220013, 'MOUFID', 'Amine', 'amine.moufid@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220014, 'IDRISSI', 'Nawal', 'nawal.idrissi@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220015, 'IDRISSI', 'Anas', 'anas.idrissi@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220016, 'AMRAOUI', 'Imane', 'imane.amraoui@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220017, 'ZEROUAL', 'Imad', 'imad.zeroual@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220018, 'TOUATI', 'Zineb', 'zineb.touati1@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220019, 'BENALI', 'Yassine', 'yassine.benali@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220020, 'AIT ALI', 'Samira', 'samira.aitali@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220021, 'AMRAOUI', 'Rachid', 'rachid.amraoui@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220022, 'TOUATI', 'Khadija', 'khadija.touati@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220023, 'FASSI', 'Yassine', 'yassine.fassi@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220024, 'BELMEHDI', 'Sara', 'sara.belmehdi@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220025, 'EL OMARI', 'Karim', 'karim.elomari@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220026, 'BENJELLOUN', 'Nadia', 'nadia.benjelloun@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220027, 'SEFRIOUI', 'Imad', 'imad.sefrioui@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220028, 'TOUATI', 'Zineb', 'zineb.touati2@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220029, 'CHERKAOUI', 'Saad', 'saad.cherkaoui@etudiant.ma', MD5('etudiant123'), '4eme annee'),
(20220030, 'ZEROUAL', 'Hind', 'hind.zeroual@etudiant.ma', MD5('etudiant123'), '4eme annee');

-- =====================================================
-- 3. TABLE MODULES (AVEC TOUS LES COEFFICIENTS)
-- =====================================================
CREATE TABLE modules (
    code_module VARCHAR(20) PRIMARY KEY,
    intitule VARCHAR(100) NOT NULL,
    semestre VARCHAR(5) NOT NULL,
    annee_etude VARCHAR(20) NOT NULL,
    coeff_cc DECIMAL(3,1) NOT NULL,
    coeff_tp DECIMAL(3,1) NOT NULL,
    coeff_projet DECIMAL(3,1) NOT NULL,
    coeff_examen DECIMAL(3,1) NOT NULL
);

INSERT INTO modules (code_module, intitule, semestre, annee_etude, coeff_cc, coeff_tp, coeff_projet, coeff_examen) VALUES
-- S1 (1ère année)
('M101', 'Algebre de base', 'S1', '1ere annee', 0.2, 0.2, 0.1, 0.5),
('M102', 'Analyse de base 1', 'S1', '1ere annee', 0.2, 0.2, 0.1, 0.5),
('M103', 'Analyse de base 2', 'S1', '1ere annee', 0.2, 0.2, 0.1, 0.5),
-- S2 (1ère année)
('M104', 'Analyse fondamentale', 'S2', '1ere annee', 0.2, 0.2, 0.1, 0.5),
('P101', 'Electromagnetisme', 'S2', '1ere annee', 0.2, 0.2, 0.1, 0.5),
('P102', 'Optique geometrique', 'S2', '1ere annee', 0.2, 0.2, 0.1, 0.5),
-- S3 (2ème année)
('M201', 'Algebre bilineaire', 'S3', '2eme annee', 0.2, 0.2, 0.1, 0.5),
('M202', 'Fonctions reelles', 'S3', '2eme annee', 0.2, 0.2, 0.1, 0.5),
('MEC101', 'Mecanique solide', 'S3', '2eme annee', 0.2, 0.2, 0.1, 0.5),
-- S4 (2ème année)
('SIG101', 'Traitement signal', 'S4', '2eme annee', 0.2, 0.2, 0.1, 0.5),
('P203', 'Optique physique', 'S4', '2eme annee', 0.2, 0.2, 0.1, 0.5),
('ELEC101', 'Electronique', 'S4', '2eme annee', 0.2, 0.2, 0.1, 0.5),
-- S5 (3ème année)
('INFO101', 'Structures donnees', 'S5', '3eme annee', 0.25, 0.15, 0.2, 0.4),
('STAT101', 'Statistique', 'S5', '3eme annee', 0.25, 0.15, 0.2, 0.4),
('ELEC201', 'Electronique numerique', 'S5', '3eme annee', 0.25, 0.15, 0.2, 0.4),
('RES101', 'Reseaux protocoles', 'S5', '3eme annee', 0.25, 0.15, 0.2, 0.4),
('BDD101', 'SI Technologies BDD', 'S5', '3eme annee', 0.25, 0.15, 0.2, 0.4),
('INFO201', 'Programmation', 'S5', '3eme annee', 0.25, 0.15, 0.2, 0.4),
-- S6 (3ème année)
('WEB101', 'Technologies Web', 'S6', '3eme annee', 0.25, 0.15, 0.2, 0.4),
('OPT101', 'Optimisation', 'S6', '3eme annee', 0.25, 0.15, 0.2, 0.4),
('SIM101', 'Modelisation', 'S6', '3eme annee', 0.25, 0.15, 0.2, 0.4),
-- S7 (4ème année)
('JAVA101', 'Java', 'S7', '4eme annee', 0.2, 0.2, 0.2, 0.4),
('IMG101', 'Traitement image', 'S7', '4eme annee', 0.2, 0.2, 0.2, 0.4),
('IA101', 'Introduction IA', 'S7', '4eme annee', 0.2, 0.2, 0.2, 0.4),
-- S8 (4ème année)
('DATA101', 'Data Management', 'S8', '4eme annee', 0.15, 0.15, 0.2, 0.5),
('SECU101', 'Securite donnees', 'S8', '4eme annee', 0.15, 0.15, 0.2, 0.5),
('BIG101', 'Fondamentaux Big Data', 'S8', '4eme annee', 0.15, 0.15, 0.2, 0.5);

-- =====================================================
-- 4. TABLE ENSEIGNE (Professeurs par module)
-- =====================================================
CREATE TABLE enseigne (
    id_prof INTEGER REFERENCES professeurs(id_prof),
    code_module VARCHAR(20) REFERENCES modules(code_module),
    PRIMARY KEY (id_prof, code_module)
);

INSERT INTO enseigne (id_prof, code_module) VALUES
(1, 'DATA101'),
(1, 'BIG101'),
(2, 'SECU101'),
(3, 'IA101'),
(4, 'JAVA101'),
(4, 'IMG101'),
(2, 'M101'), (2, 'M102'), (2, 'M103'),
(3, 'M104'), (3, 'P101'),
(4, 'P102'),
(5, 'M201'), (5, 'M202'),
(6, 'MEC101'), (6, 'SIG101'),
(7, 'P203'), (7, 'ELEC101'),
(8, 'INFO101'), (8, 'STAT101'),
(9, 'ELEC201'), (9, 'RES101'),
(10, 'BDD101'), (10, 'INFO201'),
(11, 'WEB101'), (11, 'OPT101'),
(12, 'SIM101');

-- =====================================================
-- 5. TABLE SALLES
-- =====================================================
CREATE TABLE salles (
    id_salle SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    type VARCHAR(20) NOT NULL,
    capacite INTEGER NOT NULL,
    batiment VARCHAR(20) NOT NULL,
    etage INTEGER NOT NULL
);

INSERT INTO salles (nom, type, capacite, batiment, etage) VALUES
('AmphiA', 'Amphi', 300, 'Principal', 0),
('AmphiB', 'Amphi', 250, 'Principal', 0),
('C101', 'Cours', 60, 'A', 1),
('C102', 'Cours', 60, 'A', 1),
('C103', 'Cours', 60, 'A', 1),
('C201', 'Cours', 60, 'A', 2),
('TD101', 'TD', 35, 'B', 1),
('TD102', 'TD', 35, 'B', 1),
('TD103', 'TD', 35, 'B', 1),
('TD201', 'TD', 35, 'B', 2),
('TPI101', 'TPInfo', 25, 'C', 1),
('TPI102', 'TPInfo', 25, 'C', 1),
('TPE101', 'TPElectro', 20, 'D', 1),
('TPE102', 'TPElectro', 20, 'D', 1);

-- =====================================================
-- 6. TABLE RESERVATIONS_SALLES
-- =====================================================
CREATE TABLE reservations_salles (
    id_reservation SERIAL PRIMARY KEY,
    id_prof INTEGER REFERENCES professeurs(id_prof),
    id_salle INTEGER REFERENCES salles(id_salle),
    code_module VARCHAR(20) REFERENCES modules(code_module),
    date_reservation DATE NOT NULL,
    heure_debut TIME NOT NULL,
    heure_fin TIME NOT NULL,
    statut VARCHAR(20) DEFAULT 'confirmee'
);

INSERT INTO reservations_salles (id_prof, id_salle, code_module, date_reservation, heure_debut, heure_fin, statut) VALUES
(1, 1, 'DATA101', '2025-12-01', '08:00:00', '12:00:00', 'confirmee'),
(1, 1, 'DATA101', '2025-12-03', '08:00:00', '12:00:00', 'confirmee'),
(1, 7, 'DATA101', '2025-12-05', '14:00:00', '17:00:00', 'confirmee'),
(2, 3, 'SECU101', '2025-12-02', '10:00:00', '12:00:00', 'confirmee'),
(3, 1, 'BIG101', '2025-12-04', '08:00:00', '12:00:00', 'confirmee'),
(4, 11, 'JAVA101', '2025-12-06', '14:00:00', '17:00:00', 'confirmee');

-- =====================================================
-- 7. TABLE EVENEMENTS
-- =====================================================
CREATE TABLE evenements (
    id_evenement SERIAL PRIMARY KEY,
    code_module VARCHAR(20) REFERENCES modules(code_module),
    id_salle INTEGER REFERENCES salles(id_salle),
    type_evenement VARCHAR(20) NOT NULL,
    objet VARCHAR(200) NOT NULL,
    date_evenement DATE NOT NULL,
    heure_evenement TIME NOT NULL,
    promotion VARCHAR(20) NOT NULL
);

INSERT INTO evenements (code_module, id_salle, type_evenement, objet, date_evenement, heure_evenement, promotion) VALUES
('BIG101', 1, 'TP', 'Examen final Big Data', '2026-06-25', '08:00:00', '2025-2026');

-- =====================================================
-- 8. TABLE RECLAMATIONS
-- =====================================================
CREATE TABLE reclamations (
    id_reclamation SERIAL PRIMARY KEY,
    emetteur_id INTEGER NOT NULL,
    role_emetteur VARCHAR(20) NOT NULL,
    destinataire_id INTEGER NOT NULL,
    role_destinataire VARCHAR(20) NOT NULL,
    code_module VARCHAR(20) REFERENCES modules(code_module),
    date_reclamation DATE NOT NULL,
    type_reclamation VARCHAR(30) NOT NULL,
    statut VARCHAR(20) DEFAULT 'en_attente',
    description TEXT NOT NULL,
    reponse TEXT
);

INSERT INTO reclamations (emetteur_id, role_emetteur, destinataire_id, role_destinataire, code_module, date_reclamation, type_reclamation, statut, description, reponse) VALUES
(20220001, 'etudiant', 1, 'professeur', 'DATA101', '2026-01-18', 'note', 'traitee', 
 'Monsieur Moumen, je conteste ma note de 09/20 a l examen.', 
 'Apres verification, votre note est corrigee a 14/20'),

(20220005, 'etudiant', 1, 'professeur', 'DATA101', '2026-01-20', 'absence', 'en_attente', 
 'Monsieur, j ai ete marque absent au TD.', NULL),

(20220010, 'etudiant', 1, 'professeur', 'DATA101', '2026-01-22', 'cours', 'traitee', 
 'Cours annule. Y aura-t-il un rattrapage ?', 
 'Cours de rattrapage le 05/01 a 14h en salle TPI101');

-- =====================================================
-- 9. REQUÊTES DE VÉRIFICATION
-- =====================================================

-- Statistiques
SELECT '=== STATISTIQUES ===' AS info;
SELECT 'Professeurs' AS table_name, COUNT(*) AS nb FROM professeurs
UNION ALL SELECT 'Etudiants', COUNT(*) FROM etudiants
UNION ALL SELECT 'Modules', COUNT(*) FROM modules
UNION ALL SELECT 'Enseigne', COUNT(*) FROM enseigne
UNION ALL SELECT 'Salles', COUNT(*) FROM salles
UNION ALL SELECT 'Reservations', COUNT(*) FROM reservations_salles
UNION ALL SELECT 'Evenements', COUNT(*) FROM evenements
UNION ALL SELECT 'Reclamations', COUNT(*) FROM reclamations;

-- Liste des modules avec coefficients
SELECT '=== MODULES AVEC COEFFICIENTS ===' AS info;
SELECT code_module, intitule, semestre, coeff_cc, coeff_tp, coeff_projet, coeff_examen 
FROM modules 
ORDER BY semestre;

-- Liste des étudiants
SELECT '=== LISTE DES ETUDIANTS ===' AS info;
SELECT num_apogee, nom, prenom, annee_etude FROM etudiants ORDER BY num_apogee;

select * from enseigne;



-- =====================================================
-- INSERTION DES ÉTUDIANTS HISTORIQUES
-- TABLE: etudiants
-- =====================================================

-- Promotion 2021-2022 (Laureats 2023)
INSERT INTO etudiants (num_apogee, nom, prenom, email, mot_de_passe, annee_etude) VALUES
(20180001, 'BOUCHTA', 'Rachid', 'rachid.bouchta@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180002, 'EL KHATTABI', 'Samira', 'samira.elkhattabi@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180003, 'MOUSSAOUI', 'Nabil', 'nabil.moussaoui@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180004, 'FARES', 'Rachida', 'rachida.fares@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180005, 'BENAMAR', 'Jamal', 'jamal.benamar@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180006, 'EL HADDAD', 'Naima', 'naima.elhaddad@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180007, 'BOUCHERIT', 'Mustapha', 'mustapha.boucherit@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180008, 'LOULIDI', 'Najat', 'najat.loulidi@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180009, 'MAGHRIBI', 'Hassan', 'hassan.maghribi@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180010, 'SEBTI', 'Rim', 'rim.sebti@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180011, 'BELKHIR', 'Tarik', 'tarik.belkhir@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180012, 'FENJIRO', 'Ghita', 'ghita.fenjiro@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180013, 'ZOUHRI', 'Omar', 'omar.zouhri@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180014, 'EL ALAOUI', 'Sana', 'sana.alaoui@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180015, 'BENCHERIF', 'Yacine', 'yacine.bencherif@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180016, 'BOUCHTA', 'Nadia', 'nadia.bouchta@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180017, 'EL KHATTABI', 'Karim', 'karim.elkhattabi@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180018, 'MOUSSAOUI', 'Latifa', 'latifa.moussaoui@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180019, 'FARES', 'Hicham', 'hicham.fares@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180020, 'BENAMAR', 'Fatima', 'fatima.benamar@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180021, 'EL HADDAD', 'Fouad', 'fouad.elhaddad@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180022, 'BOUCHERIT', 'Siham', 'siham.boucherit@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180023, 'LOULIDI', 'Khalid', 'khalid.loulidi@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180024, 'MAGHRIBI', 'Mouna', 'mouna.maghribi@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180025, 'SEBTI', 'Abdellah', 'abdellah.sebti@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180026, 'BELKHIR', 'Hajar', 'hajar.belkhir@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180027, 'FENJIRO', 'Said', 'said.fenjiro@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180028, 'ZOUHRI', 'Wiam', 'wiam.zouhri@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180029, 'EL ALAOUI', 'Abdel', 'abdel.alaoui@alumni.ma', MD5('etudiant123'), 'Laureat 2023'),
(20180030, 'BENCHERIF', 'Lamia', 'lamia.bencherif@alumni.ma', MD5('etudiant123'), 'Laureat 2023');

-- Promotion 2022-2023 (Laureats 2024)
INSERT INTO etudiants (num_apogee, nom, prenom, email, mot_de_passe, annee_etude) VALUES
(20190001, 'GHANNAM', 'Rachid', 'rachid.ghannam@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190002, 'EL HILALI', 'Samira', 'samira.elhilali@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190003, 'AZAMI', 'Nabil', 'nabil.azami@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190004, 'BOUABID', 'Rachida', 'rachida.bouabid@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190005, 'TABIBI', 'Jamal', 'jamal.tabibi@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190006, 'EL FASSI', 'Naima', 'naima.elfassi@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190007, 'KETTANI', 'Mustapha', 'mustapha.kettani@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190008, 'BENZAKOUR', 'Najat', 'najat.benzakour@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190009, 'EL YACOUBI', 'Hassan', 'hassan.elyacoubi@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190010, 'SLAOUI', 'Rim', 'rim.slaoui@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190011, 'BENSLIMANE', 'Tarik', 'tarik.benslimane@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190012, 'EL MOUDEN', 'Ghita', 'ghita.elmouden@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190013, 'CHAFIK', 'Omar', 'omar.chafik@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190014, 'RADI', 'Sana', 'sana.radi@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190015, 'ZIANI', 'Yacine', 'yacine.ziani@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190016, 'GHANNAM', 'Nadia', 'nadia.ghannam@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190017, 'EL HILALI', 'Karim', 'karim.elhilali@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190018, 'AZAMI', 'Latifa', 'latifa.azami@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190019, 'BOUABID', 'Hicham', 'hicham.bouabid@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190020, 'TABIBI', 'Fatima', 'fatima.tabibi@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190021, 'EL FASSI', 'Fouad', 'fouad.elfassi@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190022, 'KETTANI', 'Siham', 'siham.kettani@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190023, 'BENZAKOUR', 'Khalid', 'khalid.benzakour@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190024, 'EL YACOUBI', 'Mouna', 'mouna.elyacoubi@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190025, 'SLAOUI', 'Abdellah', 'abdellah.slaoui@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190026, 'BENSLIMANE', 'Hajar', 'hajar.benslimane@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190027, 'EL MOUDEN', 'Said', 'said.elmouden@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190028, 'CHAFIK', 'Wiam', 'wiam.chafik@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190029, 'RADI', 'Abdel', 'abdel.radi@alumni.ma', MD5('etudiant123'), 'Laureat 2024'),
(20190030, 'ZIANI', 'Lamia', 'lamia.ziani@alumni.ma', MD5('etudiant123'), 'Laureat 2024');

-- Promotion 2023-2024 (Laureats 2025)
INSERT INTO etudiants (num_apogee, nom, prenom, email, mot_de_passe, annee_etude) VALUES
(20200001, 'BOUTALEB', 'Rachid', 'rachid.boutaleb@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200002, 'EL HACHIMI', 'Samira', 'samira.elhachimi@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200003, 'MEZIANE', 'Nabil', 'nabil.meziane@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200004, 'BOUDLAL', 'Rachida', 'rachida.boudlal@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200005, 'AIT BENALI', 'Jamal', 'jamal.aitbenali@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200006, 'EL HARRAK', 'Naima', 'naima.elharrak@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200007, 'ZOUAOUI', 'Mustapha', 'mustapha.zouaoui@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200008, 'BENABDELKRIM', 'Najat', 'najat.benabdelkrim@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200009, 'EL FIKRI', 'Hassan', 'hassan.elfikri@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200010, 'TOUHAMI', 'Rim', 'rim.touhami@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200011, 'BENNIS', 'Tarik', 'tarik.bennis@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200012, 'EL KHAYAT', 'Ghita', 'ghita.elkhayat@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200013, 'GHOULAM', 'Omar', 'omar.ghoulam@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200014, 'ZERHOUNI', 'Sana', 'sana.zerhouni@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200015, 'EL MANSOURI', 'Yacine', 'yacine.elmansouri@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200016, 'BOUTALEB', 'Nadia', 'nadia.boutaleb@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200017, 'EL HACHIMI', 'Karim', 'karim.elhachimi@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200018, 'MEZIANE', 'Latifa', 'latifa.meziane@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200019, 'BOUDLAL', 'Hicham', 'hicham.boudlal@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200020, 'AIT BENALI', 'Fatima', 'fatima.aitbenali@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200021, 'EL HARRAK', 'Fouad', 'fouad.elharrak@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200022, 'ZOUAOUI', 'Siham', 'siham.zouaoui@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200023, 'BENABDELKRIM', 'Khalid', 'khalid.benabdelkrim@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200024, 'EL FIKRI', 'Mouna', 'mouna.elfikri@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200025, 'TOUHAMI', 'Abdellah', 'abdellah.touhami@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200026, 'BENNIS', 'Hajar', 'hajar.bennis@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200027, 'EL KHAYAT', 'Said', 'said.elkhayat@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200028, 'GHOULAM', 'Wiam', 'wiam.ghoulam@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200029, 'ZERHOUNI', 'Abdel', 'abdel.zerhouni@alumni.ma', MD5('etudiant123'), 'Laureat 2025'),
(20200030, 'EL MANSOURI', 'Lamia', 'lamia.elmansouri@alumni.ma', MD5('etudiant123'), 'Laureat 2025');

-- Promotion 2024-2025 (5ème année - encore en étude)
INSERT INTO etudiants (num_apogee, nom, prenom, email, mot_de_passe, annee_etude) VALUES
(20210001, 'BAHLOUL', 'Rachid', 'rachid.bahloul@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210002, 'EL JAZOULI', 'Samira', 'samira.eljazouli@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210003, 'BENHADDOU', 'Nabil', 'nabil.benhaddou@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210004, 'CHARKAOUI', 'Rachida', 'rachida.charkaoui@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210005, 'EL BAKKALI', 'Jamal', 'jamal.elbakkali@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210006, 'BENNACER', 'Naima', 'naima.bennacer@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210007, 'EL HARIM', 'Mustapha', 'mustapha.elharim@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210008, 'ZAIRI', 'Najat', 'najat.zairi@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210009, 'BENHAMOU', 'Hassan', 'hassan.benhamou@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210010, 'EL MESSAOUDI', 'Rim', 'rim.elmessaoudi@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210011, 'BOUSSAID', 'Tarik', 'tarik.boussaid@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210012, 'EL HACHMI', 'Ghita', 'ghita.elhachmi@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210013, 'ZIANE', 'Omar', 'omar.ziane@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210014, 'BENABID', 'Sana', 'sana.benabid@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210015, 'EL KHALKI', 'Yacine', 'yacine.elkhalki@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210016, 'BAHLOUL', 'Nadia', 'nadia.bahloul@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210017, 'EL JAZOULI', 'Karim', 'karim.eljazouli@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210018, 'BENHADDOU', 'Latifa', 'latifa.benhaddou@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210019, 'CHARKAOUI', 'Hicham', 'hicham.charkaoui@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210020, 'EL BAKKALI', 'Fatima', 'fatima.elbakkali@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210021, 'BENNACER', 'Fouad', 'fouad.bennacer@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210022, 'EL HARIM', 'Siham', 'siham.elharim@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210023, 'ZAIRI', 'Khalid', 'khalid.zairi@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210024, 'BENHAMOU', 'Mouna', 'mouna.benhamou@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210025, 'EL MESSAOUDI', 'Abdellah', 'abdellah.elmessaoudi@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210026, 'BOUSSAID', 'Hajar', 'hajar.boussaid@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210027, 'EL HACHMI', 'Said', 'said.elhachmi@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210028, 'ZIANE', 'Wiam', 'wiam.ziane@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210029, 'BENABID', 'Abdel', 'abdel.benabid@etudiant.ma', MD5('etudiant123'), '5eme annee'),
(20210030, 'EL KHALKI', 'Lamia', 'lamia.elkhalki@etudiant.ma', MD5('etudiant123'), '5eme annee');


update modules 
set intitule = 'Electronique Analogie Num'
where code_module = 'ELEC201' ;


SELECT * FROM Modules ;