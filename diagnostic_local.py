#!/usr/bin/env python3
"""
Script de diagnostic pour l'installation locale
Identifie et aide à résoudre les erreurs courantes
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

class DiagnosticLocal:
    def __init__(self):
        self.erreurs = []
        self.avertissements = []
        self.succes = []

    def log_erreur(self, message):
        self.erreurs.append(f"ERREUR: {message}")
        print(f"❌ ERREUR: {message}")

    def log_avertissement(self, message):
        self.avertissements.append(f"ATTENTION: {message}")
        print(f"⚠️  ATTENTION: {message}")

    def log_succes(self, message):
        self.succes.append(f"OK: {message}")
        print(f"✅ OK: {message}")

    def verifier_python(self):
        """Vérifie la version de Python"""
        print("\n🐍 Vérification de Python...")
        
        version = sys.version_info
        if version.major == 3 and version.minor >= 9:
            self.log_succes(f"Python {version.major}.{version.minor}.{version.micro}")
        else:
            self.log_erreur(f"Python {version.major}.{version.minor} détecté. Python 3.9+ requis")

    def verifier_modules(self):
        """Vérifie les modules Python requis"""
        print("\n📦 Vérification des modules...")
        
        modules_requis = [
            'flask', 'flask_sqlalchemy', 'flask_wtf', 'psycopg2',
            'reportlab', 'wtforms', 'email_validator', 'dateutil'
        ]
        
        for module in modules_requis:
            try:
                importlib.import_module(module)
                self.log_succes(f"Module {module}")
            except ImportError:
                self.log_erreur(f"Module {module} manquant")

    def verifier_fichiers(self):
        """Vérifie la présence des fichiers essentiels"""
        print("\n📁 Vérification des fichiers...")
        
        fichiers_requis = [
            'app.py', 'main.py', 'models.py', 'routes.py', 'forms.py'
        ]
        
        for fichier in fichiers_requis:
            if Path(fichier).exists():
                self.log_succes(f"Fichier {fichier}")
            else:
                self.log_erreur(f"Fichier {fichier} manquant")

    def verifier_dossiers(self):
        """Vérifie et crée les dossiers nécessaires"""
        print("\n📂 Vérification des dossiers...")
        
        dossiers = ['static/uploads', 'static/documents', 'templates']
        
        for dossier in dossiers:
            path = Path(dossier)
            if path.exists():
                self.log_succes(f"Dossier {dossier}")
            else:
                try:
                    path.mkdir(parents=True, exist_ok=True)
                    self.log_succes(f"Dossier {dossier} créé")
                except Exception as e:
                    self.log_erreur(f"Impossible de créer {dossier}: {e}")

    def verifier_env(self):
        """Vérifie la configuration d'environnement"""
        print("\n🔧 Vérification de la configuration...")
        
        if Path('.env').exists():
            self.log_succes("Fichier .env trouvé")
            
            # Charger et vérifier les variables
            try:
                from dotenv import load_dotenv
                load_dotenv()
                
                database_url = os.environ.get('DATABASE_URL')
                session_secret = os.environ.get('SESSION_SECRET')
                
                if database_url:
                    self.log_succes("DATABASE_URL configurée")
                    # Masquer les informations sensibles
                    url_safe = database_url.split('@')[1] if '@' in database_url else "localhost"
                    print(f"   Base: {url_safe}")
                else:
                    self.log_erreur("DATABASE_URL manquante dans .env")
                
                if session_secret:
                    self.log_succes("SESSION_SECRET configurée")
                else:
                    self.log_avertissement("SESSION_SECRET manquante - utilisation d'une clé par défaut")
                    
            except ImportError:
                self.log_erreur("Module python-dotenv manquant")
        else:
            self.log_erreur("Fichier .env manquant")

    def verifier_postgresql(self):
        """Vérifie PostgreSQL"""
        print("\n🐘 Vérification de PostgreSQL...")
        
        try:
            # Test de psql
            result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.log_succes(f"PostgreSQL installé: {version}")
                
                # Test de connexion si .env existe
                if Path('.env').exists():
                    try:
                        from dotenv import load_dotenv
                        load_dotenv()
                        database_url = os.environ.get('DATABASE_URL')
                        
                        if database_url:
                            # Test de connexion simple
                            import psycopg2
                            try:
                                conn = psycopg2.connect(database_url)
                                conn.close()
                                self.log_succes("Connexion à la base de données")
                            except Exception as e:
                                self.log_erreur(f"Connexion échouée: {e}")
                    except:
                        pass
            else:
                self.log_erreur("PostgreSQL non trouvé dans PATH")
                
        except FileNotFoundError:
            self.log_erreur("psql non trouvé - PostgreSQL non installé ou non configuré")

    def tester_import_app(self):
        """Test d'import de l'application"""
        print("\n🚀 Test d'import de l'application...")
        
        try:
            # Ajouter le répertoire courant au path
            sys.path.insert(0, '.')
            
            # Test d'import des modules principaux
            from app import app, db
            self.log_succes("Import de l'application Flask")
            
            # Test de configuration
            with app.app_context():
                try:
                    # Test de connexion DB
                    db.engine.connect()
                    self.log_succes("Connexion à la base via SQLAlchemy")
                except Exception as e:
                    self.log_erreur(f"Connexion SQLAlchemy échouée: {e}")
                    
        except Exception as e:
            self.log_erreur(f"Import de l'application échoué: {e}")

    def generer_solutions(self):
        """Génère des solutions pour les erreurs trouvées"""
        print("\n" + "="*60)
        print("RÉSUMÉ DU DIAGNOSTIC")
        print("="*60)
        
        print(f"\n✅ Succès: {len(self.succes)}")
        print(f"⚠️  Avertissements: {len(self.avertissements)}")
        print(f"❌ Erreurs: {len(self.erreurs)}")
        
        if self.erreurs:
            print("\n🔧 SOLUTIONS RECOMMANDÉES:")
            print("-" * 40)
            
            for erreur in self.erreurs:
                print(f"\n• {erreur}")
                
                if "Module" in erreur and "manquant" in erreur:
                    print("  Solution: pip install -r requirements_local.txt")
                elif "Fichier" in erreur and "manquant" in erreur:
                    print("  Solution: Vérifiez l'extraction du ZIP depuis Replit")
                elif "DATABASE_URL" in erreur:
                    print("  Solution: Créez un fichier .env avec DATABASE_URL")
                elif "PostgreSQL" in erreur:
                    print("  Solution: Installez PostgreSQL depuis postgresql.org")
                elif "Connexion" in erreur:
                    print("  Solution: Vérifiez que PostgreSQL est démarré et les paramètres .env")
        
        if not self.erreurs:
            print("\n🎉 Aucune erreur critique détectée!")
            print("Votre installation semble prête.")
            print("Lancez: python run_local.py")

    def executer_diagnostic_complet(self):
        """Exécute tous les tests de diagnostic"""
        print("🏠 DIAGNOSTIC D'INSTALLATION LOCALE")
        print("   Système de Gestion Immobilière")
        print("="*60)
        
        self.verifier_python()
        self.verifier_fichiers()
        self.verifier_dossiers()
        self.verifier_env()
        self.verifier_modules()
        self.verifier_postgresql()
        self.tester_import_app()
        
        self.generer_solutions()

def main():
    diagnostic = DiagnosticLocal()
    diagnostic.executer_diagnostic_complet()

if __name__ == "__main__":
    main()