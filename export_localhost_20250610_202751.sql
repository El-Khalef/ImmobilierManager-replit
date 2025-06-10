-- Export pour localhost PostgreSQL
-- Généré le 2025-06-10 20:27:51
-- 
-- Instructions d'importation :
-- 1. Créer la base : CREATE DATABASE immobilier_mauritanie;
-- 2. Importer : psql -U postgres -d immobilier_mauritanie -f export_localhost_20250610_202751.sql
-- 

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

CREATE SCHEMA IF NOT EXISTS public;
SET search_path = public, pg_catalog;

-- Table: clients
DROP TABLE IF EXISTS clients CASCADE;
CREATE TABLE clients (
    id INTEGER NOT NULL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    telephone VARCHAR(20),
    adresse VARCHAR(200),
    ville VARCHAR(100),
    code_postal VARCHAR(10),
    type_client VARCHAR(20) NOT NULL,
    date_creation TIMESTAMP,
    type_piece_identite VARCHAR(20),
    numero_piece_identite VARCHAR(50)
);

-- Données pour clients
INSERT INTO clients (id, nom, prenom, email, telephone, adresse, ville, code_postal, type_client, date_creation, type_piece_identite, numero_piece_identite) VALUES (3, 'ZEIDANE', 'Aweicha', 'aweicha@gmail.com', '49602030', '365 F-Nord Tevragh Zeina', 'Nouakchott', '', 'locataire', 2025-05-25 11:29:53.277346, 'carte_identite', '7493636352');
INSERT INTO clients (id, nom, prenom, email, telephone, adresse, ville, code_postal, type_client, date_creation, type_piece_identite, numero_piece_identite) VALUES (2, 'OULD AHMED', 'Mohamed Lemine', 'Ahmed_Ould_Ahmed@gmail.com', '22817045', '365 F-Nord Tevragh Zeina', 'Nouakchott', '', 'locataire', 2025-05-25 08:51:21.405906, 'carte_identite', '8960704607');
INSERT INTO clients (id, nom, prenom, email, telephone, adresse, ville, code_postal, type_client, date_creation, type_piece_identite, numero_piece_identite) VALUES (4, 'AL-DAOUS', 'Yahya Mohamed Rajeh', 'aldaous@gmail.com', '967733004315', '365 F-Nord Tevragh Zeina', 'Nouakchott', '', 'locataire', 2025-05-25 11:51:20.860315, 'passeport', '00039505');
INSERT INTO clients (id, nom, prenom, email, telephone, adresse, ville, code_postal, type_client, date_creation, type_piece_identite, numero_piece_identite) VALUES (5, 'ABD EL VETTAH', 'Sidi Mohamed', 'abdelvettah@gmail.com', '31366050', '', 'Nouakchott', '', 'locataire', 2025-06-01 05:36:32.971875, 'carte_identite', '1417715238');
INSERT INTO clients (id, nom, prenom, email, telephone, adresse, ville, code_postal, type_client, date_creation, type_piece_identite, numero_piece_identite) VALUES (1, 'EL KHALEF', 'Propriétaire', 'elkhafef@email.com', '36306854', '', 'Nouakchott', '', 'proprietaire', NULL, 'carte_identite', '7716097122');

-- Table: biens_immobiliers
DROP TABLE IF EXISTS biens_immobiliers CASCADE;
CREATE TABLE biens_immobiliers (
    id INTEGER NOT NULL PRIMARY KEY,
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
    charges_mensuelles DOUBLE PRECISION,
    description TEXT,
    meuble BOOLEAN,
    balcon BOOLEAN,
    parking BOOLEAN,
    ascenseur BOOLEAN,
    etage INTEGER,
    annee_construction INTEGER,
    disponible BOOLEAN,
    date_creation TIMESTAMP,
    proprietaire_id INTEGER NOT NULL,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    somelec_numero_compteur VARCHAR(50),
    somelec_code_abonnement VARCHAR(50),
    somelec_index_actuel DOUBLE PRECISION,
    somelec_date_releve DATE,
    snde_numero_compteur VARCHAR(50),
    snde_code_abonnement VARCHAR(50),
    snde_index_actuel DOUBLE PRECISION,
    snde_date_releve DATE
);

-- Données pour biens_immobiliers
INSERT INTO biens_immobiliers (id, titre, type_bien, adresse, ville, code_postal, surface, nombre_pieces, nombre_chambres, prix_achat, prix_location_mensuel, charges_mensuelles, description, meuble, balcon, parking, ascenseur, etage, annee_construction, disponible, date_creation, proprietaire_id, latitude, longitude, somelec_numero_compteur, somelec_code_abonnement, somelec_index_actuel, somelec_date_releve, snde_numero_compteur, snde_code_abonnement, snde_index_actuel, snde_date_releve) VALUES (4, 'Magasin-A', 'local', 'F-Nord sur Est Tavragh Zeina', 'Nouakchott', '', 144.0, 1, 1, NULL, 35000.0, 0.0, 'Localisation du Grand Magasin
1.	Type de localisation :
Le grand magasin est situé dans un emplacement stratégique.
2.	Détails de l''emplacement :
o	Il est situé sur une grande avenue, assurant une visibilité maximale et un flux constant de passants.
o	Il se trouve également à un angle, ce qui offre une double exposition et un accès facile depuis deux rues différentes.
3.	Avantages de l''emplacement :
o	Idéal pour attirer des clients grâce à sa visibilité accrue.
o	Possibilité d''aménager deux vitrines ou plus, augmentant les opportunités publicitaires et de présentation des produits.
', FALSE, FALSE, FALSE, FALSE, NULL, 2012, TRUE, 2025-05-25 08:35:14.790967, 1, 18.108472, -15.965972, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO biens_immobiliers (id, titre, type_bien, adresse, ville, code_postal, surface, nombre_pieces, nombre_chambres, prix_achat, prix_location_mensuel, charges_mensuelles, description, meuble, balcon, parking, ascenseur, etage, annee_construction, disponible, date_creation, proprietaire_id, latitude, longitude, somelec_numero_compteur, somelec_code_abonnement, somelec_index_actuel, somelec_date_releve, snde_numero_compteur, snde_code_abonnement, snde_index_actuel, snde_date_releve) VALUES (5, 'Magasin-B', 'local', 'F-Nord sur Est Tavragh Zeina', 'Nouakchott', '', 48.0, 1, 1, NULL, 15000.0, 0.0, '1.	Type de localisation :
Le grand magasin est situé dans un emplacement stratégique.
2.	Détails de l''emplacement :
o	Il est situé sur une grande avenue, assurant une visibilité maximale et un flux constant de passants.
3.	Avantages de l''emplacement :
o	Idéal pour attirer des clients grâce à sa visibilité accrue.
o	Possibilité d''aménager deux vitrines ou plus, augmentant les opportunités publicitaires et de présentation des produits.', FALSE, FALSE, FALSE, FALSE, 0, 2023, TRUE, 2025-05-25 08:38:29.821901, 1, 18.108472, -15.965972, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO biens_immobiliers (id, titre, type_bien, adresse, ville, code_postal, surface, nombre_pieces, nombre_chambres, prix_achat, prix_location_mensuel, charges_mensuelles, description, meuble, balcon, parking, ascenseur, etage, annee_construction, disponible, date_creation, proprietaire_id, latitude, longitude, somelec_numero_compteur, somelec_code_abonnement, somelec_index_actuel, somelec_date_releve, snde_numero_compteur, snde_code_abonnement, snde_index_actuel, snde_date_releve) VALUES (6, 'Magasin-C', 'local', 'F-Nord sur Est Tavragh Zeina', 'Nouakchott', '', 48.0, 1, 1, NULL, 15000.0, 0.0, '1.	Type de localisation :
Le grand magasin est situé dans un emplacement stratégique.
2.	Détails de l''emplacement :
o	Il est situé sur une grande avenue, assurant une visibilité maximale et un flux constant de passants.
3.	Avantages de l''emplacement :
o	Idéal pour attirer des clients grâce à sa visibilité accrue.
o	Possibilité d''aménager deux vitrines ou plus, augmentant les opportunités publicitaires et de présentation des produits.', FALSE, FALSE, FALSE, FALSE, 0, 2023, TRUE, 2025-05-25 08:40:34.788341, 1, 18.108472, -15.965972, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO biens_immobiliers (id, titre, type_bien, adresse, ville, code_postal, surface, nombre_pieces, nombre_chambres, prix_achat, prix_location_mensuel, charges_mensuelles, description, meuble, balcon, parking, ascenseur, etage, annee_construction, disponible, date_creation, proprietaire_id, latitude, longitude, somelec_numero_compteur, somelec_code_abonnement, somelec_index_actuel, somelec_date_releve, snde_numero_compteur, snde_code_abonnement, snde_index_actuel, snde_date_releve) VALUES (7, 'Magasin-D', 'bureau', 'F-Nord sur Est Tavragh Zeina', 'Nouakchott', '', 24.0, 1, 1, NULL, 5000.0, 0.0, 'Bureau est situé dans un emplacement stratégique.
	Avantages de l''emplacement :
	Idéal pour attirer des clients grâce à sa visibilité accrue.
', FALSE, FALSE, FALSE, FALSE, 0, 2023, TRUE, 2025-05-25 08:44:34.751639, 1, 18.108472, -15.965972, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO biens_immobiliers (id, titre, type_bien, adresse, ville, code_postal, surface, nombre_pieces, nombre_chambres, prix_achat, prix_location_mensuel, charges_mensuelles, description, meuble, balcon, parking, ascenseur, etage, annee_construction, disponible, date_creation, proprietaire_id, latitude, longitude, somelec_numero_compteur, somelec_code_abonnement, somelec_index_actuel, somelec_date_releve, snde_numero_compteur, snde_code_abonnement, snde_index_actuel, snde_date_releve) VALUES (1, 'C', 'appartement', '365 F-Nord Tevragh Zeina', 'Nouakchott', '', 108.0, 3, 2, NULL, 8000.0, 0.0, 'Appartement au rez-de-chaussée à droite de la rentrée avec 3 pièces dont 2 chambres, 2 toilettes et un séjour', FALSE, FALSE, FALSE, FALSE, 0, 2006, FALSE, 2025-05-25 04:31:16.918143, 1, 18.109639, -15.970278, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO biens_immobiliers (id, titre, type_bien, adresse, ville, code_postal, surface, nombre_pieces, nombre_chambres, prix_achat, prix_location_mensuel, charges_mensuelles, description, meuble, balcon, parking, ascenseur, etage, annee_construction, disponible, date_creation, proprietaire_id, latitude, longitude, somelec_numero_compteur, somelec_code_abonnement, somelec_index_actuel, somelec_date_releve, snde_numero_compteur, snde_code_abonnement, snde_index_actuel, snde_date_releve) VALUES (2, 'B', 'appartement', '365 F-Nord Tevragh Zeina', 'Nouakchott', '', 108.0, 3, 2, NULL, 9000.0, 0.0, 'Appartement au premier étage à gauche de la rentrée avec 3 pièces dont 2 chambres, 2 toilettes et un séjour', FALSE, FALSE, FALSE, FALSE, 1, 2006, FALSE, 2025-05-25 04:35:17.817167, 1, 18.109639, -15.970278, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO biens_immobiliers (id, titre, type_bien, adresse, ville, code_postal, surface, nombre_pieces, nombre_chambres, prix_achat, prix_location_mensuel, charges_mensuelles, description, meuble, balcon, parking, ascenseur, etage, annee_construction, disponible, date_creation, proprietaire_id, latitude, longitude, somelec_numero_compteur, somelec_code_abonnement, somelec_index_actuel, somelec_date_releve, snde_numero_compteur, snde_code_abonnement, snde_index_actuel, snde_date_releve) VALUES (3, 'D', 'appartement', '365 F-Nord Tevragh Zeina', 'Nouakchott', '', 108.0, 3, 2, NULL, 9000.0, 0.0, 'Appartement au premier étage à droite de la rentrée avec 3 pièces dont 2 chambres, 2 toilettes et un séjour et un parking à droite de l''entrée.', FALSE, FALSE, TRUE, FALSE, 1, 2006, FALSE, 2025-05-25 04:38:33.442116, 1, 18.109639, -15.970278, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- Table: contrats_location
DROP TABLE IF EXISTS contrats_location CASCADE;
CREATE TABLE contrats_location (
    id INTEGER NOT NULL PRIMARY KEY,
    date_debut DATE NOT NULL,
    date_fin DATE,
    loyer_mensuel DOUBLE PRECISION NOT NULL,
    charges_mensuelles DOUBLE PRECISION,
    depot_garantie DOUBLE PRECISION,
    frais_agence DOUBLE PRECISION,
    statut VARCHAR(20),
    conditions_particulieres TEXT,
    date_creation TIMESTAMP,
    bien_id INTEGER NOT NULL,
    locataire_id INTEGER NOT NULL,
    somelec_numero_compteur VARCHAR(50),
    somelec_code_abonnement VARCHAR(50),
    somelec_index_initial DOUBLE PRECISION DEFAULT 0,
    somelec_date_branchement DATE,
    somelec_quitus_precedent BOOLEAN DEFAULT false,
    snde_numero_compteur VARCHAR(50),
    snde_code_abonnement VARCHAR(50),
    snde_index_initial DOUBLE PRECISION DEFAULT 0,
    snde_date_branchement DATE,
    snde_quitus_precedent BOOLEAN DEFAULT false
);

-- Données pour contrats_location
INSERT INTO contrats_location (id, date_debut, date_fin, loyer_mensuel, charges_mensuelles, depot_garantie, frais_agence, statut, conditions_particulieres, date_creation, bien_id, locataire_id, somelec_numero_compteur, somelec_code_abonnement, somelec_index_initial, somelec_date_branchement, somelec_quitus_precedent, snde_numero_compteur, snde_code_abonnement, snde_index_initial, snde_date_branchement, snde_quitus_precedent) VALUES (1, 2021-10-26, NULL, 8000.0, 0.0, 8000.0, 0.0, 'actif', 'Le numéro de téléphone est celui de sa femme Mariem', 2025-05-25 10:23:55.890435, 1, 2, NULL, NULL, 0.0, NULL, FALSE, NULL, NULL, 0.0, NULL, FALSE);
INSERT INTO contrats_location (id, date_debut, date_fin, loyer_mensuel, charges_mensuelles, depot_garantie, frais_agence, statut, conditions_particulieres, date_creation, bien_id, locataire_id, somelec_numero_compteur, somelec_code_abonnement, somelec_index_initial, somelec_date_branchement, somelec_quitus_precedent, snde_numero_compteur, snde_code_abonnement, snde_index_initial, snde_date_branchement, snde_quitus_precedent) VALUES (2, 2024-05-28, NULL, 9000.0, 0.0, 9000.0, 0.0, 'actif', 'Pas de contrat SOMELEC', 2025-05-25 11:36:38.729002, 2, 3, NULL, NULL, 0.0, NULL, FALSE, NULL, NULL, 0.0, NULL, FALSE);
INSERT INTO contrats_location (id, date_debut, date_fin, loyer_mensuel, charges_mensuelles, depot_garantie, frais_agence, statut, conditions_particulieres, date_creation, bien_id, locataire_id, somelec_numero_compteur, somelec_code_abonnement, somelec_index_initial, somelec_date_branchement, somelec_quitus_precedent, snde_numero_compteur, snde_code_abonnement, snde_index_initial, snde_date_branchement, snde_quitus_precedent) VALUES (4, 2021-11-09, NULL, 9000.0, 0.0, 0.0, NULL, 'actif', NULL, 2025-05-25 13:29:40.521468, 3, 4, NULL, NULL, 0.0, NULL, FALSE, NULL, NULL, 0.0, NULL, FALSE);
INSERT INTO contrats_location (id, date_debut, date_fin, loyer_mensuel, charges_mensuelles, depot_garantie, frais_agence, statut, conditions_particulieres, date_creation, bien_id, locataire_id, somelec_numero_compteur, somelec_code_abonnement, somelec_index_initial, somelec_date_branchement, somelec_quitus_precedent, snde_numero_compteur, snde_code_abonnement, snde_index_initial, snde_date_branchement, snde_quitus_precedent) VALUES (6, 2022-10-23, NULL, 35000.0, 0.0, 0.0, 0.0, 'actif', '', 2025-06-01 05:49:11.168429, 4, 5, NULL, NULL, 0.0, NULL, FALSE, NULL, NULL, 0.0, NULL, FALSE);

-- Table: paiements_loyer
DROP TABLE IF EXISTS paiements_loyer CASCADE;
CREATE TABLE paiements_loyer (
    id INTEGER NOT NULL PRIMARY KEY,
    mois INTEGER NOT NULL,
    annee INTEGER NOT NULL,
    montant_loyer DOUBLE PRECISION NOT NULL,
    montant_charges DOUBLE PRECISION,
    date_paiement DATE,
    date_echeance DATE NOT NULL,
    statut VARCHAR(20),
    mode_paiement VARCHAR(50),
    reference_paiement VARCHAR(100),
    remarques TEXT,
    date_creation TIMESTAMP,
    contrat_id INTEGER NOT NULL
);

-- Données pour paiements_loyer
INSERT INTO paiements_loyer (id, mois, annee, montant_loyer, montant_charges, date_paiement, date_echeance, statut, mode_paiement, reference_paiement, remarques, date_creation, contrat_id) VALUES (1, 5, 2025, 8000.0, 0.0, 2025-05-01, 2025-05-01, 'paye', 'virement', 'Bankiliy', '', 2025-05-25 12:57:46.112074, 1);
INSERT INTO paiements_loyer (id, mois, annee, montant_loyer, montant_charges, date_paiement, date_echeance, statut, mode_paiement, reference_paiement, remarques, date_creation, contrat_id) VALUES (2, 5, 2025, 9000.0, 0.0, 2025-05-08, 2025-05-01, 'paye', 'virement', 'Bankiliy', '', 2025-05-25 12:58:47.387120, 2);
INSERT INTO paiements_loyer (id, mois, annee, montant_loyer, montant_charges, date_paiement, date_echeance, statut, mode_paiement, reference_paiement, remarques, date_creation, contrat_id) VALUES (4, 5, 2025, 35000.0, 0.0, 2025-05-10, 2025-05-01, 'paye', 'virement', 'Bankiliy', '', 2025-06-01 05:51:36.833005, 6);
INSERT INTO paiements_loyer (id, mois, annee, montant_loyer, montant_charges, date_paiement, date_echeance, statut, mode_paiement, reference_paiement, remarques, date_creation, contrat_id) VALUES (5, 6, 2025, 8000.0, 0.0, 2025-06-02, 2025-06-01, 'paye', 'virement', 'Bankiliy', '', 2025-06-04 18:43:54.089591, 1);
INSERT INTO paiements_loyer (id, mois, annee, montant_loyer, montant_charges, date_paiement, date_echeance, statut, mode_paiement, reference_paiement, remarques, date_creation, contrat_id) VALUES (3, 5, 2025, 18000.0, 0.0, 2025-05-15, 2025-05-01, 'paye', 'virement', 'Bankiliy', 'Paiement des mois de mai et juin 2025.', 2025-05-25 14:04:48.025995, 4);
INSERT INTO paiements_loyer (id, mois, annee, montant_loyer, montant_charges, date_paiement, date_echeance, statut, mode_paiement, reference_paiement, remarques, date_creation, contrat_id) VALUES (6, 6, 2025, 35000.0, 0.0, 2025-06-08, 2025-06-01, 'paye', 'virement', 'Bankiliy', '', 2025-06-08 21:38:33.772597, 6);

-- Table: photos_biens
DROP TABLE IF EXISTS photos_biens CASCADE;
CREATE TABLE photos_biens (
    id INTEGER NOT NULL PRIMARY KEY,
    nom_fichier VARCHAR(255) NOT NULL,
    nom_original VARCHAR(255),
    principale BOOLEAN,
    date_ajout TIMESTAMP,
    bien_id INTEGER NOT NULL
);

-- Table: documents_contrat
DROP TABLE IF EXISTS documents_contrat CASCADE;
CREATE TABLE documents_contrat (
    id INTEGER NOT NULL PRIMARY KEY,
    contrat_id INTEGER NOT NULL,
    nom_fichier VARCHAR(255) NOT NULL,
    nom_original VARCHAR(255) NOT NULL,
    type_document VARCHAR(50) NOT NULL,
    format_fichier VARCHAR(10) NOT NULL,
    taille_fichier INTEGER NOT NULL,
    chemin_stockage VARCHAR(500) NOT NULL,
    description TEXT,
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ajoute_par VARCHAR(100)
);

-- Données pour documents_contrat
INSERT INTO documents_contrat (id, contrat_id, nom_fichier, nom_original, type_document, format_fichier, taille_fichier, chemin_stockage, description, date_ajout, ajoute_par) VALUES (1, 1, '1e849430409549768b694ebf5fe91d41.pdf', 'Contrat_Location_Appartements_Mohamed_Lemine.pdf', 'piece_identite', 'pdf', 115430, 'static/documents/1e849430409549768b694ebf5fe91d41.pdf', 'Contrat de location', 2025-05-25 11:04:53.662704, 'Admin');
INSERT INTO documents_contrat (id, contrat_id, nom_fichier, nom_original, type_document, format_fichier, taille_fichier, chemin_stockage, description, date_ajout, ajoute_par) VALUES (2, 1, '56c6d32e71da4bf690fd2bd702f487d9.jpeg', 'Mohamed_Lemine_cni_recto.jpeg', 'piece_identite', 'jpeg', 64757, 'static/documents/56c6d32e71da4bf690fd2bd702f487d9.jpeg', 'CNI recto', 2025-05-25 11:18:50.753905, 'Admin');
INSERT INTO documents_contrat (id, contrat_id, nom_fichier, nom_original, type_document, format_fichier, taille_fichier, chemin_stockage, description, date_ajout, ajoute_par) VALUES (3, 1, 'e1e1d98d74a44326be55e7cc190ba059.jpeg', 'Mohamed_Lemine_cni_verso.jpeg', 'piece_identite', 'jpeg', 60428, 'static/documents/e1e1d98d74a44326be55e7cc190ba059.jpeg', 'CNI Verso', 2025-05-25 11:19:18.951320, 'Admin');
INSERT INTO documents_contrat (id, contrat_id, nom_fichier, nom_original, type_document, format_fichier, taille_fichier, chemin_stockage, description, date_ajout, ajoute_par) VALUES (4, 2, '9d9633a1002d4ed8be511e3007225f38.jpeg', 'Aweicha_cni_recto.jpeg', 'piece_identite', 'jpeg', 73072, 'static/documents/9d9633a1002d4ed8be511e3007225f38.jpeg', 'CNI Verso', 2025-05-25 11:38:51.990855, 'Admin');
INSERT INTO documents_contrat (id, contrat_id, nom_fichier, nom_original, type_document, format_fichier, taille_fichier, chemin_stockage, description, date_ajout, ajoute_par) VALUES (5, 2, '1353ec2d1fbb481a99aa3eedca790718.jpeg', 'Aweicha_cni_verso.jpeg', 'piece_identite', 'jpeg', 77029, 'static/documents/1353ec2d1fbb481a99aa3eedca790718.jpeg', 'CNI Verso', 2025-05-25 11:39:24.358329, 'Admin');
INSERT INTO documents_contrat (id, contrat_id, nom_fichier, nom_original, type_document, format_fichier, taille_fichier, chemin_stockage, description, date_ajout, ajoute_par) VALUES (6, 2, 'eeb05779e3624f4d84d58bfdb0c1c9e2.', 'pdf', 'piece_identite', '', 128783, 'static/documents/eeb05779e3624f4d84d58bfdb0c1c9e2.', 'Contrat de location', 2025-05-25 11:40:34.612402, 'Admin');
INSERT INTO documents_contrat (id, contrat_id, nom_fichier, nom_original, type_document, format_fichier, taille_fichier, chemin_stockage, description, date_ajout, ajoute_par) VALUES (7, 4, 'a5f21ba2e8e4449d8b4415a90a2bd8e8.jpeg', 'AL-DAOUS_Profession.jpeg', 'justificatif', 'jpeg', 36862, 'static/documents/a5f21ba2e8e4449d8b4415a90a2bd8e8.jpeg', '', 2025-05-25 13:48:12.042693, 'Admin');
INSERT INTO documents_contrat (id, contrat_id, nom_fichier, nom_original, type_document, format_fichier, taille_fichier, chemin_stockage, description, date_ajout, ajoute_par) VALUES (8, 6, 'd13a4ef238bb4868b3bc3eecfa7993e4.jpg', 'sidi_mohamed_cni.jpg', 'piece_identite', 'jpg', 89849, 'static/documents/d13a4ef238bb4868b3bc3eecfa7993e4.jpg', '', 2025-06-01 15:00:41.023899, 'Admin');

-- Table: releves_compteurs
DROP TABLE IF EXISTS releves_compteurs CASCADE;
CREATE TABLE releves_compteurs (
    id INTEGER NOT NULL PRIMARY KEY,
    type_compteur VARCHAR(20) NOT NULL,
    numero_compteur VARCHAR(50) NOT NULL,
    code_abonnement VARCHAR(50),
    date_releve DATE NOT NULL,
    index_precedent DOUBLE PRECISION,
    index_actuel DOUBLE PRECISION NOT NULL,
    consommation DOUBLE PRECISION,
    montant_facture DOUBLE PRECISION,
    statut_paiement VARCHAR(20),
    remarques TEXT,
    date_creation TIMESTAMP,
    contrat_id INTEGER
);

-- Table: comptes_comptables
DROP TABLE IF EXISTS comptes_comptables CASCADE;
CREATE TABLE comptes_comptables (
    id INTEGER NOT NULL PRIMARY KEY,
    numero_compte VARCHAR(10) NOT NULL,
    nom_compte VARCHAR(200) NOT NULL,
    type_compte VARCHAR(50) NOT NULL,
    sous_type VARCHAR(50),
    compte_parent_id INTEGER,
    actif BOOLEAN,
    date_creation TIMESTAMP
);

-- Données pour comptes_comptables
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (1, '10', 'CAPITAL ET RESERVES', 'passif', 'capitaux', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (2, '101', 'Capital', 'passif', 'capitaux', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (3, '12', 'RESULTAT DE L''EXERCICE', 'resultat', 'capitaux', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (4, '21', 'IMMOBILISATIONS CORPORELLES', 'actif', 'immobilisation', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (5, '213', 'Constructions', 'actif', 'immobilisation', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (6, '2131', 'Immeubles de rapport', 'actif', 'immobilisation', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (7, '41', 'CLIENTS ET COMPTES RATTACHES', 'actif', 'creance', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (8, '411', 'Clients', 'actif', 'creance', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (9, '4111', 'Locataires', 'actif', 'creance', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (10, '42', 'PERSONNEL', 'passif', 'dette', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (11, '44', 'ETAT ET COLLECTIVITES', 'actif', 'creance', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (12, '401', 'Fournisseurs', 'passif', 'dette', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (13, '51', 'BANQUES', 'actif', 'tresorerie', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (14, '512', 'Banques', 'actif', 'tresorerie', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (15, '53', 'CAISSE', 'actif', 'tresorerie', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (16, '531', 'Caisse', 'actif', 'tresorerie', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (17, '61', 'SERVICES EXTERIEURS', 'charge', 'exploitation', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (18, '615', 'Entretien et réparations', 'charge', 'exploitation', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (19, '616', 'Primes d''assurance', 'charge', 'exploitation', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (20, '622', 'Rémunérations d''intermédiaires', 'charge', 'exploitation', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (21, '63', 'IMPOTS ET TAXES', 'charge', 'exploitation', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (22, '635', 'Impôts et taxes directs', 'charge', 'exploitation', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (23, '70', 'VENTES', 'produit', 'exploitation', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (24, '701', 'Ventes de marchandises', 'produit', 'exploitation', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (25, '75', 'AUTRES PRODUITS', 'produit', 'exploitation', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (26, '751', 'Revenus immobiliers', 'produit', 'exploitation', NULL, NULL, NULL);
INSERT INTO comptes_comptables (id, numero_compte, nom_compte, type_compte, sous_type, compte_parent_id, actif, date_creation) VALUES (27, '7511', 'Loyers perçus', 'produit', 'exploitation', NULL, NULL, NULL);

-- Table: ecritures_comptables
DROP TABLE IF EXISTS ecritures_comptables CASCADE;
CREATE TABLE ecritures_comptables (
    id INTEGER NOT NULL PRIMARY KEY,
    numero_piece VARCHAR(50) NOT NULL,
    date_ecriture DATE NOT NULL,
    date_operation DATE NOT NULL,
    compte_debit_id INTEGER NOT NULL,
    compte_credit_id INTEGER NOT NULL,
    montant NUMERIC(15,2) NOT NULL,
    libelle VARCHAR(500) NOT NULL,
    reference_externe VARCHAR(100),
    type_operation VARCHAR(50),
    bien_id INTEGER,
    client_id INTEGER,
    validee BOOLEAN,
    saisie_par VARCHAR(100),
    date_creation TIMESTAMP
);

-- Table: budgets_previsionnels
DROP TABLE IF EXISTS budgets_previsionnels CASCADE;
CREATE TABLE budgets_previsionnels (
    id INTEGER NOT NULL PRIMARY KEY,
    bien_id INTEGER,
    annee INTEGER NOT NULL,
    mois INTEGER,
    revenus_loyers_prevus NUMERIC(15,2),
    autres_revenus_prevus NUMERIC(15,2),
    charges_courantes_prevues NUMERIC(10,2),
    travaux_prevus NUMERIC(10,2),
    taxes_impots_prevus NUMERIC(10,2),
    assurances_prevues NUMERIC(10,2),
    frais_gestion_prevus NUMERIC(10,2),
    notes TEXT,
    date_creation TIMESTAMP
);

-- Table: depenses_immobilieres
DROP TABLE IF EXISTS depenses_immobilieres CASCADE;
CREATE TABLE depenses_immobilieres (
    id INTEGER NOT NULL PRIMARY KEY,
    bien_id INTEGER NOT NULL,
    fournisseur_id INTEGER,
    type_depense VARCHAR(100) NOT NULL,
    categorie VARCHAR(50) NOT NULL,
    montant NUMERIC(10,2) NOT NULL,
    date_depense DATE NOT NULL,
    date_paiement DATE,
    statut_paiement VARCHAR(20),
    mode_paiement VARCHAR(50),
    numero_facture VARCHAR(100),
    reference_paiement VARCHAR(100),
    description TEXT NOT NULL,
    justificatif_path VARCHAR(500),
    deductible_impots BOOLEAN,
    tva_applicable BOOLEAN,
    montant_tva NUMERIC(10,2),
    ecriture_comptable_id INTEGER,
    date_creation TIMESTAMP
);

-- Mise à jour des séquences
SELECT setval('clients_id_seq', COALESCE((SELECT MAX(id) FROM clients), 1), true);
SELECT setval('biens_immobiliers_id_seq', COALESCE((SELECT MAX(id) FROM biens_immobiliers), 1), true);
SELECT setval('photos_biens_id_seq', COALESCE((SELECT MAX(id) FROM photos_biens), 1), true);
SELECT setval('contrats_location_id_seq', COALESCE((SELECT MAX(id) FROM contrats_location), 1), true);
SELECT setval('paiements_loyer_id_seq', COALESCE((SELECT MAX(id) FROM paiements_loyer), 1), true);
SELECT setval('documents_contrat_id_seq', COALESCE((SELECT MAX(id) FROM documents_contrat), 1), true);
SELECT setval('comptes_comptables_id_seq', COALESCE((SELECT MAX(id) FROM comptes_comptables), 1), true);
SELECT setval('budgets_previsionnels_id_seq', COALESCE((SELECT MAX(id) FROM budgets_previsionnels), 1), true);
SELECT setval('ecritures_comptables_id_seq', COALESCE((SELECT MAX(id) FROM ecritures_comptables), 1), true);
SELECT setval('depenses_immobilieres_id_seq', COALESCE((SELECT MAX(id) FROM depenses_immobilieres), 1), true);
SELECT setval('releves_compteurs_id_seq', COALESCE((SELECT MAX(id) FROM releves_compteurs), 1), true);

-- Export terminé avec succès
