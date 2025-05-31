"""
Outil de calibration pour déterminer les positions exactes sur le modèle PDF
Génère une grille de coordonnées pour positionner précisément les données
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.pdfgen import canvas
from io import BytesIO

# Dimensions de la page A4 en points
PAGE_WIDTH, PAGE_HEIGHT = A4

def generer_grille_calibration():
    """
    Génère un PDF avec une grille de coordonnées pour calibrer les positions
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Dessiner la grille de calibration
    _dessiner_grille_coordonnees(c)
    
    # Ajouter les marqueurs pour chaque champ à positionner
    _dessiner_marqueurs_champs(c)
    
    c.save()
    buffer.seek(0)
    return buffer

def _dessiner_grille_coordonnees(c):
    """Dessine une grille avec les coordonnées en cm"""
    
    # Grille verticale (tous les 1 cm)
    for x in range(0, int(PAGE_WIDTH/cm) + 1):
        x_pos = x * cm
        c.line(x_pos, 0, x_pos, PAGE_HEIGHT)
        if x % 2 == 0:  # Étiquettes tous les 2 cm
            c.setFont("Helvetica", 6)
            c.drawString(x_pos + 2, PAGE_HEIGHT - 10, f"{x}cm")
    
    # Grille horizontale (tous les 1 cm)
    for y in range(0, int(PAGE_HEIGHT/cm) + 1):
        y_pos = y * cm
        c.line(0, y_pos, PAGE_WIDTH, y_pos)
        if y % 2 == 0:  # Étiquettes tous les 2 cm
            c.setFont("Helvetica", 6)
            c.drawString(5, y_pos + 2, f"{y}cm")

def _dessiner_marqueurs_champs(c):
    """Dessine des marqueurs pour identifier où placer chaque champ"""
    
    c.setFont("Helvetica", 8)
    c.setFillColorRGB(1, 0, 0)  # Rouge pour les marqueurs
    
    # Liste des champs à positionner avec leurs labels
    champs = [
        {"label": "NUMERO", "desc": "Numéro de quittance (après N°)"},
        {"label": "NOM_LOC", "desc": "Nom du locataire"},
        {"label": "ADR_LOC", "desc": "Adresse du locataire"},
        {"label": "TEL_LOC", "desc": "Téléphone du locataire"},
        {"label": "VERSEMENT", "desc": "Versement effectué par"},
        {"label": "MONTANT", "desc": "Montant payé"},
        {"label": "DATE_PAI", "desc": "Date de paiement"},
        {"label": "BIEN", "desc": "Bien loué"},
        {"label": "MOIS", "desc": "Mois concerné"},
        {"label": "COMMENT", "desc": "Commentaire"},
        {"label": "DATE_ACT", "desc": "Date actuelle (en bas)"}
    ]
    
    # Placer les marqueurs sur le côté droit
    x_marqueur = PAGE_WIDTH - 5*cm
    y_start = PAGE_HEIGHT - 2*cm
    
    for i, champ in enumerate(champs):
        y_pos = y_start - (i * 0.8*cm)
        
        # Dessiner un petit carré rouge
        c.rect(x_marqueur, y_pos, 0.3*cm, 0.3*cm, fill=1)
        
        # Ajouter le label
        c.drawString(x_marqueur + 0.4*cm, y_pos + 0.1*cm, f"{champ['label']}: {champ['desc']}")

def generer_pdf_test_avec_donnees_exemple():
    """
    Génère un PDF de test avec des données d'exemple positionnées
    pour vérifier l'alignement
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Positions de test actuelles (à ajuster)
    positions_test = {
        'numero': {'x': 1.5*cm, 'y': PAGE_HEIGHT - 2.5*cm},
        'nom_locataire': {'x': 1.5*cm, 'y': PAGE_HEIGHT - 7*cm},
        'versement_par': {'x': 4.5*cm, 'y': PAGE_HEIGHT - 10*cm},
        'montant': {'x': 4.5*cm, 'y': PAGE_HEIGHT - 11*cm},
        'date_paiement': {'x': 4.5*cm, 'y': PAGE_HEIGHT - 12*cm},
        'bien_loue': {'x': 4.5*cm, 'y': PAGE_HEIGHT - 13*cm},
        'mois': {'x': 4.5*cm, 'y': PAGE_HEIGHT - 14*cm},
    }
    
    # Données d'exemple
    donnees_test = {
        'numero': "0123",
        'nom_locataire': "Mohamed Ahmed SALEM",
        'versement_par': "Mohamed Ahmed SALEM", 
        'montant': "75,000 MRU",
        'date_paiement': "15/05/2025",
        'bien_loue': "Appartement Centre-ville",
        'mois': "Mai 2025"
    }
    
    # Dessiner les données de test
    c.setFont("Helvetica", 11)
    c.setFillColorRGB(1, 0, 0)  # Rouge pour bien voir
    
    for champ, valeur in donnees_test.items():
        if champ in positions_test:
            pos = positions_test[champ]
            c.drawString(pos['x'], pos['y'], valeur)
            
            # Ajouter un petit marqueur pour identifier le champ
            c.setFont("Helvetica", 6)
            c.setFillColorRGB(0, 0, 1)  # Bleu pour le label
            c.drawString(pos['x'] - 0.5*cm, pos['y'], champ.upper())
            c.setFont("Helvetica", 11)
            c.setFillColorRGB(1, 0, 0)  # Retour au rouge
    
    c.save()
    buffer.seek(0)
    return buffer

def positions_recommandees_selon_modele():
    """
    Retourne des positions recommandées basées sur l'analyse du modèle
    Ces positions peuvent être ajustées manuellement
    """
    return {
        # À ajuster selon votre modèle exact
        'numero': {'x': 1*cm, 'y': PAGE_HEIGHT - 2.8*cm},
        'nom_locataire': {'x': 2*cm, 'y': PAGE_HEIGHT - 6.5*cm},
        'adresse_locataire': {'x': 2*cm, 'y': PAGE_HEIGHT - 7*cm},
        'telephone_locataire': {'x': 2*cm, 'y': PAGE_HEIGHT - 7.5*cm},
        'versement_par': {'x': 5*cm, 'y': PAGE_HEIGHT - 9.5*cm},
        'montant': {'x': 5*cm, 'y': PAGE_HEIGHT - 10.3*cm},
        'date_paiement': {'x': 5*cm, 'y': PAGE_HEIGHT - 11.1*cm},
        'bien_loue': {'x': 5*cm, 'y': PAGE_HEIGHT - 11.9*cm},
        'mois': {'x': 5*cm, 'y': PAGE_HEIGHT - 12.7*cm},
        'commentaire': {'x': 2*cm, 'y': PAGE_HEIGHT - 15.5*cm},
        'date_actuelle': {'x': 3*cm, 'y': PAGE_HEIGHT - 20.5*cm}
    }