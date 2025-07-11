import os
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (
    StringField, TextAreaField, FloatField, IntegerField, 
    SelectField, DateField, BooleanField, SubmitField, HiddenField
)
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional
from wtforms.widgets import TextArea
from datetime import date
from models import Client, BienImmobilier, ContratLocation
from app import db


class ClientForm(FlaskForm):
    """Formulaire pour ajouter/éditer un client"""
    nom = StringField('Nom', validators=[DataRequired(), Length(max=100)])
    prenom = StringField('Prénom', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    telephone = StringField('Téléphone', validators=[Length(max=20)])
    adresse = StringField('Adresse', validators=[Length(max=200)])
    ville = StringField('Ville', validators=[Length(max=100)])
    code_postal = StringField('Code postal', validators=[Length(max=10)])
    type_client = SelectField('Type de client', 
                             choices=[
                                 ('proprietaire', 'Propriétaire'),
                                 ('locataire', 'Locataire'),
                                 ('acheteur', 'Acheteur')
                             ],
                             validators=[DataRequired()])
    type_piece_identite = SelectField('Type de pièce d\'identité',
                                     choices=[
                                         ('carte_identite', 'Carte d\'identité'),
                                         ('passeport', 'Passeport')
                                     ],
                                     validators=[DataRequired()])
    numero_piece_identite = StringField('Numéro de pièce d\'identité', 
                                       validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Enregistrer')


class BienForm(FlaskForm):
    """Formulaire pour ajouter/éditer un bien immobilier"""
    titre = StringField('Titre', validators=[DataRequired(), Length(max=200)])
    type_bien = SelectField('Type de bien',
                           choices=[
                               ('appartement', 'Appartement'),
                               ('maison', 'Maison'),
                               ('terrain', 'Terrain'),
                               ('local', 'Local commercial'),
                               ('bureau', 'Bureau'),
                               ('garage', 'Garage')
                           ],
                           validators=[DataRequired()])
    adresse = StringField('Adresse', validators=[DataRequired(), Length(max=200)])
    ville = StringField('Ville', validators=[DataRequired(), Length(max=100)], default='Nouakchott')
    code_postal = StringField('Code postal', validators=[Optional(), Length(max=10)])
    surface = FloatField('Surface (m²)', validators=[DataRequired(), NumberRange(min=0)])
    nombre_pieces = IntegerField('Nombre de pièces', validators=[Optional(), NumberRange(min=0)])
    nombre_chambres = IntegerField('Nombre de chambres', validators=[Optional(), NumberRange(min=0)])
    prix_achat = FloatField('Prix d\'achat (€)', validators=[Optional(), NumberRange(min=0)])
    prix_location_mensuel = FloatField('Loyer mensuel (€)', validators=[Optional(), NumberRange(min=0)])
    charges_mensuelles = FloatField('Charges mensuelles (€)', validators=[Optional(), NumberRange(min=0)])
    description = TextAreaField('Description', widget=TextArea())
    meuble = BooleanField('Meublé')
    balcon = BooleanField('Balcon')
    parking = BooleanField('Parking')
    ascenseur = BooleanField('Ascenseur')
    etage = IntegerField('Étage', validators=[Optional()])
    annee_construction = IntegerField('Année de construction', validators=[Optional(), NumberRange(min=1800, max=2030)])
    latitude = FloatField('Latitude', validators=[Optional(), NumberRange(min=-90, max=90)])
    longitude = FloatField('Longitude', validators=[Optional(), NumberRange(min=-180, max=180)])
    
    # Compteurs SOMELEC (Électricité)
    somelec_numero_compteur = StringField('N° compteur SOMELEC', validators=[Optional(), Length(max=50)])
    somelec_code_abonnement = StringField('Code abonnement SOMELEC', validators=[Optional(), Length(max=50)])
    somelec_index_actuel = FloatField('Index actuel électricité (kWh)', validators=[Optional(), NumberRange(min=0)])
    somelec_date_releve = DateField('Date relevé électricité', validators=[Optional()])
    
    # Compteurs SNDE (Eau)
    snde_numero_compteur = StringField('N° compteur SNDE', validators=[Optional(), Length(max=50)])
    snde_code_abonnement = StringField('Code abonnement SNDE', validators=[Optional(), Length(max=50)])
    snde_index_actuel = FloatField('Index actuel eau (m³)', validators=[Optional(), NumberRange(min=0)])
    snde_date_releve = DateField('Date relevé eau', validators=[Optional()])
    
    proprietaire_id = SelectField('Propriétaire', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Enregistrer')
    
    def __init__(self, *args, **kwargs):
        super(BienForm, self).__init__(*args, **kwargs)
        # Charger les propriétaires
        proprietaires = Client.query.filter_by(type_client='proprietaire').all()
        self.proprietaire_id.choices = [
            (client.id, f"{client.prenom} {client.nom}") 
            for client in proprietaires
        ]
        
        # Définir EL KHALEF comme propriétaire par défaut
        if not self.proprietaire_id.data:
            el_khalef = Client.query.filter_by(nom='EL KHALEF', type_client='proprietaire').first()
            if el_khalef:
                self.proprietaire_id.data = el_khalef.id


class PhotoForm(FlaskForm):
    """Formulaire pour uploader des photos"""
    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images seulement!')
    ])
    principale = BooleanField('Photo principale')
    submit = SubmitField('Ajouter la photo')


class ContratForm(FlaskForm):
    """Formulaire pour ajouter/éditer un contrat de location"""
    bien_id = SelectField('Bien immobilier', coerce=int, validators=[DataRequired()])
    locataire_id = SelectField('Locataire', coerce=int, validators=[DataRequired()])
    date_debut = DateField('Date de début', validators=[DataRequired()])
    date_fin = DateField('Date de fin', validators=[Optional()])
    loyer_mensuel = FloatField('Loyer mensuel (€)', validators=[DataRequired(), NumberRange(min=0)])
    charges_mensuelles = FloatField('Charges mensuelles (€)', validators=[Optional(), NumberRange(min=0)])
    depot_garantie = FloatField('Dépôt de garantie (€)', validators=[Optional(), NumberRange(min=0)])
    frais_agence = FloatField('Frais d\'agence (€)', validators=[Optional(), NumberRange(min=0)])
    statut = SelectField('Statut',
                        choices=[
                            ('actif', 'Actif'),
                            ('termine', 'Terminé'),
                            ('suspendu', 'Suspendu')
                        ],
                        default='actif',
                        validators=[DataRequired()])
    conditions_particulieres = TextAreaField('Conditions particulières', widget=TextArea())
    
    # Compteurs SOMELEC (Électricité)
    somelec_numero_compteur = StringField('N° compteur SOMELEC', validators=[Optional(), Length(max=50)])
    somelec_code_abonnement = StringField('Code abonnement SOMELEC', validators=[Optional(), Length(max=50)])
    somelec_index_initial = FloatField('Index initial électricité (kWh)', validators=[Optional(), NumberRange(min=0)])
    somelec_date_branchement = DateField('Date branchement électricité', validators=[Optional()])
    somelec_quitus_precedent = BooleanField('Quitus du locataire précédent obtenu')
    
    # Compteurs SNDE (Eau)
    snde_numero_compteur = StringField('N° compteur SNDE', validators=[Optional(), Length(max=50)])
    snde_code_abonnement = StringField('Code abonnement SNDE', validators=[Optional(), Length(max=50)])
    snde_index_initial = FloatField('Index initial eau (m³)', validators=[Optional(), NumberRange(min=0)])
    snde_date_branchement = DateField('Date branchement eau', validators=[Optional()])
    snde_quitus_precedent = BooleanField('Quitus du locataire précédent obtenu')
    
    submit = SubmitField('Enregistrer')
    
    def __init__(self, *args, **kwargs):
        super(ContratForm, self).__init__(*args, **kwargs)
        # Charger les biens disponibles (qui n'ont pas de contrat actif)
        biens_avec_contrat_actif = db.session.query(ContratLocation.bien_id).filter(
            ContratLocation.statut == 'actif'
        )
        
        biens_disponibles = BienImmobilier.query.filter(
            ~BienImmobilier.id.in_(biens_avec_contrat_actif)
        ).all()
        
        self.bien_id.choices = [
            (bien.id, f"{bien.titre} - {bien.adresse_complete}") 
            for bien in biens_disponibles
        ]
        # Charger les locataires
        self.locataire_id.choices = [
            (client.id, f"{client.prenom} {client.nom}") 
            for client in Client.query.filter_by(type_client='locataire').all()
        ]


class PaiementForm(FlaskForm):
    """Formulaire pour enregistrer un paiement de loyer"""
    client_id = SelectField('Client qui paie', coerce=int, validators=[DataRequired()])
    bien_id = SelectField('Bien payé', coerce=int, validators=[DataRequired()])
    contrat_id = HiddenField('Contrat ID', validators=[DataRequired()])
    mois = SelectField('Mois',
                      choices=[
                          (1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'),
                          (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'),
                          (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')
                      ],
                      coerce=int,
                      validators=[DataRequired()])
    annee = IntegerField('Année', validators=[DataRequired(), NumberRange(min=2020, max=2030)])
    montant_loyer = FloatField('Montant du loyer (€)', validators=[DataRequired(), NumberRange(min=0)])
    montant_charges = FloatField('Montant des charges (€)', validators=[Optional(), NumberRange(min=0)])
    date_paiement = DateField('Date de paiement', validators=[Optional()])
    date_echeance = DateField('Date d\'échéance', validators=[DataRequired()])
    statut = SelectField('Statut',
                        choices=[
                            ('en_attente', 'En attente'),
                            ('paye', 'Payé'),
                            ('retard', 'En retard')
                        ],
                        default='en_attente',
                        validators=[DataRequired()])
    mode_paiement = SelectField('Mode de paiement',
                               choices=[
                                   ('', 'Non spécifié'),
                                   ('virement', 'Virement'),
                                   ('cheque', 'Chèque'),
                                   ('especes', 'Espèces'),
                                   ('prelevement', 'Prélèvement')
                               ],
                               validators=[Optional()])
    reference_paiement = StringField('Référence de paiement', validators=[Length(max=100)])
    remarques = TextAreaField('Remarques', widget=TextArea())
    submit = SubmitField('Enregistrer')
    
    def __init__(self, *args, **kwargs):
        super(PaiementForm, self).__init__(*args, **kwargs)
        # Charger les clients locataires
        self.client_id.choices = [(0, 'Sélectionnez un client')] + [
            (client.id, f"{client.prenom} {client.nom}") 
            for client in Client.query.filter_by(type_client='locataire').all()
        ]
        # Initialiser les biens vides (sera rempli via JavaScript)
        self.bien_id.choices = [(0, 'Sélectionnez d\'abord un client')]


class SearchForm(FlaskForm):
    """Formulaire de recherche pour les biens"""
    q = StringField('Recherche', validators=[Optional()])
    type_bien = SelectField('Type',
                           choices=[
                               ('', 'Tous types'),
                               ('appartement', 'Appartement'),
                               ('maison', 'Maison'),
                               ('terrain', 'Terrain'),
                               ('local', 'Local commercial'),
                               ('bureau', 'Bureau'),
                               ('garage', 'Garage')
                           ],
                           validators=[Optional()])
    ville = StringField('Ville', validators=[Optional()])
    prix_min = FloatField('Prix min (€)', validators=[Optional(), NumberRange(min=0)])
    prix_max = FloatField('Prix max (€)', validators=[Optional(), NumberRange(min=0)])
    surface_min = FloatField('Surface min (m²)', validators=[Optional(), NumberRange(min=0)])
    surface_max = FloatField('Surface max (m²)', validators=[Optional(), NumberRange(min=0)])
    disponible_uniquement = BooleanField('Disponibles uniquement')
    submit = SubmitField('Rechercher')


class DocumentContratForm(FlaskForm):
    """Formulaire pour ajouter des documents aux contrats"""
    contrat_id = SelectField('Contrat', coerce=int, validators=[DataRequired()])
    type_document = SelectField('Type de document',
                               choices=[
                                   ('piece_identite', 'Pièce d\'identité'),
                                   ('photo', 'Photo'),
                                   ('video', 'Vidéo'),
                                   ('audio', 'Audio (WhatsApp, etc.)'),
                                   ('contrat_signe', 'Contrat signé'),
                                   ('justificatif', 'Justificatif'),
                                   ('autre', 'Autre')
                               ],
                               validators=[DataRequired()])
    fichier = FileField('Fichier', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx', 
                    'mp4', 'avi', 'mov', 'mp3', 'wav', 'ogg', 'm4a'], 
                   'Format de fichier non autorisé!')
    ])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Ajouter le document')
    
    def __init__(self, *args, edit_mode=False, **kwargs):
        super(DocumentContratForm, self).__init__(*args, **kwargs)
        # Charger tous les contrats pour l'édition, seulement les actifs pour l'ajout
        if edit_mode:
            contrats = ContratLocation.query.all()
        else:
            contrats = ContratLocation.query.filter_by(statut='actif').all()
            
        self.contrat_id.choices = [
            (contrat.id, f"Contrat #{contrat.id} - {contrat.locataire.nom} {contrat.locataire.prenom}") 
            for contrat in contrats
        ]
        
        # En mode édition, le fichier n'est pas requis
        if edit_mode:
            self.fichier.validators = [
                FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx', 
                            'mp4', 'avi', 'mov', 'mp3', 'wav', 'ogg', 'm4a'], 
                           'Format de fichier non autorisé!')
            ]
            self.submit.label.text = 'Enregistrer les modifications'
        else:
            from flask_wtf.file import FileRequired
            self.fichier.validators = [
                FileRequired('Veuillez sélectionner un fichier'),
                FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx', 
                            'mp4', 'avi', 'mov', 'mp3', 'wav', 'ogg', 'm4a'], 
                           'Format de fichier non autorisé!')
            ]


class ReleveCompteurForm(FlaskForm):
    """Formulaire pour enregistrer un relevé de compteur SOMELEC ou SNDE"""
    contrat_id = SelectField('Contrat de location', coerce=int, validators=[DataRequired()])
    type_compteur = SelectField('Type de compteur',
                               choices=[
                                   ('somelec', 'SOMELEC - Électricité'),
                                   ('snde', 'SNDE - Eau')
                               ],
                               validators=[DataRequired()])
    numero_compteur = StringField('Numéro du compteur', validators=[DataRequired(), Length(max=50)])
    code_abonnement = StringField('Code d\'abonnement', validators=[Optional(), Length(max=50)])
    date_releve = DateField('Date du relevé', validators=[DataRequired()])
    index_precedent = FloatField('Index précédent', validators=[Optional(), NumberRange(min=0)], default=0)
    index_actuel = FloatField('Index actuel', validators=[DataRequired(), NumberRange(min=0)])
    montant_facture = FloatField('Montant de la facture (MRU)', validators=[Optional(), NumberRange(min=0)])
    statut_paiement = SelectField('Statut du paiement',
                                 choices=[
                                     ('en_attente', 'En attente'),
                                     ('paye_proprietaire', 'Payé par le propriétaire'),
                                     ('paye_locataire', 'Payé par le locataire')
                                 ],
                                 default='en_attente',
                                 validators=[DataRequired()])
    remarques = TextAreaField('Remarques', validators=[Optional()])
    submit = SubmitField('Enregistrer le relevé')
    
    def __init__(self, *args, **kwargs):
        super(ReleveCompteurForm, self).__init__(*args, **kwargs)
        # Charger les contrats actifs
        contrats = ContratLocation.query.filter_by(statut='actif').all()
        self.contrat_id.choices = [
            (contrat.id, f"{contrat.bien.titre} - {contrat.locataire.nom_complet}")
            for contrat in contrats
        ]
