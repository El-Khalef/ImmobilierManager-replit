# Guide de Déploiement en Production

## Configuration pour la Production

### 1. Variables d'Environnement Production
```env
# Base de données production
DATABASE_URL=postgresql://user:password@hostname:5432/production_db

# Sécurité
SESSION_SECRET=cle_secrete_complexe_64_caracteres_minimum
FLASK_ENV=production
FLASK_DEBUG=False

# Services externes
SENDGRID_API_KEY=sg.xxx
TWILIO_ACCOUNT_SID=ACxxx
TWILIO_AUTH_TOKEN=xxx
TWILIO_PHONE_NUMBER=+xxxxx
```

### 2. Modifications pour Production

#### A. Configuration App (app.py)
```python
import os
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Configuration sécurisée pour la production
    app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET')
    app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = '/var/www/uploads'  # Chemin absolu
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    
    # Sécurité HTTPS
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    return app
```

#### B. Serveur WSGI (wsgi.py)
```python
from app import create_app
import os

application = create_app()

if __name__ == "__main__":
    application.run()
```

## Options de Déploiement

### Option 1: VPS Linux (Recommandé)

#### Prérequis Serveur
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv postgresql nginx supervisor
```

#### Installation Application
```bash
# Créer utilisateur dédié
sudo useradd -m -s /bin/bash immobilier
sudo su - immobilier

# Cloner et configurer
git clone [URL_PROJET] /home/immobilier/app
cd /home/immobilier/app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Configuration Nginx
```nginx
# /etc/nginx/sites-available/immobilier
server {
    listen 80;
    server_name votre-domaine.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /home/immobilier/app/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

#### Configuration Supervisor
```ini
# /etc/supervisor/conf.d/immobilier.conf
[program:immobilier]
command=/home/immobilier/app/venv/bin/gunicorn --bind 127.0.0.1:5000 --workers 3 wsgi:application
directory=/home/immobilier/app
user=immobilier
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/immobilier.log
```

### Option 2: Heroku

#### Fichiers Requis
```python
# Procfile
web: gunicorn wsgi:application

# runtime.txt
python-3.11.5
```

#### Commandes Déploiement
```bash
heroku create nom-app-immobilier
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set SESSION_SECRET=votre_cle_secrete
git push heroku main
heroku run python -c "from app import create_app, db; app=create_app(); app.app_context().push(); db.create_all()"
```

### Option 3: DigitalOcean App Platform

#### Configuration (app.yaml)
```yaml
name: gestion-immobiliere
services:
- name: web
  source_dir: /
  github:
    repo: votre-username/votre-repo
    branch: main
  run_command: gunicorn --worker-connections 1000 --worker-class gevent wsgi:application
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: DATABASE_URL
    scope: RUN_TIME
    type: SECRET
  - key: SESSION_SECRET
    scope: RUN_TIME
    type: SECRET
databases:
- name: db
  engine: PG
  size: db-s-dev-database
```

## Sécurité et Performance

### 1. SSL/HTTPS
```bash
# Let's Encrypt (gratuit)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d votre-domaine.com
```

### 2. Sauvegarde Base de Données
```bash
# Script de sauvegarde automatique
#!/bin/bash
# /home/immobilier/backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump $DATABASE_URL > /home/immobilier/backups/backup_$DATE.sql
find /home/immobilier/backups -name "backup_*.sql" -mtime +7 -delete
```

### 3. Monitoring
```python
# logging_config.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    if not app.debug:
        file_handler = RotatingFileHandler('logs/immobilier.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
```

## Tests de Déploiement

### 1. Tests Fonctionnels
```python
# test_production.py
import requests

def test_application():
    base_url = "https://votre-domaine.com"
    
    # Test page d'accueil
    response = requests.get(base_url)
    assert response.status_code == 200
    
    # Test pages principales
    pages = ['/clients', '/biens', '/contrats', '/documents']
    for page in pages:
        response = requests.get(f"{base_url}{page}")
        assert response.status_code in [200, 302]  # 302 pour redirection login
```

### 2. Tests de Performance
```bash
# Test de charge avec Apache Benchmark
ab -n 1000 -c 10 https://votre-domaine.com/

# Monitoring ressources
htop
iotop
netstat -tuln
```

## Maintenance

### 1. Mises à Jour
```bash
# Script de mise à jour
#!/bin/bash
cd /home/immobilier/app
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo supervisorctl restart immobilier
sudo nginx -t && sudo systemctl reload nginx
```

### 2. Surveillance Logs
```bash
# Surveillance en temps réel
tail -f /var/log/immobilier.log
tail -f /var/log/nginx/access.log
tail -f /var/log/postgresql/postgresql.log
```

### 3. Optimisation Performance
```python
# Configuration Gunicorn optimisée
# gunicorn_config.py
bind = "127.0.0.1:5000"
workers = 3
worker_class = "gevent"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
```

## Coûts Estimés

### VPS (DigitalOcean/Linode)
- Serveur Basic (1GB RAM): 5-6€/mois
- Base de données PostgreSQL: Incluse
- Domaine: 10-15€/an
- SSL: Gratuit (Let's Encrypt)

### Heroku
- Dyno Basic: 7$/mois
- PostgreSQL Hobby: Gratuit (limité)
- Domaine custom: Gratuit

### Services Externes (optionnel)
- SendGrid: Plan gratuit 100 emails/jour
- Twilio: Pay-per-use SMS
- Monitoring (UptimeRobot): Gratuit

## Support Post-Déploiement

1. Documentation utilisateur complète
2. Formation administrateur
3. Scripts de maintenance automatisés
4. Monitoring et alertes configurés
5. Plan de sauvegarde et restauration