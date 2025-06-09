"""
Formulaires pour le module comptabilité
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, FloatField, DateField, SelectField, TextAreaField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Optional
from datetime import date


class DepenseForm(FlaskForm):
    """Formulaire pour enregistrer une dépense immobilière"""
    bien_id = SelectField('Bien immobilier', coerce=int, validators=[DataRequired()])
    fournisseur_id = SelectField('Fournisseur', coerce=int, validators=[Optional()])
    type_depense = SelectField('Type de dépense', 
                              choices=[
                                  ('travaux', 'Travaux'),
                                  ('maintenance', 'Maintenance'),
                                  ('reparation', 'Réparation'),
                                  ('taxes_locales', 'Taxes locales'),
                                  ('assurance', 'Assurance'),
                                  ('frais_gestion', 'Frais de gestion'),
                                  ('charges_copropriete', 'Charges de copropriété'),
                                  ('facture_energie', 'Facture énergie'),
                                  ('facture_eau', 'Facture eau'),
                                  ('honoraires', 'Honoraires'),
                                  ('frais_justice', 'Frais de justice'),
                                  ('autre', 'Autre')
                              ],
                              validators=[DataRequired()])
    categorie = SelectField('Catégorie',
                           choices=[
                               ('charge_courante', 'Charge courante'),
                               ('investissement', 'Investissement'),
                               ('reparation', 'Réparation')
                           ],
                           validators=[DataRequired()])
    montant = FloatField('Montant (MRU)', validators=[DataRequired(), NumberRange(min=0)])
    date_depense = DateField('Date de la dépense', validators=[DataRequired()], default=date.today)
    date_paiement = DateField('Date de paiement', validators=[Optional()])
    statut_paiement = SelectField('Statut du paiement',
                                 choices=[
                                     ('en_attente', 'En attente'),
                                     ('paye', 'Payé'),
                                     ('annule', 'Annulé')
                                 ],
                                 default='en_attente',
                                 validators=[DataRequired()])
    mode_paiement = SelectField('Mode de paiement',
                               choices=[
                                   ('', 'Non spécifié'),
                                   ('virement', 'Virement'),
                                   ('cheque', 'Chèque'),
                                   ('especes', 'Espèces'),
                                   ('carte', 'Carte bancaire')
                               ],
                               validators=[Optional()])
    numero_facture = StringField('Numéro de facture', validators=[Optional(), Length(max=100)])
    reference_paiement = StringField('Référence de paiement', validators=[Optional(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=1000)])
    deductible_impots = BooleanField('Déductible des impôts', default=True)
    tva_applicable = BooleanField('TVA applicable')
    montant_tva = FloatField('Montant TVA (MRU)', validators=[Optional(), NumberRange(min=0)])
    justificatif = FileField('Justificatif (facture, reçu)', 
                            validators=[FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Fichiers PDF ou images uniquement!')])
    submit = SubmitField('Enregistrer')

    def __init__(self, *args, **kwargs):
        super(DepenseForm, self).__init__(*args, **kwargs)
        from models import BienImmobilier, Client
        
        # Charger les biens
        self.bien_id.choices = [(0, 'Sélectionnez un bien')] + [
            (bien.id, f"{bien.titre} - {bien.adresse}")
            for bien in BienImmobilier.query.all()
        ]
        
        # Charger les fournisseurs (clients de type fournisseur ou tous les clients)
        self.fournisseur_id.choices = [(0, 'Nouveau fournisseur')] + [
            (client.id, client.nom_complet)
            for client in Client.query.all()
        ]


class EcritureComptableForm(FlaskForm):
    """Formulaire pour saisir une écriture comptable"""
    numero_piece = StringField('Numéro de pièce', validators=[DataRequired(), Length(max=50)])
    date_ecriture = DateField('Date d\'écriture', validators=[DataRequired()], default=date.today)
    date_operation = DateField('Date d\'opération', validators=[DataRequired()], default=date.today)
    compte_debit_id = SelectField('Compte à débiter', coerce=int, validators=[DataRequired()])
    compte_credit_id = SelectField('Compte à créditer', coerce=int, validators=[DataRequired()])
    montant = FloatField('Montant (MRU)', validators=[DataRequired(), NumberRange(min=0)])
    libelle = StringField('Libellé', validators=[DataRequired(), Length(max=500)])
    type_operation = SelectField('Type d\'opération',
                                choices=[
                                    ('loyer', 'Encaissement loyer'),
                                    ('depense', 'Dépense'),
                                    ('achat', 'Achat immobilier'),
                                    ('vente', 'Vente immobilier'),
                                    ('emprunt', 'Emprunt'),
                                    ('remboursement', 'Remboursement'),
                                    ('autre', 'Autre')
                                ],
                                validators=[Optional()])
    bien_id = SelectField('Bien concerné', coerce=int, validators=[Optional()])
    client_id = SelectField('Client concerné', coerce=int, validators=[Optional()])
    reference_externe = StringField('Référence externe', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Enregistrer')

    def __init__(self, *args, **kwargs):
        super(EcritureComptableForm, self).__init__(*args, **kwargs)
        from models import CompteComptable, BienImmobilier, Client
        
        # Charger les comptes comptables
        comptes = CompteComptable.query.filter_by(actif=True).order_by(CompteComptable.numero_compte).all()
        self.compte_debit_id.choices = [(0, 'Sélectionnez un compte')] + [
            (compte.id, f"{compte.numero_compte} - {compte.nom_compte}")
            for compte in comptes
        ]
        self.compte_credit_id.choices = self.compte_debit_id.choices
        
        # Charger les biens
        self.bien_id.choices = [(0, 'Aucun bien spécifique')] + [
            (bien.id, f"{bien.titre} - {bien.adresse}")
            for bien in BienImmobilier.query.all()
        ]
        
        # Charger les clients
        self.client_id.choices = [(0, 'Aucun client spécifique')] + [
            (client.id, client.nom_complet)
            for client in Client.query.all()
        ]


class BudgetForm(FlaskForm):
    """Formulaire pour créer/modifier un budget prévisionnel"""
    bien_id = SelectField('Bien immobilier', coerce=int, validators=[Optional()])
    annee = IntegerField('Année', validators=[DataRequired(), NumberRange(min=2020, max=2040)])
    mois = SelectField('Mois (optionnel pour budget annuel)',
                      choices=[
                          (0, 'Budget annuel'),
                          (1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'),
                          (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'),
                          (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')
                      ],
                      coerce=int,
                      default=0,
                      validators=[Optional()])
    
    # Revenus prévisionnels
    revenus_loyers_prevus = FloatField('Revenus de loyers prévus (MRU)', 
                                      validators=[Optional(), NumberRange(min=0)], default=0)
    autres_revenus_prevus = FloatField('Autres revenus prévus (MRU)', 
                                      validators=[Optional(), NumberRange(min=0)], default=0)
    
    # Dépenses prévisionnelles
    charges_courantes_prevues = FloatField('Charges courantes prévues (MRU)', 
                                          validators=[Optional(), NumberRange(min=0)], default=0)
    travaux_prevus = FloatField('Travaux prévus (MRU)', 
                               validators=[Optional(), NumberRange(min=0)], default=0)
    taxes_impots_prevus = FloatField('Taxes et impôts prévus (MRU)', 
                                    validators=[Optional(), NumberRange(min=0)], default=0)
    assurances_prevues = FloatField('Assurances prévues (MRU)', 
                                   validators=[Optional(), NumberRange(min=0)], default=0)
    frais_gestion_prevus = FloatField('Frais de gestion prévus (MRU)', 
                                     validators=[Optional(), NumberRange(min=0)], default=0)
    
    notes = TextAreaField('Notes et commentaires', validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Enregistrer')

    def __init__(self, *args, **kwargs):
        super(BudgetForm, self).__init__(*args, **kwargs)
        from models import BienImmobilier
        
        # Charger les biens
        self.bien_id.choices = [(0, 'Budget global')] + [
            (bien.id, f"{bien.titre} - {bien.adresse}")
            for bien in BienImmobilier.query.all()
        ]


class CompteComptableForm(FlaskForm):
    """Formulaire pour créer/modifier un compte comptable"""
    numero_compte = StringField('Numéro de compte', validators=[DataRequired(), Length(max=10)])
    nom_compte = StringField('Nom du compte', validators=[DataRequired(), Length(max=200)])
    type_compte = SelectField('Type de compte',
                             choices=[
                                 ('actif', 'Actif'),
                                 ('passif', 'Passif'),
                                 ('charge', 'Charge'),
                                 ('produit', 'Produit'),
                                 ('resultat', 'Résultat')
                             ],
                             validators=[DataRequired()])
    sous_type = SelectField('Sous-type',
                           choices=[
                               ('', 'Aucun'),
                               ('immobilisation', 'Immobilisation'),
                               ('creance', 'Créance'),
                               ('dette', 'Dette'),
                               ('tresorerie', 'Trésorerie'),
                               ('capitaux', 'Capitaux'),
                               ('exploitation', 'Exploitation')
                           ],
                           validators=[Optional()])
    compte_parent_id = SelectField('Compte parent', coerce=int, validators=[Optional()])
    actif = BooleanField('Compte actif', default=True)
    submit = SubmitField('Enregistrer')

    def __init__(self, *args, **kwargs):
        super(CompteComptableForm, self).__init__(*args, **kwargs)
        from models import CompteComptable
        
        # Charger les comptes parents possibles
        comptes = CompteComptable.query.filter_by(actif=True).order_by(CompteComptable.numero_compte).all()
        self.compte_parent_id.choices = [(0, 'Aucun parent')] + [
            (compte.id, f"{compte.numero_compte} - {compte.nom_compte}")
            for compte in comptes
        ]


class RapportComptableForm(FlaskForm):
    """Formulaire pour générer des rapports comptables"""
    type_rapport = SelectField('Type de rapport',
                              choices=[
                                  ('balance', 'Balance comptable'),
                                  ('compte_resultat', 'Compte de résultat'),
                                  ('bilan', 'Bilan'),
                                  ('journal', 'Journal général'),
                                  ('grand_livre', 'Grand livre'),
                                  ('tableau_flux', 'Tableau des flux de trésorerie')
                              ],
                              validators=[DataRequired()])
    date_debut = DateField('Date de début', validators=[DataRequired()])
    date_fin = DateField('Date de fin', validators=[DataRequired()])
    bien_id = SelectField('Bien spécifique', coerce=int, validators=[Optional()])
    format_export = SelectField('Format d\'export',
                               choices=[
                                   ('html', 'Affichage web'),
                                   ('pdf', 'PDF'),
                                   ('excel', 'Excel'),
                                   ('csv', 'CSV')
                               ],
                               default='html',
                               validators=[DataRequired()])
    submit = SubmitField('Générer le rapport')

    def __init__(self, *args, **kwargs):
        super(RapportComptableForm, self).__init__(*args, **kwargs)
        from models import BienImmobilier
        
        # Charger les biens
        self.bien_id.choices = [(0, 'Tous les biens')] + [
            (bien.id, f"{bien.titre} - {bien.adresse}")
            for bien in BienImmobilier.query.all()
        ]