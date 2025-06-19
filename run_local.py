#!/usr/bin/env python3
"""
Script de démarrage pour l'environnement local
Configure et démarre l'application Flask en mode développement local
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Configure l'environnement local"""
    try:
        from dotenv import load_dotenv
        
        # Charger les variables d'environnement depuis .env
        env_path = Path('.') / '.env'
        if env_path.exists():
            load_dotenv(env_path)
            print("Variables d'environnement chargées depuis .env")
        else:
            print("ATTENTION: Fichier .env non trouvé")
            print("Créez un fichier .env avec vos paramètres de base de données")
            return False
            
    except ImportError:
        print("ERREUR: python-dotenv non installé")
        print("Installez avec: pip install python-dotenv")
        return False
    
    return True

def verify_database():
    """Vérifie la configuration de la base de données"""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("ERREUR: DATABASE_URL non configurée")
        print("Ajoutez DATABASE_URL dans votre fichier .env")
        return False
    
    print(f"Base de données configurée: {database_url.split('@')[1] if '@' in database_url else 'localhost'}")
    return True

def create_directories():
    """Crée les dossiers nécessaires"""
    dirs_to_create = [
        'static/uploads',
        'static/documents'
    ]
    
    for dir_path in dirs_to_create:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"Dossier créé/vérifié: {dir_path}")

def main():
    """Fonction principale de démarrage"""
    print("=" * 60)
    print("DEMARRAGE LOCAL - Système de Gestion Immobilière")
    print("=" * 60)
    
    # Configuration de l'environnement
    if not setup_environment():
        return 1
    
    # Vérification de la base de données
    if not verify_database():
        return 1
    
    # Création des dossiers
    create_directories()
    
    try:
        # Import de l'application Flask
        from app import app, db
        
        # Configuration pour l'environnement local
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_ECHO'] = False  # Mettre True pour voir les requêtes SQL
        app.config['ENV'] = 'development'
        
        # Test de connexion à la base de données
        with app.app_context():
            try:
                db.engine.connect()
                print("Connexion à la base de données: OK")
            except Exception as e:
                print(f"ERREUR de connexion à la base de données: {e}")
                print("Vérifiez que PostgreSQL est démarré et que les paramètres sont corrects")
                return 1
        
        print("\nDémarrage du serveur de développement...")
        print("Application accessible sur: http://localhost:5000")
        print("Appuyez sur Ctrl+C pour arrêter")
        print("-" * 60)
        
        # Démarrer le serveur Flask
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=True,
            use_reloader=True,
            use_debugger=True
        )
        
    except ImportError as e:
        print(f"ERREUR d'import: {e}")
        print("Vérifiez que toutes les dépendances sont installées")
        return 1
    except Exception as e:
        print(f"ERREUR inattendue: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())