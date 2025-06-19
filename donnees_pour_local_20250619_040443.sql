-- Export des données pour installation locale
-- Créé le 19/06/2025 à 04:04:43

-- 5 clients
INSERT INTO clients (nom, prenom, email, telephone, adresse, ville, code_postal, type_client, type_piece_identite, numero_piece_identite) VALUES ('ZEIDANE', 'Aweicha', 'aweicha@gmail.com', '49602030', '365 F-Nord Tevragh Zeina', 'Nouakchott', '', 'locataire', 'carte_identite', '7493636352');
INSERT INTO clients (nom, prenom, email, telephone, adresse, ville, code_postal, type_client, type_piece_identite, numero_piece_identite) VALUES ('OULD AHMED', 'Mohamed Lemine', 'Ahmed_Ould_Ahmed@gmail.com', '22817045', '365 F-Nord Tevragh Zeina', 'Nouakchott', '', 'locataire', 'carte_identite', '8960704607');
INSERT INTO clients (nom, prenom, email, telephone, adresse, ville, code_postal, type_client, type_piece_identite, numero_piece_identite) VALUES ('AL-DAOUS', 'Yahya Mohamed Rajeh', 'aldaous@gmail.com', '967733004315', '365 F-Nord Tevragh Zeina', 'Nouakchott', '', 'locataire', 'passeport', '00039505');
INSERT INTO clients (nom, prenom, email, telephone, adresse, ville, code_postal, type_client, type_piece_identite, numero_piece_identite) VALUES ('ABD EL VETTAH', 'Sidi Mohamed', 'abdelvettah@gmail.com', '31366050', '', 'Nouakchott', '', 'locataire', 'carte_identite', '1417715238');
INSERT INTO clients (nom, prenom, email, telephone, adresse, ville, code_postal, type_client, type_piece_identite, numero_piece_identite) VALUES ('EL KHALEF', 'Propriétaire', 'elkhafef@email.com', '36306854', '', 'Nouakchott', '', 'proprietaire', 'carte_identite', '7716097122');

-- 7 biens immobiliers
INSERT INTO biens_immobiliers (titre, type_bien, adresse, ville, surface, prix_location_mensuel, proprietaire_id) VALUES ('Magasin-A', 'local', 'F-Nord sur Est Tavragh Zeina', 'Nouakchott', 144.0, 35000.0, 1);
INSERT INTO biens_immobiliers (titre, type_bien, adresse, ville, surface, prix_location_mensuel, proprietaire_id) VALUES ('Magasin-B', 'local', 'F-Nord sur Est Tavragh Zeina', 'Nouakchott', 48.0, 15000.0, 1);
INSERT INTO biens_immobiliers (titre, type_bien, adresse, ville, surface, prix_location_mensuel, proprietaire_id) VALUES ('Magasin-C', 'local', 'F-Nord sur Est Tavragh Zeina', 'Nouakchott', 48.0, 15000.0, 1);
INSERT INTO biens_immobiliers (titre, type_bien, adresse, ville, surface, prix_location_mensuel, proprietaire_id) VALUES ('Magasin-D', 'bureau', 'F-Nord sur Est Tavragh Zeina', 'Nouakchott', 24.0, 5000.0, 1);
INSERT INTO biens_immobiliers (titre, type_bien, adresse, ville, surface, prix_location_mensuel, proprietaire_id) VALUES ('C', 'appartement', '365 F-Nord Tevragh Zeina', 'Nouakchott', 108.0, 8000.0, 1);
INSERT INTO biens_immobiliers (titre, type_bien, adresse, ville, surface, prix_location_mensuel, proprietaire_id) VALUES ('B', 'appartement', '365 F-Nord Tevragh Zeina', 'Nouakchott', 108.0, 9000.0, 1);
INSERT INTO biens_immobiliers (titre, type_bien, adresse, ville, surface, prix_location_mensuel, proprietaire_id) VALUES ('D', 'appartement', '365 F-Nord Tevragh Zeina', 'Nouakchott', 108.0, 9000.0, 1);

-- 30 comptes comptables
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('10', 'CAPITAL ET RESERVES', 'passif', 'capitaux', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('101', 'Capital', 'passif', 'capitaux', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('12', 'RESULTAT DE L'EXERCICE', 'resultat', 'capitaux', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('21', 'IMMOBILISATIONS CORPORELLES', 'actif', 'immobilisation', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('213', 'Constructions', 'actif', 'immobilisation', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('2131', 'Immeubles de rapport', 'actif', 'immobilisation', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('41', 'CLIENTS ET COMPTES RATTACHES', 'actif', 'creance', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('411', 'Clients', 'actif', 'creance', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('4111', 'Locataires', 'actif', 'creance', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('42', 'PERSONNEL', 'passif', 'dette', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('44', 'ETAT ET COLLECTIVITES', 'actif', 'creance', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('401', 'Fournisseurs', 'passif', 'dette', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('51', 'BANQUES', 'actif', 'tresorerie', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('512', 'Banques', 'actif', 'tresorerie', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('53', 'CAISSE', 'actif', 'tresorerie', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('531', 'Caisse', 'actif', 'tresorerie', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('61', 'SERVICES EXTERIEURS', 'charge', 'exploitation', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('615', 'Entretien et réparations', 'charge', 'exploitation', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('616', 'Primes d'assurance', 'charge', 'exploitation', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('622', 'Rémunérations d'intermédiaires', 'charge', 'exploitation', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('63', 'IMPOTS ET TAXES', 'charge', 'exploitation', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('635', 'Impôts et taxes directs', 'charge', 'exploitation', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('70', 'VENTES', 'produit', 'exploitation', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('701', 'Ventes de marchandises', 'produit', 'exploitation', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('75', 'AUTRES PRODUITS', 'produit', 'exploitation', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('751', 'Revenus immobiliers', 'produit', 'exploitation', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('7511', 'Loyers perçus', 'produit', 'exploitation', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('623', 'Dons et libéralités', 'charge', '', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('1688', 'Autres emprunts et dettes assimilées', 'passif', '', True);
INSERT INTO comptes_comptables (numero_compte, nom_compte, type_compte, sous_type, actif) VALUES ('467', 'Propriétaires', 'passif', '', True);
