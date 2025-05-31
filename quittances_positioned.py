"""
Générateur de quittances avec positionnement précis basé sur le modèle fourni
Reproduit exactement la mise en page du modèle quittance_model.pdf
"""
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from io import BytesIO

# Dimensions de la page A4 en points
PAGE_WIDTH, PAGE_HEIGHT = A4

def generer_quittance_positioned_pdf(paiement):
    """
    Génère une quittance avec positionnement précis selon le modèle
    
    Args:
        paiement: Instance de PaiementLoyer
        
    Returns:
        BytesIO: Buffer contenant le PDF généré
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Dessiner la quittance avec positionnement précis
    _dessiner_quittance_positionnee(c, paiement)
    
    c.save()
    buffer.seek(0)
    return buffer

def _dessiner_quittance_positionnee(c, paiement):
    """Dessine la quittance avec positionnement précis selon le modèle"""
    
    # En-tête avec logo et informations société (coin supérieur droit)
    _dessiner_entete_societe(c)
    
    # Numéro de quittance (coin supérieur gauche)
    _dessiner_numero_quittance(c, paiement)
    
    # Titre principal bilingue
    _dessiner_titre_principal(c)
    
    # Section LOCATAIRE
    _dessiner_section_locataire(c, paiement)
    
    # Champs de paiement
    _dessiner_champs_paiement(c, paiement)
    
    # Section commentaire
    _dessiner_section_commentaire(c, paiement)
    
    # Signature et informations bailleur
    _dessiner_signature_bailleur(c)
    
    # Lieu et date
    _dessiner_lieu_date(c)
    
    # Texte légal en bas
    _dessiner_texte_legal(c)

def _dessiner_entete_societe(c):
    """Dessine l'en-tête de la société en haut à droite"""
    # Position : coin supérieur droit
    x_base = PAGE_WIDTH - 4*cm
    y_base = PAGE_HEIGHT - 2*cm
    
    # Logo/Nom de société
    c.setFont("Helvetica-Bold", 14)
    c.drawRightString(x_base, y_base, "Laser")
    
    c.setFont("Helvetica", 10)
    c.drawRightString(x_base, y_base - 12, "Gestion de Patrimoine")

def _dessiner_numero_quittance(c, paiement):
    """Dessine le numéro de quittance en haut à gauche"""
    # Position : coin supérieur gauche
    x = 2*cm
    y = PAGE_HEIGHT - 2*cm
    
    c.setFont("Helvetica-Bold", 12)
    numero = f"N° {paiement.id:04d}"
    c.drawString(x, y, numero)

def _dessiner_titre_principal(c):
    """Dessine le titre principal bilingue"""
    # Position : centre, sous l'en-tête
    y = PAGE_HEIGHT - 4*cm
    
    # Titre français
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredText(PAGE_WIDTH/2, y, "QUITTANCE DE LOYER")
    
    # Titre arabe (à droite)
    c.setFont("Helvetica-Bold", 14)
    c.drawRightString(PAGE_WIDTH - 2*cm, y, "وصل إيجار")

def _dessiner_section_locataire(c, paiement):
    """Dessine la section LOCATAIRE"""
    # Position de départ
    x = 2*cm
    y = PAGE_HEIGHT - 6*cm
    
    # Titre de section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, "LOCATAIRE")
    
    # Titre arabe à droite
    c.drawRightString(PAGE_WIDTH - 2*cm, y, "مستأجر")
    
    # Cadre pour les informations locataire
    rect_x = x
    rect_y = y - 3*cm
    rect_width = PAGE_WIDTH - 4*cm
    rect_height = 2.5*cm
    
    c.rect(rect_x, rect_y, rect_width, rect_height)
    
    # Informations du locataire
    client = paiement.client
    c.setFont("Helvetica", 11)
    text_y = rect_y + rect_height - 0.5*cm
    
    # Nom complet
    nom_complet = f"{client.prenom} {client.nom}"
    c.drawString(rect_x + 0.3*cm, text_y, nom_complet)
    
    # Adresse
    if client.adresse:
        c.drawString(rect_x + 0.3*cm, text_y - 0.4*cm, client.adresse)
    
    # Téléphone et email
    if client.telephone:
        c.drawString(rect_x + 0.3*cm, text_y - 0.8*cm, f"Tél: {client.telephone}")
    
    if client.email:
        c.drawString(rect_x + 0.3*cm, text_y - 1.2*cm, f"Email: {client.email}")

def _dessiner_champs_paiement(c, paiement):
    """Dessine les champs de paiement avec positionnement précis"""
    # Position de départ
    x = 2*cm
    y_start = PAGE_HEIGHT - 10*cm
    
    # Espacement entre les lignes
    line_height = 0.8*cm
    
    # Police normale
    c.setFont("Helvetica", 11)
    
    # Champ 1: Versement effectué par
    y = y_start
    c.drawString(x, y, "Versement effectué par")
    c.drawRightString(PAGE_WIDTH - 2*cm, y, "المبلغ المستلم من طرف")
    
    # Ligne pour remplir
    line_x = x + 4*cm
    line_width = PAGE_WIDTH - line_x - 6*cm
    c.line(line_x, y - 2, line_x + line_width, y - 2)
    
    # Valeur : nom du client
    client = paiement.client
    nom_complet = f"{client.prenom} {client.nom}"
    c.drawString(line_x + 0.2*cm, y, nom_complet)
    
    # Champ 2: Montant payé
    y -= line_height
    c.drawString(x, y, "Montant payé")
    c.drawRightString(PAGE_WIDTH - 2*cm, y, "المبلغ المدفوع")
    
    # Ligne et valeur
    c.line(line_x, y - 2, line_x + line_width, y - 2)
    montant_total = paiement.montant_loyer + (paiement.montant_charges or 0)
    c.drawString(line_x + 0.2*cm, y, f"{montant_total:,.0f} MRU")
    
    # Champ 3: En date du
    y -= line_height
    c.drawString(x, y, "En date du")
    c.drawRightString(PAGE_WIDTH - 2*cm, y, "تاريخ السداد")
    
    # Ligne et valeur
    c.line(line_x, y - 2, line_x + line_width, y - 2)
    if paiement.date_paiement:
        date_str = paiement.date_paiement.strftime('%d/%m/%Y')
        c.drawString(line_x + 0.2*cm, y, date_str)
    
    # Champ 4: Loyer du bien suivant
    y -= line_height
    c.drawString(x, y, "Loyer du bien suivant")
    c.drawRightString(PAGE_WIDTH - 2*cm, y, "الإيجار المتعلق بـ")
    
    # Ligne et valeur
    c.line(line_x, y - 2, line_x + line_width, y - 2)
    bien = paiement.bien
    c.drawString(line_x + 0.2*cm, y, bien.titre)
    
    # Champ 5: Au titre du mois de
    y -= line_height
    c.drawString(x, y, "Au titre du mois de")
    c.drawRightString(PAGE_WIDTH - 2*cm, y, "عن إيجار شهر")
    
    # Ligne et valeur
    c.line(line_x, y - 2, line_x + line_width, y - 2)
    mois_noms = [
        'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
        'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
    ]
    mois_str = f"{mois_noms[paiement.mois - 1]} {paiement.annee}"
    c.drawString(line_x + 0.2*cm, y, mois_str)

def _dessiner_section_commentaire(c, paiement):
    """Dessine la section commentaire"""
    # Position
    x = 2*cm
    y = PAGE_HEIGHT - 16*cm
    
    # Titre de section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, "COMMENTAIRE")
    c.drawRightString(PAGE_WIDTH - 2*cm, y, "ملاحظات إضافية")
    
    # Cadre pour commentaires
    rect_width = PAGE_WIDTH - 4*cm
    rect_height = 2*cm
    c.rect(x, y - rect_height - 0.2*cm, rect_width, rect_height)
    
    # Contenu du commentaire
    if paiement.remarques:
        c.setFont("Helvetica", 10)
        c.drawString(x + 0.3*cm, y - 0.7*cm, paiement.remarques[:100])

def _dessiner_signature_bailleur(c):
    """Dessine la section signature du bailleur"""
    # Position : centre-droite
    x = PAGE_WIDTH/2 + 1*cm
    y = PAGE_HEIGHT - 20*cm
    
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredText(x, y, "Mariem CHEIKH BRAHIM")
    
    c.setFont("Helvetica", 10)
    c.drawCentredText(x, y - 0.5*cm, "Bailleur المؤجر")
    c.drawCentredText(x, y - 1*cm, "+222 45 25 25 25")

def _dessiner_lieu_date(c):
    """Dessine le lieu et la date"""
    # Position : bas gauche
    x = 2*cm
    y = PAGE_HEIGHT - 22*cm
    
    c.setFont("Helvetica", 10)
    date_actuelle = datetime.now().strftime('%d/%m/%Y')
    c.drawString(x, y, f"Fait à : Nouakchott")
    c.drawString(x, y - 0.4*cm, f"le {date_actuelle}")

def _dessiner_texte_legal(c):
    """Dessine le texte légal en bas de page"""
    # Position : bas de page
    x = 1*cm
    y = 3*cm
    width = PAGE_WIDTH - 2*cm
    
    # Texte français
    c.setFont("Helvetica", 8)
    texte_fr = ("La présente quittance atteste que le locataire est entièrement libéré de sa dette au titre du loyer et des charges pour la période "
                "mentionnée. Elle ne vaut pas titre d'occupation, et ne présume pas du paiement des périodes antérieures ou ultérieures. Elle est "
                "établie sous réserve de l'encaissement effectif des sommes dues.")
    
    # Diviser le texte en lignes
    mots = texte_fr.split()
    lignes = []
    ligne_actuelle = ""
    
    for mot in mots:
        test_ligne = ligne_actuelle + " " + mot if ligne_actuelle else mot
        if c.stringWidth(test_ligne, "Helvetica", 8) < width:
            ligne_actuelle = test_ligne
        else:
            if ligne_actuelle:
                lignes.append(ligne_actuelle)
            ligne_actuelle = mot
    
    if ligne_actuelle:
        lignes.append(ligne_actuelle)
    
    # Dessiner les lignes
    for i, ligne in enumerate(lignes):
        c.drawString(x, y - i * 0.3*cm, ligne)
    
    # Texte arabe (simplifié)
    y_arabe = y - len(lignes) * 0.3*cm - 0.5*cm
    texte_ar = "تشهد هذه الإيصال بأن المستأجر قد أوفى بجميع التزاماته المتعلقة بالإيجار والرسوم للفترة المحددة"
    c.drawString(x, y_arabe, texte_ar)

def generer_nom_fichier_quittance_positioned(paiement):
    """Génère un nom de fichier pour la quittance positionnée"""
    client_nom = paiement.client.nom.replace(' ', '_')
    mois_str = f"{paiement.mois:02d}"
    annee = paiement.annee
    
    return f"quittance_{client_nom}_{mois_str}_{annee}.pdf"