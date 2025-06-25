# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class DashboardController(http.Controller):

    @http.route(['/gestion_comptable_sfec/dashboard'], type='http', auth='user', website=True)
    def dashboard_view(self, **kw):
        # 👉 Exemple de récupération réelle si tu as des modèles :
        # commandes_en_cours = request.env['bon.commande.client'].search_count([('etat', '=', 'en_cours')])
        # stock_critique = request.env['article'].search_count([('quantite', '<', 5)])
        # factures_impayees = request.env['facture.final'].search([('etat', '=', 'impayee')])
        # montant_impaye = sum(factures_impayees.mapped('montant'))
        # partenaires_exclusifs = request.env['partenaire.exclusif'].search_count([])

        # Pour l’instant : données fictives / statiques
        values = {
            'nb_commandes_en_cours': 123,
            'nb_articles_stock_critique': 14,
            'montant_factures_impayees': '3.540.000 FCFA',
            'nb_partenaires_exclusifs': 5,
            'alertes': [
                {
                    'date': '2025-06-25',
                    'type': 'Critique',
                    'description': 'Stock bas pour Article X',
                    'statut': 'Urgent',
                    'badge': 'danger'
                },
                {
                    'date': '2025-06-20',
                    'type': 'Avertissement',
                    'description': 'Client en retard de paiement',
                    'statut': 'À relancer',
                    'badge': 'warning'
                },
            ]
        }

        return request.render('gestion_comptable_sfec.dashboard_template', values)
