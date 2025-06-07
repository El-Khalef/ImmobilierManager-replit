# Guide d'Installation - Projet Gestion Immobilière sur Windows

## Prérequis

### 1. Python 3.11 ou supérieur
- Téléchargez depuis [python.org](https://www.python.org/downloads/)
- **Important** : Cochez "Add Python to PATH" lors de l'installation
- Vérifiez l'installation :
```cmd
python --version
pip --version
```

### 2. PostgreSQL
- Téléchargez depuis [postgresql.org](https://www.postgresql.org/downloads/windows/)
- Installez avec les paramètres par défaut
- Notez le mot de passe que vous définissez pour l'utilisateur `postgres`
- Vérifiez l'installation :
```cmd
psql --version
```

### 3. Git (optionnel)
- Téléchargez depuis [git-scm.com](https://git-scm.com/download/win)

## Étapes d'Installation

### 1. Télécharger le Projet
Si vous avez Git :
```cmd
git clone [URL_DU_PROJET]
cd [NOM_DU_PROJET]
```

Sinon, téléchargez et décompressez le projet dans un dossier.

### 2. Créer l'Environnement Virtuel
Ouvrez l'invite de commande (cmd) dans le dossier du projet :
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Installer les Dépendances
```cmd
pip install --upgrade pip
pip install flask flask-sqlalchemy flask-wtf psycopg2-binary reportlab pypdf2 python-dateutil werkzeug wtforms email-validator sendgrid twilio gunicorn
```

### 4. Configurer la Base de Données

#### A. Créer la base de données PostgreSQL
Ouvrez pgAdmin ou utilisez psql :
```sql
-- Connectez-vous avec l'utilisateur postgres
CREATE DATABASE immobilier_db;
CREATE USER immobilier_user WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE immobilier_db TO immobilier_user;
```

#### B. Configurer les Variables d'Environnement
Créez un fichier `.env` dans le dossier racine :
```env
DATABASE_URL=postgresql://immobilier_user:votre_mot_de_passe@localhost:5432/immobilier_db
SESSION_SECRET=votre_cle_secrete_unique
FLASK_ENV=development
FLASK_DEBUG=True

# Optionnel - Services externes
SENDGRID_API_KEY=votre_cle_sendgrid
TWILIO_ACCOUNT_SID=votre_sid_twilio
TWILIO_AUTH_TOKEN=votre_token_twilio
TWILIO_PHONE_NUMBER=votre_numero_twilio
```

### 5. Initialiser la Base de Données
```cmd
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Base de données initialisée')"
```

### 6. Créer les Dossiers Nécessaires
```cmd
mkdir static\uploads
mkdir static\documents
```

### 7. Lancer l'Application
```cmd
python main.py
```

L'application sera accessible sur : http://localhost:5000

## Structure des Fichiers

```
votre_projet/
├── app.py              # Configuration Flask
├── main.py             # Point d'entrée
├── models.py           # Modèles de base de données
├── routes.py           # Routes et logique métier
├── forms.py            # Formulaires Flask-WTF
├── quittances_template.py  # Génération PDF
├── .env               # Variables d'environnement
├── static/
│   ├── uploads/       # Nouveaux documents
│   ├── documents/     # Documents existants
│   └── css/           # Styles CSS
├── templates/         # Templates HTML
└── venv/             # Environnement virtuel
```

## Dépannage

### Erreur PostgreSQL
- Vérifiez que PostgreSQL est démarré (services Windows)
- Testez la connexion :
```cmd
psql -h localhost -U immobilier_user -d immobilier_db
```

### Erreur Python/Pip
- Utilisez `python -m pip` au lieu de `pip`
- Vérifiez que l'environnement virtuel est activé

### Erreur de Permissions
- Exécutez l'invite de commande en tant qu'administrateur
- Vérifiez les permissions du dossier du projet

### Port Déjà Utilisé
Si le port 5000 est occupé :
```cmd
python -c "from app import app; app.run(host='0.0.0.0', port=8000, debug=True)"
```

## Configuration Avancée

### Pour l'Envoi d'E-mails (SendGrid)
1. Créez un compte sur sendgrid.com
2. Générez une clé API
3. Ajoutez `SENDGRID_API_KEY` dans le fichier `.env`

### Pour les SMS (Twilio)
1. Créez un compte sur twilio.com
2. Obtenez vos identifiants
3. Ajoutez les variables Twilio dans le fichier `.env`

### Sauvegarde de la Base de Données
```cmd
pg_dump -U immobilier_user -h localhost immobilier_db > sauvegarde.sql
```

### Restauration de la Base de Données
```cmd
psql -U immobilier_user -h localhost immobilier_db < sauvegarde.sql
```

## Utilisation

1. **Dashboard** : Vue d'ensemble des statistiques
2. **Clients** : Gestion des propriétaires, locataires, acheteurs
3. **Biens** : Gestion du patrimoine immobilier avec cartes interactives
4. **Contrats** : Suivi des contrats de location
5. **Paiements** : Enregistrement et suivi des loyers
6. **Documents** : Stockage et prévisualisation des documents
7. **Quittances** : Génération automatique de quittances PDF

## Données de Test

Pour tester l'application, vous pouvez créer des données d'exemple via l'interface ou importer le fichier SQL fourni.

## Support

En cas de problème :
1. Vérifiez les logs dans la console
2. Consultez le fichier `GUIDE_PREVISUALISATION_DOCUMENTS.md`
3. Vérifiez la configuration de la base de données
4. Assurez-vous que tous les prérequis sont installés