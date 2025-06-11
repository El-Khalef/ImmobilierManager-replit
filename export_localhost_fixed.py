#!/usr/bin/env python3
"""
Script d'exportation corrigé pour localhost
Résout les problèmes de format de date PostgreSQL
"""

import os
import psycopg2
from datetime import datetime

def create_fixed_export():
    """Crée un export avec format de dates corrigé"""
    
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cursor = conn.cursor()
    
    filename = f'export_localhost_fixed_{datetime.now().strftime("%Y%m%d_%H%M%S")}.sql'
    
    with open(filename, 'w', encoding='utf-8') as f:
        # En-tête
        f.write('-- Export PostgreSQL corrigé pour localhost\n')
        f.write(f'-- Généré le {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        f.write('-- Format de dates corrigé pour éviter les erreurs de syntaxe\n\n')
        
        f.write('SET client_encoding = \'UTF8\';\n')
        f.write('SET standard_conforming_strings = on;\n')
        f.write('SET check_function_bodies = false;\n')
        f.write('SET client_min_messages = warning;\n')
        f.write('SET row_security = off;\n')
        f.write('SET DateStyle = \'ISO, DMY\';\n\n')
        
        # Tables dans l'ordre de dépendance
        tables = [
            'clients',
            'biens_immobiliers', 
            'contrats_location',
            'paiements_loyer',
            'photos_biens',
            'documents_contrat',
            'releves_compteurs',
            'comptes_comptables',
            'ecritures_comptables',
            'budgets_previsionnels',
            'depenses_immobilieres'
        ]
        
        for table in tables:
            # Structure de la table
            cursor.execute(f"""
                SELECT column_name, data_type, character_maximum_length, 
                       is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = %s AND table_schema = 'public'
                ORDER BY ordinal_position
            """, (table,))
            
            columns = cursor.fetchall()
            if not columns:
                continue
                
            f.write(f'\\echo "Traitement de la table {table}..."\n')
            f.write(f'DROP TABLE IF EXISTS {table} CASCADE;\n')
            
            # Créer la table
            f.write(f'CREATE TABLE {table} (\n')
            col_defs = []
            
            for col in columns:
                col_name, data_type, max_length, nullable, default = col
                col_def = f'    {col_name} '
                
                # Types de données
                if data_type == 'character varying':
                    col_def += f'VARCHAR({max_length if max_length else 255})'
                elif data_type == 'integer':
                    col_def += 'INTEGER'
                elif data_type == 'bigint':
                    col_def += 'BIGINT'
                elif data_type == 'double precision':
                    col_def += 'DOUBLE PRECISION'
                elif data_type == 'numeric':
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
                    
                if default and 'nextval' in str(default):
                    col_def += ' PRIMARY KEY GENERATED ALWAYS AS IDENTITY'
                elif default and default != 'NULL' and 'nextval' not in str(default):
                    col_def += f' DEFAULT {default}'
                
                col_defs.append(col_def)
            
            f.write(',\n'.join(col_defs))
            f.write('\n);\n\n')
            
            # Données avec format corrigé
            cursor.execute(f'SELECT * FROM {table}')
            rows = cursor.fetchall()
            
            if rows:
                col_names = [col[0] for col in columns]
                
                # Identifier les colonnes de type date/timestamp
                date_columns = set()
                for i, col in enumerate(columns):
                    if col[1] in ('date', 'timestamp without time zone'):
                        date_columns.add(i)
                
                f.write(f'\\echo "Insertion des données dans {table}..."\n')
                
                for row in rows:
                    values = []
                    for i, val in enumerate(row):
                        if val is None:
                            values.append('NULL')
                        elif i in date_columns:
                            # Format spécial pour les dates
                            if isinstance(val, (datetime)):
                                values.append(f"'{val.strftime('%Y-%m-%d %H:%M:%S')}'")
                            else:
                                values.append(f"'{val}'")
                        elif isinstance(val, str):
                            # Échapper les caractères spéciaux
                            escaped = val.replace("'", "''").replace('\\', '\\\\')
                            # Supprimer les caractères de contrôle
                            escaped = ''.join(char for char in escaped if ord(char) >= 32 or char in '\n\r\t')
                            values.append(f"'{escaped}'")
                        elif isinstance(val, bool):
                            values.append('TRUE' if val else 'FALSE')
                        else:
                            values.append(str(val))
                    
                    # Construire l'INSERT
                    insert_sql = f"INSERT INTO {table} ({', '.join(col_names)}) VALUES ({', '.join(values)});\n"
                    f.write(insert_sql)
                
                f.write('\n')
        
        # Mise à jour des séquences
        f.write('\\echo "Mise à jour des séquences..."\n')
        for table in tables:
            if table != 'comptes_comptables':  # Skip table sans auto-increment
                f.write(f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), COALESCE((SELECT MAX(id) FROM {table}), 1), true);\n")
        
        f.write('\n\\echo "Export terminé avec succès!"\n')
    
    cursor.close()
    conn.close()
    return filename

if __name__ == '__main__':
    filename = create_fixed_export()
    print(f'Export corrigé créé: {filename}')
    print('Ce fichier résout les problèmes de format de date PostgreSQL.')