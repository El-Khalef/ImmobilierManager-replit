"""
Générateur de quittances utilisant un modèle PDF existant
Superpose les données de la base sur le modèle fourni
"""
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import os

# Dimensions de la page A4 en points
PAGE_WIDTH, PAGE_HEIGHT = A4

def generer_quittance_avec_template_pdf(paiement, chemin_template=None):
    """
    Génère une quittance en utilisant le modèle PDF existant et y superpose les données
    
    Args:
        paiement: Instance de PaiementLoyer
        chemin_template: Chemin vers le modèle PDF (optionnel)
        
    Returns:
        BytesIO: Buffer contenant le PDF généré
    """
    
    # Si aucun template spécifié, créer une page avec seulement les données
    if not chemin_template or not os.path.exists(chemin_template):
        return _generer_donnees_seules(paiement)
    
    try:
        # Lire le modèle PDF existant
        with open(chemin_template, 'rb') as template_file:
            template_reader = PdfReader(template_file)
            template_page = template_reader.pages[0]
            
            # Créer un overlay avec les données
            overlay_buffer = _creer_overlay_donnees(paiement)
            overlay_reader = PdfReader(overlay_buffer)
            overlay_page = overlay_reader.pages[0]
            
            # Fusionner le template avec l'overlay
            template_page.merge_page(overlay_page)
            
            # Créer le PDF final
            writer = PdfWriter()
            writer.add_page(template_page)
            
            output_buffer = BytesIO()
            writer.write(output_buffer)
            output_buffer.seek(0)
            
            return output_buffer
            
    except Exception as e:
        # En cas d'erreur, retourner les données seules
        return _generer_donnees_seules(paiement)

def _creer_overlay_donnees(paiement):
    """Crée un PDF transparent avec seulement les données positionnées"""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Définir les positions exactes selon votre modèle
    positions = _obtenir_positions_champs()
    
    # Configuration de base pour le texte
    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0, 0, 0)  # Noir pour le texte
    
    # 1. NUMÉRO DE QUITTANCE
    numero = f"{paiement.id:04d}"
    c.drawString(positions['numero']['x'], positions['numero']['y'], numero)
    
    # 2. INFORMATIONS DU LOCATAIRE
    client = paiement.client
    nom_complet = f"{client.prenom} {client.nom}"
    
    # Nom dans la section locataire
    c.drawString(positions['nom_locataire']['x'], positions['nom_locataire']['y'], nom_complet)
    
    # Adresse si disponible
    if client.adresse:
        c.setFont("Helvetica", 10)
        c.drawString(positions['adresse_locataire']['x'], positions['adresse_locataire']['y'], client.adresse)
    
    # Téléphone si disponible
    if client.telephone:
        c.drawString(positions['telephone_locataire']['x'], positions['telephone_locataire']['y'], f"Tél: {client.telephone}")
    
    # 3. CHAMPS DE PAIEMENT (sur les lignes du modèle)
    c.setFont("Helvetica", 11)
    
    # Versement effectué par
    c.drawString(positions['versement_par']['x'], positions['versement_par']['y'], nom_complet)
    
    # Montant payé
    montant_total = paiement.montant_loyer + (paiement.montant_charges or 0)
    c.drawString(positions['montant']['x'], positions['montant']['y'], f"{montant_total:,.0f} MRU")
    
    # Date de paiement
    if paiement.date_paiement:
        date_str = paiement.date_paiement.strftime('%d/%m/%Y')
        c.drawString(positions['date_paiement']['x'], positions['date_paiement']['y'], date_str)
    
    # Bien loué
    bien = paiement.bien
    c.drawString(positions['bien_loue']['x'], positions['bien_loue']['y'], bien.titre)
    
    # Mois concerné
    mois_noms = [
        'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
        'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
    ]
    mois_str = f"{mois_noms[paiement.mois - 1]} {paiement.annee}"
    c.drawString(positions['mois']['x'], positions['mois']['y'], mois_str)
    
    # 4. COMMENTAIRES
    if paiement.remarques:
        c.setFont("Helvetica", 10)
        # Limiter le commentaire pour qu'il tienne dans l'espace prévu
        commentaire = paiement.remarques[:80]
        c.drawString(positions['commentaire']['x'], positions['commentaire']['y'], commentaire)
    
    # 5. DATE ACTUELLE
    c.setFont("Helvetica", 10)
    date_actuelle = datetime.now().strftime('%d/%m/%Y')
    c.drawString(positions['date_actuelle']['x'], positions['date_actuelle']['y'], date_actuelle)
    
    # 6. INFORMATIONS SUPPLÉMENTAIRES (optionnelles)
    c.setFont("Helvetica", 9)
    
    # Mode de paiement
    if paiement.mode_paiement:
        c.drawString(positions['mode_paiement']['x'], positions['mode_paiement']['y'], paiement.mode_paiement)
    
    # Référence de paiement
    if paiement.reference_paiement:
        c.drawString(positions['reference']['x'], positions['reference']['y'], paiement.reference_paiement)
    
    c.save()
    buffer.seek(0)
    return buffer

def _obtenir_positions_champs():
    """
    Définit les positions exactes pour chaque champ selon votre modèle
    Ces coordonnées doivent être ajustées selon votre modèle PDF exact
    """
    return {
        # Numéro de quittance (après "N° ")
        'numero': {'x': 3.5*cm, 'y': PAGE_HEIGHT - 2*cm},
        
        # Section LOCATAIRE
        'nom_locataire': {'x': 2.5*cm, 'y': PAGE_HEIGHT - 8.5*cm},
        'adresse_locataire': {'x': 2.5*cm, 'y': PAGE_HEIGHT - 9*cm},
        'telephone_locataire': {'x': 2.5*cm, 'y': PAGE_HEIGHT - 9.5*cm},
        
        # Champs de paiement (sur les lignes prévues)
        'versement_par': {'x': 6*cm, 'y': PAGE_HEIGHT - 11.5*cm},
        'montant': {'x': 6*cm, 'y': PAGE_HEIGHT - 12.3*cm},
        'date_paiement': {'x': 6*cm, 'y': PAGE_HEIGHT - 13.1*cm},
        'bien_loue': {'x': 6*cm, 'y': PAGE_HEIGHT - 13.9*cm},
        'mois': {'x': 6*cm, 'y': PAGE_HEIGHT - 14.7*cm},
        
        # Section commentaire
        'commentaire': {'x': 2.5*cm, 'y': PAGE_HEIGHT - 17*cm},
        
        # Informations en bas
        'date_actuelle': {'x': 8*cm, 'y': PAGE_HEIGHT - 22.5*cm},
        'mode_paiement': {'x': 2*cm, 'y': PAGE_HEIGHT - 24*cm},
        'reference': {'x': 8*cm, 'y': PAGE_HEIGHT - 24*cm}
    }

def _generer_donnees_seules(paiement):
    """Génère un PDF avec seulement les données (si pas de modèle)"""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Titre simple
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2*cm, PAGE_HEIGHT - 2*cm, "DONNÉES DE QUITTANCE")
    
    # Données du paiement
    c.setFont("Helvetica", 12)
    y = PAGE_HEIGHT - 4*cm
    
    client = paiement.client
    bien = paiement.bien
    
    donnees = [
        f"Numéro: {paiement.id:04d}",
        f"Locataire: {client.prenom} {client.nom}",
        f"Adresse: {client.adresse or 'Non spécifiée'}",
        f"Téléphone: {client.telephone or 'Non spécifié'}",
        f"Montant: {paiement.montant_loyer + (paiement.montant_charges or 0):,.0f} MRU",
        f"Date: {paiement.date_paiement.strftime('%d/%m/%Y') if paiement.date_paiement else 'Non spécifiée'}",
        f"Bien: {bien.titre}",
        f"Période: {['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'][paiement.mois - 1]} {paiement.annee}",
        f"Commentaire: {paiement.remarques or 'Aucun'}"
    ]
    
    for donnee in donnees:
        c.drawString(2*cm, y, donnee)
        y -= 0.8*cm
    
    c.save()
    buffer.seek(0)
    return buffer

def generer_nom_fichier_quittance_template(paiement):
    """Génère un nom de fichier pour la quittance template"""
    client_nom = paiement.client.nom.replace(' ', '_')
    mois_str = f"{paiement.mois:02d}"
    annee = paiement.annee
    
    return f"quittance_template_{client_nom}_{mois_str}_{annee}.pdf"