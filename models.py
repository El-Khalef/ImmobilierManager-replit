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
    
    # Relations
    proprietaire = db.relationship('Client', backref='biens_possedes')
    
    def __repr__(self):
        return f'<BienImmobilier {self.titre}>'
    
    @property
    def adresse_complete(self):
        return f"{self.adresse}, {self.code_postal} {self.ville}"


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
    
    return {
        'total_biens': total_biens,
        'biens_loues': biens_loues,
        'biens_disponibles': total_biens - biens_loues,
        'total_clients': total_clients,
        'revenus_mois': revenus_mois,
        'paiements_en_retard': paiements_en_retard
    }