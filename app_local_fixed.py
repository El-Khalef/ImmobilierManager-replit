import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

def formater_montant(montant):
    """Formate un montant en MRU avec séparateurs de milliers"""
    if montant is None:
        return "0"
    try:
        montant_float = float(montant)
        return f"{montant_float:,.0f}".replace(',', ' ')
    except (ValueError, TypeError):
        return "0"

def create_app():
    # create the app
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET") or "dev-secret-key-change-in-production"
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https

    # configure the database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or "postgresql://localhost/immobilier_db"
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size
    
    # Ensure upload directory exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    
    # Enable debug logging
    logging.basicConfig(level=logging.DEBUG)
    
    # initialize the app with the extension
    db.init_app(app)

    # CORRECTION POUR ENVIRONNEMENT LOCAL
    # Enregistrer la fonction formater_montant comme filtre global Jinja2
    app.jinja_env.globals['formater_montant'] = formater_montant
    
    # Enregistrer également comme filtre
    @app.template_filter('formater_montant')
    def formater_montant_filter(montant):
        return formater_montant(montant)

    with app.app_context():
        # Import models to ensure tables are created
        import models  # noqa: F401
        
        # Import and register routes
        from routes import register_routes
        register_routes(app)
        
        db.create_all()

    return app

# Create the app instance
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)