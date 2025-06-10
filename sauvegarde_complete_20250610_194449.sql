-- Sauvegarde complète de la base de données
-- Générée le 2025-06-10 19:44:49
-- 

SET session_replication_role = replica;

-- Table: clients
DELETE FROM clients;
INSERT INTO clients (id,nom,prenom,email,telephone,adresse,ville,code_postal,type_client,date_creation,type_piece_identite,numero_piece_identite) VALUES
  (3,'ZEIDANE','Aweicha','aweicha@gmail.com','49602030','365 F-Nord Tevragh Zeina','Nouakchott','','locataire',2025-05-25 11:29:53.277346,'carte_identite','7493636352'),
  (2,'OULD AHMED','Mohamed Lemine','Ahmed_Ould_Ahmed@gmail.com','22817045','365 F-Nord Tevragh Zeina','Nouakchott','','locataire',2025-05-25 08:51:21.405906,'carte_identite','8960704607'),
  (4,'AL-DAOUS','Yahya Mohamed Rajeh','aldaous@gmail.com','967733004315','365 F-Nord Tevragh Zeina','Nouakchott','','locataire',2025-05-25 11:51:20.860315,'passeport','00039505'),
  (5,'ABD EL VETTAH','Sidi Mohamed','abdelvettah@gmail.com','31366050','','Nouakchott','','locataire',2025-06-01 05:36:32.971875,'carte_identite','1417715238'),
  (1,'EL KHALEF','Propriétaire','elkhafef@email.com','36306854','','Nouakchott','','proprietaire',NULL,'carte_identite','7716097122');

-- Table: biens_immobiliers
DELETE FROM biens_immobiliers;
INSERT INTO biens_immobiliers (id,titre,type_bien,adresse,ville,code_postal,surface,nombre_pieces,nombre_chambres,prix_achat,prix_location_mensuel,charges_mensuelles,description,meuble,balcon,parking,ascenseur,etage,annee_construction,disponible,date_creation,proprietaire_id,latitude,longitude,somelec_numero_compteur,somelec_code_abonnement,somelec_index_actuel,somelec_date_releve,snde_numero_compteur,snde_code_abonnement,snde_index_actuel,snde_date_releve) VALUES
  (4,'Magasin-A','local','F-Nord sur Est Tavragh Zeina','Nouakchott','',144.0,1,1,NULL,35000.0,0.0,'Localisation du Grand Magasin
1.	Type de localisation :
Le grand magasin est situé dans un emplacement stratégique.
2.	Détails de l''emplacement :
o	Il est situé sur une grande avenue, assurant une visibilité maximale et un flux constant de passants.
o	Il se trouve également à un angle, ce qui offre une double exposition et un accès facile depuis deux rues différentes.
3.	Avantages de l''emplacement :
o	Idéal pour attirer des clients grâce à sa visibilité accrue.
o	Possibilité d''aménager deux vitrines ou plus, augmentant les opportunités publicitaires et de présentation des produits.
',FALSE,FALSE,FALSE,FALSE,NULL,2012,TRUE,2025-05-25 08:35:14.790967,1,18.108472,-15.965972,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (5,'Magasin-B','local','F-Nord sur Est Tavragh Zeina','Nouakchott','',48.0,1,1,NULL,15000.0,0.0,'1.	Type de localisation :
Le grand magasin est situé dans un emplacement stratégique.
2.	Détails de l''emplacement :
o	Il est situé sur une grande avenue, assurant une visibilité maximale et un flux constant de passants.
3.	Avantages de l''emplacement :
o	Idéal pour attirer des clients grâce à sa visibilité accrue.
o	Possibilité d''aménager deux vitrines ou plus, augmentant les opportunités publicitaires et de présentation des produits.',FALSE,FALSE,FALSE,FALSE,0,2023,TRUE,2025-05-25 08:38:29.821901,1,18.108472,-15.965972,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (6,'Magasin-C','local','F-Nord sur Est Tavragh Zeina','Nouakchott','',48.0,1,1,NULL,15000.0,0.0,'1.	Type de localisation :
Le grand magasin est situé dans un emplacement stratégique.
2.	Détails de l''emplacement :
o	Il est situé sur une grande avenue, assurant une visibilité maximale et un flux constant de passants.
3.	Avantages de l''emplacement :
o	Idéal pour attirer des clients grâce à sa visibilité accrue.
o	Possibilité d''aménager deux vitrines ou plus, augmentant les opportunités publicitaires et de présentation des produits.',FALSE,FALSE,FALSE,FALSE,0,2023,TRUE,2025-05-25 08:40:34.788341,1,18.108472,-15.965972,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (7,'Magasin-D','bureau','F-Nord sur Est Tavragh Zeina','Nouakchott','',24.0,1,1,NULL,5000.0,0.0,'Bureau est situé dans un emplacement stratégique.
	Avantages de l''emplacement :
	Idéal pour attirer des clients grâce à sa visibilité accrue.
',FALSE,FALSE,FALSE,FALSE,0,2023,TRUE,2025-05-25 08:44:34.751639,1,18.108472,-15.965972,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (1,'C','appartement','365 F-Nord Tevragh Zeina','Nouakchott','',108.0,3,2,NULL,8000.0,0.0,'Appartement au rez-de-chaussée à droite de la rentrée avec 3 pièces dont 2 chambres, 2 toilettes et un séjour',FALSE,FALSE,FALSE,FALSE,0,2006,FALSE,2025-05-25 04:31:16.918143,1,18.109639,-15.970278,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (2,'B','appartement','365 F-Nord Tevragh Zeina','Nouakchott','',108.0,3,2,NULL,9000.0,0.0,'Appartement au premier étage à gauche de la rentrée avec 3 pièces dont 2 chambres, 2 toilettes et un séjour',FALSE,FALSE,FALSE,FALSE,1,2006,FALSE,2025-05-25 04:35:17.817167,1,18.109639,-15.970278,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (3,'D','appartement','365 F-Nord Tevragh Zeina','Nouakchott','',108.0,3,2,NULL,9000.0,0.0,'Appartement au premier étage à droite de la rentrée avec 3 pièces dont 2 chambres, 2 toilettes et un séjour et un parking à droite de l''entrée.',FALSE,FALSE,TRUE,FALSE,1,2006,FALSE,2025-05-25 04:38:33.442116,1,18.109639,-15.970278,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);

-- Table: contrats_location
DELETE FROM contrats_location;
INSERT INTO contrats_location (id,date_debut,date_fin,loyer_mensuel,charges_mensuelles,depot_garantie,frais_agence,statut,conditions_particulieres,date_creation,bien_id,locataire_id,somelec_numero_compteur,somelec_code_abonnement,somelec_index_initial,somelec_date_branchement,somelec_quitus_precedent,snde_numero_compteur,snde_code_abonnement,snde_index_initial,snde_date_branchement,snde_quitus_precedent) VALUES
  (1,2021-10-26,NULL,8000.0,0.0,8000.0,0.0,'actif','Le numéro de téléphone est celui de sa femme Mariem',2025-05-25 10:23:55.890435,1,2,NULL,NULL,0.0,NULL,FALSE,NULL,NULL,0.0,NULL,FALSE),
  (2,2024-05-28,NULL,9000.0,0.0,9000.0,0.0,'actif','Pas de contrat SOMELEC',2025-05-25 11:36:38.729002,2,3,NULL,NULL,0.0,NULL,FALSE,NULL,NULL,0.0,NULL,FALSE),
  (4,2021-11-09,NULL,9000.0,0.0,0.0,NULL,'actif',NULL,2025-05-25 13:29:40.521468,3,4,NULL,NULL,0.0,NULL,FALSE,NULL,NULL,0.0,NULL,FALSE),
  (6,2022-10-23,NULL,35000.0,0.0,0.0,0.0,'actif','',2025-06-01 05:49:11.168429,4,5,NULL,NULL,0.0,NULL,FALSE,NULL,NULL,0.0,NULL,FALSE);

-- Table: paiements_loyer
DELETE FROM paiements_loyer;
INSERT INTO paiements_loyer (id,mois,annee,montant_loyer,montant_charges,date_paiement,date_echeance,statut,mode_paiement,reference_paiement,remarques,date_creation,contrat_id) VALUES
  (1,5,2025,8000.0,0.0,2025-05-01,2025-05-01,'paye','virement','Bankiliy','',2025-05-25 12:57:46.112074,1),
  (2,5,2025,9000.0,0.0,2025-05-08,2025-05-01,'paye','virement','Bankiliy','',2025-05-25 12:58:47.387120,2),
  (4,5,2025,35000.0,0.0,2025-05-10,2025-05-01,'paye','virement','Bankiliy','',2025-06-01 05:51:36.833005,6),
  (5,6,2025,8000.0,0.0,2025-06-02,2025-06-01,'paye','virement','Bankiliy','',2025-06-04 18:43:54.089591,1),
  (3,5,2025,18000.0,0.0,2025-05-15,2025-05-01,'paye','virement','Bankiliy','Paiement des mois de mai et juin 2025.',2025-05-25 14:04:48.025995,4),
  (6,6,2025,35000.0,0.0,2025-06-08,2025-06-01,'paye','virement','Bankiliy','',2025-06-08 21:38:33.772597,6);

-- Table: photos_biens
DELETE FROM photos_biens;

-- Table: documents_contrat
DELETE FROM documents_contrat;
INSERT INTO documents_contrat (id,contrat_id,nom_fichier,nom_original,type_document,format_fichier,taille_fichier,chemin_stockage,description,date_ajout,ajoute_par) VALUES
  (1,1,'1e849430409549768b694ebf5fe91d41.pdf','Contrat_Location_Appartements_Mohamed_Lemine.pdf','piece_identite','pdf',115430,'static/documents/1e849430409549768b694ebf5fe91d41.pdf','Contrat de location',2025-05-25 11:04:53.662704,'Admin'),
  (2,1,'56c6d32e71da4bf690fd2bd702f487d9.jpeg','Mohamed_Lemine_cni_recto.jpeg','piece_identite','jpeg',64757,'static/documents/56c6d32e71da4bf690fd2bd702f487d9.jpeg','CNI recto',2025-05-25 11:18:50.753905,'Admin'),
  (3,1,'e1e1d98d74a44326be55e7cc190ba059.jpeg','Mohamed_Lemine_cni_verso.jpeg','piece_identite','jpeg',60428,'static/documents/e1e1d98d74a44326be55e7cc190ba059.jpeg','CNI Verso',2025-05-25 11:19:18.951320,'Admin'),
  (4,2,'9d9633a1002d4ed8be511e3007225f38.jpeg','Aweicha_cni_recto.jpeg','piece_identite','jpeg',73072,'static/documents/9d9633a1002d4ed8be511e3007225f38.jpeg','CNI Verso',2025-05-25 11:38:51.990855,'Admin'),
  (5,2,'1353ec2d1fbb481a99aa3eedca790718.jpeg','Aweicha_cni_verso.jpeg','piece_identite','jpeg',77029,'static/documents/1353ec2d1fbb481a99aa3eedca790718.jpeg','CNI Verso',2025-05-25 11:39:24.358329,'Admin'),
  (6,2,'eeb05779e3624f4d84d58bfdb0c1c9e2.','pdf','piece_identite','',128783,'static/documents/eeb05779e3624f4d84d58bfdb0c1c9e2.','Contrat de location',2025-05-25 11:40:34.612402,'Admin'),
  (7,4,'a5f21ba2e8e4449d8b4415a90a2bd8e8.jpeg','AL-DAOUS_Profession.jpeg','justificatif','jpeg',36862,'static/documents/a5f21ba2e8e4449d8b4415a90a2bd8e8.jpeg','',2025-05-25 13:48:12.042693,'Admin'),
  (8,6,'d13a4ef238bb4868b3bc3eecfa7993e4.jpg','sidi_mohamed_cni.jpg','piece_identite','jpg',89849,'static/documents/d13a4ef238bb4868b3bc3eecfa7993e4.jpg','',2025-06-01 15:00:41.023899,'Admin');

-- Table: releves_compteurs
DELETE FROM releves_compteurs;

-- Table: comptes_comptables
DELETE FROM comptes_comptables;
INSERT INTO comptes_comptables (id,numero_compte,nom_compte,type_compte,sous_type,compte_parent_id,actif,date_creation) VALUES
  (1,'10','CAPITAL ET RESERVES','passif','capitaux',NULL,NULL,NULL),
  (2,'101','Capital','passif','capitaux',NULL,NULL,NULL),
  (3,'12','RESULTAT DE L''EXERCICE','resultat','capitaux',NULL,NULL,NULL),
  (4,'21','IMMOBILISATIONS CORPORELLES','actif','immobilisation',NULL,NULL,NULL),
  (5,'213','Constructions','actif','immobilisation',NULL,NULL,NULL),
  (6,'2131','Immeubles de rapport','actif','immobilisation',NULL,NULL,NULL),
  (7,'41','CLIENTS ET COMPTES RATTACHES','actif','creance',NULL,NULL,NULL),
  (8,'411','Clients','actif','creance',NULL,NULL,NULL),
  (9,'4111','Locataires','actif','creance',NULL,NULL,NULL),
  (10,'42','PERSONNEL','passif','dette',NULL,NULL,NULL),
  (11,'44','ETAT ET COLLECTIVITES','actif','creance',NULL,NULL,NULL),
  (12,'401','Fournisseurs','passif','dette',NULL,NULL,NULL),
  (13,'51','BANQUES','actif','tresorerie',NULL,NULL,NULL),
  (14,'512','Banques','actif','tresorerie',NULL,NULL,NULL),
  (15,'53','CAISSE','actif','tresorerie',NULL,NULL,NULL),
  (16,'531','Caisse','actif','tresorerie',NULL,NULL,NULL),
  (17,'61','SERVICES EXTERIEURS','charge','exploitation',NULL,NULL,NULL),
  (18,'615','Entretien et réparations','charge','exploitation',NULL,NULL,NULL),
  (19,'616','Primes d''assurance','charge','exploitation',NULL,NULL,NULL),
  (20,'622','Rémunérations d''intermédiaires','charge','exploitation',NULL,NULL,NULL),
  (21,'63','IMPOTS ET TAXES','charge','exploitation',NULL,NULL,NULL),
  (22,'635','Impôts et taxes directs','charge','exploitation',NULL,NULL,NULL),
  (23,'70','VENTES','produit','exploitation',NULL,NULL,NULL),
  (24,'701','Ventes de marchandises','produit','exploitation',NULL,NULL,NULL),
  (25,'75','AUTRES PRODUITS','produit','exploitation',NULL,NULL,NULL),
  (26,'751','Revenus immobiliers','produit','exploitation',NULL,NULL,NULL),
  (27,'7511','Loyers perçus','produit','exploitation',NULL,NULL,NULL);

-- Table: ecritures_comptables
DELETE FROM ecritures_comptables;

-- Table: budgets_previsionnels
DELETE FROM budgets_previsionnels;

-- Table: depenses_immobilieres
DELETE FROM depenses_immobilieres;

SET session_replication_role = DEFAULT;
SELECT setval('clients_id_seq', COALESCE((SELECT MAX(id) FROM clients), 1));
SELECT setval('biens_immobiliers_id_seq', COALESCE((SELECT MAX(id) FROM biens_immobiliers), 1));
SELECT setval('photos_biens_id_seq', COALESCE((SELECT MAX(id) FROM photos_biens), 1));
SELECT setval('contrats_location_id_seq', COALESCE((SELECT MAX(id) FROM contrats_location), 1));
SELECT setval('paiements_loyer_id_seq', COALESCE((SELECT MAX(id) FROM paiements_loyer), 1));
SELECT setval('documents_contrat_id_seq', COALESCE((SELECT MAX(id) FROM documents_contrat), 1));
SELECT setval('comptes_comptables_id_seq', COALESCE((SELECT MAX(id) FROM comptes_comptables), 1));
SELECT setval('budgets_previsionnels_id_seq', COALESCE((SELECT MAX(id) FROM budgets_previsionnels), 1));
SELECT setval('ecritures_comptables_id_seq', COALESCE((SELECT MAX(id) FROM ecritures_comptables), 1));
SELECT setval('depenses_immobilieres_id_seq', COALESCE((SELECT MAX(id) FROM depenses_immobilieres), 1));
SELECT setval('releves_compteurs_id_seq', COALESCE((SELECT MAX(id) FROM releves_compteurs), 1));
