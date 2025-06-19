#!/usr/bin/env python3
"""
Test rapide pour identifier les erreurs d'installation locale
Exécutez ce script pour un diagnostic immédiat
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test des imports critiques"""
    print("Test des imports...")
    
    modules_critiques = [
        ('flask', 'Flask'),
        ('sqlalchemy', 'SQLAlchemy'), 
        ('psycopg2', 'PostgreSQL'),
        ('reportlab', 'PDF'),
        ('wtforms', 'Formulaires')
    ]
    
    erreurs_import = []
    
    for module, description in modules_critiques:
        try:
            __import__(module)
            print(f"  ✓ {description}")
        except ImportError as e:
            erreurs_import.append((module, description, str(e)))
            print(f"  ✗ {description}: {e}")
    
    return erreurs_import

def test_fichiers():
    """Test des fichiers essentiels"""
    print("\nTest des fichiers...")
    
    fichiers_essentiels = [
        'app.py', 'main.py', 'models.py', 'routes.py', 'forms.py'
    ]
    
    fichiers_manquants = []
    
    for fichier in fichiers_essentiels:
        if Path(fichier).exists():
            print(f"  ✓ {fichier}")
        else:
            fichiers_manquants.append(fichier)
            print(f"  ✗ {fichier} manquant")
    
    return fichiers_manquants

def test_configuration():
    """Test de la configuration"""
    print("\nTest de la configuration...")
    
    problemes_config = []
    
    # Test fichier .env
    if Path('.env').exists():
        print("  ✓ Fichier .env trouvé")
        
        # Tenter de lire les variables
        try:
            with open('.env', 'r') as f:
                contenu = f.read()
                if 'DATABASE_URL=' in contenu:
                    print("  ✓ DATABASE_URL configurée")
                else:
                    problemes_config.append("DATABASE_URL manquante dans .env")
                    print("  ✗ DATABASE_URL manquante")
                    
                if 'SESSION_SECRET=' in contenu:
                    print("  ✓ SESSION_SECRET configurée")
                else:
                    problemes_config.append("SESSION_SECRET manquante dans .env")
                    print("  ✗ SESSION_SECRET manquante")
        except Exception as e:
            problemes_config.append(f"Erreur lecture .env: {e}")
            print(f"  ✗ Erreur lecture .env: {e}")
    else:
        problemes_config.append("Fichier .env manquant")
        print("  ✗ Fichier .env manquant")
    
    return problemes_config

def test_application():
    """Test de l'application Flask"""
    print("\nTest de l'application...")
    
    erreurs_app = []
    
    try:
        # Ajouter le répertoire au path
        sys.path.insert(0, '.')
        
        # Test import application
        from app import app
        print("  ✓ Import de l'application Flask")
        
        # Test configuration basique
        with app.app_context():
            print("  ✓ Contexte Flask")
            
            # Test import des modèles
            try:
                from models import Client, BienImmobilier
                print("  ✓ Import des modèles")
            except Exception as e:
                erreurs_app.append(f"Erreur import modèles: {e}")
                print(f"  ✗ Erreur import modèles: {e}")
                
    except Exception as e:
        erreurs_app.append(f"Erreur application Flask: {e}")
        print(f"  ✗ Erreur application Flask: {e}")
    
    return erreurs_app

def generer_rapport(erreurs_import, fichiers_manquants, problemes_config, erreurs_app):
    """Génère un rapport avec solutions"""
    
    print("\n" + "="*50)
    print("RAPPORT DE TEST RAPIDE")
    print("="*50)
    
    total_problemes = len(erreurs_import) + len(fichiers_manquants) + len(problemes_config) + len(erreurs_app)
    
    if total_problemes == 0:
        print("\n🎉 Aucun problème détecté!")
        print("Votre installation semble fonctionnelle.")
        print("Lancez: python run_local.py")
        return
    
    print(f"\n{total_problemes} problème(s) détecté(s)")
    
    # Solutions pour les imports
    if erreurs_import:
        print("\n📦 MODULES MANQUANTS:")
        for module, desc, erreur in erreurs_import:
            print(f"  • {desc} ({module})")
        print("  SOLUTION: pip install -r requirements_local.txt")
        print("           ou exécutez install_local_windows.bat")
    
    # Solutions pour les fichiers
    if fichiers_manquants:
        print("\n📁 FICHIERS MANQUANTS:")
        for fichier in fichiers_manquants:
            print(f"  • {fichier}")
        print("  SOLUTION: Vérifiez l'extraction complète du ZIP depuis Replit")
    
    # Solutions pour la configuration
    if problemes_config:
        print("\n🔧 PROBLÈMES DE CONFIGURATION:")
        for probleme in problemes_config:
            print(f"  • {probleme}")
        print("  SOLUTION: Copiez .env.template vers .env et configurez vos paramètres")
    
    # Solutions pour l'application
    if erreurs_app:
        print("\n🚀 PROBLÈMES D'APPLICATION:")
        for erreur in erreurs_app:
            print(f"  • {erreur}")
        print("  SOLUTION: Vérifiez tous les points ci-dessus puis relancez le test")

def main():
    print("TEST RAPIDE - Installation Locale")
    print("Système de Gestion Immobilière")
    print("-" * 40)
    
    erreurs_import = test_imports()
    fichiers_manquants = test_fichiers()
    problemes_config = test_configuration()
    erreurs_app = test_application()
    
    generer_rapport(erreurs_import, fichiers_manquants, problemes_config, erreurs_app)

if __name__ == "__main__":
    main()