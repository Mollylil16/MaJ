# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class DashboardController(http.Controller):

    @http.route(['/gestion_comptable_sfec/dashboard'], type='http', auth='user', website=True)
    def dashboard_view(self, **kw):
        # Tu peux ici calculer ou récupérer dynamiquement les données du dashboard si nécessaire
        values = {
            'nb_commandes_en_cours': 123,
            'nb_articles_stock_critique': 14,
            'montant_factures_impayees': '3.540.000 FCFA',
            'nb_partenaires_exclusifs': 5,
            # Ajouter d'autres valeurs ici si besoin
        }
        return request.render('gestion_comptable_sfec.dashboard_template', values)
