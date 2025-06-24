# Gestion Comptable SFEC

[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/SFEC/gestion_comptable_sfec/actions)
[![Coverage Status](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/SFEC/gestion_comptable_sfec/actions)

## Description

Module de gestion comptable complet pour la SFEC (STEAM AND FLUIDS EXPERT COMPANY)

## Spécialités de SFEC

SFEC est une entreprise spécialisée dans :
- Les systèmes de vapeur
- Les fluides industriels
- Les solutions techniques innovantes
- L'optimisation des processus industriels

## Fonctionnalités Principales

### Gestion des Clients et Fournisseurs
- Gestion complète des clients industriels
- Gestion des fournisseurs spécialisés en fluides et équipements
- Système de tags pour la classification des partenaires par secteur industriel
- Gestion des conditions commerciales spécifiques aux équipements industriels

### Gestion des Commandes
- Création et suivi des bons de commande pour équipements industriels
- Gestion des spécifications techniques
- Workflow adapté aux processus industriels
- Génération automatique des numéros de commande avec préfixe annuel

### Gestion des Factures
- Création de factures pour équipements et services industriels
- Gestion des paiements clients
- Workflow complet adapté aux besoins industriels
- Génération automatique des numéros de facture avec préfixe annuel

### Gestion du Stock
- Suivi des mouvements de stock pour équipements industriels
- Gestion des entrées et sorties de matériels spécifiques
- Alertes de niveaux bas de stock pour pièces critiques
- Rapports de stock optimisés pour la maintenance industrielle

### Gestion des Paiements
- Gestion des paiements pour équipements industriels
- Suivi des règlements pour projets industriels
- Génération automatique des numéros de paiement avec préfixe annuel
- Workflow complet adapté aux processus de validation industriels

### Rapports et Analyses
- Rapport de trésorerie complet adapté aux besoins industriels
- Statistiques des paiements par secteur industriel
- Statistiques du stock par type d'équipement
- Tableau de bord personnalisé pour la direction industrielle

## Sécurité et Accès

### Groupes d'Utilisateurs
- Comptable : Accès de base à la création et modification des documents
- Superviseur : Validation et approbation des documents
- Directeur : Accès complet avec approbation finale
- Ingénieur : Accès aux données techniques et spécifications

### États des Documents
- Brouillon : Document en cours de création
- Confirmé : Document validé par le comptable
- Approuvé : Document validé par le superviseur
- Payé : Document règlé (pour les paiements)
- Accusé : Document reçu (pour les commandes)
- Validé : Document validé par l'ingénieur (pour les spécifications techniques)

### Gestion des Clients et Fournisseurs
- Gestion complète des clients avec informations d'entreprise et adresses
- Gestion des fournisseurs avec partenariats exclusifs
- Système de tags pour la classification des partenaires
- Gestion des conditions commerciales

### Gestion des Commandes
- Création et suivi des bons de commande clients
- Gestion des lignes de commande
- Workflow complet : Brouillon → Confirmé → Approuvé → Accusé de réception
- Génération automatique des numéros de commande

### Gestion des Factures
- Création de factures proforma et finales
- Gestion des paiements clients
- Workflow complet : Brouillon → Confirmé → Approuvé → Payé
- Génération automatique des numéros de facture

### Gestion du Stock
- Suivi des mouvements de stock
- Gestion des entrées et sorties de produits
- Alertes de niveaux bas de stock
- Rapports de stock en temps réel

### Gestion des Paiements
- Gestion des paiements clients et fournisseurs
- Suivi des règlements
- Génération automatique des numéros de paiement
- Workflow complet : Brouillon → Confirmé → Approuvé → Payé

### Rapports et Analyses
- Rapport de trésorerie complet
- Statistiques des paiements
- Statistiques du stock
- Tableau de bord personnalisé

## Sécurité et Accès

### Groupes d'Utilisateurs
- Comptable : Accès de base à la création et modification des documents
- Superviseur : Validation et approbation des documents
- Directeur : Accès complet avec approbation finale

### États des Documents
- Brouillon : Document en cours de création
- Confirmé : Document validé par le comptable
- Approuvé : Document validé par le superviseur
- Payé : Document règlé (pour les paiements)
- Accusé : Document reçu (pour les commandes)

## Optimisations Techniques

### Index
- Index sur les champs clés pour les performances
- Index sur les dates pour les requêtes chronologiques
- Index sur les relations Many2One pour les jointures rapides

### Contraintes
- Contraintes d'unicité sur les numéros de documents
- Contraintes de non-nullité sur les champs obligatoires
- Vérifications de cohérence des données

### Scripts de Maintenance
- Nettoyage automatique des documents annulés
- Optimisation des séquences
- Vérifications périodiques des données
- Alertes de stock automatiques

## Installation

1. Assurez-vous d'avoir Odoo 16.0 installé
2. Installez les dépendances requises
3. Activez le mode développeur dans Odoo
4. Installez le module "Gestion Comptable SFEC"
5. Configurez les paramètres spécifiques aux équipements industriels

## Configuration Spécifique

1. Configuration des types d'équipements industriels
2. Paramétrage des seuils de stock pour pièces critiques
3. Configuration des workflows spécifiques aux projets industriels
4. Paramétrage des rapports adaptés aux besoins industriels
5. Configuration des alertes pour la maintenance préventive

## Configuration

1. Configurez les séquences pour chaque type de document
2. Créez les groupes d'utilisateurs nécessaires
3. Configurez les workflows selon vos besoins
4. Paramétrez les alertes de stock

## Support

Pour toute question ou problème, contactez le support SFEC à support@sfec.fr

## Version

1.0.0 - Version initiale complète

## Licence

Propriété de SFEC - Tous droits réservés

Le module Gestion Comptable SFEC est une solution complète pour la gestion comptable d'entreprise, spécialement conçue pour gérer les flux financiers, les commandes, et les relations avec les fournisseurs. Ce module inclut des fonctionnalités avancées pour les partenariats exclusifs avec SPIRAX SARCO et APPROTECH.

## Fonctionnalités Principales

### 1. Gestion des Flux Commerciaux
- **Client-Entreprise**
  - Gestion des bons de commande
  - Factures proforma
  - Accusés de réception
  - Factures finales
  - Paiements clients

- **Entreprise-Fournisseurs**
  - Demandes d'achat
  - Factures fournisseurs
  - Commandes fournisseurs
  - Paiements fournisseurs
  - Suivi des livraisons

### 2. Gestion des Partenariats Exclusifs
- Gestion des partenariats avec SPIRAX SARCO et APPROTECH
- Validation automatique des commandes
- Suivi des performances
- Statistiques détaillées

### 3. Tableau de Bord
- Indicateurs de performance clés
- Graphiques d'évolution
- Alertes en temps réel
- Statistiques des stocks
- Suivi des paiements

### 4. Gestion des Stocks
- Entrées et sorties de stock
- Alertes stock bas
- Suivi des mouvements
- Réapprovisionnement automatique

### 5. Interface Utilisateur
- Design néomorphique moderne
- Animations fluides
- Interface responsive
- Validation en temps réel
- Messages de statut clairs

## Installation

1. Assurez-vous d'avoir les dépendances nécessaires installées :
   ```bash
   pip install odoo
   ```

2. Ajoutez le module à votre liste de modules Odoo :
   ```bash
   addons_path=/path/to/your/addons,/path/to/gestion_comptable_sfec
   ```

3. Mettez à jour la liste des modules :
   ```bash
   python -m odoo -c /path/to/odoo.conf -u all
   ```

4. Installez le module via l'interface web d'Odoo :
   - Allez dans le menu "Apps"
   - Recherchez "Gestion Comptable SFEC"
   - Cliquez sur "Installer"

## Configuration

1. Configuration des Partenariats Exclusifs :
   - Allez dans "Gestion Comptable > Partenariats Exclusifs"
   - Configurez les partenariats avec SPIRAX SARCO et APPROTECH
   - Définissez les conditions particulières

2. Configuration des Alertes :
   - Allez dans "Gestion Comptable > Configuration > Alertes"
   - Configurez les seuils de stock
   - Définissez les relances automatiques

## Dépendances

- Odoo >= 16.0
- Python >= 3.8
- PostgreSQL >= 13
- Les modules Odoo suivants :
  - sale
  - purchase
  - stock
  - account
  - contacts
  - mail
  - base_automation
  - report_xlsx
  - web_tour
  - web_responsive
  - web_widget_colorpicker
  - web_widget_one2many_tags

## Support

Pour obtenir du support ou signaler des bugs :

- Email : support@sfec.com
- Site web : https://sfec.com
- GitHub : https://github.com/SFEC/gestion_comptable_sfec/issues

## Contributing

1. Fork le projet
2. Créez votre branche de fonctionnalité (`git checkout -b feature/amazing-feature`)
3. Commit vos changements (`git commit -m 'Add some amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request

## Licence

Ce module est sous licence LGPL-3. Consultez le fichier LICENSE pour plus de détails.

## Version

1.0.0 - Version initiale complète avec toutes les fonctionnalités principales
