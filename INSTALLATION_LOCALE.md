# Guide d'Installation Locale - Système de Gestion Immobilière

## Vue d'ensemble
Ce guide vous permet d'installer et de faire fonctionner votre système de gestion immobilière en local sur votre ordinateur Windows, sans affecter la version Replit qui fonctionne parfaitement.

## Prérequis à installer

### 1. Python 3.11
- Téléchargez Python 3.11 depuis https://www.python.org/downloads/
- **IMPORTANT** : Cochez "Add Python to PATH" lors de l'installation
- Vérifiez l'installation en ouvrant un terminal et tapant : `python --version`

### 2. PostgreSQL
- Téléchargez PostgreSQL 16 depuis https://www.postgresql.org/download/windows/
- Installez avec les paramètres par défaut
- **Notez bien le mot de passe administrateur que vous définissez**
- Le service PostgreSQL doit démarrer automatiquement

### 3. Git (optionnel mais recommandé)
- Téléchargez depuis https://git-scm.com/download/win

## Étapes d'installation

### Étape 1 : Préparation du dossier
1. Créez un dossier pour votre projet : `C:\MonProjetImmobilier`
2. Extrayez le fichier ZIP de Replit dans ce dossier
3. Ouvrez un terminal (CMD ou PowerShell) dans ce dossier

### Étape 2 : Configuration de l'environnement virtuel Python
```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
venv\Scripts\activate

# Mettre à jour pip
python -m pip install --upgrade pip
```

### Étape 3 : Installation des dépendances
```bash
# Installer toutes les dépendances
pip install flask==3.1.1
pip install flask-sqlalchemy==3.1.1
pip install flask-wtf==1.2.2
pip install psycopg2-binary==2.9.10
pip install reportlab==4.4.1
pip install gunicorn==23.0.0
pip install python-dateutil==2.9.0
pip install email-validator
pip install sendgrid
pip install twilio
pip install werkzeug
pip install wtforms
pip install pypdf2
pip install translations
```

### Étape 4 : Configuration de la base de données PostgreSQL

#### 4.1 Création de la base de données
```sql
-- Ouvrez pgAdmin ou utilisez psql
-- Connectez-vous avec l'utilisateur postgres et le mot de passe défini

CREATE DATABASE gestion_immobiliere;
CREATE USER immobilier_user WITH PASSWORD 'motdepasse_securise';
GRANT ALL PRIVILEGES ON DATABASE gestion_immobiliere TO immobilier_user;
```

#### 4.2 Configuration des variables d'environnement
Créez un fichier `.env` dans le dossier racine du projet :

```env
# Base de données
DATABASE_URL=postgresql://immobilier_user:motdepasse_securise@localhost:5432/gestion_immobiliere

# Sécurité
SESSION_SECRET=votre_clé_secrète_très_longue_et_complexe

# Services optionnels (laissez vide si non utilisés)
SENDGRID_API_KEY=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
```

### Étape 5 : Modification pour l'environnement local

#### 5.1 Créer un fichier de démarrage local
Créez `run_local.py` :

```python
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Importer l'application
from main import app

if __name__ == '__main__':
    # Configuration pour l'environnement local
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_ECHO'] = False  # Mettre True pour voir les requêtes SQL
    
    print("🚀 Démarrage du serveur local...")
    print("📧 Application accessible sur : http://localhost:5000")
    print("🛑 Appuyez sur Ctrl+C pour arrêter")
    
    # Démarrer le serveur de développement Flask
    app.run(host='127.0.0.1', port=5000, debug=True)
```

#### 5.2 Installer python-dotenv
```bash
pip install python-dotenv
```

#### 5.3 Modifier app.py pour supporter .env
Ajoutez au début de `app.py` :

```python
import os
from dotenv import load_dotenv

# Charger les variables d'environnement en local
load_dotenv()
```

### Étape 6 : Import des données depuis Replit

#### 6.1 Exporter les données depuis Replit
Depuis Replit, exécutez ce script pour créer un export :

```python
# Script à exécuter sur Replit pour créer l'export
import subprocess
import os
from datetime import datetime

# Créer un export de la base de données
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
export_file = f"export_pour_local_{timestamp}.sql"

# Commande d'export PostgreSQL
cmd = f"pg_dump {os.environ['DATABASE_URL']} > {export_file}"
subprocess.run(cmd, shell=True)

print(f"Export créé : {export_file}")
print("Téléchargez ce fichier depuis Replit pour l'importer en local")
```

#### 6.2 Importer en local
```bash
# Dans votre terminal local, importez les données
psql -U immobilier_user -d gestion_immobiliere -f export_pour_local_XXXXXXXX.sql
```

### Étape 7 : Premier démarrage
```bash
# Activer l'environnement virtuel si ce n'est pas fait
venv\Scripts\activate

# Démarrer l'application
python run_local.py
```

## Structure des dossiers après installation
```
C:\MonProjetImmobilier\
├── venv\                    # Environnement virtuel Python
├── static\                  # Fichiers statiques
│   ├── uploads\            # Photos des biens
│   └── documents\          # Documents des contrats
├── templates\              # Templates HTML
├── .env                    # Variables d'environnement (À CRÉER)
├── run_local.py           # Script de démarrage local (À CRÉER)
├── app.py                 # Application Flask
├── main.py                # Point d'entrée
├── models.py              # Modèles de base de données
├── routes.py              # Routes principales
├── routes_comptabilite.py # Routes comptabilité
├── forms.py               # Formulaires
├── quittances.py          # Génération PDF
└── autres fichiers...
```

## Résolution des erreurs courantes

### Erreur : Module non trouvé
```bash
# Solution : Vérifier que l'environnement virtuel est activé
venv\Scripts\activate
pip list  # Vérifier les modules installés
```

### Erreur : Connexion à la base de données
1. Vérifiez que PostgreSQL est démarré
2. Vérifiez les paramètres dans `.env`
3. Testez la connexion : `psql -U immobilier_user -d gestion_immobiliere`

### Erreur : Port 5000 déjà utilisé
```python
# Dans run_local.py, changez le port
app.run(host='127.0.0.1', port=5001, debug=True)
```

### Erreur : Permissions de fichiers
- Créez manuellement les dossiers `static/uploads` et `static/documents`
- Vérifiez les droits d'écriture

## Scripts utiles

### Sauvegarde locale
Créez `backup_local.bat` :
```batch
@echo off
echo Sauvegarde de la base de données...
set timestamp=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
pg_dump -U immobilier_user gestion_immobiliere > backup_local_%timestamp%.sql
echo Sauvegarde terminée : backup_local_%timestamp%.sql
pause
```

### Démarrage rapide
Créez `start_app.bat` :
```batch
@echo off
cd /d "C:\MonProjetImmobilier"
call venv\Scripts\activate
python run_local.py
pause
```

## Maintenance

### Mise à jour depuis Replit
1. Téléchargez la nouvelle version ZIP depuis Replit
2. Sauvegardez votre base de données locale
3. Remplacez les fichiers (gardez `.env` et `run_local.py`)
4. Redémarrez l'application

### Synchronisation des données
- Exportez régulièrement depuis Replit
- Importez en local selon vos besoins
- Évitez de modifier les données locales si vous voulez rester synchronisé

## Support
- Gardez toujours une sauvegarde de votre base de données
- Testez d'abord en local avant toute modification
- La version Replit reste votre référence principale

---
**Note importante** : Ce guide permet d'avoir une copie locale indépendante. Toute modification locale n'affectera pas la version Replit qui continue de fonctionner normalement.