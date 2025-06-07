@echo off
chcp 65001 >nul
echo ========================================
echo 🏠 GESTION IMMOBILIÈRE - SETUP RAPIDE
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    echo Téléchargez Python depuis https://python.org/downloads/
    echo N'oubliez pas de cocher "Add Python to PATH"
    pause
    exit /b 1
)

echo ✅ Python détecté
python --version

REM Créer l'environnement virtuel
echo.
echo 📦 Création de l'environnement virtuel...
python -m venv venv
if errorlevel 1 (
    echo ❌ Erreur lors de la création de l'environnement virtuel
    pause
    exit /b 1
)

REM Activer l'environnement virtuel
echo.
echo 🔧 Activation de l'environnement virtuel...
call venv\Scripts\activate

REM Installer les dépendances
echo.
echo 📥 Installation des dépendances...
python install_dependencies.py

REM Créer le fichier .env si inexistant
if not exist .env (
    echo.
    echo 📝 Création du fichier de configuration...
    copy .env.template .env >nul 2>&1
    echo ⚠️  IMPORTANT: Modifiez le fichier .env avec vos paramètres de base de données
)

echo.
echo ========================================
echo ✅ INSTALLATION TERMINÉE
echo ========================================
echo.
echo Prochaines étapes:
echo 1. Installez PostgreSQL si ce n'est pas fait
echo 2. Créez la base de données 'immobilier_db'
echo 3. Modifiez le fichier .env avec vos paramètres
echo 4. Lancez: python main.py
echo.
echo Consultez INSTALLATION_WINDOWS.md pour les détails
echo.
pause