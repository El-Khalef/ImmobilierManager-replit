from app import app  # noqa: F401
from models import formater_montant

# Rendre la fonction disponible dans tous les templates
app.jinja_env.globals.update(formater_montant=formater_montant)
