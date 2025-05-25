from datetime import datetime, date
from app import db
from sqlalchemy import func


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
    type_piece_identite = db.Column(db.String(20), nullable=False)  # carte_identite, passeport
    numero_piece_identite = db.Column(db.String(50), nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    biens_proprietaire = db.relationship('BienImmobilier', backref='proprietaire', lazy=True)
    contrats_locataire = db.relationship('ContratLocation', backref='locataire', lazy=True)
    
    def __repr__(self):
        return f'<Client {self.prenom} {self.nom}>'
    
    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"


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
    disponible = db.Column(db.Boolean, default=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Clé étrangère
    proprietaire_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    
    # Relations
    photos = db.relationship('PhotoBien', backref='bien', lazy=True, cascade='all, delete-orphan')
    contrats = db.relationship('ContratLocation', backref='bien', lazy=True)
    
    def __repr__(self):
        return f'<BienImmobilier {self.titre}>'
    
    @property
    def adresse_complete(self):
        return f"{self.adresse}, {self.code_postal} {self.ville}"
    
    @property
    def photo_principale(self):
        photo = PhotoBien.query.filter_by(bien_id=self.id, principale=True).first()
        return photo.nom_fichier if photo else None


class PhotoBien(db.Model):
    """Modèle pour les photos des biens"""
    __tablename__ = 'photos_biens'
    
    id = db.Column(db.Integer, primary_key=True)
    nom_fichier = db.Column(db.String(255), nullable=False)
    nom_original = db.Column(db.String(255))
    principale = db.Column(db.Boolean, default=False)
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Clé étrangère
    bien_id = db.Column(db.Integer, db.ForeignKey('biens_immobiliers.id'), nullable=False)
    
    def __repr__(self):
        return f'<PhotoBien {self.nom_fichier}>'


class ContratLocation(db.Model):
    """Modèle pour les contrats de location"""
    __tablename__ = 'contrats_location'
    
    id = db.Column(db.Integer, primary_key=True)
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date)
    loyer_mensuel = db.Column(db.Float, nullable=False)
    charges_mensuelles = db.Column(db.Float, default=0)
    depot_garantie = db.Column(db.Float, default=0)
    frais_agence = db.Column(db.Float, default=0)
    statut = db.Column(db.String(20), default='actif')  # actif, termine, suspendu
    conditions_particulieres = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Clés étrangères
    bien_id = db.Column(db.Integer, db.ForeignKey('biens_immobiliers.id'), nullable=False)
    locataire_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    
    # Relations
    paiements = db.relationship('PaiementLoyer', backref='contrat', lazy=True)
    
    def __repr__(self):
        return f'<ContratLocation {self.id} - {self.bien.titre}>'
    
    @property
    def loyer_total(self):
        return self.loyer_mensuel + self.charges_mensuelles
    
    @property
    def est_actif(self):
        return self.statut == 'actif' and (not self.date_fin or self.date_fin > date.today())


class PaiementLoyer(db.Model):
    """Modèle pour les paiements de loyer"""
    __tablename__ = 'paiements_loyer'
    
    id = db.Column(db.Integer, primary_key=True)
    mois = db.Column(db.Integer, nullable=False)  # 1-12
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
    
    # Clé étrangère
    contrat_id = db.Column(db.Integer, db.ForeignKey('contrats_location.id'), nullable=False)
    
    def __repr__(self):
        return f'<PaiementLoyer {self.mois}/{self.annee} - {self.statut}>'
    
    @property
    def montant_total(self):
        return self.montant_loyer + self.montant_charges
    
    @property
    def periode(self):
        mois_noms = [
            'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
            'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
        ]
        return f"{mois_noms[self.mois - 1]} {self.annee}"
    
    @property
    def est_en_retard(self):
        return self.statut != 'paye' and self.date_echeance < date.today()


# Fonctions utilitaires pour les statistiques du dashboard
def get_dashboard_stats():
    """Récupère les statistiques pour le dashboard"""
    total_biens = BienImmobilier.query.count()
    biens_loues = BienImmobilier.query.join(ContratLocation).filter(
        ContratLocation.statut == 'actif'
    ).count()
    biens_disponibles = total_biens - biens_loues
    
    total_clients = Client.query.count()
    
    revenus_mois = db.session.query(
        func.sum(PaiementLoyer.montant_loyer + PaiementLoyer.montant_charges)
    ).filter(
        PaiementLoyer.statut == 'paye',
        PaiementLoyer.mois == date.today().month,
        PaiementLoyer.annee == date.today().year
    ).scalar() or 0
    
    paiements_en_retard = PaiementLoyer.query.filter(
        PaiementLoyer.statut != 'paye',
        PaiementLoyer.date_echeance < date.today()
    ).count()
    
    return {
        'total_biens': total_biens,
        'biens_loues': biens_loues,
        'biens_disponibles': biens_disponibles,
        'total_clients': total_clients,
        'revenus_mois': float(revenus_mois),
        'paiements_en_retard': paiements_en_retard
    }
