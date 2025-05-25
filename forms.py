import os
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (
    StringField, TextAreaField, FloatField, IntegerField, 
    SelectField, DateField, BooleanField, SubmitField, HiddenField
)
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional
from wtforms.widgets import TextArea
from models import Client, BienImmobilier, ContratLocation


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
    submit = SubmitField('Enregistrer')
    
    def __init__(self, *args, **kwargs):
        super(ContratForm, self).__init__(*args, **kwargs)
        # Charger les biens disponibles
        self.bien_id.choices = [
            (bien.id, f"{bien.titre} - {bien.adresse_complete}") 
            for bien in BienImmobilier.query.filter_by(disponible=True).all()
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
        FileRequired('Veuillez sélectionner un fichier'),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx', 
                    'mp4', 'avi', 'mov', 'mp3', 'wav', 'ogg', 'm4a'], 
                   'Format de fichier non autorisé!')
    ])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Ajouter le document')
    
    def __init__(self, *args, **kwargs):
        super(DocumentContratForm, self).__init__(*args, **kwargs)
        # Charger les contrats actifs
        contrats = ContratLocation.query.filter_by(statut='actif').all()
        self.contrat_id.choices = [
            (contrat.id, f"Contrat #{contrat.id} - {contrat.locataire.nom_complet}") 
            for contrat in contrats
        ]
