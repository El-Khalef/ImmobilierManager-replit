import os
import uuid
from datetime import datetime, date
from flask import render_template, request, redirect, url_for, flash, jsonify, current_app, send_file, make_response
from werkzeug.utils import secure_filename
from sqlalchemy import or_, and_
from app import db
from models import (
    Client, BienImmobilier, PhotoBien, ContratLocation, 
    PaiementLoyer, DocumentContrat, get_dashboard_stats
)
from forms import (
    ClientForm, BienForm, PhotoForm, ContratForm, 
    PaiementForm, SearchForm, DocumentContratForm
)
from quittances import generer_quittance_pdf, generer_nom_fichier_quittance
from quittances_bilingue import generer_quittance_bilingue_pdf, generer_nom_fichier_quittance_bilingue


def register_routes(app):
    """Enregistre toutes les routes de l'application"""
    
    @app.route('/')
    def index():
        """Page d'accueil avec dashboard"""
        stats = get_dashboard_stats()
        recent_contrats = ContratLocation.query.filter_by(statut='actif').limit(5).all()
        paiements_en_retard = PaiementLoyer.query.filter(
            PaiementLoyer.statut != 'paye',
            PaiementLoyer.date_echeance < date.today()
        ).limit(5).all()
        
        return render_template('dashboard.html', 
                             stats=stats, 
                             recent_contrats=recent_contrats,
                             paiements_en_retard=paiements_en_retard)
    
    # Routes pour les clients
    @app.route('/clients/')
    def clients_index():
        """Liste des clients"""
        page = request.args.get('page', 1, type=int)
        type_filter = request.args.get('type', '')
        search = request.args.get('search', '')
        
        query = Client.query
        
        if type_filter:
            query = query.filter_by(type_client=type_filter)
        
        if search:
            query = query.filter(
                or_(
                    Client.nom.ilike(f'%{search}%'),
                    Client.prenom.ilike(f'%{search}%'),
                    Client.email.ilike(f'%{search}%')
                )
            )
        
        clients = query.order_by(Client.nom, Client.prenom).paginate(
            page=page, per_page=20, error_out=False
        )
        
        return render_template('clients/index.html', 
                             clients=clients, 
                             type_filter=type_filter,
                             search=search)
    
    @app.route('/clients/<int:id>')
    def clients_detail(id):
        """Détail d'un client"""
        client = Client.query.get_or_404(id)
        return render_template('clients/detail.html', client=client)
    
    @app.route('/clients/add', methods=['GET', 'POST'])
    def clients_add():
        """Ajouter un client"""
        form = ClientForm()
        if form.validate_on_submit():
            # Vérifier que l'email n'existe pas déjà
            existing_client = Client.query.filter_by(email=form.email.data).first()
            if existing_client:
                flash('Un client avec cet email existe déjà.', 'danger')
                return render_template('clients/form.html', form=form, title='Ajouter un client')
            
            client = Client(
                nom=form.nom.data,
                prenom=form.prenom.data,
                email=form.email.data,
                telephone=form.telephone.data,
                adresse=form.adresse.data,
                ville=form.ville.data,
                code_postal=form.code_postal.data,
                type_client=form.type_client.data,
                type_piece_identite=form.type_piece_identite.data,
                numero_piece_identite=form.numero_piece_identite.data
            )
            db.session.add(client)
            db.session.commit()
            flash(f'Client {client.nom_complet} ajouté avec succès.', 'success')
            return redirect(url_for('clients_index'))
        
        return render_template('clients/form.html', form=form, title='Ajouter un client')
    
    @app.route('/clients/<int:id>/edit', methods=['GET', 'POST'])
    def clients_edit(id):
        """Éditer un client"""
        client = Client.query.get_or_404(id)
        form = ClientForm(obj=client)
        
        if form.validate_on_submit():
            # Vérifier que l'email n'existe pas déjà (sauf pour ce client)
            existing_client = Client.query.filter(
                and_(Client.email == form.email.data, Client.id != id)
            ).first()
            if existing_client:
                flash('Un autre client avec cet email existe déjà.', 'danger')
                return render_template('clients/form.html', form=form, client=client, title='Modifier le client')
            
            form.populate_obj(client)
            db.session.commit()
            flash(f'Client {client.nom_complet} modifié avec succès.', 'success')
            return redirect(url_for('clients_detail', id=client.id))
        
        return render_template('clients/form.html', form=form, client=client, title='Modifier le client')
    
    @app.route('/clients/<int:id>/delete', methods=['POST'])
    def clients_delete(id):
        """Supprimer un client"""
        client = Client.query.get_or_404(id)
        
        # Vérifier qu'il n'y a pas de contraintes
        if client.biens_proprietaire or client.contrats_locataire:
            flash('Impossible de supprimer ce client car il a des biens ou contrats associés.', 'danger')
            return redirect(url_for('clients_detail', id=id))
        
        nom_complet = client.nom_complet
        db.session.delete(client)
        db.session.commit()
        flash(f'Client {nom_complet} supprimé avec succès.', 'success')
        return redirect(url_for('clients_index'))
    
    # Routes pour les biens immobiliers
    @app.route('/biens/')
    def biens_index():
        """Liste des biens immobiliers"""
        page = request.args.get('page', 1, type=int)
        form = SearchForm(request.args)
        
        query = BienImmobilier.query
        
        # Appliquer les filtres de recherche
        if form.q.data:
            search_term = f'%{form.q.data}%'
            query = query.filter(
                or_(
                    BienImmobilier.titre.ilike(search_term),
                    BienImmobilier.adresse.ilike(search_term),
                    BienImmobilier.ville.ilike(search_term),
                    BienImmobilier.description.ilike(search_term)
                )
            )
        
        if form.type_bien.data:
            query = query.filter_by(type_bien=form.type_bien.data)
        
        if form.ville.data:
            query = query.filter(BienImmobilier.ville.ilike(f'%{form.ville.data}%'))
        
        if form.prix_min.data:
            query = query.filter(BienImmobilier.prix_location_mensuel >= form.prix_min.data)
        
        if form.prix_max.data:
            query = query.filter(BienImmobilier.prix_location_mensuel <= form.prix_max.data)
        
        if form.surface_min.data:
            query = query.filter(BienImmobilier.surface >= form.surface_min.data)
        
        if form.surface_max.data:
            query = query.filter(BienImmobilier.surface <= form.surface_max.data)
        
        if form.disponible_uniquement.data:
            query = query.filter_by(disponible=True)
        
        biens = query.order_by(BienImmobilier.date_creation.desc()).paginate(
            page=page, per_page=20, error_out=False
        )
        
        return render_template('biens/index.html', biens=biens, form=form)
    
    @app.route('/biens/<int:id>')
    def biens_detail(id):
        """Détail d'un bien immobilier"""
        bien = BienImmobilier.query.get_or_404(id)
        return render_template('biens/detail.html', bien=bien)
    
    @app.route('/biens/add', methods=['GET', 'POST'])
    def biens_add():
        """Ajouter un bien immobilier"""
        form = BienForm()
        if form.validate_on_submit():
            bien = BienImmobilier(
                titre=form.titre.data,
                type_bien=form.type_bien.data,
                adresse=form.adresse.data,
                ville=form.ville.data,
                code_postal=form.code_postal.data,
                surface=form.surface.data,
                nombre_pieces=form.nombre_pieces.data,
                nombre_chambres=form.nombre_chambres.data,
                prix_achat=form.prix_achat.data,
                prix_location_mensuel=form.prix_location_mensuel.data,
                charges_mensuelles=form.charges_mensuelles.data,
                description=form.description.data,
                meuble=form.meuble.data,
                balcon=form.balcon.data,
                parking=form.parking.data,
                ascenseur=form.ascenseur.data,
                etage=form.etage.data,
                annee_construction=form.annee_construction.data,
                proprietaire_id=form.proprietaire_id.data
            )
            db.session.add(bien)
            db.session.commit()
            flash(f'Bien "{bien.titre}" ajouté avec succès.', 'success')
            return redirect(url_for('biens_detail', id=bien.id))
        
        return render_template('biens/form.html', form=form, title='Ajouter un bien')
    
    @app.route('/biens/<int:id>/edit', methods=['GET', 'POST'])
    def biens_edit(id):
        """Éditer un bien immobilier"""
        bien = BienImmobilier.query.get_or_404(id)
        form = BienForm(obj=bien)
        
        if form.validate_on_submit():
            form.populate_obj(bien)
            db.session.commit()
            flash(f'Bien "{bien.titre}" modifié avec succès.', 'success')
            return redirect(url_for('biens_detail', id=bien.id))
        
        return render_template('biens/form.html', form=form, bien=bien, title='Modifier le bien')
    
    @app.route('/biens/<int:id>/photos', methods=['GET', 'POST'])
    def biens_photos(id):
        """Gérer les photos d'un bien"""
        bien = BienImmobilier.query.get_or_404(id)
        form = PhotoForm()
        
        if form.validate_on_submit():
            file = form.photo.data
            if file:
                # Générer un nom de fichier unique
                filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Si c'est défini comme photo principale, désactiver les autres
                if form.principale.data:
                    PhotoBien.query.filter_by(bien_id=bien.id, principale=True).update({'principale': False})
                
                photo = PhotoBien(
                    nom_fichier=filename,
                    nom_original=file.filename,
                    principale=form.principale.data,
                    bien_id=bien.id
                )
                db.session.add(photo)
                db.session.commit()
                flash('Photo ajoutée avec succès.', 'success')
                return redirect(url_for('biens_photos', id=id))
        
        return render_template('biens/detail.html', bien=bien, photo_form=form)
    
    @app.route('/biens/<int:bien_id>/photos/<int:photo_id>/delete', methods=['POST'])
    def photo_delete(bien_id, photo_id):
        """Supprimer une photo"""
        photo = PhotoBien.query.get_or_404(photo_id)
        if photo.bien_id != bien_id:
            flash('Photo non trouvée.', 'danger')
            return redirect(url_for('biens_detail', id=bien_id))
        
        # Supprimer le fichier physique
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], photo.nom_fichier)
        if os.path.exists(filepath):
            os.remove(filepath)
        
        db.session.delete(photo)
        db.session.commit()
        flash('Photo supprimée avec succès.', 'success')
        return redirect(url_for('biens_detail', id=bien_id))
    
    # Routes pour les contrats
    @app.route('/contrats/')
    def contrats_index():
        """Liste des contrats de location"""
        page = request.args.get('page', 1, type=int)
        statut_filter = request.args.get('statut', '')
        
        query = ContratLocation.query
        
        if statut_filter:
            query = query.filter_by(statut=statut_filter)
        
        contrats = query.order_by(ContratLocation.date_creation.desc()).paginate(
            page=page, per_page=20, error_out=False
        )
        
        return render_template('contrats/index.html', contrats=contrats, statut_filter=statut_filter)
    
    @app.route('/contrats/<int:id>')
    def contrats_detail(id):
        """Détail d'un contrat de location"""
        contrat = ContratLocation.query.get_or_404(id)
        return render_template('contrats/detail.html', contrat=contrat)
    
    @app.route('/contrats/add', methods=['GET', 'POST'])
    def contrats_add():
        """Ajouter un contrat de location"""
        form = ContratForm()
        if form.validate_on_submit():
            # Marquer le bien comme non disponible
            bien = BienImmobilier.query.get(form.bien_id.data)
            bien.disponible = False
            
            contrat = ContratLocation(
                bien_id=form.bien_id.data,
                locataire_id=form.locataire_id.data,
                date_debut=form.date_debut.data,
                date_fin=form.date_fin.data,
                loyer_mensuel=form.loyer_mensuel.data,
                charges_mensuelles=form.charges_mensuelles.data,
                depot_garantie=form.depot_garantie.data,
                frais_agence=form.frais_agence.data,
                statut=form.statut.data,
                conditions_particulieres=form.conditions_particulieres.data
            )
            db.session.add(contrat)
            db.session.commit()
            flash('Contrat de location créé avec succès.', 'success')
            return redirect(url_for('contrats_detail', id=contrat.id))
        
        return render_template('contrats/form.html', form=form, title='Nouveau contrat')
    
    @app.route('/contrats/<int:id>/edit', methods=['GET', 'POST'])
    def contrats_edit(id):
        """Éditer un contrat de location"""
        contrat = ContratLocation.query.get_or_404(id)
        form = ContratForm(obj=contrat)
        
        if form.validate_on_submit():
            # Gérer la disponibilité du bien
            if contrat.statut == 'actif' and form.statut.data != 'actif':
                contrat.bien.disponible = True
            elif contrat.statut != 'actif' and form.statut.data == 'actif':
                contrat.bien.disponible = False
            
            form.populate_obj(contrat)
            db.session.commit()
            flash('Contrat modifié avec succès.', 'success')
            return redirect(url_for('contrats_detail', id=contrat.id))
        
        return render_template('contrats/form.html', form=form, contrat=contrat, title='Modifier le contrat')
    
    # Routes pour les paiements
    @app.route('/paiements/')
    def paiements_index():
        """Liste des paiements de loyer"""
        page = request.args.get('page', 1, type=int)
        statut_filter = request.args.get('statut', '')
        mois_filter = request.args.get('mois', '', type=str)
        annee_filter = request.args.get('annee', '', type=str)
        
        query = PaiementLoyer.query
        
        if statut_filter:
            query = query.filter_by(statut=statut_filter)
        
        if mois_filter:
            query = query.filter_by(mois=int(mois_filter))
        
        if annee_filter:
            query = query.filter_by(annee=int(annee_filter))
        
        paiements = query.order_by(
            PaiementLoyer.annee.desc(), 
            PaiementLoyer.mois.desc()
        ).paginate(page=page, per_page=20, error_out=False)
        
        return render_template('paiements/index.html', 
                             paiements=paiements,
                             statut_filter=statut_filter,
                             mois_filter=mois_filter,
                             annee_filter=annee_filter)
    
    @app.route('/paiements/add', methods=['GET', 'POST'])
    def paiements_add():
        """Ajouter un paiement de loyer"""
        contrat_id = request.args.get('contrat_id', type=int)
        form = PaiementForm()
        
        if contrat_id:
            form.contrat_id.data = contrat_id
            contrat = ContratLocation.query.get(contrat_id)
            if contrat:
                form.montant_loyer.data = contrat.loyer_mensuel
                form.montant_charges.data = contrat.charges_mensuelles
        
        # Validation personnalisée pour les champs dynamiques
        if request.method == 'POST':
            client_id = form.client_id.data
            bien_id = form.bien_id.data
            
            if client_id and bien_id:
                # Vérifier qu'il existe un contrat actif entre ce client et ce bien
                contrat = ContratLocation.query.filter_by(
                    locataire_id=client_id,
                    bien_id=bien_id,
                    statut='actif'
                ).first()
                
                if contrat:
                    form.contrat_id.data = contrat.id
                    # Mettre à jour les choix valides pour éviter l'erreur "Not a valid choice"
                    form.bien_id.choices = [(bien_id, "Bien sélectionné")]
                    form.client_id.choices = [(client_id, "Client sélectionné")]
                else:
                    flash('Aucun contrat actif trouvé pour ce client et ce bien.', 'danger')
                    return render_template('paiements/form.html', form=form, title='Ajouter un paiement')
        
        if form.validate_on_submit():
            # Vérifier qu'il n'y a pas déjà un paiement pour cette période
            existing = PaiementLoyer.query.filter_by(
                contrat_id=form.contrat_id.data,
                mois=form.mois.data,
                annee=form.annee.data
            ).first()
            
            if existing:
                flash('Un paiement existe déjà pour cette période.', 'danger')
                return render_template('paiements/form.html', form=form, title='Nouveau paiement')
            
            paiement = PaiementLoyer(
                contrat_id=form.contrat_id.data,
                mois=form.mois.data,
                annee=form.annee.data,
                montant_loyer=form.montant_loyer.data,
                montant_charges=form.montant_charges.data,
                date_paiement=form.date_paiement.data,
                date_echeance=form.date_echeance.data,
                statut=form.statut.data,
                mode_paiement=form.mode_paiement.data,
                reference_paiement=form.reference_paiement.data,
                remarques=form.remarques.data
            )
            db.session.add(paiement)
            db.session.commit()
            flash('Paiement enregistré avec succès.', 'success')
            return redirect(url_for('paiements_index'))
        
        return render_template('paiements/form.html', form=form, title='Nouveau paiement')
    
    @app.route('/paiements/<int:id>/edit', methods=['GET', 'POST'])
    def paiements_edit(id):
        """Éditer un paiement de loyer"""
        paiement = PaiementLoyer.query.get_or_404(id)
        form = PaiementForm(obj=paiement)
        
        # Initialiser les choix pour éviter l'erreur "Not a valid choice"
        contrat = paiement.contrat
        form.client_id.data = contrat.locataire_id
        form.bien_id.data = contrat.bien_id
        form.contrat_id.data = contrat.id
        
        # Définir les choix valides
        form.client_id.choices = [(contrat.locataire_id, f"{contrat.locataire.prenom} {contrat.locataire.nom}")]
        form.bien_id.choices = [(contrat.bien_id, contrat.bien.titre)]
        
        # Validation personnalisée pour les champs dynamiques
        if request.method == 'POST':
            client_id = form.client_id.data
            bien_id = form.bien_id.data
            
            if client_id and bien_id:
                # Vérifier qu'il existe un contrat actif entre ce client et ce bien
                contrat_check = ContratLocation.query.filter_by(
                    locataire_id=client_id,
                    bien_id=bien_id,
                    statut='actif'
                ).first()
                
                if contrat_check:
                    form.contrat_id.data = contrat_check.id
                    # Mettre à jour les choix valides pour éviter l'erreur "Not a valid choice"
                    form.bien_id.choices = [(bien_id, "Bien sélectionné")]
                    form.client_id.choices = [(client_id, "Client sélectionné")]
                else:
                    flash('Aucun contrat actif trouvé pour ce client et ce bien.', 'danger')
                    return render_template('paiements/form.html', form=form, paiement=paiement, title='Modifier le paiement')
        
        if form.validate_on_submit():
            form.populate_obj(paiement)
            db.session.commit()
            flash('Paiement modifié avec succès.', 'success')
            return redirect(url_for('paiements_index'))
        
        return render_template('paiements/form.html', form=form, paiement=paiement, title='Modifier le paiement')
    
    # === ROUTES POUR LES DOCUMENTS ===
    
    @app.route('/documents/')
    def documents_index():
        """Liste des documents"""
        documents = DocumentContrat.query.order_by(DocumentContrat.date_ajout.desc()).all()
        return render_template('documents/index.html', documents=documents)
    
    @app.route('/documents/add', methods=['GET', 'POST'])
    def documents_add():
        """Ajouter un document"""
        form = DocumentContratForm()
        if form.validate_on_submit():
            fichier = form.fichier.data
            
            # Sécuriser le nom du fichier
            nom_original = secure_filename(fichier.filename)
            extension = nom_original.rsplit('.', 1)[1].lower() if '.' in nom_original else ''
            nom_unique = f"{uuid.uuid4().hex}.{extension}"
            
            # Définir le chemin de stockage
            dossier_documents = os.path.join(current_app.static_folder, 'documents')
            os.makedirs(dossier_documents, exist_ok=True)
            chemin_fichier = os.path.join(dossier_documents, nom_unique)
            
            try:
                # Sauvegarder le fichier
                fichier.save(chemin_fichier)
                
                # Obtenir la taille du fichier
                taille_fichier = os.path.getsize(chemin_fichier)
                
                # Créer l'enregistrement en base
                document = DocumentContrat(
                    contrat_id=form.contrat_id.data,
                    nom_fichier=nom_unique,
                    nom_original=nom_original,
                    type_document=form.type_document.data,
                    format_fichier=extension,
                    taille_fichier=taille_fichier,
                    chemin_stockage=f"static/documents/{nom_unique}",
                    description=form.description.data,
                    ajoute_par="Admin"  # À adapter selon votre système d'authentification
                )
                
                db.session.add(document)
                db.session.commit()
                
                flash(f'Document {nom_original} ajouté avec succès.', 'success')
                return redirect(url_for('documents_index'))
                
            except Exception as e:
                flash(f'Erreur lors de l\'upload du fichier: {str(e)}', 'danger')
                # Supprimer le fichier si l'enregistrement en base a échoué
                if os.path.exists(chemin_fichier):
                    os.remove(chemin_fichier)
        
        return render_template('documents/form.html', form=form, title='Ajouter un document')
    
    @app.route('/documents/<int:id>/delete', methods=['POST'])
    def documents_delete(id):
        """Supprimer un document"""
        document = DocumentContrat.query.get_or_404(id)
        
        try:
            # Supprimer le fichier physique
            if os.path.exists(document.chemin_stockage):
                os.remove(document.chemin_stockage)
            
            # Supprimer l'enregistrement en base
            db.session.delete(document)
            db.session.commit()
            
            flash('Document supprimé avec succès.', 'success')
        except Exception as e:
            flash(f'Erreur lors de la suppression: {str(e)}', 'danger')
        
        return redirect(url_for('documents_index'))
    
    @app.route('/contrats/<int:id>/documents')
    def contrats_documents(id):
        """Voir les documents d'un contrat"""
        contrat = ContratLocation.query.get_or_404(id)
        documents = DocumentContrat.query.filter_by(contrat_id=id).order_by(DocumentContrat.date_ajout.desc()).all()
        return render_template('contrats/documents.html', contrat=contrat, documents=documents)
    
    # === API ROUTES ===
    
    @app.route('/api/clients/<int:client_id>/biens')
    def api_client_biens(client_id):
        """API pour récupérer les biens d'un client (pour les paiements)"""
        # Récupérer les contrats actifs du client
        contrats = ContratLocation.query.filter_by(
            locataire_id=client_id, 
            statut='actif'
        ).all()
        
        biens_data = []
        for contrat in contrats:
            bien = contrat.bien
            biens_data.append({
                'id': bien.id,
                'titre': bien.titre,
                'adresse': bien.adresse_complete,
                'contrat_id': contrat.id,
                'loyer_mensuel': float(contrat.loyer_mensuel),
                'charges_mensuelles': float(contrat.charges_mensuelles)
            })
        
        return jsonify(biens_data)
    
    # === ROUTES POUR LES QUITTANCES ===
    
    @app.route('/paiements/<int:id>/quittance')
    def generer_quittance(id):
        """Générer et télécharger la quittance pour un paiement"""
        paiement = PaiementLoyer.query.get_or_404(id)
        
        # Vérifier que le paiement est bien payé
        if paiement.statut != 'paye':
            flash('Une quittance ne peut être générée que pour un paiement effectué.', 'warning')
            return redirect(url_for('paiements_index'))
        
        try:
            # Générer le PDF
            pdf_buffer = generer_quittance_pdf(paiement)
            nom_fichier = generer_nom_fichier_quittance(paiement)
            
            # Créer la réponse avec le PDF
            response = make_response(pdf_buffer.getvalue())
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = f'attachment; filename="{nom_fichier}"'
            
            return response
            
        except Exception as e:
            flash(f'Erreur lors de la génération de la quittance: {str(e)}', 'danger')
            return redirect(url_for('paiements_index'))
    
    @app.route('/quittances/<int:id>/bilingue')
    def generer_quittance_bilingue(id):
        """Génère une quittance bilingue (français-arabe) en PDF"""
        paiement = PaiementLoyer.query.get_or_404(id)
        
        if paiement.statut != 'paye':
            flash('Cette quittance ne peut être générée que pour un paiement confirmé.', 'warning')
            return redirect(url_for('paiements_index'))
        
        try:
            # Générer le PDF bilingue
            pdf_buffer = generer_quittance_bilingue_pdf(paiement)
            nom_fichier = generer_nom_fichier_quittance_bilingue(paiement)
            
            # Créer la réponse avec le PDF
            response = make_response(pdf_buffer.getvalue())
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = f'attachment; filename="{nom_fichier}"'
            
            return response
            
        except Exception as e:
            flash(f'Erreur lors de la génération de la quittance bilingue: {str(e)}', 'danger')
            return redirect(url_for('paiements_index'))
    
    @app.route('/contrats/<int:id>/quittances')
    def contrats_quittances(id):
        """Liste des quittances disponibles pour un contrat"""
        contrat = ContratLocation.query.get_or_404(id)
        
        # Récupérer tous les paiements payés de ce contrat
        paiements_payes = PaiementLoyer.query.filter_by(
            contrat_id=id,
            statut='paye'
        ).order_by(PaiementLoyer.annee.desc(), PaiementLoyer.mois.desc()).all()
        
        return render_template('contrats/quittances.html', 
                             contrat=contrat, 
                             paiements=paiements_payes)
    
    @app.route('/quittances')
    def quittances_index():
        """Liste de toutes les quittances disponibles"""
        page = request.args.get('page', 1, type=int)
        client_filter = request.args.get('client', '')
        annee_filter = request.args.get('annee', '', type=str)
        
        # Construire la requête de base
        query = PaiementLoyer.query.filter_by(statut='paye')
        
        # Appliquer les filtres
        if client_filter:
            query = query.join(ContratLocation).join(Client).filter(
                or_(
                    Client.nom.ilike(f'%{client_filter}%'),
                    Client.prenom.ilike(f'%{client_filter}%')
                )
            )
        
        if annee_filter:
            try:
                annee = int(annee_filter)
                query = query.filter(PaiementLoyer.annee == annee)
            except ValueError:
                pass
        
        # Pagination
        paiements = query.order_by(
            PaiementLoyer.annee.desc(),
            PaiementLoyer.mois.desc()
        ).paginate(page=page, per_page=20, error_out=False)
        
        return render_template('quittances/index.html', 
                             paiements=paiements,
                             client_filter=client_filter,
                             annee_filter=annee_filter)
