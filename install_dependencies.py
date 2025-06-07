#!/usr/bin/env python3
"""
Script d'installation automatique des dépendances pour le projet de gestion immobilière
Usage: python install_dependencies.py
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Exécute une commande et affiche le résultat"""
    print(f"\n{'='*50}")
    print(f"📦 {description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Succès: {description}")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de: {description}")
        print(f"Code d'erreur: {e.returncode}")
        if e.stderr:
            print(f"Erreur: {e.stderr}")
        return False

def install_dependencies():
    """Installe toutes les dépendances nécessaires"""
    print("🚀 Installation des dépendances pour le projet de gestion immobilière")
    
    # Liste des packages à installer
    packages = [
        "Flask==2.3.3",
        "Flask-SQLAlchemy==3.0.5", 
        "Flask-WTF==1.1.1",
        "psycopg2-binary==2.9.7",
        "reportlab==4.0.4",
        "PyPDF2==3.0.1",
        "python-dateutil==2.8.2",
        "Werkzeug==2.3.7",
        "WTForms==3.0.1",
        "email-validator==2.0.0",
        "sendgrid==6.10.0",
        "twilio==8.5.0",
        "gunicorn==21.2.0"
    ]
    
    # Mettre à jour pip
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Mise à jour de pip")
    
    # Installer chaque package
    success_count = 0
    for package in packages:
        if run_command(f"{sys.executable} -m pip install {package}", f"Installation de {package}"):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"📊 RÉSUMÉ DE L'INSTALLATION")
    print(f"{'='*60}")
    print(f"✅ Packages installés avec succès: {success_count}/{len(packages)}")
    print(f"❌ Échecs: {len(packages) - success_count}")
    
    if success_count == len(packages):
        print("\n🎉 Toutes les dépendances ont été installées avec succès!")
        print("\nProchaines étapes:")
        print("1. Configurez PostgreSQL")
        print("2. Créez le fichier .env avec vos variables")
        print("3. Lancez l'application avec: python main.py")
    else:
        print("\n⚠️  Certaines dépendances n'ont pas pu être installées.")
        print("Vérifiez les erreurs ci-dessus et réessayez.")

def create_env_template():
    """Crée un template de fichier .env"""
    env_content = """# Configuration de la base de données
DATABASE_URL=postgresql://immobilier_user:votre_mot_de_passe@localhost:5432/immobilier_db

# Clé secrète pour les sessions (changez cette valeur)
SESSION_SECRET=changez_cette_cle_secrete_unique

# Configuration Flask
FLASK_ENV=development
FLASK_DEBUG=True

# Services externes (optionnel)
# SENDGRID_API_KEY=votre_cle_sendgrid
# TWILIO_ACCOUNT_SID=votre_sid_twilio
# TWILIO_AUTH_TOKEN=votre_token_twilio
# TWILIO_PHONE_NUMBER=votre_numero_twilio
"""
    
    if not os.path.exists('.env'):
        with open('.env.template', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("\n📝 Fichier .env.template créé!")
        print("Copiez ce fichier vers .env et modifiez les valeurs selon votre configuration.")

def create_directories():
    """Crée les dossiers nécessaires"""
    directories = ['static/uploads', 'static/documents']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Dossier créé: {directory}")

if __name__ == "__main__":
    print("🏠 PROJET DE GESTION IMMOBILIÈRE - INSTALLATION")
    print("=" * 60)
    
    # Vérifier que Python est disponible
    print(f"🐍 Python version: {sys.version}")
    
    # Installer les dépendances
    install_dependencies()
    
    # Créer les dossiers
    print(f"\n{'='*50}")
    print("📁 CRÉATION DES DOSSIERS")
    print(f"{'='*50}")
    create_directories()
    
    # Créer le template d'environnement
    print(f"\n{'='*50}")
    print("⚙️  CONFIGURATION")
    print(f"{'='*50}")
    create_env_template()
    
    print(f"\n{'='*60}")
    print("🎯 INSTALLATION TERMINÉE")
    print(f"{'='*60}")
    print("Consultez le fichier INSTALLATION_WINDOWS.md pour les étapes suivantes.")