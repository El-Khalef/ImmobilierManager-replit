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
            depense = DepenseImmobiliere(
                bien_id=form.bien_id.data if form.bien_id.data != 0 else None,
                fournisseur_id=form.fournisseur_id.data if form.fournisseur_id.data != 0 else None,
                type_depense=form.type_depense.data,
                categorie=form.categorie.data,
                montant=form.montant.data,
                date_depense=form.date_depense.data,
                date_paiement=form.date_paiement.data,
                statut_paiement=form.statut_paiement.data,
                mode_paiement=form.mode_paiement.data,
                numero_facture=form.numero_facture.data,
                reference_paiement=form.reference_paiement.data,
                description=form.description.data,
                justificatif_path=justificatif_path,
                deductible_impots=form.deductible_impots.data,
                tva_applicable=form.tva_applicable.data,
                montant_tva=form.montant_tva.data or 0
            )
            
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
            ecriture = EcritureComptable(
                numero_piece=form.numero_piece.data,
                date_ecriture=form.date_ecriture.data,
                date_operation=form.date_operation.data,
                compte_debit_id=form.compte_debit_id.data,
                compte_credit_id=form.compte_credit_id.data,
                montant=form.montant.data,
                libelle=form.libelle.data,
                type_operation=form.type_operation.data,
                bien_id=form.bien_id.data if form.bien_id.data != 0 else None,
                client_id=form.client_id.data if form.client_id.data != 0 else None,
                reference_externe=form.reference_externe.data,
                validee=True,
                saisie_par='Admin'
            )
            
            db.session.add(ecriture)
            db.session.commit()
            
            flash('Écriture comptable enregistrée avec succès.', 'success')
            return redirect(url_for('ecritures_index'))
        
        return render_template('comptabilite/ecritures/form.html', 
                             form=form, 
                             titre="Ajouter une écriture")
    
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
            budget = BudgetPrevisionnel(
                bien_id=form.bien_id.data if form.bien_id.data != 0 else None,
                annee=form.annee.data,
                mois=form.mois.data if form.mois.data != 0 else None,
                revenus_loyers_prevus=form.revenus_loyers_prevus.data or 0,
                autres_revenus_prevus=form.autres_revenus_prevus.data or 0,
                charges_courantes_prevues=form.charges_courantes_prevues.data or 0,
                travaux_prevus=form.travaux_prevus.data or 0,
                taxes_impots_prevus=form.taxes_impots_prevus.data or 0,
                assurances_prevues=form.assurances_prevues.data or 0,
                frais_gestion_prevus=form.frais_gestion_prevus.data or 0,
                notes=form.notes.data
            )
            
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
        form = RapportComptableForm()
        
        if form.validate_on_submit():
            # Rediriger vers le rapport spécifique
            return redirect(url_for('generer_rapport',
                                  type_rapport=form.type_rapport.data,
                                  date_debut=form.date_debut.data,
                                  date_fin=form.date_fin.data,
                                  bien_id=form.bien_id.data if form.bien_id.data != 0 else None,
                                  format_export=form.format_export.data))
        
        return render_template('comptabilite/rapports/form.html', form=form)
    
    @app.route('/comptabilite/rapports/generer')
    def generer_rapport():
        """Génère et affiche un rapport comptable"""
        type_rapport = request.args.get('type_rapport')
        date_debut = datetime.strptime(request.args.get('date_debut'), '%Y-%m-%d').date()
        date_fin = datetime.strptime(request.args.get('date_fin'), '%Y-%m-%d').date()
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
        ecriture = EcritureComptable(
            numero_piece=f"DEP{depense.id:06d}",
            date_ecriture=depense.date_paiement or depense.date_depense,
            date_operation=depense.date_depense,
            compte_debit_id=compte_charge.id,
            compte_credit_id=compte_tresorerie.id,
            montant=depense.montant_total,
            libelle=f"{depense.type_depense} - {depense.description[:100]}",
            reference_externe=f"depense_{depense.id}",
            type_operation='depense',
            bien_id=depense.bien_id,
            client_id=depense.fournisseur_id,
            validee=True,
            saisie_par='Auto'
        )
        
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