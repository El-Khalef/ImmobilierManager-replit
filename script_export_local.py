#!/usr/bin/env python3
"""
Script d'exportation automatique pour localhost
Crée une sauvegarde optimisée pour l'importation locale
"""

import os
import psycopg2
from datetime import datetime

def create_local_export():
    """Crée un export optimisé pour localhost"""
    
    # Connexion à la base de données
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cursor = conn.cursor()
    
    # Nom du fichier d'export
    filename = f'export_localhost_{datetime.now().strftime("%Y%m%d_%H%M%S")}.sql'
    
    with open(filename, 'w', encoding='utf-8') as f:
        # En-tête optimisé pour localhost
        f.write('-- Export pour localhost PostgreSQL\n')
        f.write(f'-- Généré le {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        f.write('-- \n')
        f.write('-- Instructions d\'importation :\n')
        f.write('-- 1. Créer la base : CREATE DATABASE immobilier_mauritanie;\n')
        f.write('-- 2. Importer : psql -U postgres -d immobilier_mauritanie -f ' + filename + '\n')
        f.write('-- \n\n')
        
        # Configuration pour l'import
        f.write('SET client_encoding = \'UTF8\';\n')
        f.write('SET standard_conforming_strings = on;\n')
        f.write('SET check_function_bodies = false;\n')
        f.write('SET client_min_messages = warning;\n')
        f.write('SET row_security = off;\n\n')
        
        # Création du schéma et extensions si nécessaires
        f.write('CREATE SCHEMA IF NOT EXISTS public;\n')
        f.write('SET search_path = public, pg_catalog;\n\n')
        
        # Obtenir la structure des tables dans l'ordre de création
        tables_info = {
            'clients': ['id', 'nom', 'prenom', 'email', 'telephone', 'adresse', 'ville', 'code_postal', 'type_client', 'date_creation', 'type_piece_identite', 'numero_piece_identite'],
            'biens_immobiliers': ['id', 'titre', 'type_bien', 'adresse', 'ville', 'code_postal', 'surface', 'nombre_pieces', 'nombre_chambres', 'prix_achat', 'prix_location_mensuel', 'charges_mensuelles', 'description', 'meuble', 'balcon', 'parking', 'ascenseur', 'etage', 'annee_construction', 'disponible', 'date_creation', 'proprietaire_id', 'latitude', 'longitude'],
            'contrats_location': ['id', 'bien_id', 'locataire_id', 'date_debut', 'date_fin', 'loyer_mensuel', 'charges_mensuelles', 'depot_garantie', 'frais_agence', 'statut', 'conditions_particulieres', 'date_creation', 'somelec_numero_compteur', 'somelec_code_abonnement', 'somelec_index_initial', 'somelec_date_branchement', 'somelec_quitus_precedent', 'snde_numero_compteur', 'snde_code_abonnement', 'snde_index_initial', 'snde_date_branchement', 'snde_quitus_precedent'],
            'paiements_loyer': ['id', 'contrat_id', 'mois', 'annee', 'montant_loyer', 'montant_charges', 'date_paiement', 'date_echeance', 'statut', 'mode_paiement', 'reference_paiement', 'remarques', 'date_creation'],
            'photos_biens': ['id', 'bien_id', 'nom_fichier', 'chemin_fichier', 'principale', 'date_upload'],
            'documents_contrat': ['id', 'contrat_id', 'type_document', 'nom_fichier', 'chemin_fichier', 'description', 'date_upload'],
            'releves_compteurs': ['id', 'contrat_id', 'type_compteur', 'numero_compteur', 'code_abonnement', 'date_releve', 'index_precedent', 'index_actuel', 'consommation', 'montant_facture', 'statut_paiement', 'remarques', 'date_creation'],
            'comptes_comptables': ['id', 'numero_compte', 'nom_compte', 'type_compte', 'description', 'actif'],
            'ecritures_comptables': ['id', 'date_ecriture', 'numero_piece', 'libelle', 'compte_debit_id', 'compte_credit_id', 'montant', 'description', 'date_creation'],
            'budgets_previsionnels': ['id', 'annee', 'mois', 'compte_id', 'montant_prevu', 'montant_realise', 'description', 'date_creation'],
            'depenses_immobilieres': ['id', 'bien_id', 'type_depense', 'montant', 'date_depense', 'description', 'fournisseur', 'numero_facture', 'date_creation']
        }
        
        # Créer les tables avec leurs structures
        for table_name, columns in tables_info.items():
            # Obtenir la définition de la table
            cursor.execute(f"""
                SELECT column_name, data_type, character_maximum_length, 
                       is_nullable, column_default, numeric_precision, numeric_scale
                FROM information_schema.columns 
                WHERE table_name = %s AND table_schema = 'public'
                ORDER BY ordinal_position
            """, (table_name,))
            
            table_columns = cursor.fetchall()
            if not table_columns:
                continue
                
            f.write(f'-- Table: {table_name}\n')
            f.write(f'DROP TABLE IF EXISTS {table_name} CASCADE;\n')
            f.write(f'CREATE TABLE {table_name} (\n')
            
            column_defs = []
            for col in table_columns:
                col_name, data_type, max_length, nullable, default, precision, scale = col
                
                # Construire la définition de colonne
                col_def = f'    {col_name} '
                
                if data_type == 'character varying':
                    col_def += f'VARCHAR({max_length})'
                elif data_type == 'integer':
                    col_def += 'INTEGER'
                elif data_type == 'bigint':
                    col_def += 'BIGINT'
                elif data_type == 'double precision':
                    col_def += 'DOUBLE PRECISION'
                elif data_type == 'numeric':
                    if precision and scale:
                        col_def += f'NUMERIC({precision},{scale})'
                    else:
                        col_def += 'NUMERIC'
                elif data_type == 'boolean':
                    col_def += 'BOOLEAN'
                elif data_type == 'date':
                    col_def += 'DATE'
                elif data_type == 'timestamp without time zone':
                    col_def += 'TIMESTAMP'
                elif data_type == 'text':
                    col_def += 'TEXT'
                else:
                    col_def += data_type.upper()
                
                if nullable == 'NO':
                    col_def += ' NOT NULL'
                    
                if default:
                    if 'nextval' in default:
                        col_def += ' PRIMARY KEY'
                    elif default != 'NULL':
                        col_def += f' DEFAULT {default}'
                
                column_defs.append(col_def)
            
            f.write(',\n'.join(column_defs))
            f.write('\n);\n\n')
            
            # Ajouter les données
            cursor.execute(f'SELECT * FROM {table_name}')
            rows = cursor.fetchall()
            
            if rows:
                f.write(f'-- Données pour {table_name}\n')
                col_names = [col[0] for col in table_columns]
                
                for row in rows:
                    values = []
                    for val in row:
                        if val is None:
                            values.append('NULL')
                        elif isinstance(val, str):
                            escaped = val.replace("'", "''").replace('\\', '\\\\')
                            values.append(f"'{escaped}'")
                        elif isinstance(val, bool):
                            values.append('TRUE' if val else 'FALSE')
                        else:
                            values.append(str(val))
                    
                    f.write(f"INSERT INTO {table_name} ({', '.join(col_names)}) VALUES ({', '.join(values)});\n")
                
                f.write('\n')
        
        # Rétablir les séquences
        f.write('-- Mise à jour des séquences\n')
        cursor.execute("""
            SELECT sequence_name, table_name 
            FROM information_schema.sequences s
            JOIN information_schema.tables t ON t.table_name = REPLACE(s.sequence_name, '_id_seq', '')
            WHERE s.sequence_schema = 'public' AND t.table_schema = 'public'
        """)
        
        sequences = cursor.fetchall()
        for seq_name, table_name in sequences:
            f.write(f"SELECT setval('{seq_name}', COALESCE((SELECT MAX(id) FROM {table_name}), 1), true);\n")
        
        f.write('\n-- Export terminé avec succès\n')
    
    cursor.close()
    conn.close()
    
    return filename

if __name__ == '__main__':
    filename = create_local_export()
    print(f'Export créé pour localhost: {filename}')
    print(f'Taille du fichier: {os.path.getsize(filename)} bytes')
    print('\nPour importer:')
    print('1. Créez la base: CREATE DATABASE immobilier_mauritanie;')
    print(f'2. Importez: psql -U postgres -d immobilier_mauritanie -f {filename}')