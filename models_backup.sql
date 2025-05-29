-- =============================================
-- EXPORT SQL COMPLET - SYSTÈME DE GESTION IMMOBILIÈRE
-- Société Laser Services
-- Date: 26/05/2025
-- =============================================

-- =============================================
-- 1. STRUCTURE DES TABLES
-- =============================================

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
    type_piece_identite VARCHAR(50) NOT NULL,
    numero_piece_identite VARCHAR(50) NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table biens_immobiliers
CREATE TABLE biens_immobiliers (
    id SERIAL PRIMARY KEY,
    titre VARCHAR(200) NOT NULL,
    type_bien VARCHAR(50) NOT NULL,
    adresse VARCHAR(200) NOT NULL,
    ville VARCHAR(100) NOT NULL DEFAULT 'Nouakchott',
    code_postal VARCHAR(10),
    surface FLOAT NOT NULL,
    nombre_pieces INTEGER,
    nombre_chambres INTEGER,
    prix_achat FLOAT,
    prix_location_mensuel FLOAT,
    charges_mensuelles FLOAT DEFAULT 0,
    description TEXT,
    meuble BOOLEAN DEFAULT FALSE,
    balcon BOOLEAN DEFAULT FALSE,
    parking BOOLEAN DEFAULT FALSE,
    ascenseur BOOLEAN DEFAULT FALSE,
    etage INTEGER,
    annee_construction INTEGER,
    proprietaire_id INTEGER NOT NULL REFERENCES clients(id),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table photos_biens
CREATE TABLE photos_biens (
    id SERIAL PRIMARY KEY,
    bien_id INTEGER NOT NULL REFERENCES biens_immobiliers(id) ON DELETE CASCADE,
    nom_fichier VARCHAR(255) NOT NULL,
    principale BOOLEAN DEFAULT FALSE,
    date_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table contrats_location
CREATE TABLE contrats_location (
    id SERIAL PRIMARY KEY,
    bien_id INTEGER NOT NULL REFERENCES biens_immobiliers(id),
    locataire_id INTEGER NOT NULL REFERENCES clients(id),
    date_debut DATE NOT NULL,
    date_fin DATE,
    loyer_mensuel FLOAT NOT NULL,
    charges_mensuelles FLOAT DEFAULT 0,
    depot_garantie FLOAT DEFAULT 0,
    frais_agence FLOAT DEFAULT 0,
    statut VARCHAR(20) DEFAULT 'actif',
    conditions_particulieres TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table paiements_loyer
CREATE TABLE paiements_loyer (
    id SERIAL PRIMARY KEY,
    contrat_id INTEGER NOT NULL REFERENCES contrats_location(id),
    mois INTEGER NOT NULL,
    annee INTEGER NOT NULL,
    montant_loyer FLOAT NOT NULL,
    montant_charges FLOAT DEFAULT 0,
    date_paiement DATE,
    date_echeance DATE NOT NULL,
    statut VARCHAR(20) DEFAULT 'en_attente',
    mode_paiement VARCHAR(50),
    reference_paiement VARCHAR(100),
    remarques TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table documents_contrat
CREATE TABLE documents_contrat (
    id SERIAL PRIMARY KEY,
    contrat_id INTEGER NOT NULL REFERENCES contrats_location(id) ON DELETE CASCADE,
    type_document VARCHAR(50) NOT NULL,
    nom_fichier VARCHAR(255) NOT NULL,
    chemin_fichier VARCHAR(500) NOT NULL,
    taille_fichier INTEGER,
    description TEXT,
    date_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- 2. DONNÉES EXISTANTES
-- =============================================

-- Insertion des clients
INSERT INTO clients (id, nom, prenom, email, telephone, adresse, ville, code_postal, type_client, type_piece_identite, numero_piece_identite, date_creation) VALUES
(1, 'EL KHALEF', 'Propriétaire', 'elkhafef@email.com', NULL, NULL, 'Nouakchott', NULL, 'proprietaire', 'carte_identite', 'CI001234567', NULL),
(2, 'OULD AHMED', 'Mohamed Lemine', 'Ahmed_Ould_Ahmed@gmail.com', '22817045', '365 F-Nord Tevragh Zeina', 'Nouakchott', NULL, 'locataire', 'carte_identite', '8960704607', '2025-05-25 08:51:21.405906'),
(3, 'ZEIDANE', 'Aweicha', 'aweicha@gmail.com', '49602030', '365 F-Nord Tevragh Zeina', 'Nouakchott', NULL, 'locataire', 'carte_identite', '7493636352', '2025-05-25 11:29:53.277346'),
(4, 'AL-DAOUS', 'Yahya Mohamed Rajeh', 'aldaous@gmail.com', '967733004315', '365 F-Nord Tevragh Zeina', 'Nouakchott', NULL, 'locataire', 'passeport', '00039505', '2025-05-25 11:51:20.860315');

-- Insertion des biens immobiliers
INSERT INTO biens_immobiliers (id, titre, type_bien, adresse, ville, code_postal, surface, nombre_pieces, nombre_chambres, prix_achat, prix_location_mensuel, charges_mensuelles, description, meuble, balcon, parking, ascenseur, etage, annee_construction, proprietaire_id, date_creation) VALUES
(1, 'C', 'appartement', '365 F-Nord Tevragh Zeina', 'Nouakchott', NULL, 108, 3, 2, NULL, 8000, 0, 'Appartement au rez-de-chaussée à droite de la rentrée avec 3 pièces dont 2 chambres, 2 toilettes et un séjour', false, false, false, false, 0, 2006, 1, '2025-05-25 04:31:16.918143'),
(2, 'B', 'appartement', '365 F-Nord Tevragh Zeina', 'Nouakchott', NULL, 108, 3, 2, NULL, 9000, 0, 'Appartement au premier étage à gauche de la rentrée avec 3 pièces dont 2 chambres, 2 toilettes et un séjour', false, false, false, false, 1, 2006, 1, '2025-05-25 04:35:17.817167'),
(3, 'D', 'appartement', '365 F-Nord Tevragh Zeina', 'Nouakchott', NULL, 108, 3, 2, NULL, 9000, 0, 'Appartement au premier étage à droite de la rentrée avec 3 pièces dont 2 chambres, 2 toilettes et un séjour et un parking à droite de l''entrée.', false, false, true, false, 1, 2006, 1, '2025-05-25 04:38:33.442116'),
(4, 'Magasin', 'local', 'F-Nord sur Est Tavragh Zeina', 'Nouakchott', NULL, 144, 1, 1, NULL, 35000, 0, 'Localisation du Grand Magasin
1.      Type de localisation :
Le grand magasin est situé dans un emplacement stratégique.
2.      Détails de l''emplacement :
o       Il est situé sur une grande avenue, assurant une visibilité maximale et un flux constant de passants.
o       Il se trouve également à un angle, ce qui offre une double exposition et un accès facile depuis deux rues différentes.
3.      Avantages de l''emplacement :
o       Idéal pour attirer des clients grâce à sa visibilité accrue.
o       Possibilité d''aménager deux vitrines ou plus, augmentant les opportunités publicitaires et de présentation des produits.', false, false, false, false, NULL, 2012, 1, '2025-05-25 08:35:14.790967'),
(5, 'Magasin', 'local', 'F-Nord sur Est Tavragh Zeina', 'Nouakchott', NULL, 48, 1, 1, NULL, 15000, 0, '1.       Type de localisation :
Le grand magasin est situé dans un emplacement stratégique.
2.      Détails de l''emplacement :
o       Il est situé sur une grande avenue, assurant une visibilité maximale et un flux constant de passants.
3.      Avantages de l''emplacement :
o       Idéal pour attirer des clients grâce à sa visibilité accrue.
o       Possibilité d''aménager deux vitrines ou plus, augmentant les opportunités publicitaires et de présentation des produits.', false, false, false, false, 0, 2023, 1, '2025-05-25 08:38:29.821901'),
(6, 'Magasin', 'local', 'F-Nord sur Est Tavragh Zeina', 'Nouakchott', NULL, 48, 1, 1, NULL, 15000, 0, '1.       Type de localisation :
Le grand magasin est situé dans un emplacement stratégique.
2.      Détails de l''emplacement :
o       Il est situé sur une grande avenue, assurant une visibilité maximale et un flux constant de passants.
3.      Avantages de l''emplacement :
o       Idéal pour attirer des clients grâce à sa visibilité accrue.
o       Possibilité d''aménager deux vitrines ou plus, augmentant les opportunités publicitaires et de présentation des produits.', false, false, false, false, 0, 2023, 1, '2025-05-25 08:40:34.788341'),
(7, 'Magasin', 'bureau', 'F-Nord sur Est Tavragh Zeina', 'Nouakchott', NULL, 24, 1, 1, NULL, 50, 0, 'Bureau est situé dans un emplacement stratégique.
        Avantages de l''emplacement :
        Idéal pour attirer des clients grâce à sa visibilité accrue.', false, false, false, false, 0, 2023, 1, '2025-05-25 08:44:34.751639');

-- Insertion des contrats de location
INSERT INTO contrats_location (id, bien_id, locataire_id, date_debut, date_fin, loyer_mensuel, charges_mensuelles, depot_garantie, frais_agence, statut, conditions_particulieres, date_creation) VALUES
(1, 1, 2, '2021-10-26', NULL, 8000, 0, 8000, 0, 'actif', 'Le numéro de téléphone est celui de sa femme Mariem', '2025-05-25 10:23:55.890435'),
(2, 2, 3, '2024-05-28', NULL, 9000, 0, 9000, 0, 'actif', 'Pas de contrat SOMELEC', '2025-05-25 11:36:38.729002'),
(4, 3, 4, '2021-11-09', NULL, 9000, 0, 0, NULL, 'actif', NULL, '2025-05-25 13:29:40.521468');

-- Insertion des paiements de loyer
INSERT INTO paiements_loyer (id, contrat_id, mois, annee, montant_loyer, montant_charges, date_paiement, date_echeance, statut, mode_paiement, reference_paiement, remarques, date_creation) VALUES
(1, 1, 5, 2025, 8000, 0, '2025-05-01', '2025-05-01', 'paye', 'virement', 'Bankiliy', NULL, '2025-05-25 12:57:46.112074'),
(2, 2, 5, 2025, 9000, 0, '2025-05-08', '2025-05-01', 'paye', 'virement', 'Bankiliy', NULL, '2025-05-25 12:58:47.38712'),
(3, 4, 5, 2025, 9000, 0, '2025-05-15', '2025-05-01', 'paye', 'virement', 'Bankiliy', NULL, '2025-05-25 14:04:48.025995');

-- Insertion des documents de contrat
INSERT INTO documents_contrat (id, contrat_id, nom_fichier, type_document, taille_fichier, chemin_fichier, description, date_upload) VALUES
(1, 1, '1e849430409549768b694ebf5fe91d41.pdf', 'piece_identite', 115430, 'static/documents/1e849430409549768b694ebf5fe91d41.pdf', 'Contrat de location', '2025-05-25 11:04:53.662704'),
(2, 1, '56c6d32e71da4bf690fd2bd702f487d9.jpeg', 'piece_identite', 64757, 'static/documents/56c6d32e71da4bf690fd2bd702f487d9.jpeg', 'CNI recto', '2025-05-25 11:18:50.753905'),
(3, 1, 'e1e1d98d74a44326be55e7cc190ba059.jpeg', 'piece_identite', 60428, 'static/documents/e1e1d98d74a44326be55e7cc190ba059.jpeg', 'CNI Verso', '2025-05-25 11:19:18.95132'),
(4, 2, '9d9633a1002d4ed8be511e3007225f38.jpeg', 'piece_identite', 73072, 'static/documents/9d9633a1002d4ed8be511e3007225f38.jpeg', 'CNI Verso', '2025-05-25 11:38:51.990855'),
(5, 2, '1353ec2d1fbb481a99aa3eedca790718.jpeg', 'piece_identite', 77029, 'static/documents/1353ec2d1fbb481a99aa3eedca790718.jpeg', 'CNI Verso', '2025-05-25 11:39:24.358329'),
(6, 2, 'eeb05779e3624f4d84d58bfdb0c1c9e2.pdf', 'piece_identite', 128783, 'static/documents/eeb05779e3624f4d84d58bfdb0c1c9e2.pdf', 'Contrat de location', '2025-05-25 11:40:34.612402'),
(7, 4, 'a5f21ba2e8e4449d8b4415a90a2bd8e8.jpeg', 'justificatif', 36862, 'static/documents/a5f21ba2e8e4449d8b4415a90a2bd8e8.jpeg', NULL, '2025-05-25 13:48:12.042693');

-- =============================================
-- 3. MISE À JOUR DES SÉQUENCES
-- =============================================

-- Réinitialisation des séquences pour éviter les conflits d'ID
SELECT setval('clients_id_seq', (SELECT MAX(id) FROM clients));
SELECT setval('biens_immobiliers_id_seq', (SELECT MAX(id) FROM biens_immobiliers));
SELECT setval('contrats_location_id_seq', (SELECT MAX(id) FROM contrats_location));
SELECT setval('paiements_loyer_id_seq', (SELECT MAX(id) FROM paiements_loyer));
SELECT setval('documents_contrat_id_seq', (SELECT MAX(id) FROM documents_contrat));

-- =============================================
-- 4. INDEX ET CONTRAINTES OPTIONNELS
-- =============================================

-- Index pour améliorer les performances
CREATE INDEX IF NOT EXISTS idx_biens_proprietaire ON biens_immobiliers(proprietaire_id);
CREATE INDEX IF NOT EXISTS idx_contrats_bien ON contrats_location(bien_id);
CREATE INDEX IF NOT EXISTS idx_contrats_locataire ON contrats_location(locataire_id);
CREATE INDEX IF NOT EXISTS idx_paiements_contrat ON paiements_loyer(contrat_id);
CREATE INDEX IF NOT EXISTS idx_documents_contrat ON documents_contrat(contrat_id);

-- =============================================
-- FIN DE L'EXPORT
-- =============================================