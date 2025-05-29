"""
Module pour les traductions français-arabe
"""

# Dictionnaire des traductions
TRANSLATIONS = {
    'fr': {
        # Quittance
        'receipt_title': 'QUITTANCE DE LOYER',
        'receipt_number': 'Quittance N°',
        'landlord': 'Bailleur',
        'tenant': 'Locataire',
        'property': 'Bien loué',
        'address': 'Adresse',
        'period': 'Période',
        'rent_amount': 'Montant du loyer',
        'charges_amount': 'Montant des charges',
        'total_amount': 'Montant total',
        'payment_date': 'Date de paiement',
        'payment_method': 'Mode de paiement',
        'signature': 'Signature du bailleur',
        'currency': 'ouguiyas',
        'phone': 'Téléphone',
        'email': 'Email',
        
        # Contrat
        'contract_title': 'CONTRAT DE LOCATION',
        'start_date': 'Date de début',
        'end_date': 'Date de fin',
        'monthly_rent': 'Loyer mensuel',
        'security_deposit': 'Dépôt de garantie',
        'special_conditions': 'Conditions particulières',
        
        # Mois
        'january': 'Janvier',
        'february': 'Février',
        'march': 'Mars',
        'april': 'Avril',
        'may': 'Mai',
        'june': 'Juin',
        'july': 'Juillet',
        'august': 'Août',
        'september': 'Septembre',
        'october': 'Octobre',
        'november': 'Novembre',
        'december': 'Décembre',
    },
    'ar': {
        # Quittance
        'receipt_title': 'إيصال إيجار',
        'receipt_number': 'رقم الإيصال',
        'landlord': 'المؤجر',
        'tenant': 'المستأجر',
        'property': 'العقار المؤجر',
        'address': 'العنوان',
        'period': 'الفترة',
        'rent_amount': 'مبلغ الإيجار',
        'charges_amount': 'مبلغ الرسوم',
        'total_amount': 'المبلغ الإجمالي',
        'payment_date': 'تاريخ الدفع',
        'payment_method': 'طريقة الدفع',
        'signature': 'توقيع المؤجر',
        'currency': 'أوقية',
        'phone': 'الهاتف',
        'email': 'البريد الإلكتروني',
        
        # Contrat
        'contract_title': 'عقد إيجار',
        'start_date': 'تاريخ البداية',
        'end_date': 'تاريخ النهاية',
        'monthly_rent': 'الإيجار الشهري',
        'security_deposit': 'التأمين',
        'special_conditions': 'شروط خاصة',
        
        # Mois
        'january': 'يناير',
        'february': 'فبراير',
        'march': 'مارس',
        'april': 'أبريل',
        'may': 'مايو',
        'june': 'يونيو',
        'july': 'يوليو',
        'august': 'أغسطس',
        'september': 'سبتمبر',
        'october': 'أكتوبر',
        'november': 'نوفمبر',
        'december': 'ديسمبر',
    }
}

def get_translation(key, language='fr'):
    """
    Récupère une traduction pour une clé donnée
    
    Args:
        key: Clé de traduction
        language: Code de langue ('fr' ou 'ar')
    
    Returns:
        str: Texte traduit
    """
    return TRANSLATIONS.get(language, {}).get(key, key)

def get_month_name(month_number, language='fr'):
    """
    Récupère le nom du mois dans la langue spécifiée
    
    Args:
        month_number: Numéro du mois (1-12)
        language: Code de langue ('fr' ou 'ar')
    
    Returns:
        str: Nom du mois traduit
    """
    months = [
        'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    if 1 <= month_number <= 12:
        month_key = months[month_number - 1]
        return get_translation(month_key, language)
    
    return str(month_number)

def format_currency(amount, language='fr'):
    """
    Formate un montant avec la devise appropriée
    
    Args:
        amount: Montant numérique
        language: Code de langue ('fr' ou 'ar')
    
    Returns:
        str: Montant formaté avec devise
    """
    currency = get_translation('currency', language)
    if language == 'ar':
        return f"{amount:,.2f} {currency}"
    else:
        return f"{amount:,.2f} {currency}"