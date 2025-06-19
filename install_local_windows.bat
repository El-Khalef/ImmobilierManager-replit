@echo off
echo.
echo ========================================
echo INSTALLATION LOCALE - GESTION IMMOBILIERE
echo ========================================
echo.

:: Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou pas dans PATH
    echo Installez Python 3.11 depuis https://www.python.org/downloads/
    echo IMPORTANT: Cochez "Add Python to PATH" lors de l'installation
    pause
    exit /b 1
)

echo Python detecte: 
python --version

:: Créer l'environnement virtuel
echo.
echo Creation de l'environnement virtuel...
python -m venv venv
if errorlevel 1 (
    echo ERREUR: Impossible de creer l'environnement virtuel
    pause
    exit /b 1
)

:: Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

:: Mettre à jour pip
echo Mise a jour de pip...
python -m pip install --upgrade pip

:: Installer les dépendances
echo.
echo Installation des dependances...
if exist requirements_local.txt (
    pip install -r requirements_local.txt
) else (
    echo Installation des modules un par un...
    pip install Flask==3.1.1
    pip install Flask-SQLAlchemy==3.1.1
    pip install Flask-WTF==1.2.2
    pip install psycopg2-binary==2.9.10
    pip install reportlab==4.4.1
    pip install python-dateutil==2.9.0
    pip install email-validator
    pip install WTForms
    pip install python-dotenv
    pip install sendgrid
    pip install twilio
    pip install gunicorn
    pip install PyPDF2
)

if errorlevel 1 (
    echo ERREUR: Installation des dependances echouee
    pause
    exit /b 1
)

:: Créer les dossiers nécessaires
echo.
echo Creation des dossiers...
if not exist "static\uploads" mkdir "static\uploads"
if not exist "static\documents" mkdir "static\documents"

:: Vérifier si .env existe
if not exist ".env" (
    echo.
    echo ATTENTION: Fichier .env manquant
    echo Creation d'un fichier .env template...
    
    echo # Configuration pour l'environnement local > .env
    echo # MODIFIEZ ces valeurs selon votre configuration >> .env
    echo. >> .env
    echo # Base de donnees PostgreSQL >> .env
    echo DATABASE_URL=postgresql://immobilier_user:votre_mot_de_passe@localhost:5432/gestion_immobiliere >> .env
    echo. >> .env
    echo # Cle secrete pour Flask (changez cette valeur^) >> .env
    echo SESSION_SECRET=votre_cle_secrete_tres_longue_et_complexe_changez_moi >> .env
    echo. >> .env
    echo # Services optionnels (laissez vide si non utilises^) >> .env
    echo SENDGRID_API_KEY= >> .env
    echo TWILIO_ACCOUNT_SID= >> .env
    echo TWILIO_AUTH_TOKEN= >> .env
    echo TWILIO_PHONE_NUMBER= >> .env
    
    echo.
    echo Fichier .env cree avec des valeurs par defaut
    echo IMPORTANT: Editez le fichier .env avec vos vrais parametres
)

:: Lancer le diagnostic
echo.
echo Lancement du diagnostic...
python diagnostic_local.py

echo.
echo ========================================
echo INSTALLATION TERMINEE
echo ========================================
echo.
echo Prochaines etapes:
echo 1. Configurez PostgreSQL si ce n'est pas fait
echo 2. Editez le fichier .env avec vos parametres
echo 3. Importez vos donnees depuis Replit
echo 4. Lancez: python run_local.py
echo.
echo Consultez INSTALLATION_LOCALE.md pour plus de details
echo.
pause