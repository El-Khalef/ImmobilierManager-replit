"""
Routes pour le module comptabilité
"""
from flask import render_template, request, redirect, url_for, flash, jsonify, make_response
from datetime import datetime, date
from sqlalchemy import extract, func, and_, or_
from app import db
from models import (BienImmobilier, Client, CompteComptable, EcritureComptable, 
                   DepenseImmobiliere, BudgetPrevisionnel, PaiementLoyer,
                   initialiser_plan_comptable, formater_montant)
from forms_comptabilite import (DepenseForm, EcritureComptableForm, BudgetForm, 
                               CompteComptableForm, RapportComptableForm)
import os
from werkzeug.utils import secure_filename


def register_comptabilite_routes(app):
    """Enregistre toutes les routes de comptabilité"""
    

    
    @app.route('/comptabilite')
    def comptabilite_dashboard():
        """Dashboard principal de la comptabilité"""
        # Statistiques générales
        mois_actuel = datetime.now().month
        annee_actuelle = datetime.now().year
        
        # Revenus du mois
        revenus_mois = db.session.query(func.sum(PaiementLoyer.montant_loyer + PaiementLoyer.montant_charges)).filter(
            PaiementLoyer.mois == mois_actuel,
            PaiementLoyer.annee == annee_actuelle,
            PaiementLoyer.statut == 'paye'
        ).scalar() or 0
        
        # Dépenses du mois
        depenses_mois = db.session.query(func.sum(DepenseImmobiliere.montant)).filter(
            extract('month', DepenseImmobiliere.date_depense) == mois_actuel,
            extract('year', DepenseImmobiliere.date_depense) == annee_actuelle,
            DepenseImmobiliere.statut_paiement == 'paye'
        ).scalar() or 0
        
        # Résultat du mois
        resultat_mois = revenus_mois - depenses_mois
        
        # Revenus de l'année
        revenus_annee = db.session.query(func.sum(PaiementLoyer.montant_loyer + PaiementLoyer.montant_charges)).filter(
            PaiementLoyer.annee == annee_actuelle,
            PaiementLoyer.statut == 'paye'
        ).scalar() or 0
        
        # Dépenses de l'année
        depenses_annee = db.session.query(func.sum(DepenseImmobiliere.montant)).filter(
            extract('year', DepenseImmobiliere.date_depense) == annee_actuelle,
            DepenseImmobiliere.statut_paiement == 'paye'
        ).scalar() or 0
        
        # Résultat de l'année
        resultat_annee = revenus_annee - depenses_annee
        
        # Dépenses en attente
        depenses_en_attente = DepenseImmobiliere.query.filter(
            DepenseImmobiliere.statut_paiement == 'en_attente'
        ).count()
        
        # Dernières écritures
        dernieres_ecritures = EcritureComptable.query.order_by(
            EcritureComptable.date_creation.desc()
        ).limit(10).all()
        
        # Répartition des dépenses par type
        depenses_par_type = db.session.query(
            DepenseImmobiliere.type_depense,
            func.sum(DepenseImmobiliere.montant).label('total')
        ).filter(
            extract('year', DepenseImmobiliere.date_depense) == annee_actuelle,
            DepenseImmobiliere.statut_paiement == 'paye'
        ).group_by(DepenseImmobiliere.type_depense).all()
        
        stats = {
            'revenus_mois': revenus_mois,
            'depenses_mois': depenses_mois,
            'resultat_mois': resultat_mois,
            'revenus_annee': revenus_annee,
            'depenses_annee': depenses_annee,
            'resultat_annee': resultat_annee,
            'depenses_en_attente': depenses_en_attente
        }
        
        return render_template('comptabilite/dashboard.html',
                             stats=stats,
                             dernieres_ecritures=dernieres_ecritures,
                             depenses_par_type=depenses_par_type,
                             formater_montant=formater_montant)
    
    @app.route('/comptabilite/depenses')
    def depenses_index():
        """Liste des dépenses"""
        page = request.args.get('page', 1, type=int)
        
        # Filtres
        bien_id = request.args.get('bien_id', type=int)
        type_depense = request.args.get('type_depense')
        statut = request.args.get('statut')
        
        query = DepenseImmobiliere.query
        
        if bien_id:
            query = query.filter(DepenseImmobiliere.bien_id == bien_id)
        if type_depense:
            query = query.filter(DepenseImmobiliere.type_depense == type_depense)
        if statut:
            query = query.filter(DepenseImmobiliere.statut_paiement == statut)
        
        depenses = query.order_by(DepenseImmobiliere.date_depense.desc()).paginate(
            page=page, per_page=20, error_out=False
        )
        
        # Pour les filtres
        biens = BienImmobilier.query.all()
        types_depenses = db.session.query(DepenseImmobiliere.type_depense.distinct()).all()
        
        return render_template('comptabilite/depenses/index.html',
                             depenses=depenses,
                             biens=biens,
                             types_depenses=[t[0] for t in types_depenses],
                             formater_montant=formater_montant)
    
    @app.route('/comptabilite/depenses/ajouter', methods=['GET', 'POST'])
    def depenses_add():
        """Ajouter une nouvelle dépense"""
        form = DepenseForm()
        
        if form.validate_on_submit():
            # Traitement du fichier justificatif
            justificatif_path = None
            if form.justificatif.data:
                fichier = form.justificatif.data
                nom_fichier = secure_filename(fichier.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                nom_fichier = f"{timestamp}_{nom_fichier}"
                
                upload_folder = 'static/documents/comptabilite'
                os.makedirs(upload_folder, exist_ok=True)
                justificatif_path = os.path.join(upload_folder, nom_fichier)
                fichier.save(justificatif_path)
            
            # Créer la dépense
            depense = DepenseImmobiliere()
            depense.bien_id = form.bien_id.data if form.bien_id.data != 0 else None
            depense.fournisseur_id = form.fournisseur_id.data if form.fournisseur_id.data != 0 else None
            depense.type_depense = form.type_depense.data
            depense.categorie = form.categorie.data
            depense.montant = form.montant.data
            depense.date_depense = form.date_depense.data
            depense.date_paiement = form.date_paiement.data
            depense.statut_paiement = form.statut_paiement.data
            depense.mode_paiement = form.mode_paiement.data
            depense.numero_facture = form.numero_facture.data
            depense.reference_paiement = form.reference_paiement.data
            depense.description = form.description.data
            depense.justificatif_path = justificatif_path
            depense.deductible_impots = form.deductible_impots.data
            depense.tva_applicable = form.tva_applicable.data
            depense.montant_tva = form.montant_tva.data or 0
            
            db.session.add(depense)
            
            # Si payé, créer l'écriture comptable automatiquement
            if form.statut_paiement.data == 'paye':
                creer_ecriture_depense(depense)
            
            db.session.commit()
            flash('Dépense enregistrée avec succès.', 'success')
            return redirect(url_for('depenses_index'))
        
        return render_template('comptabilite/depenses/form.html', form=form, titre="Ajouter une dépense")
    
    @app.route('/comptabilite/depenses/<int:id>')
    def depenses_detail(id):
        """Détail d'une dépense"""
        depense = DepenseImmobiliere.query.get_or_404(id)
        return render_template('comptabilite/depenses/detail.html', 
                             depense=depense, 
                             formater_montant=formater_montant)
    
    @app.route('/comptabilite/depenses/<int:id>/modifier', methods=['GET', 'POST'])
    def depenses_edit(id):
        """Modifier une dépense"""
        depense = DepenseImmobiliere.query.get_or_404(id)
        form = DepenseForm(obj=depense)
        
        if form.validate_on_submit():
            # Traitement du nouveau fichier justificatif
            if form.justificatif.data:
                # Supprimer l'ancien fichier
                if depense.justificatif_path and os.path.exists(depense.justificatif_path):
                    os.remove(depense.justificatif_path)
                
                # Sauvegarder le nouveau
                fichier = form.justificatif.data
                nom_fichier = secure_filename(fichier.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                nom_fichier = f"{timestamp}_{nom_fichier}"
                
                upload_folder = 'static/documents/comptabilite'
                os.makedirs(upload_folder, exist_ok=True)
                depense.justificatif_path = os.path.join(upload_folder, nom_fichier)
                fichier.save(depense.justificatif_path)
            
            # Mettre à jour les champs
            form.populate_obj(depense)
            
            # Gérer les valeurs nulles pour les SelectField
            if form.bien_id.data == 0:
                depense.bien_id = None
            if form.fournisseur_id.data == 0:
                depense.fournisseur_id = None
            
            db.session.commit()
            flash('Dépense modifiée avec succès.', 'success')
            return redirect(url_for('depenses_detail', id=id))
        
        return render_template('comptabilite/depenses/form.html', 
                             form=form, 
                             depense=depense,
                             titre="Modifier la dépense")
    
    @app.route('/comptabilite/ecritures')
    def ecritures_index():
        """Journal général - Liste des écritures comptables"""
        page = request.args.get('page', 1, type=int)
        
        # Filtres
        compte_id = request.args.get('compte_id', type=int)
        type_operation = request.args.get('type_operation')
        date_debut = request.args.get('date_debut')
        date_fin = request.args.get('date_fin')
        
        query = EcritureComptable.query
        
        if compte_id:
            query = query.filter(
                or_(EcritureComptable.compte_debit_id == compte_id,
                    EcritureComptable.compte_credit_id == compte_id)
            )
        if type_operation:
            query = query.filter(EcritureComptable.type_operation == type_operation)
        if date_debut:
            try:
                date_debut_obj = datetime.strptime(date_debut, '%Y-%m-%d').date()
                query = query.filter(EcritureComptable.date_operation >= date_debut_obj)
            except ValueError:
                pass
        if date_fin:
            try:
                date_fin_obj = datetime.strptime(date_fin, '%Y-%m-%d').date()
                query = query.filter(EcritureComptable.date_operation <= date_fin_obj)
            except ValueError:
                pass
        
        ecritures = query.order_by(EcritureComptable.date_operation.desc()).paginate(
            page=page, per_page=20, error_out=False
        )
        
        # Pour les filtres
        comptes = CompteComptable.query.filter_by(actif=True).order_by(CompteComptable.numero_compte).all()
        types_operations = db.session.query(EcritureComptable.type_operation.distinct()).all()
        
        return render_template('comptabilite/ecritures/index.html',
                             ecritures=ecritures,
                             comptes=comptes,
                             types_operations=[t[0] for t in types_operations if t[0]],
                             formater_montant=formater_montant)
    
    @app.route('/comptabilite/ecritures/ajouter', methods=['GET', 'POST'])
    def ecritures_add():
        """Ajouter une écriture comptable"""
        form = EcritureComptableForm()
        
        if form.validate_on_submit():
            ecriture = EcritureComptable()
            # Générer automatiquement le numéro de pièce si vide
            if form.numero_piece.data:
                ecriture.numero_piece = form.numero_piece.data
            else:
                ecriture.numero_piece = EcritureComptable.generer_numero_piece()
            ecriture.date_ecriture = form.date_ecriture.data
            ecriture.date_operation = form.date_operation.data
            ecriture.compte_debit_id = form.compte_debit_id.data
            ecriture.compte_credit_id = form.compte_credit_id.data
            ecriture.montant = form.montant.data
            ecriture.libelle = form.libelle.data
            ecriture.type_operation = form.type_operation.data
            ecriture.bien_id = form.bien_id.data if form.bien_id.data != 0 else None
            ecriture.client_id = form.client_id.data if form.client_id.data != 0 else None
            ecriture.reference_externe = form.reference_externe.data
            ecriture.validee = True
            ecriture.saisie_par = 'Admin'
            
            db.session.add(ecriture)
            db.session.commit()
            
            flash('Écriture comptable enregistrée avec succès.', 'success')
            return redirect(url_for('ecritures_index'))
        
        return render_template('comptabilite/ecritures/form.html', 
                             form=form, 
                             titre="Ajouter une écriture")
    
    @app.route('/comptabilite/ecritures/generer-numero')
    def generer_numero_piece():
        """API pour générer un numéro de pièce automatiquement"""
        numero = EcritureComptable.generer_numero_piece()
        return jsonify({'numero': numero})
    
    @app.route('/comptabilite/ecritures/<int:id>/modifier', methods=['GET', 'POST'])
    def ecritures_edit(id):
        """Modifier une écriture comptable"""
        ecriture = EcritureComptable.query.get_or_404(id)
        form = EcritureComptableForm(obj=ecriture)
        
        if form.validate_on_submit():
            # Générer automatiquement le numéro de pièce si vide
            if form.numero_piece.data:
                ecriture.numero_piece = form.numero_piece.data
            else:
                ecriture.numero_piece = EcritureComptable.generer_numero_piece()
                
            ecriture.date_ecriture = form.date_ecriture.data
            ecriture.date_operation = form.date_operation.data
            ecriture.compte_debit_id = form.compte_debit_id.data
            ecriture.compte_credit_id = form.compte_credit_id.data
            ecriture.montant = form.montant.data
            ecriture.libelle = form.libelle.data
            ecriture.type_operation = form.type_operation.data
            ecriture.reference_externe = form.reference_externe.data
            ecriture.bien_id = form.bien_id.data if form.bien_id.data != 0 else None
            ecriture.client_id = form.client_id.data if form.client_id.data != 0 else None
            
            try:
                db.session.commit()
                flash('Écriture comptable modifiée avec succès.', 'success')
                return redirect(url_for('ecritures_index'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erreur lors de la modification: {str(e)}', 'error')
        
        return render_template('comptabilite/ecritures/form.html', 
                             form=form, 
                             titre="Modifier l'écriture",
                             ecriture=ecriture)
    
    @app.route('/comptabilite/ecritures/<int:id>/supprimer', methods=['POST'])
    def ecritures_delete(id):
        """Supprimer une écriture comptable"""
        ecriture = EcritureComptable.query.get_or_404(id)
        
        try:
            db.session.delete(ecriture)
            db.session.commit()
            flash('Écriture comptable supprimée avec succès.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la suppression: {str(e)}', 'error')
        
        return jsonify({'success': True})
    
    @app.route('/comptabilite/comptes')
    def comptes_index():
        """Plan comptable"""
        comptes = CompteComptable.query.order_by(CompteComptable.numero_compte).all()
        
        # Calcul des soldes pour chaque compte
        for compte in comptes:
            compte.solde_debit_calc = compte.solde_debit
            compte.solde_credit_calc = compte.solde_credit
            compte.solde_net_calc = compte.solde_net
        
        return render_template('comptabilite/comptes/index.html',
                             comptes=comptes,
                             formater_montant=formater_montant)
    
    @app.route('/comptabilite/comptes/initialiser', methods=['POST'])
    def comptes_initialiser():
        """Initialiser le plan comptable de base"""
        if initialiser_plan_comptable():
            flash('Plan comptable initialisé avec succès.', 'success')
        else:
            flash('Erreur lors de l\'initialisation du plan comptable.', 'danger')
        
        return redirect(url_for('comptes_index'))
    
    @app.route('/comptabilite/comptes/ajouter', methods=['GET', 'POST'])
    def comptes_add():
        """Ajouter un nouveau compte comptable"""
        form = CompteComptableForm()
        
        if form.validate_on_submit():
            compte = CompteComptable()
            compte.numero_compte = form.numero_compte.data
            compte.nom_compte = form.nom_compte.data
            compte.type_compte = form.type_compte.data
            compte.actif = form.actif.data
            
            try:
                db.session.add(compte)
                db.session.commit()
                flash('Compte comptable ajouté avec succès.', 'success')
                return redirect(url_for('comptes_index'))
            except Exception as e:
                db.session.rollback()
                flash('Erreur lors de l\'ajout du compte comptable.', 'danger')
        
        return render_template('comptabilite/comptes/form.html',
                             form=form,
                             title='Ajouter un compte comptable')
    
    @app.route('/comptabilite/comptes/<int:id>/modifier', methods=['GET', 'POST'])
    def comptes_edit(id):
        """Modifier un compte comptable"""
        compte = CompteComptable.query.get_or_404(id)
        form = CompteComptableForm(obj=compte)
        
        if form.validate_on_submit():
            compte.numero_compte = form.numero_compte.data
            compte.nom_compte = form.nom_compte.data
            compte.type_compte = form.type_compte.data
            compte.actif = form.actif.data
            
            try:
                db.session.commit()
                flash('Compte comptable modifié avec succès.', 'success')
                return redirect(url_for('comptes_index'))
            except Exception as e:
                db.session.rollback()
                flash('Erreur lors de la modification du compte.', 'danger')
        
        return render_template('comptabilite/comptes/form.html', 
                             form=form, 
                             title="Modifier le compte",
                             compte=compte)
    
    @app.route('/comptabilite/comptes/<int:id>/supprimer', methods=['POST'])
    def comptes_delete(id):
        """Supprimer un compte comptable"""
        compte = CompteComptable.query.get_or_404(id)
        
        # Vérifier s'il y a des écritures liées à ce compte
        ecritures_debit = EcritureComptable.query.filter_by(compte_debit_id=id).count()
        ecritures_credit = EcritureComptable.query.filter_by(compte_credit_id=id).count()
        
        if ecritures_debit > 0 or ecritures_credit > 0:
            return jsonify({'error': 'Impossible de supprimer ce compte car il est utilisé dans des écritures comptables.'})
        
        try:
            db.session.delete(compte)
            db.session.commit()
            flash('Compte comptable supprimé avec succès.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la suppression: {str(e)}', 'error')
        
        return jsonify({'success': True})
    
    @app.route('/comptabilite/comptes/<int:id>/detail')
    def compte_detail(id):
        """Consultation détaillée d'un compte comptable"""
        compte = CompteComptable.query.get_or_404(id)
        
        # Récupérer les paramètres de filtre
        date_debut = request.args.get('date_debut')
        date_fin = request.args.get('date_fin')
        
        # Query de base pour les écritures
        ecritures_debit = EcritureComptable.query.filter_by(compte_debit_id=id)
        ecritures_credit = EcritureComptable.query.filter_by(compte_credit_id=id)
        
        # Appliquer les filtres de date si fournis
        if date_debut:
            try:
                date_debut_obj = datetime.strptime(date_debut, '%Y-%m-%d').date()
                ecritures_debit = ecritures_debit.filter(EcritureComptable.date_ecriture >= date_debut_obj)
                ecritures_credit = ecritures_credit.filter(EcritureComptable.date_ecriture >= date_debut_obj)
            except ValueError:
                flash('Format de date de début invalide', 'error')
        
        if date_fin:
            try:
                date_fin_obj = datetime.strptime(date_fin, '%Y-%m-%d').date()
                ecritures_debit = ecritures_debit.filter(EcritureComptable.date_ecriture <= date_fin_obj)
                ecritures_credit = ecritures_credit.filter(EcritureComptable.date_ecriture <= date_fin_obj)
            except ValueError:
                flash('Format de date de fin invalide', 'error')
        
        # Récupérer toutes les écritures
        ecritures_debit_list = ecritures_debit.all()
        ecritures_credit_list = ecritures_credit.all()
        
        # Créer une liste consolidée avec indication débit/crédit
        mouvements = []
        
        for ecriture in ecritures_debit_list:
            mouvements.append({
                'ecriture': ecriture,
                'date': ecriture.date_ecriture,
                'numero_piece': ecriture.numero_piece,
                'libelle': ecriture.libelle,
                'debit': float(ecriture.montant),
                'credit': 0,
                'contrepartie': ecriture.compte_credit
            })
        
        for ecriture in ecritures_credit_list:
            mouvements.append({
                'ecriture': ecriture,
                'date': ecriture.date_ecriture,
                'numero_piece': ecriture.numero_piece,
                'libelle': ecriture.libelle,
                'debit': 0,
                'credit': float(ecriture.montant),
                'contrepartie': ecriture.compte_debit
            })
        
        # Trier par date croissante
        mouvements.sort(key=lambda x: x['date'])
        
        # Calculer le solde progressif
        solde_progressif = 0
        for mouvement in mouvements:
            solde_progressif += mouvement['debit'] - mouvement['credit']
            mouvement['solde_progressif'] = solde_progressif
        
        # Calculer totaux
        total_debit = sum(m['debit'] for m in mouvements)
        total_credit = sum(m['credit'] for m in mouvements)
        solde_final = total_debit - total_credit
        
        # Déterminer le sens du solde selon le type de compte
        if compte.type_compte in ['actif', 'charge']:
            # Comptes de nature débitrice
            if solde_final >= 0:
                solde_sens = 'débiteur'
                solde_absolu = solde_final
            else:
                solde_sens = 'créditeur'
                solde_absolu = -solde_final
        else:
            # Comptes de nature créditrice (passif, produit)
            if solde_final <= 0:
                solde_sens = 'créditeur'
                solde_absolu = -solde_final
            else:
                solde_sens = 'débiteur'
                solde_absolu = solde_final
        
        return render_template('comptabilite/comptes/detail.html',
                             compte=compte,
                             mouvements=mouvements,
                             total_debit=total_debit,
                             total_credit=total_credit,
                             solde_final=solde_final,
                             solde_sens=solde_sens,
                             solde_absolu=solde_absolu,
                             date_debut=date_debut,
                             date_fin=date_fin,
                             formater_montant=formater_montant)
    
    @app.route('/comptabilite/consultation-comptes')
    def consultation_comptes():
        """Page de sélection de compte pour consultation"""
        # Récupérer tous les comptes actifs
        comptes = CompteComptable.query.filter_by(actif=True).order_by(CompteComptable.numero_compte).all()
        
        # Recherche par terme
        terme_recherche = request.args.get('q', '').strip()
        if terme_recherche:
            comptes = CompteComptable.query.filter(
                and_(
                    CompteComptable.actif == True,
                    or_(
                        CompteComptable.numero_compte.ilike(f'%{terme_recherche}%'),
                        CompteComptable.nom_compte.ilike(f'%{terme_recherche}%')
                    )
                )
            ).order_by(CompteComptable.numero_compte).all()
        
        return render_template('comptabilite/consultation/index.html',
                             comptes=comptes,
                             terme_recherche=terme_recherche)
    
    @app.route('/comptabilite/journaux')
    def journaux_index():
        """Liste des journaux comptables"""
        # Définir les types de journaux avec leurs critères
        journaux = [
            {
                'code': 'VT',
                'nom': 'Journal des Ventes',
                'description': 'Encaissements de loyers et ventes',
                'types': ['loyer', 'vente']
            },
            {
                'code': 'AC',
                'nom': 'Journal des Achats',
                'description': 'Achats et dépenses diverses',
                'types': ['achat', 'depense']
            },
            {
                'code': 'BQ',
                'nom': 'Journal de Banque',
                'description': 'Opérations bancaires et financières',
                'types': ['virement', 'emprunt', 'remboursement']
            },
            {
                'code': 'OD',
                'nom': 'Journal des Opérations Diverses',
                'description': 'Autres opérations comptables',
                'types': ['autre', None]
            }
        ]
        
        # Calculer les totaux pour chaque journal
        for journal in journaux:
            if journal['types'][0] is None:
                # Pour OD, prendre les écritures sans type ou avec type 'autre'
                total = db.session.query(func.sum(EcritureComptable.montant)).filter(
                    or_(
                        EcritureComptable.type_operation.is_(None),
                        EcritureComptable.type_operation == 'autre'
                    )
                ).scalar() or 0
                count = db.session.query(func.count(EcritureComptable.id)).filter(
                    or_(
                        EcritureComptable.type_operation.is_(None),
                        EcritureComptable.type_operation == 'autre'
                    )
                ).scalar() or 0
            else:
                total = db.session.query(func.sum(EcritureComptable.montant)).filter(
                    EcritureComptable.type_operation.in_(journal['types'])
                ).scalar() or 0
                count = db.session.query(func.count(EcritureComptable.id)).filter(
                    EcritureComptable.type_operation.in_(journal['types'])
                ).scalar() or 0
            
            journal['total'] = float(total)
            journal['count'] = count
        
        return render_template('comptabilite/journaux/index.html',
                             journaux=journaux,
                             formater_montant=formater_montant)
    
    @app.route('/comptabilite/journaux/<code>')
    def journaux_detail(code):
        """Détail d'un journal comptable"""
        # Définir les journaux et leurs critères
        journaux_config = {
            'VT': {
                'nom': 'Journal des Ventes',
                'description': 'Encaissements de loyers et ventes',
                'types': ['loyer', 'vente']
            },
            'AC': {
                'nom': 'Journal des Achats', 
                'description': 'Achats et dépenses diverses',
                'types': ['achat', 'depense']
            },
            'BQ': {
                'nom': 'Journal de Banque',
                'description': 'Opérations bancaires et financières', 
                'types': ['virement', 'emprunt', 'remboursement']
            },
            'OD': {
                'nom': 'Journal des Opérations Diverses',
                'description': 'Autres opérations comptables',
                'types': ['autre', None]
            }
        }
        
        if code not in journaux_config:
            flash('Journal non trouvé.', 'error')
            return redirect(url_for('journaux_index'))
        
        journal = journaux_config[code]
        journal['code'] = code
        
        # Récupérer les écritures correspondantes
        if code == 'OD':
            # Pour OD, prendre les écritures sans type ou avec type 'autre'
            ecritures = EcritureComptable.query.filter(
                or_(
                    EcritureComptable.type_operation.is_(None),
                    EcritureComptable.type_operation == 'autre'
                )
            ).order_by(EcritureComptable.date_ecriture.desc(), EcritureComptable.numero_piece.desc()).all()
        else:
            ecritures = EcritureComptable.query.filter(
                EcritureComptable.type_operation.in_(journal['types'])
            ).order_by(EcritureComptable.date_ecriture.desc(), EcritureComptable.numero_piece.desc()).all()
        
        # Calculer les totaux
        total_montant = sum(float(e.montant) for e in ecritures)
        
        return render_template('comptabilite/journaux/detail.html',
                             journal=journal,
                             ecritures=ecritures,
                             total_montant=total_montant,
                             formater_montant=formater_montant)
    
    @app.route('/comptabilite/budgets')
    def budgets_index():
        """Liste des budgets prévisionnels"""
        budgets = BudgetPrevisionnel.query.order_by(
            BudgetPrevisionnel.annee.desc(),
            BudgetPrevisionnel.mois.desc()
        ).all()
        
        return render_template('comptabilite/budgets/index.html',
                             budgets=budgets,
                             formater_montant=formater_montant)
    
    @app.route('/comptabilite/budgets/ajouter', methods=['GET', 'POST'])
    def budgets_add():
        """Ajouter un budget prévisionnel"""
        form = BudgetForm()
        
        if form.validate_on_submit():
            budget = BudgetPrevisionnel()
            budget.bien_id = form.bien_id.data if form.bien_id.data != 0 else None
            budget.annee = form.annee.data
            budget.mois = form.mois.data if form.mois.data != 0 else None
            budget.revenus_loyers_prevus = form.revenus_loyers_prevus.data or 0
            budget.autres_revenus_prevus = form.autres_revenus_prevus.data or 0
            budget.charges_courantes_prevues = form.charges_courantes_prevues.data or 0
            budget.travaux_prevus = form.travaux_prevus.data or 0
            budget.taxes_impots_prevus = form.taxes_impots_prevus.data or 0
            budget.assurances_prevues = form.assurances_prevues.data or 0
            budget.frais_gestion_prevus = form.frais_gestion_prevus.data or 0
            budget.notes = form.notes.data
            
            db.session.add(budget)
            db.session.commit()
            
            flash('Budget prévisionnel créé avec succès.', 'success')
            return redirect(url_for('budgets_index'))
        
        return render_template('comptabilite/budgets/form.html', 
                             form=form, 
                             titre="Créer un budget prévisionnel")
    
    @app.route('/comptabilite/rapports', methods=['GET', 'POST'])
    def rapports_comptables():
        """Génération de rapports comptables"""
        from models import BienImmobilier
        from datetime import datetime, date
        
        # Récupérer les biens pour le formulaire
        biens = BienImmobilier.query.all()
        
        # Dates par défaut
        date_fin = date.today()
        date_debut = date_fin.replace(month=1, day=1)
        
        return render_template('comptabilite/rapports/form.html', 
                             biens=biens,
                             date_debut=date_debut,
                             date_fin=date_fin)
    
    @app.route('/comptabilite/rapports/generer')
    def generer_rapport():
        """Génère et affiche un rapport comptable"""
        type_rapport = request.args.get('type_rapport')
        date_debut_str = request.args.get('date_debut')
        date_fin_str = request.args.get('date_fin')
        
        if date_debut_str and date_fin_str:
            try:
                date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d').date()
                date_fin = datetime.strptime(date_fin_str, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                # Dates par défaut en cas d'erreur
                date_fin = datetime.now().date()
                date_debut = date_fin.replace(month=1, day=1)
        else:
            # Dates par défaut si non spécifiées
            date_fin = datetime.now().date()
            date_debut = date_fin.replace(month=1, day=1)
        bien_id = request.args.get('bien_id', type=int)
        format_export = request.args.get('format_export', 'html')
        
        if type_rapport == 'balance':
            return generer_balance_comptable(date_debut, date_fin, bien_id, format_export)
        elif type_rapport == 'compte_resultat':
            return generer_compte_resultat(date_debut, date_fin, bien_id, format_export)
        elif type_rapport == 'journal':
            return generer_journal_general(date_debut, date_fin, bien_id, format_export)
        else:
            flash('Type de rapport non supporté.', 'warning')
            return redirect(url_for('rapports_comptables'))


def creer_ecriture_depense(depense):
    """Crée automatiquement l'écriture comptable pour une dépense"""
    # Compte de charge (débit) - selon le type de dépense
    comptes_charges = {
        'travaux': '615',  # Entretien et réparations
        'maintenance': '615',
        'reparation': '615',
        'assurance': '616',  # Primes d'assurance
        'taxes_locales': '635',  # Impôts et taxes directs
        'frais_gestion': '622',  # Rémunérations d'intermédiaires
    }
    
    numero_compte_charge = comptes_charges.get(depense.type_depense, '61')  # Services extérieurs par défaut
    compte_charge = CompteComptable.query.filter_by(numero_compte=numero_compte_charge).first()
    
    # Compte de trésorerie (crédit) - Banque par défaut
    compte_tresorerie = CompteComptable.query.filter_by(numero_compte='512').first()
    
    if compte_charge and compte_tresorerie:
        ecriture = EcritureComptable()
        ecriture.numero_piece = f"DEP{depense.id:06d}"
        ecriture.date_ecriture = depense.date_paiement or depense.date_depense
        ecriture.date_operation = depense.date_depense
        ecriture.compte_debit_id = compte_charge.id
        ecriture.compte_credit_id = compte_tresorerie.id
        ecriture.montant = depense.montant + (depense.montant_tva or 0)
        ecriture.libelle = f"{depense.type_depense} - {depense.description[:100]}"
        ecriture.reference_externe = f"depense_{depense.id}"
        ecriture.type_operation = 'depense'
        ecriture.bien_id = depense.bien_id
        ecriture.client_id = depense.fournisseur_id
        ecriture.validee = True
        ecriture.saisie_par = 'Auto'
        
        db.session.add(ecriture)
        depense.ecriture_comptable_id = ecriture.id


def generer_balance_comptable(date_debut, date_fin, bien_id, format_export):
    """Génère la balance comptable"""
    # Requête pour récupérer tous les comptes avec leurs soldes
    comptes = CompteComptable.query.filter_by(actif=True).order_by(CompteComptable.numero_compte).all()
    
    balance_data = []
    total_debit = 0
    total_credit = 0
    
    for compte in comptes:
        # Calcul des mouvements débiteurs
        debit = db.session.query(func.sum(EcritureComptable.montant)).filter(
            EcritureComptable.compte_debit_id == compte.id,
            EcritureComptable.date_operation.between(date_debut, date_fin),
            EcritureComptable.validee == True
        ).scalar() or 0
        
        # Calcul des mouvements créditeurs
        credit = db.session.query(func.sum(EcritureComptable.montant)).filter(
            EcritureComptable.compte_credit_id == compte.id,
            EcritureComptable.date_operation.between(date_debut, date_fin),
            EcritureComptable.validee == True
        ).scalar() or 0
        
        # Solde net
        solde = debit - credit
        
        if debit > 0 or credit > 0 or solde != 0:
            balance_data.append({
                'compte': compte,
                'debit': debit,
                'credit': credit,
                'solde': solde
            })
            total_debit += debit
            total_credit += credit
    
    if format_export == 'html':
        return render_template('comptabilite/rapports/balance.html',
                             balance_data=balance_data,
                             total_debit=total_debit,
                             total_credit=total_credit,
                             date_debut=date_debut,
                             date_fin=date_fin,
                             formater_montant=formater_montant)
    
    # TODO: Implémenter les autres formats (PDF, Excel, CSV)
    return "Format non supporté", 400


def generer_compte_resultat(date_debut, date_fin, bien_id, format_export):
    """Génère le compte de résultat"""
    # Comptes de produits (classe 7)
    comptes_produits = CompteComptable.query.filter(
        CompteComptable.numero_compte.like('7%'),
        CompteComptable.actif == True
    ).all()
    
    # Comptes de charges (classe 6)
    comptes_charges = CompteComptable.query.filter(
        CompteComptable.numero_compte.like('6%'),
        CompteComptable.actif == True
    ).all()
    
    produits_data = []
    charges_data = []
    total_produits = 0
    total_charges = 0
    
    # Calcul des produits
    for compte in comptes_produits:
        credit = db.session.query(func.sum(EcritureComptable.montant)).filter(
            EcritureComptable.compte_credit_id == compte.id,
            EcritureComptable.date_operation.between(date_debut, date_fin),
            EcritureComptable.validee == True
        ).scalar() or 0
        
        if credit > 0:
            produits_data.append({
                'compte': compte,
                'montant': credit
            })
            total_produits += credit
    
    # Calcul des charges
    for compte in comptes_charges:
        debit = db.session.query(func.sum(EcritureComptable.montant)).filter(
            EcritureComptable.compte_debit_id == compte.id,
            EcritureComptable.date_operation.between(date_debut, date_fin),
            EcritureComptable.validee == True
        ).scalar() or 0
        
        if debit > 0:
            charges_data.append({
                'compte': compte,
                'montant': debit
            })
            total_charges += debit
    
    resultat = total_produits - total_charges
    
    if format_export == 'html':
        return render_template('comptabilite/rapports/compte_resultat.html',
                             produits_data=produits_data,
                             charges_data=charges_data,
                             total_produits=total_produits,
                             total_charges=total_charges,
                             resultat=resultat,
                             date_debut=date_debut,
                             date_fin=date_fin,
                             formater_montant=formater_montant)
    
    return "Format non supporté", 400


def generer_journal_general(date_debut, date_fin, bien_id, format_export):
    """Génère le journal général"""
    query = EcritureComptable.query.filter(
        EcritureComptable.date_operation.between(date_debut, date_fin),
        EcritureComptable.validee == True
    )
    
    if bien_id:
        query = query.filter(EcritureComptable.bien_id == bien_id)
    
    ecritures = query.order_by(EcritureComptable.date_operation, EcritureComptable.id).all()
    
    if format_export == 'html':
        return render_template('comptabilite/rapports/journal.html',
                             ecritures=ecritures,
                             date_debut=date_debut,
                             date_fin=date_fin,
                             formater_montant=formater_montant)
    
    return "Format non supporté", 400