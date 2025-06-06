# Guide de Prévisualisation des Documents

## Fonctionnalités Ajoutées

### 1. Aperçu des Documents
- **Route**: `/documents/<id>/preview`
- **Fonctionnalité**: Affichage des documents directement dans le navigateur
- **Formats supportés**: 
  - PDF (aperçu intégré)
  - Images (JPG, PNG, GIF)
  - Vidéos (MP4, AVI, MOV)
  - Audio (MP3, WAV, OGG)
  - Documents Word (lien de téléchargement)

### 2. Modification des Documents
- **Route**: `/documents/<id>/edit`
- **Fonctionnalités**:
  - Modification des métadonnées (contrat, type, description)
  - Remplacement optionnel du fichier
  - Préservation du fichier existant si aucun nouveau fichier n'est fourni

### 3. Interface Améliorée
- **Boutons d'action** dans la liste des documents:
  - Aperçu (bleu)
  - Modifier (vert)
  - Télécharger (gris)
  - Supprimer (rouge)

## Structure des Templates

### templates/documents/preview.html
Template complet pour l'aperçu des documents avec:
- Informations détaillées du document
- Prévisualisation adaptée au type de fichier
- Actions rapides (modifier, télécharger, supprimer)
- Liens vers le contrat et le client associés

### templates/documents/edit.html
Formulaire d'édition avec:
- Champs modifiables (contrat, type, description)
- Upload optionnel d'un nouveau fichier
- Aperçu du fichier actuel
- Informations contextuelles

## Configuration Technique

### Upload des Fichiers
```python
# Configuration dans app.py
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max
```

### Sécurité
- Validation des types de fichiers autorisés
- Noms de fichiers sécurisés avec UUID
- Vérification de l'existence des fichiers
- Gestion des erreurs de téléchargement

### Types de Fichiers Supportés
- **Images**: jpg, jpeg, png, gif
- **Documents**: pdf, doc, docx
- **Vidéos**: mp4, avi, mov, webm
- **Audio**: mp3, wav, ogg, m4a

## Utilisation

### Pour Prévisualiser un Document
1. Aller dans la liste des documents
2. Cliquer sur le bouton "Aperçu" (icône œil bleue)
3. Le document s'affiche selon son type
4. Utiliser les actions rapides pour modifier ou télécharger

### Pour Modifier un Document
1. Depuis l'aperçu, cliquer sur "Modifier"
2. Ou directement depuis la liste avec le bouton "Modifier"
3. Modifier les champs souhaités
4. Optionnellement, remplacer le fichier
5. Enregistrer les modifications

### Navigation
- Breadcrumbs pour faciliter la navigation
- Liens directs vers le contrat et le client
- Retour rapide vers la liste des documents

## Avantages

1. **Gain de temps**: Plus besoin de télécharger pour consulter
2. **Facilité d'usage**: Interface intuitive et responsive
3. **Productivité**: Actions rapides directement depuis l'aperçu
4. **Sécurité**: Gestion appropriée des fichiers et permissions
5. **Flexibilité**: Support de multiples formats de fichiers

## Maintenance

### Ajout de Nouveaux Types de Fichiers
1. Ajouter l'extension dans `forms.py` (FileAllowed)
2. Ajouter la logique d'aperçu dans `preview.html`
3. Tester l'upload et l'affichage

### Dépannage
- Vérifier la configuration `UPLOAD_FOLDER`
- S'assurer que le dossier uploads existe et est accessible
- Contrôler les permissions de fichiers
- Vérifier la taille maximale des fichiers