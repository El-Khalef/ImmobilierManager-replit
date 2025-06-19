# Installation Locale - Guide Rapide

## Fichiers créés pour votre installation locale

J'ai préparé tous les fichiers nécessaires pour installer votre système en local sans affecter la version Replit :

### 📋 Guide complet
- **INSTALLATION_LOCALE.md** - Guide détaillé étape par étape

### 🚀 Scripts d'installation automatique
- **install_local_windows.bat** - Installation automatique pour Windows
- **requirements_local.txt** - Liste des dépendances Python

### 🔧 Configuration
- **.env.template** - Modèle de configuration à copier vers .env
- **run_local.py** - Script de démarrage pour l'environnement local

### 🔍 Diagnostic et test
- **test_rapide.py** - Test immédiat des problèmes
- **diagnostic_local.py** - Diagnostic complet avec solutions

### 📊 Export des données
- **export_simple.py** - Export des données depuis Replit
- **donnees_pour_local_20250619_040443.sql** - Vos données exportées

## Installation en 3 étapes

### 1. Téléchargement
- Téléchargez le ZIP depuis Replit
- Extrayez dans un dossier local (ex: C:\MonProjetImmobilier)

### 2. Installation automatique
```cmd
# Dans le dossier du projet
install_local_windows.bat
```

### 3. Configuration
- Éditez le fichier .env créé
- Configurez votre base PostgreSQL
- Importez vos données

## Test rapide
```cmd
python test_rapide.py
```

## Démarrage
```cmd
python run_local.py
```

## Support des erreurs

Envoyez-moi les erreurs que vous rencontrez et j'identifierai les solutions spécifiques.

Les erreurs courantes et leurs solutions sont documentées dans les scripts de diagnostic.