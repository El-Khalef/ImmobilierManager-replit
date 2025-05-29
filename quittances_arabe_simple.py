"""
Générateur de quittances en version arabe simple (sans caractères arabes)
Utilise uniquement des caractères latins pour éviter les problèmes de police
"""
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from io import BytesIO

def generer_quittance_arabe_simple_pdf(paiement):
    """
    Génère une quittance en version arabe translitérée (sans caractères arabes)
    
    Args:
        paiement: Instance de PaiementLoyer
        
    Returns:
        BytesIO: Buffer contenant le PDF généré
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, 
                           topMargin=1.5*cm, bottomMargin=1.5*cm)
    
    story = []
    
    # Générer la page en arabe translitéré
    story.extend(_generer_page_arabe_transliteree(paiement))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def _generer_page_arabe_transliteree(paiement):
    """
    Génère une page de quittance en arabe translitéré
    """
    elements = []
    styles = getSampleStyleSheet()
    
    # Styles avec alignement RTL
    title_style = ParagraphStyle(
        'TitleAR',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=30,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    header_style = ParagraphStyle(
        'HeaderAR',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_RIGHT,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    content_style = ParagraphStyle(
        'ContentAR',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_RIGHT,
        spaceAfter=8
    )
    
    # En-tête de l'entreprise
    company_data = [
        ['Al-hatif: +222 45 25 25 25', 'Société Laser Services'],
        ['Al-bareed: contact@laserservices.mr', 'Mariem CHEIKH BRAHIM'],
        ['', 'Nouakchott, Mauritania']
    ]
    
    company_table = Table(company_data, colWidths=[8*cm, 8*cm])
    company_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    elements.append(company_table)
    elements.append(Spacer(1, 20))
    
    # Titre principal
    title_text = "ISAL IJAR - RECU DE LOYER"
    elements.append(Paragraph(title_text, title_style))
    
    # Numéro de quittance
    receipt_number = f"LSS-{paiement.id:06d}"
    receipt_info = f"Raqam al-isal: {receipt_number}"
    elements.append(Paragraph(receipt_info, header_style))
    
    current_date = datetime.now().strftime('%d/%m/%Y')
    date_info = f"Nouakchott, {current_date}"
    elements.append(Paragraph(date_info, content_style))
    elements.append(Spacer(1, 20))
    
    # Informations du bailleur
    elements.append(Paragraph("Al-mu'ajjir - LE BAILLEUR:", header_style))
    
    landlord_info = [
        "Société Laser Services",
        "Mumaththala bi: Mariem CHEIKH BRAHIM",
        "Al-hatif: +222 45 25 25 25",
        "Al-bareed: contact@laserservices.mr"
    ]
    
    for info in landlord_info:
        elements.append(Paragraph(info, content_style))
    
    elements.append(Spacer(1, 15))
    
    # Informations du locataire
    elements.append(Paragraph("Al-musta'jir - LE LOCATAIRE:", header_style))
    
    client = paiement.client
    tenant_info = [
        f"{client.prenom} {client.nom}",
        f"Al-'unwan: {client.adresse_complete}",
        f"Al-hatif: {client.telephone or 'Ghayr muddakhal'}",
        f"Al-bareed: {client.email}"
    ]
    
    for info in tenant_info:
        elements.append(Paragraph(info, content_style))
    
    elements.append(Spacer(1, 15))
    
    # Informations du bien
    elements.append(Paragraph("Al-'aqar al-mu'ajjar - PROPRIETE LOUEE:", header_style))
    
    bien = paiement.bien
    property_info = [
        bien.titre,
        f"Al-'unwan: {bien.adresse_complete}"
    ]
    
    for info in property_info:
        elements.append(Paragraph(info, content_style))
    
    elements.append(Spacer(1, 20))
    
    # Détails du paiement
    mois_noms_ar = [
        'Yanayir', 'Fibrayir', 'Mars', 'Abril', 'Mayu', 'Yunyu',
        'Yulyu', 'Aghustus', 'Sibtambir', 'Uktubar', 'Nufambir', 'Disambir'
    ]
    month_name = mois_noms_ar[paiement.mois - 1]
    period_text = f"{month_name} {paiement.annee}"
    period_info = f"Al-fatra - PERIODE: {period_text}"
    elements.append(Paragraph(period_info, header_style))
    
    # Tableau des montants
    payment_data = [
        ["Mablag al-ijar - MONTANT DU LOYER", f"{paiement.montant_loyer:,.0f} ouguiya"],
    ]
    
    if paiement.montant_charges and paiement.montant_charges > 0:
        payment_data.append([
            "Mablag ar-rusum - CHARGES", 
            f"{paiement.montant_charges:,.0f} ouguiya"
        ])
    
    total_amount = paiement.montant_total
    payment_data.append([
        "Al-mablag al-ijmali - MONTANT TOTAL", 
        f"{total_amount:,.0f} ouguiya"
    ])
    
    payment_table = Table(payment_data, colWidths=[10*cm, 6*cm])
    payment_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (-1, -1), (-1, -1), colors.lightgrey),
        ('FONTNAME', (-1, -1), (-1, -1), 'Helvetica-Bold'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(payment_table)
    elements.append(Spacer(1, 20))
    
    # Date de paiement
    if paiement.date_paiement:
        payment_date_text = f"Tareekh ad-daf' - DATE DE PAIEMENT: {paiement.date_paiement.strftime('%d/%m/%Y')}"
        elements.append(Paragraph(payment_date_text, content_style))
    
    # Mode de paiement
    if paiement.mode_paiement:
        payment_method_text = f"Tariqat ad-daf' - MODE DE PAIEMENT: {paiement.mode_paiement}"
        elements.append(Paragraph(payment_method_text, content_style))
    
    elements.append(Spacer(1, 30))
    
    # Signature
    signature_text = "Tawqee' al-mu'ajjir - SIGNATURE DU BAILLEUR"
    signature_style = ParagraphStyle(
        'Signature',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_LEFT,
        spaceAfter=40
    )
    elements.append(Paragraph(signature_text, signature_style))
    
    # Note de bas de page
    language_note = "An-nuskha al-'arabiyya - VERSION ARABE"
    note_style = ParagraphStyle(
        'Note',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(language_note, note_style))
    
    return elements

def generer_nom_fichier_quittance_arabe(paiement):
    """
    Génère un nom de fichier approprié pour la quittance arabe
    """
    client_nom = paiement.client.nom.replace(' ', '_')
    mois_str = f"{paiement.mois:02d}"
    annee = paiement.annee
    
    return f"quittance_arabe_{client_nom}_{mois_str}_{annee}.pdf"