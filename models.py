"""
Version simplifiée des modèles sans conflits SQLAlchemy
"""
from datetime import datetime, date
from app import db


def formater_montant(montant):
    """Formate un montant avec des espaces comme séparateurs de milliers"""
    if montant is None:
        return "0"
    return f"{montant:,.2f}".replace(",", " ").replace(".", ",").rstrip("0").rstrip(",")


class Client(db.Model):
    """Modèle pour les clients (propriétaires, locataires, acheteurs)"""
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telephone = db.Column(db.String(20))
    adresse = db.Column(db.String(200))
    ville = db.Column(db.String(100))
    code_postal = db.Column(db.String(10))
    type_client = db.Column(db.String(20), nullable=False)  # proprietaire, locataire, acheteur
    type_piece_identite = db.Column(db.String(50), nullable=False)  # carte_identite, passeport
    numero_piece_identite = db.Column(db.String(50), nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Client {self.prenom} {self.nom}>'
    
    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"
    
    @property
    def adresse_complete(self):
        parts = [self.adresse, self.ville]
        if self.code_postal:
            parts.insert(1, self.code_postal)
        return ", ".join(filter(None, parts))


class BienImmobilier(db.Model):
    """Modèle pour les biens immobiliers"""
    __tablename__ = 'biens_immobiliers'
    
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    type_bien = db.Column(db.String(50), nullable=False)  # appartement, maison, terrain, local
    adresse = db.Column(db.String(200), nullable=False)
    ville = db.Column(db.String(100), nullable=False)
    code_postal = db.Column(db.String(10), nullable=False)
    surface = db.Column(db.Float, nullable=False)
    nombre_pieces = db.Column(db.Integer)
    nombre_chambres = db.Column(db.Integer)
    prix_achat = db.Column(db.Float)
    prix_location_mensuel = db.Column(db.Float)
    charges_mensuelles = db.Column(db.Float, default=0)
    description = db.Column(db.Text)
    meuble = db.Column(db.Boolean, default=False)
    balcon = db.Column(db.Boolean, default=False)
    parking = db.Column(db.Boolean, default=False)
    ascenseur = db.Column(db.Boolean, default=False)
    etage = db.Column(db.Integer)
    annee_construction = db.Column(db.Integer)
    proprietaire_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Coordonnées géographiques
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    # Informations compteurs et abonnements
    somelec_numero_compteur = db.Column(db.String(50), nullable=True)  # Numéro compteur électricité
    somelec_code_abonnement = db.Column(db.String(50), nullable=True)  # Code abonnement SOMELEC
    somelec_index_actuel = db.Column(db.Float, nullable=True)  # Index actuel du compteur électricité
    somelec_date_releve = db.Column(db.Date, nullable=True)  # Date du dernier relevé
    
    snde_numero_compteur = db.Column(db.String(50), nullable=True)  # Numéro compteur eau
    snde_code_abonnement = db.Column(db.String(50), nullable=True)  # Code abonnement SNDE
    snde_index_actuel = db.Column(db.Float, nullable=True)  # Index actuel du compteur eau
    snde_date_releve = db.Column(db.Date, nullable=True)  # Date du dernier relevé
    
    # Relations
    proprietaire = db.relationship('Client', backref='biens_possedes')
    
    def __repr__(self):
        return f'<BienImmobilier {self.titre}>'
    
    @property
    def adresse_complete(self):
        return f"{self.adresse}, {self.code_postal} {self.ville}"
    
    @property
    def has_coordinates(self):
        """Vérifie si le bien a des coordonnées GPS"""
        return self.latitude is not None and self.longitude is not None
    
    def set_coordinates(self, lat, lng):
        """Définit les coordonnées GPS du bien"""
        self.latitude = float(lat) if lat else None
        self.longitude = float(lng) if lng else None


class ContratLocation(db.Model):
    """Modèle pour les contrats de location"""
    __tablename__ = 'contrats_location'
    
    id = db.Column(db.Integer, primary_key=True)
    bien_id = db.Column(db.Integer, db.ForeignKey('biens_immobiliers.id'), nullable=False)
    locataire_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date)
    loyer_mensuel = db.Column(db.Float, nullable=False)
    charges_mensuelles = db.Column(db.Float, default=0)
    depot_garantie = db.Column(db.Float, default=0)
    frais_agence = db.Column(db.Float, default=0)
    statut = db.Column(db.String(20), default='actif')  # actif, termine, suspendu
    conditions_particulieres = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    bien = db.relationship('BienImmobilier', backref='contrats')
    locataire = db.relationship('Client', backref='contrats_locataire')
    
    def __repr__(self):
        return f'<ContratLocation {self.id}>'
    
    @property
    def loyer_total(self):
        return self.loyer_mensuel + (self.charges_mensuelles or 0)


class PaiementLoyer(db.Model):
    """Modèle pour les paiements de loyer"""
    __tablename__ = 'paiements_loyer'
    
    id = db.Column(db.Integer, primary_key=True)
    contrat_id = db.Column(db.Integer, db.ForeignKey('contrats_location.id'), nullable=False)
    mois = db.Column(db.Integer, nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    montant_loyer = db.Column(db.Float, nullable=False)
    montant_charges = db.Column(db.Float, default=0)
    date_paiement = db.Column(db.Date)
    date_echeance = db.Column(db.Date, nullable=False)
    statut = db.Column(db.String(20), default='en_attente')  # en_attente, paye, retard
    mode_paiement = db.Column(db.String(50))  # virement, cheque, especes, prelevement
    reference_paiement = db.Column(db.String(100))
    remarques = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    contrat = db.relationship('ContratLocation', backref='paiements')
    
    def __repr__(self):
        return f'<PaiementLoyer {self.mois}/{self.annee} - {self.statut}>'
    
    @property
    def montant_total(self):
        return self.montant_loyer + (self.montant_charges or 0)


class ReleveCompteur(db.Model):
    """Modèle pour l'historique des relevés de compteurs SOMELEC et SNDE"""
    __tablename__ = 'releves_compteurs'
    
    id = db.Column(db.Integer, primary_key=True)
    bien_id = db.Column(db.Integer, db.ForeignKey('biens_immobiliers.id'), nullable=False)
    type_compteur = db.Column(db.String(20), nullable=False)  # 'somelec' ou 'snde'
    numero_compteur = db.Column(db.String(50), nullable=False)
    code_abonnement = db.Column(db.String(50))
    date_releve = db.Column(db.Date, nullable=False)
    index_precedent = db.Column(db.Float, default=0)
    index_actuel = db.Column(db.Float, nullable=False)
    consommation = db.Column(db.Float)  # Calculée automatiquement
    montant_facture = db.Column(db.Float)  # Montant de la facture si disponible
    statut_paiement = db.Column(db.String(20), default='en_attente')  # en_attente, paye_proprietaire, paye_locataire
    locataire_id = db.Column(db.Integer, db.ForeignKey('clients.id'))  # Locataire responsable du paiement
    remarques = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    bien = db.relationship('BienImmobilier', backref='releves_compteurs')
    locataire = db.relationship('Client', backref='releves_compteurs')
    
    def __repr__(self):
        return f'<ReleveCompteur {self.type_compteur} - {self.bien.titre}>'
    
    @property
    def unite_mesure(self):
        """Retourne l'unité de mesure selon le type de compteur"""
        return 'kWh' if self.type_compteur == 'somelec' else 'm³'
    
    def calculer_consommation(self):
        """Calcule la consommation depuis le dernier relevé"""
        if self.index_actuel and self.index_precedent:
            self.consommation = self.index_actuel - self.index_precedent
        return self.consommation or 0
    
    @property
    def client(self):
        """Accès au client via le contrat"""
        return self.contrat.locataire if self.contrat else None
    
    @property 
    def bien(self):
        """Accès au bien via le contrat"""
        return self.contrat.bien if self.contrat else None
    
    @property
    def periode(self):
        mois_noms = [
            'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
            'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
        ]
        return f"{mois_noms[self.mois - 1]} {self.annee}"


class PhotoBien(db.Model):
    """Modèle pour les photos des biens immobiliers"""
    __tablename__ = 'photos_biens'
    
    id = db.Column(db.Integer, primary_key=True)
    bien_id = db.Column(db.Integer, db.ForeignKey('biens_immobiliers.id'), nullable=False)
    nom_fichier = db.Column(db.String(255), nullable=False)
    chemin_fichier = db.Column(db.String(500), nullable=False)
    principale = db.Column(db.Boolean, default=False)
    date_upload = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PhotoBien {self.nom_fichier}>'


class DocumentContrat(db.Model):
    """Modèle pour les documents liés aux contrats"""
    __tablename__ = 'documents_contrat'
    
    id = db.Column(db.Integer, primary_key=True)
    contrat_id = db.Column(db.Integer, db.ForeignKey('contrats_location.id'), nullable=False)
    nom_fichier = db.Column(db.String(255), nullable=False)
    nom_original = db.Column(db.String(255))
    type_document = db.Column(db.String(50), nullable=False)
    format_fichier = db.Column(db.String(10))
    taille_fichier = db.Column(db.Integer)
    chemin_stockage = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)
    ajoute_par = db.Column(db.String(100))
    
    # Relations
    contrat = db.relationship('ContratLocation', backref='documents')
    
    def __repr__(self):
        return f'<DocumentContrat {self.nom_fichier}>'


# =============================================
# MODÈLES COMPTABLES
# =============================================

class CompteComptable(db.Model):
    """Plan comptable - Comptes pour la comptabilité"""
    __tablename__ = 'comptes_comptables'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_compte = db.Column(db.String(10), unique=True, nullable=False)  # Ex: 411001, 512000
    nom_compte = db.Column(db.String(200), nullable=False)
    type_compte = db.Column(db.String(50), nullable=False)  # actif, passif, charge, produit, resultat
    sous_type = db.Column(db.String(50))  # immobilisation, creance, dette, etc.
    compte_parent_id = db.Column(db.Integer, db.ForeignKey('comptes_comptables.id'))
    actif = db.Column(db.Boolean, default=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    compte_parent = db.relationship('CompteComptable', remote_side=[id], backref='sous_comptes')
    ecritures_debit = db.relationship('EcritureComptable', 
                                    foreign_keys='EcritureComptable.compte_debit_id',
                                    backref='compte_debit')
    ecritures_credit = db.relationship('EcritureComptable',
                                     foreign_keys='EcritureComptable.compte_credit_id', 
                                     backref='compte_credit')
    
    def __repr__(self):
        return f'<Compte {self.numero_compte} - {self.nom_compte}>'
    
    @property
    def solde_debit(self):
        """Calcule le solde débiteur du compte"""
        total_debit = db.session.query(db.func.sum(EcritureComptable.montant)).filter(
            EcritureComptable.compte_debit_id == self.id
        ).scalar() or 0
        return total_debit
    
    @property
    def solde_credit(self):
        """Calcule le solde créditeur du compte"""
        total_credit = db.session.query(db.func.sum(EcritureComptable.montant)).filter(
            EcritureComptable.compte_credit_id == self.id
        ).scalar() or 0
        return total_credit
    
    @property
    def solde_net(self):
        """Calcule le solde net du compte"""
        return self.solde_debit - self.solde_credit


class EcritureComptable(db.Model):
    """Écritures comptables - Journal général"""
    __tablename__ = 'ecritures_comptables'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_piece = db.Column(db.String(50), nullable=False)  # Numéro de la pièce justificative
    date_ecriture = db.Column(db.Date, nullable=False, default=date.today)
    date_operation = db.Column(db.Date, nullable=False)  # Date réelle de l'opération
    compte_debit_id = db.Column(db.Integer, db.ForeignKey('comptes_comptables.id'), nullable=False)
    compte_credit_id = db.Column(db.Integer, db.ForeignKey('comptes_comptables.id'), nullable=False)
    montant = db.Column(db.Numeric(15, 2), nullable=False)
    libelle = db.Column(db.String(500), nullable=False)
    reference_externe = db.Column(db.String(100))  # Référence vers paiement_loyer, depense, etc.
    type_operation = db.Column(db.String(50))  # loyer, depense, vente, achat, etc.
    bien_id = db.Column(db.Integer, db.ForeignKey('biens_immobiliers.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    validee = db.Column(db.Boolean, default=False)
    saisie_par = db.Column(db.String(100))
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    bien = db.relationship('BienImmobilier', backref='ecritures_comptables')
    client = db.relationship('Client', backref='ecritures_comptables')
    
    def __repr__(self):
        return f'<Ecriture {self.numero_piece} - {self.montant} MRU>'


class DepenseImmobiliere(db.Model):
    """Dépenses liées aux biens immobiliers"""
    __tablename__ = 'depenses_immobilieres'
    
    id = db.Column(db.Integer, primary_key=True)
    bien_id = db.Column(db.Integer, db.ForeignKey('biens_immobiliers.id'), nullable=False)
    fournisseur_id = db.Column(db.Integer, db.ForeignKey('clients.id'))  # Utilise la table clients
    type_depense = db.Column(db.String(100), nullable=False)  # travaux, maintenance, taxes, assurance, etc.
    categorie = db.Column(db.String(50), nullable=False)  # charge_courante, investissement, reparation
    montant = db.Column(db.Numeric(10, 2), nullable=False)
    date_depense = db.Column(db.Date, nullable=False)
    date_paiement = db.Column(db.Date)
    statut_paiement = db.Column(db.String(20), default='en_attente')  # en_attente, paye, annule
    mode_paiement = db.Column(db.String(50))  # virement, cheque, especes
    numero_facture = db.Column(db.String(100))
    reference_paiement = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)
    justificatif_path = db.Column(db.String(500))  # Chemin vers le fichier justificatif
    deductible_impots = db.Column(db.Boolean, default=True)
    tva_applicable = db.Column(db.Boolean, default=False)
    montant_tva = db.Column(db.Numeric(10, 2), default=0)
    ecriture_comptable_id = db.Column(db.Integer, db.ForeignKey('ecritures_comptables.id'))
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    bien = db.relationship('BienImmobilier', backref='depenses')
    fournisseur = db.relationship('Client', backref='depenses_fournies')
    ecriture = db.relationship('EcritureComptable', backref='depense_source')
    
    def __repr__(self):
        return f'<Depense {self.type_depense} - {self.montant} MRU>'
    
    @property
    def montant_total(self):
        """Montant total incluant la TVA"""
        return self.montant + (self.montant_tva or 0)


class BudgetPrevisionnel(db.Model):
    """Budget prévisionnel par bien ou global"""
    __tablename__ = 'budgets_previsionnels'
    
    id = db.Column(db.Integer, primary_key=True)
    bien_id = db.Column(db.Integer, db.ForeignKey('biens_immobiliers.id'))  # NULL = budget global
    annee = db.Column(db.Integer, nullable=False)
    mois = db.Column(db.Integer)  # NULL = budget annuel
    
    # Prévisions de revenus
    revenus_loyers_prevus = db.Column(db.Numeric(15, 2), default=0)
    autres_revenus_prevus = db.Column(db.Numeric(15, 2), default=0)
    
    # Prévisions de dépenses
    charges_courantes_prevues = db.Column(db.Numeric(10, 2), default=0)
    travaux_prevus = db.Column(db.Numeric(10, 2), default=0)
    taxes_impots_prevus = db.Column(db.Numeric(10, 2), default=0)
    assurances_prevues = db.Column(db.Numeric(10, 2), default=0)
    frais_gestion_prevus = db.Column(db.Numeric(10, 2), default=0)
    
    notes = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    bien = db.relationship('BienImmobilier', backref='budgets')
    
    @property
    def total_revenus_prevus(self):
        return (self.revenus_loyers_prevus or 0) + (self.autres_revenus_prevus or 0)
    
    @property
    def total_depenses_prevues(self):
        return sum(filter(None, [
            self.charges_courantes_prevues,
            self.travaux_prevus,
            self.taxes_impots_prevus,
            self.assurances_prevues,
            self.frais_gestion_prevus
        ]))
    
    @property
    def resultat_previsionnel(self):
        return self.total_revenus_prevus - self.total_depenses_prevues


def get_dashboard_stats():
    """Récupère les statistiques pour le dashboard"""
    total_biens = BienImmobilier.query.count()
    biens_loues = db.session.query(BienImmobilier).join(ContratLocation).filter(
        ContratLocation.statut == 'actif'
    ).count()
    
    total_clients = Client.query.count()
    
    # Calcul du revenu du mois actuel
    mois_actuel = datetime.now().month
    annee_actuelle = datetime.now().year
    
    revenus_mois = db.session.query(db.func.sum(PaiementLoyer.montant_loyer + PaiementLoyer.montant_charges)).filter(
        PaiementLoyer.mois == mois_actuel,
        PaiementLoyer.annee == annee_actuelle,
        PaiementLoyer.statut == 'paye'
    ).scalar() or 0
    
    # Calcul des paiements en retard
    paiements_en_retard = PaiementLoyer.query.filter(
        PaiementLoyer.statut != 'paye',
        PaiementLoyer.date_echeance < date.today()
    ).count()
    
    # Calcul des dépenses du mois
    depenses_mois = db.session.query(db.func.sum(DepenseImmobiliere.montant)).filter(
        db.extract('month', DepenseImmobiliere.date_depense) == mois_actuel,
        db.extract('year', DepenseImmobiliere.date_depense) == annee_actuelle,
        DepenseImmobiliere.statut_paiement == 'paye'
    ).scalar() or 0
    
    return {
        'total_biens': total_biens,
        'biens_loues': biens_loues,
        'biens_disponibles': total_biens - biens_loues,
        'total_clients': total_clients,
        'revenus_mois': revenus_mois,
        'depenses_mois': depenses_mois,
        'resultat_mois': revenus_mois - depenses_mois,
        'paiements_en_retard': paiements_en_retard
    }


def initialiser_plan_comptable():
    """Initialise le plan comptable de base pour l'immobilier"""
    comptes_base = [
        # CLASSE 1 - COMPTES DE CAPITAUX
        ('10', 'CAPITAL ET RESERVES', 'passif', 'capitaux'),
        ('101', 'Capital', 'passif', 'capitaux'),
        ('12', 'RESULTAT DE L\'EXERCICE', 'resultat', 'capitaux'),
        
        # CLASSE 2 - COMPTES D'IMMOBILISATIONS
        ('21', 'IMMOBILISATIONS CORPORELLES', 'actif', 'immobilisation'),
        ('213', 'Constructions', 'actif', 'immobilisation'),
        ('2131', 'Immeubles de rapport', 'actif', 'immobilisation'),
        
        # CLASSE 4 - COMPTES DE TIERS
        ('41', 'CLIENTS ET COMPTES RATTACHES', 'actif', 'creance'),
        ('411', 'Clients', 'actif', 'creance'),
        ('4111', 'Locataires', 'actif', 'creance'),
        ('42', 'PERSONNEL', 'passif', 'dette'),
        ('44', 'ETAT ET COLLECTIVITES', 'actif', 'creance'),
        ('401', 'Fournisseurs', 'passif', 'dette'),
        
        # CLASSE 5 - COMPTES FINANCIERS
        ('51', 'BANQUES', 'actif', 'tresorerie'),
        ('512', 'Banques', 'actif', 'tresorerie'),
        ('53', 'CAISSE', 'actif', 'tresorerie'),
        ('531', 'Caisse', 'actif', 'tresorerie'),
        
        # CLASSE 6 - COMPTES DE CHARGES
        ('61', 'SERVICES EXTERIEURS', 'charge', 'exploitation'),
        ('615', 'Entretien et réparations', 'charge', 'exploitation'),
        ('616', 'Primes d\'assurance', 'charge', 'exploitation'),
        ('622', 'Rémunérations d\'intermédiaires', 'charge', 'exploitation'),
        ('63', 'IMPOTS ET TAXES', 'charge', 'exploitation'),
        ('635', 'Impôts et taxes directs', 'charge', 'exploitation'),
        
        # CLASSE 7 - COMPTES DE PRODUITS
        ('70', 'VENTES', 'produit', 'exploitation'),
        ('701', 'Ventes de marchandises', 'produit', 'exploitation'),
        ('75', 'AUTRES PRODUITS', 'produit', 'exploitation'),
        ('751', 'Revenus immobiliers', 'produit', 'exploitation'),
        ('7511', 'Loyers perçus', 'produit', 'exploitation'),
    ]
    
    for numero, nom, type_compte, sous_type in comptes_base:
        compte_existant = CompteComptable.query.filter_by(numero_compte=numero).first()
        if not compte_existant:
            nouveau_compte = CompteComptable(
                numero_compte=numero,
                nom_compte=nom,
                type_compte=type_compte,
                sous_type=sous_type
            )
            db.session.add(nouveau_compte)
    
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False