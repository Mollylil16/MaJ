# -*- coding: utf-8 -*-
{
    'name': 'Gestion Comptable SFEC',
    'version': '1.0.0',
    'category': 'Accounting',
    'summary': "Automatisation complète des processus comptables pour l'entreprise",
    'description': """
Module Odoo personnalisé pour gérer :
- les interactions client-entreprise (bon de commande, facture proforma, facture finale),
- les achats auprès des fournisseurs (demande, bon de commande, facture),
- la gestion de stock (entrée/sortie),
- le volet financier (paiements par caisse, banque, crédit),
- la traçabilité des clients et entreprises partenaires.
""",
    'author': 'SFEC2',
    'website': 'https://SFEC.com',
    'support': 'support@sfec.com',
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
    'auto_install': False,
    'controllers': [
    'gestion_comptable_sfec.controllers.dashboard_controller',
],
    'depends': [
        'sale',
        'purchase',
        'stock',
        'account',
        'contacts',
        'mail',
        'base_automation',
        'report_xlsx',
        'web_tour',
        'base_import',
        'web',
    ],
    'assets': {
        'web.assets_backend': [
            'gestion_comptable_sfec/static/src/css/neumorphic.css',
            'gestion_comptable_sfec/static/src/css/form_styles.css',
            'gestion_comptable_sfec/static/src/css/drag_drop.css',
            'gestion_comptable_sfec/static/src/css/custom_tags.css',
            'gestion_comptable_sfec/static/src/js/neumorphic.js',
            'gestion_comptable_sfec/static/src/js/form_interactions.js',
            'gestion_comptable_sfec/static/src/js/drag_drop_widget.js',
            'gestion_comptable_sfec/static/src/js/advanced_filters.js',
        ],
        'web.assets_qweb': [
            'gestion_comptable_sfec/static/src/xml/drag_drop_template.xml',
        ]
    },
    'data': [
    # Sécurité
    'security/groups.xml',
    'security/ir.model.access.csv',

    'views/entreprise_views.xml',
    'views/client_views.xml',
    'views/bon_commande_client_view.xml',
    'views/facture_proforma_view.xml',
    'views/accuse_reception_view.xml',
    'views/facture_finale_view.xml',
    'views/paiement_client_view.xml',
    'views/dashboard_template.xml',
    'views/drag_drop_view.xml',
    'views/fournisseur_views.xml',
    'views/bon_commande_fournisseur_view.xml',
    'views/facture_fournisseur_view.xml',
    'views/paiement_fournisseur_view.xml',
    'views/partenariat_exclusif_view.xml',
    'views/reception_fournisseur_view.xml',
    'views/article_view.xml',
    'views/stock_mouvement_view.xml',
    'views/report_views.xml',
    'views/facture_finale_view.xml',
    'views/statistique_paiement_view.xml',
    'views/menu.xml',
    # Vues
    'views/ligne_commande_client_view.xml',
    'views/ligne_facture_proforma_view.xml',
    'views/ligne_livraison_article_fournisseur_view.xml',
    

    # Données
    'data/fournisseur_data.xml',
    'data/partenariat_exclusif_data.xml',
    'data/workflow_data.xml',
    'data/states_data.xml',
    'data/mail_template_data.xml',
    'data/sequence.xml',
    'data/indexes.xml',
    'data/constraints.xml',
    'data/sfec_specifics.xml',
    'data/deployment_procedures.xml',
    'data/import_data.xml',

    # Rapports
    'report/tresorerie_report.xml',
    'report/templates/tresorerie_report_template.xml',
    'report/report_templates.xml',
    'report/report_actions.xml',
    'report/facture_finale_report.xml',
    'report/facture_finale_report_template.xml',
    'report/paiement_client_report.xml',
    'report/paiement_client_report_template.xml',
    'reports/report_facture.py',

    # Tours
    'tours/accounting_tour.py',
],


    'images': [
        'static/description/icon.png'
    ],
}
