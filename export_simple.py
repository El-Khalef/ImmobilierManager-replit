"""
Export simple des données pour installation locale
"""
import os
from datetime import datetime
from app import app, db
from models import *

def export_donnees():
    """Exporte les données essentielles en SQL"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"donnees_pour_local_{timestamp}.sql"
    
    with app.app_context():
        with open(nom_fichier, 'w', encoding='utf-8') as f:
            f.write("-- Export des données pour installation locale\n")
            f.write(f"-- Créé le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n\n")
            
            # Clients
            clients = Client.query.all()
            f.write(f"-- {len(clients)} clients\n")
            for client in clients:
                f.write(f"INSERT INTO clients (nom, prenom, email, telephone, adresse, ville, code_postal, type_client, type_piece_identite, numero_piece_identite) VALUES ('{client.nom}', '{client.prenom}', '{client.email}', '{client.telephone or ''}', '{client.adresse or ''}', '{client.ville or ''}', '{client.code_postal or ''}', '{client.type_client}', '{client.type_piece_identite}', '{client.numero_piece_identite}');\n")
            
            # Biens immobiliers
            biens = BienImmobilier.query.all()
            f.write(f"\n-- {len(biens)} biens immobiliers\n")
            for bien in biens:
                f.write(f"INSERT INTO biens_immobiliers (titre, type_bien, adresse, ville, surface, prix_location_mensuel, proprietaire_id) VALUES ('{bien.titre}', '{bien.type_bien}', '{bien.adresse}', '{bien.ville}', {bien.surface}, {bien.prix_location_mensuel or 0}, {bien.proprietaire_id});\n")
            
            # Comptes comptables
            comptes = CompteComptable.query.all()
            f.write(f"\n-- {len(comptes)} comptes comptables\n")
            for compte in comptes:
                f.write(f"INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('{compte.numero_compte}', '{compte.nom_compte}', '{compte.type_compte}', '{compte.sous_type or ''}', {compte.actif});\n")
    
    print(f"Export créé: {nom_fichier}")
    return nom_fichier

if __name__ == "__main__":
    export_donnees()