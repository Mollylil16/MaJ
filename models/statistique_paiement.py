from odoo import models, fields, api
from datetime import date, timedelta

class StatistiquePaiement(models.TransientModel):
    _name = 'gestion_comptable_sfec.statistique_paiement'
    _description = "Rapport statistique des paiements"

    total_recu = fields.Float(string="Total Reçu", compute='_compute_stats')
    total_a_recevoir = fields.Float(string="Total à Recevoir", compute='_compute_stats')
    top_clients = fields.Text(string="Top Clients", compute='_compute_stats')

    @api.depends('total_recu', 'total_a_recevoir')
    def _compute_stats(self):
        for record in self:
            factures = self.env['gestion_comptable_sfec.facture_finale'].search([])
            total_recu = sum(f.montant_total for f in factures if f.statut == 'payee')
            total_a_recevoir = sum(f.montant_total for f in factures if f.statut in ['en_attente', 'partiellement_payee'])

            # Stats top clients
            client_map = {}
            for f in factures:
                if f.statut == 'payee':
                    nom_client = f.client_id.name
                    client_map[nom_client] = client_map.get(nom_client, 0) + f.montant_total
            top = sorted(client_map.items(), key=lambda x: x[1], reverse=True)[:5]

            record.total_recu = total_recu
            record.total_a_recevoir = total_a_recevoir
            record.top_clients = "\n".join([f"{nom}: {montant:.2f} FCFA" for nom, montant in top])
