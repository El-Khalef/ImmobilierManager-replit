"""
Module pour la génération de quittances de loyer bilingues (français-arabe) en PDF
"""
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from translations import get_translation, get_month_name, format_currency

def generer_quittance_bilingue_pdf(paiement):
    """
    Génère une quittance de loyer bilingue (français-arabe) en PDF
    
    Args:
        paiement: Instance de PaiementLoyer
        
    Returns:
        BytesIO: Buffer contenant le PDF généré
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, 
                           topMargin=1.5*cm, bottomMargin=1.5*cm)
    
    story = []
    
    # Générer la version française
    story.extend(_generer_page_quittance(paiement, 'fr'))
    
    # Saut de page
    story.append(PageBreak())
    
    # Générer la version arabe
    story.extend(_generer_page_quittance(paiement, 'ar'))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def _generer_page_quittance(paiement, language):
    """
    Génère une page de quittance dans la langue spécifiée
    
    Args:
        paiement: Instance de PaiementLoyer
        language: Code de langue ('fr' ou 'ar')
        
    Returns:
        list: Liste des éléments pour le PDF
    """
    elements = []
    styles = getSampleStyleSheet()
    
    # Styles personnalisés
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=30,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_LEFT,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    content_style = ParagraphStyle(
        'Content',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_LEFT,
        spaceAfter=8
    )
    
    # Styles pour l'arabe
    if language == 'ar':
        title_style = ParagraphStyle(
            'CustomTitleAR',
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
        ['Société Laser Services', get_translation('phone', language) + ': +222 45 25 25 25'],
        ['Mariem CHEIKH BRAHIM', get_translation('email', language) + ': contact@laserservices.mr'],
        ['Nouakchott, Mauritanie', '']
    ]
    
    company_table = Table(company_data, colWidths=[8*cm, 8*cm])
    company_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT' if language == 'fr' else 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT' if language == 'fr' else 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    elements.append(company_table)
    elements.append(Spacer(1, 20))
    
    # Titre principal
    title_text = get_translation('receipt_title', language)
    elements.append(Paragraph(title_text, title_style))
    
    # Numéro de quittance et date
    receipt_number = f"LSS-{paiement.id:06d}"
    receipt_info = f"{get_translation('receipt_number', language)}: {receipt_number}"
    elements.append(Paragraph(receipt_info, header_style))
    
    current_date = datetime.now().strftime('%d/%m/%Y')
    date_info = f"Nouakchott, le {current_date}"
    elements.append(Paragraph(date_info, content_style))
    elements.append(Spacer(1, 20))
    
    # Informations du bailleur
    landlord_title = get_translation('landlord', language)
    elements.append(Paragraph(landlord_title + ":", header_style))
    
    landlord_info = [
        "Société Laser Services",
        "Représentée par : Mariem CHEIKH BRAHIM",
        get_translation('phone', language) + ": +222 45 25 25 25",
        get_translation('email', language) + ": contact@laserservices.mr"
    ]
    
    for info in landlord_info:
        elements.append(Paragraph(info, content_style))
    
    elements.append(Spacer(1, 15))
    
    # Informations du locataire
    tenant_title = get_translation('tenant', language)
    elements.append(Paragraph(tenant_title + ":", header_style))
    
    client = paiement.client
    tenant_info = [
        f"{client.prenom} {client.nom}",
        f"{get_translation('address', language)}: {client.adresse_complete}",
        f"{get_translation('phone', language)}: {client.telephone or 'Non renseigné'}",
        f"{get_translation('email', language)}: {client.email}"
    ]
    
    for info in tenant_info:
        elements.append(Paragraph(info, content_style))
    
    elements.append(Spacer(1, 15))
    
    # Informations du bien
    property_title = get_translation('property', language)
    elements.append(Paragraph(property_title + ":", header_style))
    
    bien = paiement.bien
    property_info = [
        bien.titre,
        f"{get_translation('address', language)}: {bien.adresse_complete}"
    ]
    
    for info in property_info:
        elements.append(Paragraph(info, content_style))
    
    elements.append(Spacer(1, 20))
    
    # Détails du paiement
    month_name = get_month_name(paiement.mois, language)
    period_text = f"{month_name} {paiement.annee}"
    period_info = f"{get_translation('period', language)}: {period_text}"
    elements.append(Paragraph(period_info, header_style))
    
    # Tableau des montants
    payment_data = [
        [get_translation('rent_amount', language), format_currency(paiement.montant_loyer, language)],
    ]
    
    if paiement.montant_charges and paiement.montant_charges > 0:
        payment_data.append([
            get_translation('charges_amount', language), 
            format_currency(paiement.montant_charges, language)
        ])
    
    total_amount = paiement.montant_total
    payment_data.append([
        get_translation('total_amount', language), 
        format_currency(total_amount, language)
    ])
    
    payment_table = Table(payment_data, colWidths=[10*cm, 6*cm])
    payment_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (0, -1), 'LEFT' if language == 'fr' else 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT' if language == 'fr' else 'LEFT'),
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
        payment_date_text = f"{get_translation('payment_date', language)}: {paiement.date_paiement.strftime('%d/%m/%Y')}"
        elements.append(Paragraph(payment_date_text, content_style))
    
    # Mode de paiement
    if paiement.mode_paiement:
        payment_method_text = f"{get_translation('payment_method', language)}: {paiement.mode_paiement}"
        elements.append(Paragraph(payment_method_text, content_style))
    
    elements.append(Spacer(1, 30))
    
    # Signature
    signature_text = get_translation('signature', language)
    signature_style = ParagraphStyle(
        'Signature',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_RIGHT if language == 'fr' else TA_LEFT,
        spaceAfter=40
    )
    elements.append(Paragraph(signature_text, signature_style))
    
    # Note de bas de page pour indiquer la langue
    language_note = "Version française" if language == 'fr' else "النسخة العربية"
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

def generer_nom_fichier_quittance_bilingue(paiement):
    """
    Génère un nom de fichier approprié pour la quittance bilingue
    
    Args:
        paiement: Instance de PaiementLoyer
        
    Returns:
        str: Nom du fichier
    """
    client_nom = paiement.client.nom.replace(' ', '_')
    mois_str = f"{paiement.mois:02d}"
    annee = paiement.annee
    
    return f"quittance_bilingue_{client_nom}_{mois_str}_{annee}.pdf"