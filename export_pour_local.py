#!/usr/bin/env python3
"""
Script d'export pour installation locale
Crée un export PostgreSQL compatible avec l'installation locale
"""

import os
import subprocess
import sys
from datetime import datetime

def creer_export_local():
    """Crée un export de la base de données pour l'installation locale"""
    
    print("🔄 Création de l'export pour installation locale...")
    
    # Générer le nom du fichier avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_file = f"export_pour_local_{timestamp}.sql"
    
    try:
        # URL de la base de données depuis les variables d'environnement
        database_url = os.environ.get('DATABASE_URL')
        
        if not database_url:
            print("❌ Erreur : DATABASE_URL non trouvée dans les variables d'environnement")
            return False
        
        print(f"📊 Export de la base de données...")
        print(f"📁 Fichier de sortie : {export_file}")
        
        # Commande pg_dump avec options pour la compatibilité locale
        cmd = [
            'pg_dump',
            database_url,
            '--clean',                    # Nettoyer avant création
            '--if-exists',               # Éviter les erreurs si tables n'existent pas
            '--no-owner',                # Pas de propriétaire spécifique
            '--no-privileges',           # Pas de privilèges spécifiques
            '--verbose',                 # Mode verbeux
            '--file', export_file        # Fichier de sortie
        ]
        
        # Exécuter la commande
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Export créé avec succès : {export_file}")
            
            # Afficher la taille du fichier
            try:
                file_size = os.path.getsize(export_file)
                print(f"📊 Taille du fichier : {file_size / 1024:.1f} KB")
            except:
                pass
            
            print("\n📋 Instructions pour l'installation locale :")
            print("1. Téléchargez ce fichier depuis Replit")
            print("2. Suivez le guide INSTALLATION_LOCALE.md")
            print("3. Importez avec : psql -U immobilier_user -d gestion_immobiliere -f " + export_file)
            
            return True
        else:
            print(f"❌ Erreur lors de l'export :")
            print(f"Code de retour : {result.returncode}")
            print(f"Erreur : {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur inattendue : {str(e)}")
        return False

def verifier_donnees():
    """Vérifie les données avant export"""
    try:
        from app import app, db
        from models import Client, BienImmobilier, ContratLocation, PaiementLoyer, CompteComptable, EcritureComptable
        
        with app.app_context():
            stats = {
                'Clients': Client.query.count(),
                'Biens immobiliers': BienImmobilier.query.count(),
                'Contrats': ContratLocation.query.count(),
                'Paiements': PaiementLoyer.query.count(),
                'Comptes comptables': CompteComptable.query.count(),
                'Écritures comptables': EcritureComptable.query.count(),
            }
            
            print("📊 Statistiques des données à exporter :")
            for nom, count in stats.items():
                print(f"   • {nom}: {count}")
            
            total = sum(stats.values())
            print(f"\n📈 Total des enregistrements : {total}")
            
            if total == 0:
                print("⚠️  Attention : Aucune donnée trouvée à exporter")
                return False
            
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification : {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("=" * 60)
    print("🏠 EXPORT POUR INSTALLATION LOCALE")
    print("   Système de Gestion Immobilière")
    print("=" * 60)
    
    # Vérifier les données
    if not verifier_donnees():
        print("❌ Impossible de continuer sans données valides")
        return
    
    # Demander confirmation
    print("\n❓ Voulez-vous créer l'export pour l'installation locale ? (o/n)")
    response = input().lower().strip()
    
    if response in ['o', 'oui', 'y', 'yes']:
        success = creer_export_local()
        
        if success:
            print("\n✅ Export terminé avec succès !")
            print("📥 Téléchargez le fichier .sql créé")
            print("📖 Consultez INSTALLATION_LOCALE.md pour la suite")
        else:
            print("\n❌ L'export a échoué")
            print("🔍 Vérifiez les logs ci-dessus pour plus de détails")
    else:
        print("❌ Export annulé")

if __name__ == "__main__":
    main()