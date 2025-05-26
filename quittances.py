"""
Module pour la génération de quittances de loyer en PDF
"""
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO

def generer_quittance_pdf(paiement):
    """
    Génère une quittance de loyer en PDF pour un paiement donné
    
    Args:
        paiement: Instance de PaiementLoyer
        
    Returns:
        BytesIO: Buffer contenant le PDF généré
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, 
                           topMargin=2*cm, bottomMargin=2*cm)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=30,
        textColor=colors.darkblue
    )
    
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_LEFT,
        spaceAfter=12
    )
    
    content_style = ParagraphStyle(
        'Content',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_LEFT,
        spaceAfter=8
    )
    
    # Contenu du document
    story = []
    
    # Informations de la société bailleuse en en-tête
    bailleur_style = ParagraphStyle(
        'Bailleur',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    contact_style = ParagraphStyle(
        'Contact',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=4
    )
    
    story.append(Paragraph("SOCIÉTÉ LASER SERVICES", bailleur_style))
    story.append(Paragraph("Représentant : Mariem CHEIKH BRAHIM", contact_style))
    story.append(Paragraph("Téléphone : 36317881", contact_style))
    story.append(Paragraph("Email : hadramimr84@gmail.com", contact_style))
    story.append(Spacer(1, 20))
    
    # Titre
    story.append(Paragraph("QUITTANCE DE LOYER", title_style))
    story.append(Spacer(1, 20))
    
    # Récupération du contrat pour les informations suivantes
    contrat = paiement.contrat
    
    story.append(Spacer(1, 10))
    
    # Informations du locataire
    locataire = contrat.locataire
    story.append(Paragraph("<b>LOCATAIRE :</b>", header_style))
    story.append(Paragraph(f"{locataire.nom} {locataire.prenom}", content_style))
    if locataire.adresse:
        story.append(Paragraph(f"{locataire.adresse}", content_style))
        story.append(Paragraph(f"{locataire.code_postal or ''} {locataire.ville or 'Nouakchott'}", content_style))
    if locataire.telephone:
        story.append(Paragraph(f"Tél : {locataire.telephone}", content_style))
    if locataire.email:
        story.append(Paragraph(f"Email : {locataire.email}", content_style))
    
    story.append(Spacer(1, 20))
    
    # Informations du bien
    bien = contrat.bien
    story.append(Paragraph("<b>BIEN LOUÉ :</b>", header_style))
    story.append(Paragraph(f"Désignation : {bien.titre} ({bien.type_bien})", content_style))
    story.append(Paragraph(f"Adresse : {bien.adresse_complete}", content_style))
    if bien.surface:
        story.append(Paragraph(f"Surface : {bien.surface} m²", content_style))
    
    story.append(Spacer(1, 20))
    
    # Détails du paiement
    mois_noms = ['', 'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
                 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    
    story.append(Paragraph("<b>DÉTAILS DU PAIEMENT :</b>", header_style))
    
    # Tableau des détails
    data = [
        ['Période', f"{mois_noms[paiement.mois]} {paiement.annee}"],
        ['Loyer', f"{paiement.montant_loyer:,.0f} €".replace(',', ' ')],
    ]
    
    if paiement.montant_charges and paiement.montant_charges > 0:
        data.append(['Charges', f"{paiement.montant_charges:,.0f} €".replace(',', ' ')])
    
    total = paiement.montant_total
    data.append(['TOTAL', f"{total:,.0f} €".replace(',', ' ')])
    
    if paiement.date_paiement:
        data.append(['Date de paiement', paiement.date_paiement.strftime('%d/%m/%Y')])
    
    if paiement.mode_paiement and paiement.mode_paiement != '':
        modes = {
            'virement': 'Virement bancaire',
            'cheque': 'Chèque',
            'especes': 'Espèces',
            'prelevement': 'Prélèvement automatique'
        }
        data.append(['Mode de paiement', modes.get(paiement.mode_paiement, paiement.mode_paiement)])
    
    if paiement.reference_paiement:
        data.append(['Référence', paiement.reference_paiement])
    
    table = Table(data, colWidths=[4*cm, 6*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightblue),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 30))
    
    # Texte de certification
    story.append(Paragraph(
        f"La Société Laser Services, représentée par Mariem CHEIKH BRAHIM, "
        f"gestionnaire du bien ci-dessus désigné, reconnais avoir reçu de "
        f"{locataire.nom} {locataire.prenom}, la somme de "
        f"<b>{total:,.0f} euros</b> ".replace(',', ' ') +
        f"pour le loyer et charges de la période du {mois_noms[paiement.mois]} {paiement.annee}.",
        content_style
    ))
    
    story.append(Spacer(1, 20))
    
    # Date et lieu d'émission
    date_emission = datetime.now().strftime('%d/%m/%Y')
    story.append(Paragraph(f"Fait à Nouakchott, le {date_emission}", content_style))
    
    story.append(Spacer(1, 30))
    
    # Signature
    signature_style = ParagraphStyle(
        'Signature',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_RIGHT,
        spaceAfter=8
    )
    
    story.append(Paragraph("Signature du bailleur :", signature_style))
    story.append(Spacer(1, 40))
    story.append(Paragraph("Mariem CHEIKH BRAHIM", signature_style))
    story.append(Paragraph("Représentant - Société Laser Services", signature_style))
    
    # Génération du PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

def generer_nom_fichier_quittance(paiement):
    """
    Génère un nom de fichier approprié pour la quittance
    
    Args:
        paiement: Instance de PaiementLoyer
        
    Returns:
        str: Nom du fichier
    """
    locataire = paiement.contrat.locataire
    mois_noms = ['', 'janv', 'fevr', 'mars', 'avr', 'mai', 'juin',
                 'juil', 'aout', 'sept', 'oct', 'nov', 'dec']
    
    nom_clean = locataire.nom.replace(' ', '_').replace('-', '_')
    prenom_clean = locataire.prenom.replace(' ', '_').replace('-', '_')
    mois_nom = mois_noms[paiement.mois]
    
    return f"quittance_{nom_clean}_{prenom_clean}_{mois_nom}_{paiement.annee}.pdf"