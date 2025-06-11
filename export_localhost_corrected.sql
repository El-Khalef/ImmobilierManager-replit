-- Export PostgreSQL corrigé pour localhost
-- Généré le 2025-06-11 avec format de dates compatible
-- Résout les erreurs de syntaxe des timestamps

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

-- Supprimer les tables existantes
DROP TABLE IF EXISTS depenses_immobilieres CASCADE;
DROP TABLE IF EXISTS budgets_previsionnels CASCADE;
DROP TABLE IF EXISTS ecritures_comptables CASCADE;
DROP TABLE IF EXISTS comptes_comptables CASCADE;
DROP TABLE IF EXISTS releves_compteurs CASCADE;
DROP TABLE IF EXISTS documents_contrat CASCADE;
DROP TABLE IF EXISTS photos_biens CASCADE;
DROP TABLE IF EXISTS paiements_loyer CASCADE;
DROP TABLE IF EXISTS contrats_location CASCADE;
DROP TABLE IF EXISTS biens_immobiliers CASCADE;
DROP TABLE IF EXISTS clients CASCADE;

-- Table clients
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    telephone VARCHAR(20),
    adresse VARCHAR(200),
    ville VARCHAR(100),
    code_postal VARCHAR(10),
    type_client VARCHAR(20) NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    type_piece_identite VARCHAR(50) NOT NULL,
    numero_piece_identite VARCHAR(50) NOT NULL
);

-- Données clients
INSERT INTO clients (id, nom, prenom, email, telephone, adresse, ville, code_postal, type_client, date_creation, type_piece_identite, numero_piece_identite) VALUES 
(1, 'EL KHALEF', 'Propriétaire', 'elkhafef@email.com', '36306854', '', 'Nouakchott', '', 'proprietaire', NULL, 'carte_identite', '7716097122'),
(2, 'OULD AHMED', 'Mohamed Lemine', 'Ahmed_Ould_Ahmed@gmail.com', '22817045', '365 F-Nord Tevragh Zeina', 'Nouakchott', '', 'locataire', '2025-05-25 08:51:21', 'carte_identite', '8960704607'),
(3, 'ZEIDANE', 'Aweicha', 'aweicha@gmail.com', '49602030', '365 F-Nord Tevragh Zeina', 'Nouakchott', '', 'locataire', '2025-05-25 11:29:53', 'carte_identite', '7493636352'),
(4, 'AL-DAOUS', 'Yahya Mohamed Rajeh', 'aldaous@gmail.com', '967733004315', '365 F-Nord Tevragh Zeina', 'Nouakchott', '', 'locataire', '2025-05-25 11:51:20', 'passeport', '00039505'),
(5, 'ABD EL VETTAH', 'Sidi Mohamed', 'abdelvettah@gmail.com', '31366050', '', 'Nouakchott', '', 'locataire', '2025-06-01 05:36:32', 'carte_identite', '1417715238');

-- Table biens_immobiliers
CREATE TABLE biens_immobiliers (
    id SERIAL PRIMARY KEY,
    titre VARCHAR(200) NOT NULL,
    type_bien VARCHAR(50) NOT NULL,
    adresse VARCHAR(200) NOT NULL,
    ville VARCHAR(100) NOT NULL,
    code_postal VARCHAR(10) NOT NULL,
    surface DOUBLE PRECISION NOT NULL,
    nombre_pieces INTEGER,
    nombre_chambres INTEGER,
    prix_achat DOUBLE PRECISION,
    prix_location_mensuel DOUBLE PRECISION,
    charges_mensuelles DOUBLE PRECISION DEFAULT 0,
    description TEXT,
    meuble BOOLEAN DEFAULT FALSE,
    balcon BOOLEAN DEFAULT FALSE,
    parking BOOLEAN DEFAULT FALSE,
    ascenseur BOOLEAN DEFAULT FALSE,
    etage INTEGER,
    annee_construction INTEGER,
    disponible BOOLEAN DEFAULT TRUE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    proprietaire_id INTEGER NOT NULL REFERENCES clients(id),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);

-- Données biens_immobiliers
INSERT INTO biens_immobiliers (id, titre, type_bien, adresse, ville, code_postal, surface, nombre_pieces, nombre_chambres, prix_achat, prix_location_mensuel, charges_mensuelles, description, meuble, balcon, parking, ascenseur, etage, annee_construction, disponible, date_creation, proprietaire_id, latitude, longitude) VALUES 
(1, 'C', 'appartement', '365 F-Nord Tevragh Zeina', 'Nouakchott', '', 108.0, 3, 2, NULL, 8000.0, 0.0, 'Appartement au rez-de-chaussée à droite de la rentrée avec 3 pièces dont 2 chambres, 2 toilettes et un séjour', FALSE, FALSE, FALSE, FALSE, 0, 2006, FALSE, '2025-05-25 04:31:16', 1, 18.109639, -15.970278),
(2, 'B', 'appartement', '365 F-Nord Tevragh Zeina', 'Nouakchott', '', 108.0, 3, 2, NULL, 9000.0, 0.0, 'Appartement au premier étage à gauche de la rentrée avec 3 pièces dont 2 chambres, 2 toilettes et un séjour', FALSE, FALSE, FALSE, FALSE, 1, 2006, FALSE, '2025-05-25 04:35:17', 1, 18.109639, -15.970278),
(3, 'D', 'appartement', '365 F-Nord Tevragh Zeina', 'Nouakchott', '', 108.0, 3, 2, NULL, 9000.0, 0.0, 'Appartement au premier étage à droite de la rentrée avec 3 pièces dont 2 chambres, 2 toilettes et un séjour et un parking à droite de l''entrée.', FALSE, FALSE, TRUE, FALSE, 1, 2006, FALSE, '2025-05-25 04:38:33', 1, 18.109639, -15.970278),
(4, 'Magasin-A', 'local', 'F-Nord sur Est Tavragh Zeina', 'Nouakchott', '', 144.0, 1, 1, NULL, 35000.0, 0.0, 'Localisation du Grand Magasin', FALSE, FALSE, FALSE, FALSE, NULL, 2012, TRUE, '2025-05-25 08:35:14', 1, 18.108472, -15.965972),
(5, 'Magasin-B', 'local', 'F-Nord sur Est Tavragh Zeina', 'Nouakchott', '', 48.0, 1, 1, NULL, 15000.0, 0.0, 'Grand magasin situé dans un emplacement stratégique.', FALSE, FALSE, FALSE, FALSE, 0, 2023, TRUE, '2025-05-25 08:38:29', 1, 18.108472, -15.965972),
(6, 'Magasin-C', 'local', 'F-Nord sur Est Tavragh Zeina', 'Nouakchott', '', 48.0, 1, 1, NULL, 15000.0, 0.0, 'Grand magasin situé dans un emplacement stratégique.', FALSE, FALSE, FALSE, FALSE, 0, 2023, TRUE, '2025-05-25 08:40:34', 1, 18.108472, -15.965972),
(7, 'Magasin-D', 'bureau', 'F-Nord sur Est Tavragh Zeina', 'Nouakchott', '', 24.0, 1, 1, NULL, 5000.0, 0.0, 'Bureau situé dans un emplacement stratégique.', FALSE, FALSE, FALSE, FALSE, 0, 2023, TRUE, '2025-05-25 08:44:34', 1, 18.108472, -15.965972);

-- Table contrats_location
CREATE TABLE contrats_location (
    id SERIAL PRIMARY KEY,
    bien_id INTEGER NOT NULL REFERENCES biens_immobiliers(id),
    locataire_id INTEGER NOT NULL REFERENCES clients(id),
    date_debut DATE NOT NULL,
    date_fin DATE,
    loyer_mensuel DOUBLE PRECISION NOT NULL,
    charges_mensuelles DOUBLE PRECISION DEFAULT 0,
    depot_garantie DOUBLE PRECISION DEFAULT 0,
    frais_agence DOUBLE PRECISION DEFAULT 0,
    statut VARCHAR(20) DEFAULT 'actif',
    conditions_particulieres TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    somelec_numero_compteur VARCHAR(50),
    somelec_code_abonnement VARCHAR(50),
    somelec_index_initial DOUBLE PRECISION DEFAULT 0,
    somelec_date_branchement DATE,
    somelec_quitus_precedent BOOLEAN DEFAULT FALSE,
    snde_numero_compteur VARCHAR(50),
    snde_code_abonnement VARCHAR(50),
    snde_index_initial DOUBLE PRECISION DEFAULT 0,
    snde_date_branchement DATE,
    snde_quitus_precedent BOOLEAN DEFAULT FALSE
);

-- Données contrats_location
INSERT INTO contrats_location (id, bien_id, locataire_id, date_debut, date_fin, loyer_mensuel, charges_mensuelles, depot_garantie, frais_agence, statut, conditions_particulieres, date_creation, somelec_numero_compteur, somelec_code_abonnement, somelec_index_initial, somelec_date_branchement, somelec_quitus_precedent, snde_numero_compteur, snde_code_abonnement, snde_index_initial, snde_date_branchement, snde_quitus_precedent) VALUES 
(1, 1, 3, '2025-05-25', NULL, 8000.0, 0.0, 16000.0, 800.0, 'actif', NULL, '2025-05-25 11:29:53', NULL, NULL, 0, NULL, FALSE, NULL, NULL, 0, NULL, FALSE),
(2, 2, 2, '2025-05-25', NULL, 9000.0, 0.0, 18000.0, 900.0, 'actif', NULL, '2025-05-25 08:51:21', NULL, NULL, 0, NULL, FALSE, NULL, NULL, 0, NULL, FALSE),
(3, 3, 4, '2025-05-25', NULL, 9000.0, 0.0, 18000.0, 900.0, 'actif', NULL, '2025-05-25 11:51:20', NULL, NULL, 0, NULL, FALSE, NULL, NULL, 0, NULL, FALSE),
(4, 7, 5, '2025-06-01', NULL, 5000.0, 0.0, 10000.0, 500.0, 'actif', NULL, '2025-06-01 05:36:32', NULL, NULL, 0, NULL, FALSE, NULL, NULL, 0, NULL, FALSE);

-- Table paiements_loyer
CREATE TABLE paiements_loyer (
    id SERIAL PRIMARY KEY,
    contrat_id INTEGER NOT NULL REFERENCES contrats_location(id),
    mois INTEGER NOT NULL,
    annee INTEGER NOT NULL,
    montant_loyer DOUBLE PRECISION NOT NULL,
    montant_charges DOUBLE PRECISION DEFAULT 0,
    date_paiement DATE,
    date_echeance DATE NOT NULL,
    statut VARCHAR(20) DEFAULT 'en_attente',
    mode_paiement VARCHAR(20),
    reference_paiement VARCHAR(100),
    remarques TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table photos_biens
CREATE TABLE photos_biens (
    id SERIAL PRIMARY KEY,
    bien_id INTEGER NOT NULL REFERENCES biens_immobiliers(id),
    nom_fichier VARCHAR(255) NOT NULL,
    chemin_fichier VARCHAR(500) NOT NULL,
    principale BOOLEAN DEFAULT FALSE,
    date_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table documents_contrat
CREATE TABLE documents_contrat (
    id SERIAL PRIMARY KEY,
    contrat_id INTEGER NOT NULL REFERENCES contrats_location(id),
    type_document VARCHAR(50) NOT NULL,
    nom_fichier VARCHAR(255) NOT NULL,
    chemin_fichier VARCHAR(500) NOT NULL,
    description TEXT,
    date_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table releves_compteurs
CREATE TABLE releves_compteurs (
    id SERIAL PRIMARY KEY,
    contrat_id INTEGER NOT NULL REFERENCES contrats_location(id),
    type_compteur VARCHAR(20) NOT NULL,
    numero_compteur VARCHAR(50) NOT NULL,
    code_abonnement VARCHAR(50),
    date_releve DATE NOT NULL,
    index_precedent DOUBLE PRECISION DEFAULT 0,
    index_actuel DOUBLE PRECISION NOT NULL,
    consommation DOUBLE PRECISION,
    montant_facture DOUBLE PRECISION,
    statut_paiement VARCHAR(20) DEFAULT 'en_attente',
    remarques TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table comptes_comptables
CREATE TABLE comptes_comptables (
    id SERIAL PRIMARY KEY,
    numero_compte VARCHAR(10) NOT NULL UNIQUE,
    nom_compte VARCHAR(200) NOT NULL,
    type_compte VARCHAR(20) NOT NULL,
    description TEXT,
    actif BOOLEAN DEFAULT TRUE
);

-- Données comptes_comptables
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, description, actif) VALUES 
('101', 'Capital', 'capitaux', 'Capital social', TRUE),
('120', 'Résultat de l''exercice', 'capitaux', 'Bénéfice ou perte de l''exercice', TRUE),
('164', 'Emprunts auprès des établissements de crédit', 'dettes', 'Dettes bancaires', TRUE),
('2013', 'Constructions', 'immobilisations', 'Bâtiments et constructions', TRUE),
('2018', 'Autres immobilisations corporelles', 'immobilisations', 'Autres biens corporels', TRUE),
('401', 'Fournisseurs', 'dettes', 'Dettes envers les fournisseurs', TRUE),
('411', 'Clients', 'creances', 'Créances sur les clients', TRUE),
('421', 'Personnel - rémunérations dues', 'dettes', 'Salaires à payer', TRUE),
('4456', 'TVA déductible', 'creances', 'TVA récupérable', TRUE),
('4457', 'TVA collectée', 'dettes', 'TVA à reverser', TRUE),
('512', 'Banque', 'tresorerie', 'Comptes bancaires', TRUE),
('53', 'Caisse', 'tresorerie', 'Espèces en caisse', TRUE),
('601', 'Achats de matières premières', 'charges', 'Achats de matières', TRUE),
('6063', 'Fournitures d''entretien', 'charges', 'Produits d''entretien', TRUE),
('613', 'Locations', 'charges', 'Loyers payés', TRUE),
('6226', 'Honoraires', 'charges', 'Frais de conseil', TRUE),
('625', 'Déplacements, missions', 'charges', 'Frais de déplacement', TRUE),
('641', 'Rémunérations du personnel', 'charges', 'Salaires', TRUE),
('658', 'Charges diverses de gestion courante', 'charges', 'Autres charges', TRUE),
('7013', 'Locations', 'produits', 'Revenus locatifs', TRUE),
('7088', 'Autres produits d''activités annexes', 'produits', 'Autres revenus', TRUE);

-- Table ecritures_comptables
CREATE TABLE ecritures_comptables (
    id SERIAL PRIMARY KEY,
    date_ecriture DATE NOT NULL,
    numero_piece VARCHAR(50),
    libelle VARCHAR(200) NOT NULL,
    compte_debit_id INTEGER NOT NULL REFERENCES comptes_comptables(id),
    compte_credit_id INTEGER NOT NULL REFERENCES comptes_comptables(id),
    montant DOUBLE PRECISION NOT NULL,
    description TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table budgets_previsionnels
CREATE TABLE budgets_previsionnels (
    id SERIAL PRIMARY KEY,
    annee INTEGER NOT NULL,
    mois INTEGER NOT NULL,
    compte_id INTEGER NOT NULL REFERENCES comptes_comptables(id),
    montant_prevu DOUBLE PRECISION NOT NULL,
    montant_realise DOUBLE PRECISION DEFAULT 0,
    description TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table depenses_immobilieres
CREATE TABLE depenses_immobilieres (
    id SERIAL PRIMARY KEY,
    bien_id INTEGER NOT NULL REFERENCES biens_immobiliers(id),
    type_depense VARCHAR(50) NOT NULL,
    montant DOUBLE PRECISION NOT NULL,
    date_depense DATE NOT NULL,
    description TEXT,
    fournisseur VARCHAR(200),
    numero_facture VARCHAR(100),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mise à jour des séquences
SELECT setval(pg_get_serial_sequence('clients', 'id'), (SELECT MAX(id) FROM clients), true);
SELECT setval(pg_get_serial_sequence('biens_immobiliers', 'id'), (SELECT MAX(id) FROM biens_immobiliers), true);
SELECT setval(pg_get_serial_sequence('contrats_location', 'id'), (SELECT MAX(id) FROM contrats_location), true);
SELECT setval(pg_get_serial_sequence('comptes_comptables', 'id'), (SELECT MAX(id) FROM comptes_comptables), true);

-- Export terminé avec succès