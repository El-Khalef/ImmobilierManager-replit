import os
from pathlib import Path

# Configuration de la structure
PROJECT_NAME = "immobilier_app"
STRUCTURE = {
    "app": {
        "__init__.py": """from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import biens, clients
    app.register_blueprint(biens.bp)
    app.register_blueprint(clients.bp)

    return app
""",
        "config.py": """import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'une-cle-secrete-tres-secure'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \\
        'postgresql://username:password@localhost/immobilier_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
""",
        "models.py": """from datetime import datetime
from app import db

class BienImmobilier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_bien = db.Column(db.String(50), nullable=False)  # Appartement, maison, terrain...
    adresse = db.Column(db.String(200), nullable=False)
    ville = db.Column(db.String(100), nullable=False)
    code_postal = db.Column(db.String(20), nullable=False)
    surface = db.Column(db.Float, nullable=False)
    prix = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    disponibilite = db.Column(db.Boolean, default=True)
    # Relations
    proprietaire_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    photos = db.relationship('Photo', backref='bien', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<BienImmobilier {self.adresse}, {self.ville}>'

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telephone = db.Column(db.String(20))
    type_client = db.Column(db.String(20), nullable=False)  # Propriétaire, locataire, acheteur...
    biens = db.relationship('BienImmobilier', backref='proprietaire', lazy=True)

    def __repr__(self):
        return f'<Client {self.prenom} {self.nom}>'

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_fichier = db.Column(db.String(100), nullable=False)
    est_principale = db.Column(db.Boolean, default=False)
    bien_id = db.Column(db.Integer, db.ForeignKey('bien_immobilier.id'), nullable=False)

    def __repr__(self):
        return f'<Photo {self.nom_fichier}>'
""",
        "routes": {
            "__init__.py": "",
            "biens.py": """from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import BienImmobilier, Photo
from app.routes.forms import BienForm

bp = Blueprint('biens', __name__)

@bp.route('/')
@login_required
def index():
    biens = BienImmobilier.query.all()
    return render_template('biens/index.html', biens=biens)

@bp.route('/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter():
    form = BienForm()
    if form.validate_on_submit():
        bien = BienImmobilier(
            type_bien=form.type_bien.data,
            adresse=form.adresse.data,
            ville=form.ville.data,
            code_postal=form.code_postal.data,
            surface=form.surface.data,
            prix=form.prix.data,
            description=form.description.data,
            proprietaire_id=form.proprietaire_id.data
        )
        db.session.add(bien)
        db.session.commit()
        flash('Bien immobilier ajouté avec succès!', 'success')
        return redirect(url_for('biens.index'))
    return render_template('biens/ajouter.html', form=form)

@bp.route('/<int:id>')
@login_required
def detail(id):
    bien = BienImmobilier.query.get_or_404(id)
    return render_template('biens/detail.html', bien=bien)
""",
            "clients.py": """from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Client
from app.routes.forms import ClientForm

bp = Blueprint('clients', __name__)

@bp.route('/')
@login_required
def index():
    clients = Client.query.all()
    return render_template('clients/index.html', clients=clients)

@bp.route('/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter():
    form = ClientForm()
    if form.validate_on_submit():
        client = Client(
            nom=form.nom.data,
            prenom=form.prenom.data,
            email=form.email.data,
            telephone=form.telephone.data,
            type_client=form.type_client.data
        )
        db.session.add(client)
        db.session.commit()
        flash('Client ajouté avec succès!', 'success')
        return redirect(url_for('clients.index'))
    return render_template('clients/ajouter.html', form=form)
""",
            "forms.py": """from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class BienForm(FlaskForm):
    type_bien = SelectField('Type de bien', choices=[
        ('appartement', 'Appartement'),
        ('maison', 'Maison'),
        ('terrain', 'Terrain'),
        ('local', 'Local commercial')
    ], validators=[DataRequired()])
    adresse = StringField('Adresse', validators=[DataRequired(), Length(max=200)])
    ville = StringField('Ville', validators=[DataRequired(), Length(max=100)])
    code_postal = StringField('Code postal', validators=[DataRequired(), Length(max=20)])
    surface = FloatField('Surface (m²)', validators=[DataRequired()])
    prix = FloatField('Prix (€)', validators=[DataRequired()])
    description = TextAreaField('Description')
    proprietaire_id = SelectField('Propriétaire', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Enregistrer')

class ClientForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired(), Length(max=100)])
    prenom = StringField('Prénom', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    telephone = StringField('Téléphone', validators=[Length(max=20)])
    type_client = SelectField('Type de client', choices=[
        ('proprietaire', 'Propriétaire'),
        ('locataire', 'Locataire'),
        ('acheteur', 'Acheteur')
    ], validators=[DataRequired()])
    submit = SubmitField('Enregistrer')
"""
        },
        "templates": {
            "base.html": """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Gestion Immobilière{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    {% include 'partials/navbar.html' %}
    
    <div class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </div>

    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>
</body>
</html>
""",
            "partials": {
                "navbar.html": """<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container">
        <a class="navbar-brand" href="{{ url_for('biens.index') }}">Gestion Immobilière</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav me-auto">
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('biens.index') }}">Biens</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('clients.index') }}">Clients</a>
                </li>
            </ul>
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link" href="#">Déconnexion</a>
                </li>
            </ul>
        </div>
    </div>
</nav>
"""
            },
            "biens": {
                "index.html": """{% extends "base.html" %}

{% block title %}Liste des biens immobiliers{% endblock %}

{% block content %}
<h1>Liste des biens immobiliers</h1>
<a href="{{ url_for('biens.ajouter') }}" class="btn btn-primary mb-3">Ajouter un bien</a>

<div class="table-responsive">
    <table class="table table-striped">
        <thead>
            <tr>
                <th>ID</th>
                <th>Type</th>
                <th>Adresse</th>
                <th>Ville</th>
                <th>Prix</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for bien in biens %}
            <tr>
                <td>{{ bien.id }}</td>
                <td>{{ bien.type_bien }}</td>
                <td>{{ bien.adresse }}</td>
                <td>{{ bien.ville }}</td>
                <td>{{ bien.prix }} €</td>
                <td>
                    <a href="{{ url_for('biens.detail', id=bien.id) }}" class="btn btn-sm btn-info">Voir</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
""",
                "ajouter.html": """{% extends "base.html" %}

{% block title %}Ajouter un bien immobilier{% endblock %}

{% block content %}
<h1>Ajouter un bien immobilier</h1>

<form method="POST">
    {{ form.hidden_tag() }}
    
    <div class="mb-3">
        {{ form.type_bien.label(class="form-label") }}
        {{ form.type_bien(class="form-select") }}
    </div>
    
    <div class="mb-3">
        {{ form.adresse.label(class="form-label") }}
        {{ form.adresse(class="form-control") }}
    </div>
    
    <div class="row mb-3">
        <div class="col">
            {{ form.ville.label(class="form-label") }}
            {{ form.ville(class="form-control") }}
        </div>
        <div class="col">
            {{ form.code_postal.label(class="form-label") }}
            {{ form.code_postal(class="form-control") }}
        </div>
    </div>
    
    <div class="row mb-3">
        <div class="col">
            {{ form.surface.label(class="form-label") }}
            {{ form.surface(class="form-control") }}
        </div>
        <div class="col">
            {{ form.prix.label(class="form-label") }}
            {{ form.prix(class="form-control") }}
        </div>
    </div>
    
    <div class="mb-3">
        {{ form.description.label(class="form-label") }}
        {{ form.description(class="form-control", rows=3) }}
    </div>
    
    <div class="mb-3">
        {{ form.proprietaire_id.label(class="form-label") }}
        {{ form.proprietaire_id(class="form-select") }}
    </div>
    
    <button type="submit" class="btn btn-primary">Enregistrer</button>
</form>
{% endblock %}
""",
                "detail.html": """{% extends "base.html" %}

{% block title %}Détails du bien #{{ bien.id }}{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8">
        <h1>Bien #{{ bien.id }}</h1>
        <p><strong>Type:</strong> {{ bien.type_bien }}</p>
        <p><strong>Adresse:</strong> {{ bien.adresse }}, {{ bien.code_postal }} {{ bien.ville }}</p>
        <p><strong>Surface:</strong> {{ bien.surface }} m²</p>
        <p><strong>Prix:</strong> {{ bien.prix }} €</p>
        <p><strong>Description:</strong><br>{{ bien.description }}</p>
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title">Propriétaire</h5>
            </div>
            <div class="card-body">
                <p class="card-text">
                    {{ bien.proprietaire.prenom }} {{ bien.proprietaire.nom }}<br>
                    {{ bien.proprietaire.email }}<br>
                    {{ bien.proprietaire.telephone }}
                </p>
            </div>
        </div>
    </div>
</div>

<a href="{{ url_for('biens.index') }}" class="btn btn-secondary mt-3">Retour à la liste</a>
{% endblock %}
"""
            },
            "clients": {
                "index.html": """{% extends "base.html" %}

{% block title %}Liste des clients{% endblock %}

{% block content %}
<h1>Liste des clients</h1>
<a href="{{ url_for('clients.ajouter') }}" class="btn btn-primary mb-3">Ajouter un client</a>

<div class="table-responsive">
    <table class="table table-striped">
        <thead>
            <tr>
                <th>ID</th>
                <th>Nom</th>
                <th>Email</th>
                <th>Téléphone</th>
                <th>Type</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for client in clients %}
            <tr>
                <td>{{ client.id }}</td>
                <td>{{ client.prenom }} {{ client.nom }}</td>
                <td>{{ client.email }}</td>
                <td>{{ client.telephone }}</td>
                <td>{{ client.type_client }}</td>
                <td>
                    <a href="#" class="btn btn-sm btn-info">Voir</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
""",
                "ajouter.html": """{% extends "base.html" %}

{% block title %}Ajouter un client{% endblock %}

{% block content %}
<h1>Ajouter un client</h1>

<form method="POST">
    {{ form.hidden_tag() }}
    
    <div class="row mb-3">
        <div class="col">
            {{ form.prenom.label(class="form-label") }}
            {{ form.prenom(class="form-control") }}
        </div>
        <div class="col">
            {{ form.nom.label(class="form-label") }}
            {{ form.nom(class="form-control") }}
        </div>
    </div>
    
    <div class="mb-3">
        {{ form.email.label(class="form-label") }}
        {{ form.email(class="form-control") }}
    </div>
    
    <div class="mb-3">
        {{ form.telephone.label(class="form-label") }}
        {{ form.telephone(class="form-control") }}
    </div>
    
    <div class="mb-3">
        {{ form.type_client.label(class="form-label") }}
        {{ form.type_client(class="form-select") }}
    </div>
    
    <button type="submit" class="btn btn-primary">Enregistrer</button>
</form>
{% endblock %}
"""
            }
        },
        "static": {
            "css": {
                "style.css": """body {
    padding-top: 20px;
    padding-bottom: 20px;
}

.alert {
    margin-top: 20px;
}

.table {
    margin-top: 20px;
}

.form-group {
    margin-bottom: 15px;
}
"""
            },
            "js": {
                "script.js": """// JavaScript personnalisé pour l'application
console.log('Application de gestion immobilière chargée');

document.addEventListener('DOMContentLoaded', function() {
    // Initialisation des composants ici
});
"""
            },
            "uploads": {
                ".gitkeep": ""
            }
        }
    },
    "migrations": {
        "README": "Ce dossier contient les migrations de base de données générées par Flask-Migrate"
    },
    "instance": {
        ".gitkeep": ""
    },
    "venv": {
        ".gitkeep": ""
    },
    ".env": """# Configuration d'environnement
SECRET_KEY=votre_cle_secrete_ici
DATABASE_URL=postgresql://username:password@localhost/immobilier_db
FLASK_APP=run.py
FLASK_ENV=development
""",
    "requirements.txt": """Flask==2.0.1
Flask-SQLAlchemy==2.5.1
Flask-Migrate==3.1.0
psycopg2-binary==2.9.1
python-dotenv==0.19.0
WTForms==3.0.1
Flask-Login==0.5.0
Flask-WTF==1.0.0
""",
    "run.py": """from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
"""
}

def create_project_structure(base_path, structure):
    for name, content in structure.items():
        path = base_path / name
        
        if isinstance(content, dict):
            # C'est un dossier
            path.mkdir(exist_ok=True)
            create_project_structure(path, content)
        else:
            # C'est un fichier
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Créé: {path}")

def main():
    project_path = Path(PROJECT_NAME)
    
    if project_path.exists():
        print(f"Le dossier {PROJECT_NAME} existe déjà. Veuillez le supprimer ou choisir un autre nom.")
        return
    
    print(f"Création de la structure du projet {PROJECT_NAME}...")
    project_path.mkdir()
    
    create_project_structure(project_path, STRUCTURE)
    
    print("\nStructure créée avec succès!")
    print("Prochaines étapes:")
    print("1. Créez un environnement virtuel: python -m venv venv")
    print("2. Activez l'environnement: venv\\Scripts\\activate")
    print("3. Installez les dépendances: pip install -r requirements.txt")
    print("4. Configurez votre base de données PostgreSQL et mettez à jour .env")
    print("5. Initialisez la base de données: flask db init && flask db migrate && flask db upgrade")
    print("6. Lancez l'application: python run.py")

if __name__ == "__main__":
    main()