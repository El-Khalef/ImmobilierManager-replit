# Guide d'importation de la base de données en local

## 1. Préparer PostgreSQL local

### Connexion à PostgreSQL
```bash
# Se connecter en tant qu'utilisateur postgres
sudo -u postgres psql
# Ou sur Windows depuis l'invite de commande PostgreSQL
psql -U postgres
```

### Créer la base de données
```sql
-- Créer une nouvelle base de données
CREATE DATABASE immobilier_mauritanie;

-- Créer un utilisateur dédié (optionnel)
CREATE USER immobilier_user WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE immobilier_mauritanie TO immobilier_user;

-- Quitter psql
\q
```

## 2. Importer les données

### Option A : Avec l'utilisateur postgres
```bash
psql -U postgres -d immobilier_mauritanie -f sauvegarde_complete_20250610_194449.sql
```

### Option B : Avec un utilisateur personnalisé
```bash
psql -U immobilier_user -d immobilier_mauritanie -h localhost -f sauvegarde_complete_20250610_194449.sql
```

## 3. Configurer l'application pour le localhost

### Modifier les variables d'environnement locales
Créez un fichier `.env` dans votre projet :
```
DATABASE_URL=postgresql://immobilier_user:votre_mot_de_passe@localhost:5432/immobilier_mauritanie
SESSION_SECRET=votre_cle_secrete_locale
```

### Ou modifiez directement dans app.py pour les tests :
```python
# Pour les tests en local uniquement
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://immobilier_user:votre_mot_de_passe@localhost:5432/immobilier_mauritanie"
```

## 4. Vérifier l'importation

```sql
-- Se connecter à la base
psql -U immobilier_user -d immobilier_mauritanie -h localhost

-- Vérifier les tables
\dt

-- Compter les enregistrements
SELECT 'clients' as table_name, COUNT(*) as count FROM clients
UNION ALL
SELECT 'biens_immobiliers', COUNT(*) FROM biens_immobiliers
UNION ALL
SELECT 'contrats_location', COUNT(*) FROM contrats_location
UNION ALL
SELECT 'paiements_loyer', COUNT(*) FROM paiements_loyer;
```

## 5. Résolution des problèmes courants

### Erreur de permission
```bash
# Donner les permissions sur le schéma public
sudo -u postgres psql -d immobilier_mauritanie -c "GRANT ALL ON SCHEMA public TO immobilier_user;"
sudo -u postgres psql -d immobilier_mauritanie -c "GRANT ALL ON ALL TABLES IN SCHEMA public TO immobilier_user;"
sudo -u postgres psql -d immobilier_mauritanie -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO immobilier_user;"
```

### Erreur d'encodage
```bash
# Forcer l'encodage UTF-8
psql -U postgres -d immobilier_mauritanie -f sauvegarde_complete_20250610_194449.sql --set client_encoding=UTF8
```

### Réinitialiser complètement
```sql
-- Supprimer et recréer la base
DROP DATABASE IF EXISTS immobilier_mauritanie;
CREATE DATABASE immobilier_mauritanie WITH ENCODING 'UTF8';
```