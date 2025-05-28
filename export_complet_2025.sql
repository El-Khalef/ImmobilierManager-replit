-- =============================================
-- EXPORT SQL COMPLET - SYSTÈME DE GESTION IMMOBILIÈRE
-- Société Laser Services
-- Date de création: 28/05/2025
-- =============================================

-- Instructions d'utilisation :
-- 1. Créer une nouvelle base PostgreSQL
-- 2. Exécuter ce script SQL complet
-- 3. Toutes vos données seront restaurées

-- =============================================
-- CRÉATION DES TABLES
-- =============================================

-- Table clients
CREATE TABLE IF NOT EXISTS clients (
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
CREATE TABLE IF NOT EXISTS biens_immobiliers (
    id SERIAL PRIMARY KEY,
    titre VARCHAR(200) NOT NULL,
    type_bien VARCHAR(50) NOT NULL,
    adresse VARCHAR(200) NOT NULL,
    ville VARCHAR(100) NOT NULL,
    code_postal VARCHAR(10),
    surface FLOAT NOT NULL,
    nombre_pieces INTEGER,
    nombre_chambres INTEGER,
    prix_achat FLOAT,
    prix_location_mensuel FLOAT,
    charges_mensuelles FLOAT,
    description TEXT,
    meuble BOOLEAN DEFAULT FALSE,
    balcon BOOLEAN DEFAULT FALSE,
    parking BOOLEAN DEFAULT FALSE,
    ascenseur BOOLEAN DEFAULT FALSE,
    etage INTEGER,
    annee_construction INTEGER,
    proprietaire_id INTEGER NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (proprietaire_id) REFERENCES clients(id) ON DELETE CASCADE
);

-- Table photos_biens
CREATE TABLE IF NOT EXISTS photos_biens (
    id SERIAL PRIMARY KEY,
    bien_id INTEGER NOT NULL,
    nom_fichier VARCHAR(255) NOT NULL,
    chemin_fichier VARCHAR(500) NOT NULL,
    principale BOOLEAN DEFAULT FALSE,
    date_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bien_id) REFERENCES biens_immobiliers(id) ON DELETE CASCADE
);

-- Table contrats_location
CREATE TABLE IF NOT EXISTS contrats_location (
    id SERIAL PRIMARY KEY,
    bien_id INTEGER NOT NULL,
    locataire_id INTEGER NOT NULL,
    date_debut DATE NOT NULL,
    date_fin DATE,
    loyer_mensuel FLOAT NOT NULL,
    charges_mensuelles FLOAT,
    depot_garantie FLOAT,
    frais_agence FLOAT,
    statut VARCHAR(20) DEFAULT 'actif',
    conditions_particulieres TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bien_id) REFERENCES biens_immobiliers(id) ON DELETE CASCADE,
    FOREIGN KEY (locataire_id) REFERENCES clients(id) ON DELETE CASCADE
);

-- Table paiements_loyer
CREATE TABLE IF NOT EXISTS paiements_loyer (
    id SERIAL PRIMARY KEY,
    contrat_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    bien_id INTEGER NOT NULL,
    mois INTEGER NOT NULL,
    annee INTEGER NOT NULL,
    montant_loyer FLOAT NOT NULL,
    montant_charges FLOAT,
    date_paiement DATE,
    date_echeance DATE NOT NULL,
    statut VARCHAR(20) DEFAULT 'en_attente',
    mode_paiement VARCHAR(50),
    reference_paiement VARCHAR(100),
    remarques TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contrat_id) REFERENCES contrats_location(id) ON DELETE CASCADE,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE,
    FOREIGN KEY (bien_id) REFERENCES biens_immobiliers(id) ON DELETE CASCADE
);

-- Table documents_contrat
CREATE TABLE IF NOT EXISTS documents_contrat (
    id SERIAL PRIMARY KEY,
    contrat_id INTEGER NOT NULL,
    type_document VARCHAR(50) NOT NULL,
    nom_fichier VARCHAR(255) NOT NULL,
    chemin_fichier VARCHAR(500) NOT NULL,
    description TEXT,
    date_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contrat_id) REFERENCES contrats_location(id) ON DELETE CASCADE
);

-- =============================================
-- INSERTION DES DONNÉES
-- =============================================

-- Cette section sera générée automatiquement avec vos données actuelles
-- Veuillez exécuter la requête suivante pour obtenir toutes vos données :
