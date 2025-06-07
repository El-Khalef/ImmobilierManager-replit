-- Sauvegarde complète de la base de données - Gestion Immobilière
-- Date de création: 2025-06-07
-- Généré automatiquement

-- =============================================
-- Structure des tables
-- =============================================

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
    type_client VARCHAR(20) NOT NULL CHECK (type_client IN ('proprietaire', 'locataire', 'acheteur')),
    type_piece_identite VARCHAR(20) CHECK (type_piece_identite IN ('carte_identite', 'passeport')),
    numero_piece_identite VARCHAR(50),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table biens_immobiliers
CREATE TABLE biens_immobiliers (
    id SERIAL PRIMARY KEY,
    titre VARCHAR(200) NOT NULL,
    type_bien VARCHAR(50) NOT NULL CHECK (type_bien IN ('appartement', 'maison', 'terrain', 'local', 'bureau', 'garage')),
    adresse VARCHAR(200) NOT NULL,
    ville VARCHAR(100) NOT NULL DEFAULT 'Nouakchott',
    code_postal VARCHAR(10) NOT NULL DEFAULT '11111',
    surface DECIMAL(10,2) NOT NULL,
    nombre_pieces INTEGER,
    nombre_chambres INTEGER,
    prix_achat DECIMAL(15,2),
    prix_location_mensuel DECIMAL(10,2),
    charges_mensuelles DECIMAL(10,2),
    description TEXT,
    meuble BOOLEAN DEFAULT FALSE,
    balcon BOOLEAN DEFAULT FALSE,
    parking BOOLEAN DEFAULT FALSE,
    ascenseur BOOLEAN DEFAULT FALSE,
    etage INTEGER,
    annee_construction INTEGER,
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    proprietaire_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    disponible BOOLEAN DEFAULT TRUE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table contrats_location
CREATE TABLE contrats_location (
    id SERIAL PRIMARY KEY,
    bien_id INTEGER NOT NULL REFERENCES biens_immobiliers(id) ON DELETE CASCADE,
    locataire_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    date_debut DATE NOT NULL,
    date_fin DATE,
    loyer_mensuel DECIMAL(10,2) NOT NULL,
    charges_mensuelles DECIMAL(10,2),
    depot_garantie DECIMAL(10,2),
    frais_agence DECIMAL(10,2),
    statut VARCHAR(20) DEFAULT 'actif' CHECK (statut IN ('actif', 'termine', 'suspendu')),
    conditions_particulieres TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table paiements_loyer
CREATE TABLE paiements_loyer (
    id SERIAL PRIMARY KEY,
    contrat_id INTEGER NOT NULL REFERENCES contrats_location(id) ON DELETE CASCADE,
    mois INTEGER NOT NULL CHECK (mois BETWEEN 1 AND 12),
    annee INTEGER NOT NULL CHECK (annee BETWEEN 2020 AND 2030),
    montant_loyer DECIMAL(10,2) NOT NULL,
    montant_charges DECIMAL(10,2),
    date_paiement DATE,
    date_echeance DATE NOT NULL,
    statut VARCHAR(20) DEFAULT 'en_attente' CHECK (statut IN ('en_attente', 'paye', 'retard')),
    mode_paiement VARCHAR(50),
    reference_paiement VARCHAR(100),
    remarques TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table photos_biens
CREATE TABLE photos_biens (
    id SERIAL PRIMARY KEY,
    bien_id INTEGER NOT NULL REFERENCES biens_immobiliers(id) ON DELETE CASCADE,
    nom_fichier VARCHAR(255) NOT NULL,
    nom_original VARCHAR(255),
    principale BOOLEAN DEFAULT FALSE,
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table documents_contrat
CREATE TABLE documents_contrat (
    id SERIAL PRIMARY KEY,
    contrat_id INTEGER NOT NULL REFERENCES contrats_location(id) ON DELETE CASCADE,
    type_document VARCHAR(50) NOT NULL CHECK (type_document IN ('piece_identite', 'photo', 'video', 'audio', 'contrat_signe', 'justificatif', 'autre')),
    nom_fichier VARCHAR(255) NOT NULL,
    nom_original VARCHAR(255) NOT NULL,
    chemin_stockage VARCHAR(500) NOT NULL,
    format_fichier VARCHAR(10) NOT NULL,
    taille_fichier INTEGER NOT NULL,
    description TEXT,
    ajoute_par VARCHAR(100),
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- Index pour améliorer les performances
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
-- Vues utiles
-- =============================================

-- Vue des paiements avec informations complètes
CREATE OR REPLACE VIEW v_paiements_complets AS
SELECT 
    p.id,
    p.mois,
    p.annee,
    p.montant_loyer,
    p.montant_charges,
    p.date_paiement,
    p.date_echeance,
    p.statut,
    p.mode_paiement,
    p.reference_paiement,
    p.remarques,
    c.id as contrat_id,
    c.loyer_mensuel as loyer_contrat,
    loc.nom as locataire_nom,
    loc.prenom as locataire_prenom,
    loc.telephone as locataire_telephone,
    b.titre as bien_titre,
    b.adresse as bien_adresse,
    b.ville as bien_ville,
    prop.nom as proprietaire_nom,
    prop.prenom as proprietaire_prenom
FROM paiements_loyer p
JOIN contrats_location c ON p.contrat_id = c.id
JOIN clients loc ON c.locataire_id = loc.id
JOIN biens_immobiliers b ON c.bien_id = b.id
JOIN clients prop ON b.proprietaire_id = prop.id;

-- Vue des biens avec informations propriétaires
CREATE OR REPLACE VIEW v_biens_complets AS
SELECT 
    b.*,
    c.nom as proprietaire_nom,
    c.prenom as proprietaire_prenom,
    c.telephone as proprietaire_telephone,
    c.email as proprietaire_email,
    COUNT(ct.id) as nb_contrats,
    COUNT(CASE WHEN ct.statut = 'actif' THEN 1 END) as nb_contrats_actifs
FROM biens_immobiliers b
JOIN clients c ON b.proprietaire_id = c.id
LEFT JOIN contrats_location ct ON b.id = ct.bien_id
GROUP BY b.id, c.id;

-- =============================================
-- Fonction utile pour calculer le client d'un paiement
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
-- Triggers pour maintenir la cohérence
-- =============================================

-- Trigger pour mettre à jour la disponibilité des biens
CREATE OR REPLACE FUNCTION update_bien_disponibilite()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' AND NEW.statut = 'actif' THEN
        UPDATE biens_immobiliers SET disponible = FALSE WHERE id = NEW.bien_id;
    ELSIF TG_OP = 'UPDATE' THEN
        IF OLD.statut != 'actif' AND NEW.statut = 'actif' THEN
            UPDATE biens_immobiliers SET disponible = FALSE WHERE id = NEW.bien_id;
        ELSIF OLD.statut = 'actif' AND NEW.statut != 'actif' THEN
            -- Vérifier s'il n'y a plus d'autres contrats actifs
            IF NOT EXISTS (SELECT 1 FROM contrats_location WHERE bien_id = NEW.bien_id AND statut = 'actif' AND id != NEW.id) THEN
                UPDATE biens_immobiliers SET disponible = TRUE WHERE id = NEW.bien_id;
            END IF;
        END IF;
    ELSIF TG_OP = 'DELETE' AND OLD.statut = 'actif' THEN
        -- Vérifier s'il n'y a plus d'autres contrats actifs
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
-- Données d'exemple (optionnel)
-- =============================================

-- Commentez cette section si vous ne voulez pas les données d'exemple

/*
-- Propriétaires exemples
INSERT INTO clients (nom, prenom, email, telephone, type_client, type_piece_identite, numero_piece_identite) VALUES
('OULD AHMED', 'Mohamed', 'mohamed.ahmed@email.mr', '+222 45 67 89 01', 'proprietaire', 'carte_identite', 'CI123456789'),
('MINT SALEM', 'Fatima', 'fatima.salem@email.mr', '+222 45 67 89 02', 'proprietaire', 'carte_identite', 'CI987654321');

-- Locataires exemples  
INSERT INTO clients (nom, prenom, email, telephone, adresse, ville, type_client, type_piece_identite, numero_piece_identite) VALUES
('BA', 'Amadou', 'amadou.ba@email.mr', '+222 45 67 89 03', 'Quartier Sebkha', 'Nouakchott', 'locataire', 'carte_identite', 'CI456789123'),
('DIALLO', 'Aicha', 'aicha.diallo@email.mr', '+222 45 67 89 04', 'Quartier Teyarett', 'Nouakchott', 'locataire', 'passeport', 'PA789123456');

-- Biens immobiliers exemples
INSERT INTO biens_immobiliers (titre, type_bien, adresse, surface, nombre_pieces, nombre_chambres, prix_location_mensuel, charges_mensuelles, proprietaire_id) VALUES
('Appartement 3 pièces Sebkha', 'appartement', 'Rue 456, Quartier Sebkha', 85.50, 3, 2, 45000, 5000, 1),
('Villa familiale Teyarett', 'maison', 'Avenue de la Paix, Teyarett', 120.00, 5, 3, 75000, 8000, 2);

-- Contrats exemples
INSERT INTO contrats_location (bien_id, locataire_id, date_debut, loyer_mensuel, charges_mensuelles, depot_garantie) VALUES
(1, 3, '2025-01-01', 45000, 5000, 90000),
(2, 4, '2025-02-01', 75000, 8000, 150000);

-- Paiements exemples
INSERT INTO paiements_loyer (contrat_id, mois, annee, montant_loyer, montant_charges, date_echeance, statut) VALUES
(1, 1, 2025, 45000, 5000, '2025-01-31', 'paye'),
(1, 2, 2025, 45000, 5000, '2025-02-28', 'paye'),
(2, 2, 2025, 75000, 8000, '2025-02-28', 'paye'),
(2, 3, 2025, 75000, 8000, '2025-03-31', 'en_attente');
*/

-- =============================================
-- Fin de la sauvegarde
-- =============================================

COMMIT;