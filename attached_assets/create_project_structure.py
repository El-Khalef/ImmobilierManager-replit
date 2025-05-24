import os

# Définir la structure des dossiers et fichiers
structure = {
    "gestion_immobilier_web": {
        "app.py": "",
        "config.py": "",
        "requirements.txt": "Flask\nFlask-SQLAlchemy\nFlask-Migrate\npsycopg2",
        "templates": {
            "base.html": """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/static/css/styles.css">
    <title>{% block title %}Gestion Immobilière{% endblock %}</title>
</head>
<body>
    <header>
        <h1>Gestion Immobilière</h1>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer>
        <p>&copy; 2025 Gestion Immobilière</p>
    </footer>
</body>
</html>""",
            "index.html": """{% extends "base.html" %}

{% block title %}Accueil{% endblock %}

{% block content %}
<h2>Bienvenue dans l'application de gestion immobilière</h2>
<a href="/proprietaires/">Voir les propriétaires</a>
<a href="/biens/">Voir les biens</a>
{% endblock %}""",
            "formulaire.html": """{% extends "base.html" %}

{% block title %}Ajouter un Propriétaire{% endblock %}

{% block content %}
<h2>Ajouter un Propriétaire</h2>
<form method="POST" action="/proprietaires/add">
    <label for="nom">Nom :</label>
    <input type="text" id="nom" name="nom" required>
    
    <label for="prenom">Prénom :</label>
    <input type="text" id="prenom" name="prenom">
    
    <label for="email">Email :</label>
    <input type="email" id="email" name="email">
    
    <label for="telephone">Téléphone :</label>
    <input type="text" id="telephone" name="telephone">
    
    <button type="submit">Ajouter</button>
</form>
{% endblock %}""",
        },
        "static": {
            "css": {
                "styles.css": """body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    line-height: 1.6;
}
header {
    background: #333;
    color: #fff;
    padding: 1rem;
    text-align: center;
}
footer {
    background: #333;
    color: #fff;
    text-align: center;
    padding: 0.5rem;
    position: fixed;
    bottom: 0;
    width: 100%;
}"""
            },
            "js": {
                "scripts.js": "// Placeholder for JavaScript functionality"
            }
        },
        "models": {
            "__init__.py": "",
            "models.py": "# Placeholder for SQLAlchemy models"
        },
        "routes": {
            "__init__.py": "",
            "proprietaires.py": "# Placeholder for proprietaires routes",
            "biens.py": "# Placeholder for biens routes",
            "autres_routes.py": "# Placeholder for other routes"
        },
        "migrations": {}
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w", encoding="utf-8") as file:
                file.write(content)

if __name__ == "__main__":
    root = "gestion_immobilier_web"
    if not os.path.exists(root):
        os.makedirs(root)
    create_structure(root, structure)
    print(f"Structure de projet créée dans le dossier '{root}'")
