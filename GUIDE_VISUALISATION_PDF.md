# Guide Complet : Ajouter la Visualisation PDF en Mode Aperçu

## 1. Vue d'ensemble de la fonctionnalité

Cette fonctionnalité permettra aux utilisateurs de :
- Visualiser les documents PDF directement dans le navigateur
- Modifier les documents depuis l'aperçu
- Éviter les téléchargements répétés

## 2. Architecture actuelle du projet

### Structure des fichiers importants :
```
votre_projet/
├── app.py                 # Configuration Flask principale
├── models.py              # Modèles de base de données
├── routes.py              # Routes et logique métier
├── forms.py               # Formulaires Flask-WTF
├── templates/             # Templates HTML
│   ├── base.html         # Template de base
│   ├── contrats/         # Templates des contrats
│   └── documents/        # Templates des documents
├── static/               # Fichiers statiques (CSS, JS)
└── quittances_template.py # Génération PDF
```

## 3. Dépendances nécessaires

### Packages Python requis :
```python
# Déjà installés dans votre projet :
- Flask
- Flask-SQLAlchemy
- ReportLab (pour PDF)

# À ajouter si nécessaire :
- PyPDF2 (déjà installé)
```

### Technologies front-end :
```html
<!-- Déjà inclus via Bootstrap : -->
- Bootstrap CSS/JS
- jQuery (optionnel)

<!-- À ajouter : -->
- PDF.js (bibliothèque JavaScript pour afficher PDF)
```

## 4. Étapes d'implémentation

### Étape 1 : Modifier le modèle DocumentContrat

**Fichier à modifier :** `models.py`

**Localisation :** Cherchez la classe `DocumentContrat` (environ ligne 200-250)

**Modification à apporter :**
```python
# Ajouter une méthode pour obtenir l'URL d'aperçu
def get_preview_url(self):
    """Retourne l'URL pour l'aperçu du document"""
    return url_for('document_preview', doc_id=self.id)

def get_edit_url(self):
    """Retourne l'URL pour modifier le document"""
    return url_for('document_edit', doc_id=self.id)
```

### Étape 2 : Ajouter les nouvelles routes

**Fichier à modifier :** `routes.py`

**Où ajouter :** Après les routes existantes des documents (cherchez `@app.route('/documents/`)

**Code à ajouter :**
```python
@app.route('/documents/<int:doc_id>/preview')
def document_preview(doc_id):
    """Affiche l'aperçu d'un document"""
    document = DocumentContrat.query.get_or_404(doc_id)
    
    # Construire le chemin du fichier
    chemin_fichier = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'uploads'), 
                                  document.nom_fichier)
    
    # Vérifier que le fichier existe
    if not os.path.exists(chemin_fichier):
        flash('Fichier non trouvé', 'error')
        return redirect(url_for('documents_index'))
    
    return render_template('documents/preview.html', 
                         document=document,
                         fichier_url=url_for('document_file', doc_id=doc_id))

@app.route('/documents/<int:doc_id>/file')
def document_file(doc_id):
    """Sert le fichier document pour l'aperçu"""
    document = DocumentContrat.query.get_or_404(doc_id)
    chemin_fichier = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'uploads'), 
                                  document.nom_fichier)
    
    if not os.path.exists(chemin_fichier):
        return "Fichier non trouvé", 404
    
    return send_file(chemin_fichier, as_attachment=False)

@app.route('/documents/<int:doc_id>/edit')
def document_edit(doc_id):
    """Page d'édition d'un document"""
    document = DocumentContrat.query.get_or_404(doc_id)
    form = DocumentContratForm(obj=document)
    
    # Pré-remplir le formulaire avec les données existantes
    form.contrat_id.data = document.contrat_id
    form.type_document.data = document.type_document
    form.description.data = document.description
    
    return render_template('documents/edit.html', 
                         form=form, 
                         document=document)
```

### Étape 3 : Créer le template d'aperçu

**Fichier à créer :** `templates/documents/preview.html`

**Contenu :**
```html
{% extends "base.html" %}

{% block title %}Aperçu - {{ document.nom_fichier }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-12">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h2>Aperçu du document</h2>
                <div>
                    <a href="{{ document.get_edit_url() }}" class="btn btn-primary">
                        <i class="fas fa-edit"></i> Modifier
                    </a>
                    <a href="{{ url_for('documents_index') }}" class="btn btn-secondary">
                        <i class="fas fa-arrow-left"></i> Retour
                    </a>
                </div>
            </div>
            
            <!-- Informations du document -->
            <div class="card mb-3">
                <div class="card-body">
                    <h5 class="card-title">{{ document.nom_fichier }}</h5>
                    <p class="card-text">
                        <strong>Type :</strong> {{ document.type_document }}<br>
                        <strong>Contrat :</strong> {{ document.contrat.bien.titre if document.contrat else 'N/A' }}<br>
                        <strong>Description :</strong> {{ document.description or 'Aucune description' }}
                    </p>
                </div>
            </div>
            
            <!-- Aperçu PDF -->
            {% if document.nom_fichier.lower().endswith('.pdf') %}
            <div class="card">
                <div class="card-header">
                    <h5>Aperçu PDF</h5>
                </div>
                <div class="card-body p-0">
                    <iframe src="{{ fichier_url }}" 
                            width="100%" 
                            height="800px" 
                            style="border: none;">
                        <p>Votre navigateur ne supporte pas l'affichage PDF. 
                           <a href="{{ fichier_url }}" target="_blank">Télécharger le fichier</a>
                        </p>
                    </iframe>
                </div>
            </div>
            {% else %}
            <div class="alert alert-info">
                <h5>Aperçu non disponible</h5>
                <p>L'aperçu n'est disponible que pour les fichiers PDF.</p>
                <a href="{{ fichier_url }}" class="btn btn-primary" target="_blank">
                    Ouvrir le fichier
                </a>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```

### Étape 4 : Créer le template d'édition

**Fichier à créer :** `templates/documents/edit.html`

**Contenu :**
```html
{% extends "base.html" %}

{% block title %}Modifier - {{ document.nom_fichier }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-8">
            <h2>Modifier le document</h2>
            
            <form method="POST" enctype="multipart/form-data">
                {{ form.hidden_tag() }}
                
                <div class="card">
                    <div class="card-body">
                        <div class="mb-3">
                            {{ form.contrat_id.label(class="form-label") }}
                            {{ form.contrat_id(class="form-select") }}
                        </div>
                        
                        <div class="mb-3">
                            {{ form.type_document.label(class="form-label") }}
                            {{ form.type_document(class="form-select") }}
                        </div>
                        
                        <div class="mb-3">
                            {{ form.description.label(class="form-label") }}
                            {{ form.description(class="form-control", rows="3") }}
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Fichier actuel</label>
                            <p class="text-muted">{{ document.nom_fichier }}</p>
                            {{ form.fichier.label(class="form-label") }}
                            {{ form.fichier(class="form-control") }}
                            <small class="form-text text-muted">
                                Laissez vide pour conserver le fichier actuel
                            </small>
                        </div>
                    </div>
                </div>
                
                <div class="mt-3">
                    {{ form.submit(class="btn btn-primary") }}
                    <a href="{{ url_for('document_preview', doc_id=document.id) }}" 
                       class="btn btn-secondary">Annuler</a>
                </div>
            </form>
        </div>
        
        <div class="col-md-4">
            <div class="card">
                <div class="card-header">
                    <h5>Aperçu actuel</h5>
                </div>
                <div class="card-body">
                    {% if document.nom_fichier.lower().endswith('.pdf') %}
                    <iframe src="{{ url_for('document_file', doc_id=document.id) }}" 
                            width="100%" 
                            height="400px" 
                            style="border: 1px solid #ddd;">
                    </iframe>
                    {% else %}
                    <p class="text-muted">Aperçu non disponible pour ce type de fichier</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Étape 5 : Modifier la liste des documents

**Fichier à modifier :** `templates/documents/index.html`

**Modification :** Ajouter des boutons d'aperçu dans le tableau

**Code à ajouter :** Dans la colonne "Actions" du tableau :
```html
<a href="{{ url_for('document_preview', doc_id=document.id) }}" 
   class="btn btn-sm btn-info" title="Aperçu">
    <i class="fas fa-eye"></i>
</a>
```

## 5. Configuration des uploads

### Fichier à modifier : `app.py`

**Ajout de configuration :**
```python
import os

# Configuration des uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Créer le dossier uploads s'il n'existe pas
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
```

## 6. Gestion des erreurs et sécurité

### Validation des types de fichiers

**Dans routes.py, ajouter :**
```python
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

### Sécurisation des accès fichiers

**Dans la route document_file :**
```python
@app.route('/documents/<int:doc_id>/file')
def document_file(doc_id):
    document = DocumentContrat.query.get_or_404(doc_id)
    
    # Vérification de sécurité : s'assurer que le fichier appartient bien à un document
    chemin_fichier = os.path.join(current_app.config['UPLOAD_FOLDER'], 
                                  secure_filename(document.nom_fichier))
    
    # Vérifier que le chemin ne sort pas du dossier uploads
    chemin_absolu = os.path.abspath(chemin_fichier)
    dossier_uploads = os.path.abspath(current_app.config['UPLOAD_FOLDER'])
    
    if not chemin_absolu.startswith(dossier_uploads):
        return "Accès interdit", 403
    
    if not os.path.exists(chemin_fichier):
        return "Fichier non trouvé", 404
    
    return send_file(chemin_fichier, as_attachment=False)
```

## 7. Tests et validation

### Étapes de test :

1. **Test d'aperçu :**
   - Uploadez un document PDF
   - Cliquez sur le bouton "Aperçu"
   - Vérifiez que le PDF s'affiche correctement

2. **Test d'édition :**
   - Depuis l'aperçu, cliquez sur "Modifier"
   - Changez la description
   - Sauvegardez et vérifiez les modifications

3. **Test de sécurité :**
   - Tentez d'accéder à un fichier inexistant
   - Vérifiez que les erreurs sont gérées proprement

## 8. Déploiement et hébergement

### Options d'hébergement :

1. **Replit Deployments (recommandé) :**
   - Votre projet est déjà sur Replit
   - Utilisez le bouton "Deploy" dans l'interface
   - Configuration automatique

2. **Heroku :**
   ```bash
   # Créer un fichier requirements.txt
   pip freeze > requirements.txt
   
   # Créer un Procfile
   echo "web: gunicorn main:app" > Procfile
   
   # Déployer
   git init
   git add .
   git commit -m "Initial commit"
   heroku create votre-app-name
   git push heroku main
   ```

3. **VPS (DigitalOcean, Linode) :**
   ```bash
   # Sur le serveur
   sudo apt update
   sudo apt install python3-pip nginx
   pip3 install -r requirements.txt
   
   # Configuration Nginx
   sudo nano /etc/nginx/sites-available/votre-app
   ```

### Préparation pour l'autonomie :

1. **Documentation du code :**
   - Commentez vos modifications
   - Créez un README.md avec les instructions
   - Documentez les variables d'environnement

2. **Structure des fichiers :**
   ```
   votre_projet/
   ├── README.md              # Instructions d'installation
   ├── requirements.txt       # Dépendances Python
   ├── .env.example          # Variables d'environnement
   ├── docs/                 # Documentation
   └── tests/                # Tests unitaires
   ```

3. **Variables d'environnement :**
   ```bash
   # .env
   DATABASE_URL=postgresql://...
   FLASK_SECRET_KEY=votre_clé_secrète
   UPLOAD_FOLDER=/path/to/uploads
   ```

## 9. Maintenance et évolutions futures

### Améliorations possibles :

1. **Annotations PDF :**
   - Intégrer PDF.js avec annotations
   - Sauvegarder les annotations en base

2. **Versioning des documents :**
   - Historique des modifications
   - Comparaison de versions

3. **Recherche dans les documents :**
   - Extraction de texte PDF
   - Index de recherche full-text

### Outils de développement :

1. **Debugging :**
   ```python
   # Dans app.py
   if __name__ == '__main__':
       app.run(debug=True, host='0.0.0.0', port=5000)
   ```

2. **Logs :**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

3. **Base de données :**
   ```bash
   # Backup
   pg_dump $DATABASE_URL > backup.sql
   
   # Restore
   psql $DATABASE_URL < backup.sql
   ```

## 10. Ressources pour continuer seul

### Documentation officielle :
- Flask : https://flask.palletsprojects.com/
- SQLAlchemy : https://docs.sqlalchemy.org/
- Bootstrap : https://getbootstrap.com/docs/
- PDF.js : https://mozilla.github.io/pdf.js/

### Communautés :
- Stack Overflow (tag: flask, python)
- Reddit : r/flask, r/python
- Discord : Python Discord Server

### Outils utiles :
- VS Code avec extensions Python
- Postman pour tester les APIs
- pgAdmin pour gérer PostgreSQL

Ce guide vous donne toutes les clés pour implémenter et maintenir cette fonctionnalité de manière autonome. Chaque section explique non seulement le "quoi" mais aussi le "pourquoi" et le "comment", vous permettant de comprendre et d'adapter le code selon vos besoins futurs.