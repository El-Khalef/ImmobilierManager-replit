-- Sauvegarde complète avec données réelles - Gestion Immobilière
-- Date de création: 2025-06-07 16:15
-- Contient toutes les données actuelles de la base

-- =============================================
-- SUPPRESSION ET RECRÉATION DES TABLES
-- =============================================

DROP TABLE IF EXISTS documents_contrat CASCADE;
DROP TABLE IF EXISTS photos_biens CASCADE;
DROP TABLE IF EXISTS paiements_loyer CASCADE;
DROP TABLE IF EXISTS contrats_location CASCADE;
DROP TABLE IF EXISTS biens_immobiliers CASCADE;
DROP TABLE IF EXISTS clients CASCADE;

-- =============================================
-- STRUCTURE DES TABLES
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
    type_client VARCHAR(20) NOT NULL CHECK (type_client IN ('proprietaire', 'locataire', 'acheteur')),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    type_piece_identite VARCHAR(20) CHECK (type_piece_identite IN ('carte_identite', 'passeport')),
    numero_piece_identite VARCHAR(50)
);

-- Table biens_immobiliers
CREATE TABLE biens_immobiliers (
    id SERIAL PRIMARY KEY,
    titre VARCHAR(200) NOT NULL,
    type_bien VARCHAR(50) NOT NULL CHECK (type_bien IN ('appartement', 'maison', 'terrain', 'local', 'bureau', 'garage')),
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
    meuble BOOLEAN DEFAULT FALSE,
    balcon BOOLEAN DEFAULT FALSE,
    parking BOOLEAN DEFAULT FALSE,
    ascenseur BOOLEAN DEFAULT FALSE,
    etage INTEGER,
    annee_construction INTEGER,
    disponible BOOLEAN DEFAULT TRUE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    proprietaire_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);

-- Table contrats_location
CREATE TABLE contrats_location (
    id SERIAL PRIMARY KEY,
    date_debut DATE NOT NULL,
    date_fin DATE,
    loyer_mensuel DOUBLE PRECISION NOT NULL,
    charges_mensuelles DOUBLE PRECISION,
    depot_garantie DOUBLE PRECISION,
    frais_agence DOUBLE PRECISION,
    statut VARCHAR(20) DEFAULT 'actif' CHECK (statut IN ('actif', 'termine', 'suspendu')),
    conditions_particulieres TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    bien_id INTEGER NOT NULL REFERENCES biens_immobiliers(id) ON DELETE CASCADE,
    locataire_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE CASCADE
);

-- Table paiements_loyer
CREATE TABLE paiements_loyer (
    id SERIAL PRIMARY KEY,
    mois INTEGER NOT NULL CHECK (mois BETWEEN 1 AND 12),
    annee INTEGER NOT NULL CHECK (annee BETWEEN 2020 AND 2030),
    montant_loyer DOUBLE PRECISION NOT NULL,
    montant_charges DOUBLE PRECISION,
    date_paiement DATE,
    date_echeance DATE NOT NULL,
    statut VARCHAR(20) DEFAULT 'en_attente' CHECK (statut IN ('en_attente', 'paye', 'retard')),
    mode_paiement VARCHAR(50),
    reference_paiement VARCHAR(100),
    remarques TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    contrat_id INTEGER NOT NULL REFERENCES contrats_location(id) ON DELETE CASCADE
);

-- Table photos_biens
CREATE TABLE photos_biens (
    id SERIAL PRIMARY KEY,
    nom_fichier VARCHAR(255) NOT NULL,
    nom_original VARCHAR(255),
    principale BOOLEAN DEFAULT FALSE,
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    bien_id INTEGER NOT NULL REFERENCES biens_immobiliers(id) ON DELETE CASCADE
);

-- Table documents_contrat
CREATE TABLE documents_contrat (
    id SERIAL PRIMARY KEY,
    contrat_id INTEGER NOT NULL REFERENCES contrats_location(id) ON DELETE CASCADE,
    nom_fichier VARCHAR(255) NOT NULL,
    nom_original VARCHAR(255) NOT NULL,
    type_document VARCHAR(50) NOT NULL CHECK (type_document IN ('piece_identite', 'photo', 'video', 'audio', 'contrat_signe', 'justificatif', 'autre')),
    format_fichier VARCHAR(10) NOT NULL,
    taille_fichier INTEGER NOT NULL,
    chemin_stockage VARCHAR(500) NOT NULL,
    description TEXT,
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ajoute_par VARCHAR(100)
);

-- =============================================
-- INSERTION DES DONNÉES RÉELLES
-- =============================================

-- Réinitialiser les séquences
ALTER SEQUENCE clients_id_seq RESTART WITH 1;
ALTER SEQUENCE biens_immobiliers_id_seq RESTART WITH 1;
ALTER SEQUENCE contrats_location_id_seq RESTART WITH 1;
ALTER SEQUENCE paiements_loyer_id_seq RESTART WITH 1;
ALTER SEQUENCE photos_biens_id_seq RESTART WITH 1;
ALTER SEQUENCE documents_contrat_id_seq RESTART WITH 1;

-- CLIENTS
INSERT INTO clients (id, nom, prenom, email, telephone, adresse, ville, code_postal, type_client, date_creation, type_piece_identite, numero_piece_identite) VALUES
(1, 'EL KHALEF', 'Propriétaire', 'elkhafef@email.com', '36306854', NULL, 'Nouakchott', NULL, 'proprietaire', NULL, 'carte_identite', '7716097122'),
(2, 'OULD AHMED', 'Mohamed Lemine', 'Ahmed_Ould_Ahmed@gmail.com', '22817045', '365 F-Nord Tevragh Zeina', 'Nouakchott', NULL, 'locataire', '2025-05-25 08:51:21.405906', 'carte_identite', '8960704607'),
(3, 'ZEIDANE', 'Aweicha', 'aweicha@gmail.com', '49602030', '365 F-Nord Tevragh Zeina', 'Nouakchott', NULL, 'locataire', '2025-05-25 11:29:53.277346', 'carte_identite', '7493636352'),
(4, 'AL-DAOUS', 'Yahya Mohamed Rajeh', 'aldaous@gmail.com', '967733004315', '365 F-Nord Tevragh Zeina', 'Nouakchott', NULL, 'locataire', '2025-05-25 11:51:20.860315', 'passeport', '00039505'),
(5, 'ABD EL VETTAH', 'Sidi Mohamed', 'abdelvettah@gmail.com', '31366050', NULL, 'Nouakchott', NULL, 'locataire', '2025-06-01 05:36:32.971875', 'carte_identite', '1417715238');

-- BIENS IMMOBILIERS
INSERT INTO biens_immobiliers (id, titre, type_bien, adresse, ville, code_postal, surface, nombre_pieces, nombre_chambres, prix_achat, prix_location_mensuel, charges_mensuelles, description, meuble, balcon, parking, ascenseur, etage, annee_construction, disponible, date_creation, proprietaire_id, latitude, longitude) VALUES
(1, 'C', 'appartement', '365 F-Nord Tevragh Zeina', 'Nouakchott', '', 108, 3, 2, NULL, 8000, 0, 'Appartement au rez-de-chaussée à droite de la rentrée avec 3 pièces dont 2 chambres, 2 toilettes et un séjour', false, false, false, false, 0, 2006, false, '2025-05-25 04:31:16.918143', 1, 18.109639, -15.970278),
(2, 'B', 'appartement', '365 F-Nord Tevragh Zeina', 'Nouakchott', '', 108, 3, 2, NULL, 9000, 0, 'Appartement au premier étage à gauche de la rentrée avec 3 pièces dont 2 chambres, 2 toilettes et un séjour', false, false, false, false, 1, 2006, false, '2025-05-25 04:35:17.817167', 1, 18.109639, -15.970278),
(3, 'D', 'appartement', '365 F-Nord Tevragh Zeina', 'Nouakchott', '', 108, 3, 2, NULL, 9000, 0, 'Appartement au premier étage à droite de la rentrée avec 3 pièces dont 2 chambres, 2 toilettes et un séjour et un parking à droite de l''entrée.', false, false, true, false, 1, 2006, false, '2025-05-25 04:38:33.442116', 1, 18.109639, -15.970278),
(4, 'Magasin-A', 'local', 'F-Nord sur Est Tavragh Zeina', 'Nouakchott', '', 144, 1, 1, NULL, 35000, 0, 'Localisation du Grand Magasin
1.	Type de localisation :
Le grand magasin est situé dans un emplacement stratégique.
2.	Détails de l''emplacement :
o	Il est situé sur une grande avenue, assurant une visibilité maximale et un flux constant de passants.
o	Il se trouve également à un angle, ce qui offre une double exposition et un accès facile depuis deux rues différentes.
3.	Avantages de l''emplacement :
o	Idéal pour attirer des clients grâce à sa visibilité accrue.
o	Possibilité d''aménager deux vitrines ou plus, augmentant les opportunités publicitaires et de présentation des produits.', false, false, false, false, NULL, 2012, true, '2025-05-25 08:35:14.790967', 1, 18.108472, -15.965972),
(5, 'Magasin-B', 'local', 'F-Nord sur Est Tavragh Zeina', 'Nouakchott', '', 48, 1, 1, NULL, 15000, 0, '1.	Type de localisation :
Le grand magasin est situé dans un emplacement stratégique.
2.	Détails de l''emplacement :
o	Il est situé sur une grande avenue, assurant une visibilité maximale et un flux constant de passants.
3.	Avantages de l''emplacement :
o	Idéal pour attirer des clients grâce à sa visibilité accrue.
o	Possibilité d''aménager deux vitrines ou plus, augmentant les opportunités publicitaires et de présentation des produits.', false, false, false, false, 0, 2023, true, '2025-05-25 08:38:29.821901', 1, 18.108472, -15.965972),
(6, 'Magasin-C', 'local', 'F-Nord sur Est Tavragh Zeina', 'Nouakchott', '', 48, 1, 1, NULL, 15000, 0, '1.	Type de localisation :
Le grand magasin est situé dans un emplacement stratégique.
2.	Détails de l''emplacement :
o	Il est situé sur une grande avenue, assurant une visibilité maximale et un flux constant de passants.
3.	Avantages de l''emplacement :
o	Idéal pour attirer des clients grâce à sa visibilité accrue.
o	Possibilité d''aménager deux vitrines ou plus, augmentant les opportunités publicitaires et de présentation des produits.', false, false, false, false, 0, 2023, true, '2025-05-25 08:40:34.788341', 1, 18.108472, -15.965972),
(7, 'Magasin-D', 'bureau', 'F-Nord sur Est Tavragh Zeina', 'Nouakchott', '', 24, 1, 1, NULL, 5000, 0, 'Bureau est situé dans un emplacement stratégique.
	Avantages de l''emplacement :
	Idéal pour attirer des clients grâce à sa visibilité accrue.', false, false, false, false, 0, 2023, true, '2025-05-25 08:44:34.751639', 1, 18.108472, -15.965972);

-- CONTRATS DE LOCATION
INSERT INTO contrats_location (id, date_debut, date_fin, loyer_mensuel, charges_mensuelles, depot_garantie, frais_agence, statut, conditions_particulieres, date_creation, bien_id, locataire_id) VALUES
(1, '2021-10-26', NULL, 8000, 0, 8000, 0, 'actif', 'Le numéro de téléphone est celui de sa femme Mariem', '2025-05-25 10:23:55.890435', 1, 2),
(2, '2024-05-28', NULL, 9000, 0, 9000, 0, 'actif', 'Pas de contrat SOMELEC', '2025-05-25 11:36:38.729002', 2, 3),
(4, '2021-11-09', NULL, 9000, 0, 0, NULL, 'actif', NULL, '2025-05-25 13:29:40.521468', 3, 4),
(6, '2022-10-23', NULL, 35000, 0, 0, 0, 'actif', NULL, '2025-06-01 05:49:11.168429', 4, 5);

-- PAIEMENTS DE LOYER
INSERT INTO paiements_loyer (id, mois, annee, montant_loyer, montant_charges, date_paiement, date_echeance, statut, mode_paiement, reference_paiement, remarques, date_creation, contrat_id) VALUES
(1, 5, 2025, 8000, 0, '2025-05-01', '2025-05-01', 'paye', 'virement', 'Bankiliy', NULL, '2025-05-25 12:57:46.112074', 1),
(2, 5, 2025, 9000, 0, '2025-05-08', '2025-05-01', 'paye', 'virement', 'Bankiliy', NULL, '2025-05-25 12:58:47.38712', 2),
(3, 5, 2025, 18000, 0, '2025-05-15', '2025-05-01', 'paye', 'virement', 'Bankiliy', 'Paiement des mois de mai et juin 2025.', '2025-05-25 14:04:48.025995', 4),
(4, 5, 2025, 35000, 0, '2025-05-10', '2025-05-01', 'paye', 'virement', 'Bankiliy', NULL, '2025-06-01 05:51:36.833005', 6),
(5, 6, 2025, 8000, 0, '2025-06-02', '2025-06-01', 'paye', 'virement', 'Bankiliy', NULL, '2025-06-04 18:43:54.089591', 1);

-- DOCUMENTS DES CONTRATS
INSERT INTO documents_contrat (id, contrat_id, nom_fichier, nom_original, type_document, format_fichier, taille_fichier, chemin_stockage, description, date_ajout, ajoute_par) VALUES
(1, 1, '1e849430409549768b694ebf5fe91d41.pdf', 'Contrat_Location_Appartements_Mohamed_Lemine.pdf', 'piece_identite', 'pdf', 115430, 'static/documents/1e849430409549768b694ebf5fe91d41.pdf', 'Contrat de location', '2025-05-25 11:04:53.662704', 'Admin'),
(2, 1, '56c6d32e71da4bf690fd2bd702f487d9.jpeg', 'Mohamed_Lemine_cni_recto.jpeg', 'piece_identite', 'jpeg', 64757, 'static/documents/56c6d32e71da4bf690fd2bd702f487d9.jpeg', 'CNI recto', '2025-05-25 11:18:50.753905', 'Admin'),
(3, 1, 'e1e1d98d74a44326be55e7cc190ba059.jpeg', 'Mohamed_Lemine_cni_verso.jpeg', 'piece_identite', 'jpeg', 60428, 'static/documents/e1e1d98d74a44326be55e7cc190ba059.jpeg', 'CNI Verso', '2025-05-25 11:19:18.95132', 'Admin'),
(4, 2, '9d9633a1002d4ed8be511e3007225f38.jpeg', 'Aweicha_cni_recto.jpeg', 'piece_identite', 'jpeg', 73072, 'static/documents/9d9633a1002d4ed8be511e3007225f38.jpeg', 'CNI Verso', '2025-05-25 11:38:51.990855', 'Admin'),
(5, 2, '1353ec2d1fbb481a99aa3eedca790718.jpeg', 'Aweicha_cni_verso.jpeg', 'piece_identite', 'jpeg', 77029, 'static/documents/1353ec2d1fbb481a99aa3eedca790718.jpeg', 'CNI Verso', '2025-05-25 11:39:24.358329', 'Admin'),
(6, 2, 'eeb05779e3624f4d84d58bfdb0c1c9e2.', 'pdf', 'piece_identite', '', 128783, 'static/documents/eeb05779e3624f4d84d58bfdb0c1c9e2.', 'Contrat de location', '2025-05-25 11:40:34.612402', 'Admin'),
(7, 4, 'a5f21ba2e8e4449d8b4415a90a2bd8e8.jpeg', 'AL-DAOUS_Profession.jpeg', 'justificatif', 'jpeg', 36862, 'static/documents/a5f21ba2e8e4449d8b4415a90a2bd8e8.jpeg', NULL, '2025-05-25 13:48:12.042693', 'Admin'),
(8, 6, 'd13a4ef238bb4868b3bc3eecfa7993e4.jpg', 'sidi_mohamed_cni.jpg', 'piece_identite', 'jpg', 89849, 'static/documents/d13a4ef238bb4868b3bc3eecfa7993e4.jpg', NULL, '2025-06-01 15:00:41.023899', 'Admin');

-- =============================================
-- MISE À JOUR DES SÉQUENCES
-- =============================================

SELECT setval('clients_id_seq', COALESCE((SELECT MAX(id) FROM clients), 1));
SELECT setval('biens_immobiliers_id_seq', COALESCE((SELECT MAX(id) FROM biens_immobiliers), 1));
SELECT setval('contrats_location_id_seq', COALESCE((SELECT MAX(id) FROM contrats_location), 1));
SELECT setval('paiements_loyer_id_seq', COALESCE((SELECT MAX(id) FROM paiements_loyer), 1));
SELECT setval('photos_biens_id_seq', COALESCE((SELECT MAX(id) FROM photos_biens), 1));
SELECT setval('documents_contrat_id_seq', COALESCE((SELECT MAX(id) FROM documents_contrat), 1));

-- =============================================
-- INDEX POUR LES PERFORMANCES
-- =============================================

CREATE INDEX idx_biens_proprietaire ON biens_immobiliers(proprietaire_id);
CREATE INDEX idx_biens_type ON biens_immobiliers(type_bien);
CREATE INDEX idx_biens_ville ON biens_immobiliers(ville);
CREATE INDEX idx_biens_disponible ON biens_immobiliers(disponible);

CREATE INDEX idx_contrats_bien ON contrats_location(bien_id);
CREATE INDEX idx_contrats_locataire ON contrats_location(locataire_id);
CREATE INDEX idx_contrats_statut ON contrats_location(statut);

CREATE INDEX idx_paiements_contrat ON paiements_loyer(contrat_id);
CREATE INDEX idx_paiements_statut ON paiements_loyer(statut);
CREATE INDEX idx_paiements_mois_annee ON paiements_loyer(mois, annee);

CREATE INDEX idx_photos_bien ON photos_biens(bien_id);
CREATE INDEX idx_documents_contrat ON documents_contrat(contrat_id);

-- =============================================
-- FONCTION POUR OBTENIR LE CLIENT D'UN PAIEMENT
-- =============================================

CREATE OR REPLACE FUNCTION get_client_from_paiement(paiement_id INTEGER)
RETURNS TABLE(client_id INTEGER, client_nom VARCHAR, client_prenom VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        loc.id,
        loc.nom,
        loc.prenom
    FROM paiements_loyer p
    JOIN contrats_location c ON p.contrat_id = c.id
    JOIN clients loc ON c.locataire_id = loc.id
    WHERE p.id = paiement_id;
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- TRIGGER POUR LA DISPONIBILITÉ DES BIENS
-- =============================================

CREATE OR REPLACE FUNCTION update_bien_disponibilite()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' AND NEW.statut = 'actif' THEN
        UPDATE biens_immobiliers SET disponible = FALSE WHERE id = NEW.bien_id;
    ELSIF TG_OP = 'UPDATE' THEN
        IF OLD.statut != 'actif' AND NEW.statut = 'actif' THEN
            UPDATE biens_immobiliers SET disponible = FALSE WHERE id = NEW.bien_id;
        ELSIF OLD.statut = 'actif' AND NEW.statut != 'actif' THEN
            IF NOT EXISTS (SELECT 1 FROM contrats_location WHERE bien_id = NEW.bien_id AND statut = 'actif' AND id != NEW.id) THEN
                UPDATE biens_immobiliers SET disponible = TRUE WHERE id = NEW.bien_id;
            END IF;
        END IF;
    ELSIF TG_OP = 'DELETE' AND OLD.statut = 'actif' THEN
        IF NOT EXISTS (SELECT 1 FROM contrats_location WHERE bien_id = OLD.bien_id AND statut = 'actif') THEN
            UPDATE biens_immobiliers SET disponible = TRUE WHERE id = OLD.bien_id;
        END IF;
    END IF;
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_bien_disponibilite
    AFTER INSERT OR UPDATE OR DELETE ON contrats_location
    FOR EACH ROW EXECUTE FUNCTION update_bien_disponibilite();

-- =============================================
-- FIN DE LA SAUVEGARDE
-- =============================================

COMMIT;

-- Statistiques après import
SELECT 'Clients' as table_name, COUNT(*) as nb_lignes FROM clients
UNION ALL
SELECT 'Biens immobiliers', COUNT(*) FROM biens_immobiliers
UNION ALL
SELECT 'Contrats location', COUNT(*) FROM contrats_location
UNION ALL
SELECT 'Paiements loyer', COUNT(*) FROM paiements_loyer
UNION ALL
SELECT 'Documents contrat', COUNT(*) FROM documents_contrat
UNION ALL
SELECT 'Photos biens', COUNT(*) FROM photos_biens;