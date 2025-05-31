"""
Générateur de quittances par superposition de données sur modèle PDF
Utilise le modèle existant et y ajoute uniquement les données dynamiques de la base
"""
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.pdfgen import canvas
from io import BytesIO
import os

# Dimensions de la page A4 en points
PAGE_WIDTH, PAGE_HEIGHT = A4

def generer_quittance_overlay_pdf(paiement):
    """
    Génère une quittance en superposant les données sur un modèle vierge
    
    Args:
        paiement: Instance de PaiementLoyer
        
    Returns:
        BytesIO: Buffer contenant le PDF généré
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Superposer uniquement les données dynamiques
    _superposer_donnees_dynamiques(c, paiement)
    
    c.save()
    buffer.seek(0)
    return buffer

def _superposer_donnees_dynamiques(c, paiement):
    """Superpose uniquement les données de la base de données sur le modèle"""
    
    # Configuration de base pour le texte
    c.setFont("Helvetica", 11)
    
    # 1. NUMÉRO DE QUITTANCE (en haut à gauche)
    numero = f"{paiement.id:04d}"
    c.drawString(3.5*cm, PAGE_HEIGHT - 2*cm, numero)
    
    # 2. INFORMATIONS DU LOCATAIRE (dans le cadre LOCATAIRE)
    client = paiement.client
    x_locataire = 2.5*cm
    y_locataire_base = PAGE_HEIGHT - 8.5*cm
    
    # Nom complet du locataire
    nom_complet = f"{client.prenom} {client.nom}"
    c.drawString(x_locataire, y_locataire_base, nom_complet)
    
    # Adresse du locataire
    if client.adresse:
        c.drawString(x_locataire, y_locataire_base - 0.4*cm, client.adresse)
    
    # Téléphone du locataire
    if client.telephone:
        c.drawString(x_locataire, y_locataire_base - 0.8*cm, f"Tél: {client.telephone}")
    
    # Email du locataire
    if client.email:
        c.drawString(x_locataire, y_locataire_base - 1.2*cm, f"Email: {client.email}")
    
    # 3. CHAMPS DE PAIEMENT (sur les lignes prévues)
    x_donnees = 6*cm  # Position X pour les données sur les lignes
    y_base_champs = PAGE_HEIGHT - 11*cm
    espacement = 0.8*cm
    
    # Versement effectué par (nom du client)
    c.drawString(x_donnees, y_base_champs, nom_complet)
    
    # Montant payé
    montant_total = paiement.montant_loyer + (paiement.montant_charges or 0)
    c.drawString(x_donnees, y_base_champs - espacement, f"{montant_total:,.0f} MRU")
    
    # Date de paiement
    if paiement.date_paiement:
        date_str = paiement.date_paiement.strftime('%d/%m/%Y')
        c.drawString(x_donnees, y_base_champs - 2*espacement, date_str)
    
    # Bien loué
    bien = paiement.bien
    c.drawString(x_donnees, y_base_champs - 3*espacement, bien.titre)
    
    # Mois concerné
    mois_noms = [
        'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
        'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
    ]
    mois_str = f"{mois_noms[paiement.mois - 1]} {paiement.annee}"
    c.drawString(x_donnees, y_base_champs - 4*espacement, mois_str)
    
    # 4. COMMENTAIRES (dans la section commentaire)
    if paiement.remarques:
        c.setFont("Helvetica", 10)
        y_commentaire = PAGE_HEIGHT - 17*cm
        # Limiter à 100 caractères pour tenir dans le cadre
        commentaire = paiement.remarques[:100]
        c.drawString(2.5*cm, y_commentaire, commentaire)
    
    # 5. DATE ACTUELLE (en bas à gauche)
    c.setFont("Helvetica", 10)
    date_actuelle = datetime.now().strftime('%d/%m/%Y')
    c.drawString(2*cm, PAGE_HEIGHT - 22*cm, date_actuelle)
    
    # 6. DÉTAILS SUPPLÉMENTAIRES (optionnels)
    c.setFont("Helvetica", 9)
    
    # Mode de paiement (si spécifié)
    if paiement.mode_paiement:
        c.drawString(2*cm, PAGE_HEIGHT - 23*cm, f"Mode: {paiement.mode_paiement}")
    
    # Référence de paiement (si spécifiée)
    if paiement.reference_paiement:
        c.drawString(8*cm, PAGE_HEIGHT - 23*cm, f"Réf: {paiement.reference_paiement}")

def generer_quittance_overlay_avec_fond_pdf(paiement, chemin_modele=None):
    """
    Version avancée qui superpose les données sur un PDF modèle existant
    (nécessite PyPDF2 ou pdfrw - non implémenté pour l'instant)
    """
    # Cette fonction pourrait être développée pour utiliser votre PDF modèle
    # comme arrière-plan et y superposer les données
    pass

def generer_nom_fichier_quittance_overlay(paiement):
    """Génère un nom de fichier pour la quittance overlay"""
    client_nom = paiement.client.nom.replace(' ', '_')
    mois_str = f"{paiement.mois:02d}"
    annee = paiement.annee
    
    return f"quittance_overlay_{client_nom}_{mois_str}_{annee}.pdf"

# Fonction utilitaire pour ajuster les positions si nécessaire
def ajuster_positions_pour_modele():
    """
    Retourne un dictionnaire des positions exactes pour chaque champ
    Ces positions peuvent être ajustées selon votre modèle exact
    """
    positions = {
        'numero_quittance': {'x': 3.5*cm, 'y': PAGE_HEIGHT - 2*cm},
        'nom_locataire': {'x': 2.5*cm, 'y': PAGE_HEIGHT - 8.5*cm},
        'versement_par': {'x': 6*cm, 'y': PAGE_HEIGHT - 11*cm},
        'montant': {'x': 6*cm, 'y': PAGE_HEIGHT - 11.8*cm},
        'date_paiement': {'x': 6*cm, 'y': PAGE_HEIGHT - 12.6*cm},
        'bien_loue': {'x': 6*cm, 'y': PAGE_HEIGHT - 13.4*cm},
        'mois': {'x': 6*cm, 'y': PAGE_HEIGHT - 14.2*cm},
        'commentaire': {'x': 2.5*cm, 'y': PAGE_HEIGHT - 17*cm},
        'date_actuelle': {'x': 2*cm, 'y': PAGE_HEIGHT - 22*cm}
    }
    return positions