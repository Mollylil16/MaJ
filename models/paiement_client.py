from odoo import models, fields

class PaiementClient(models.Model):
    _name = 'gestion_comptable_sfec.paiement_client'
    _description = "Paiement Client"

    client_id = fields.Many2one('gestion_comptable_sfec.client', string="Client", required=True)
    facture_id = fields.Many2one('gestion_comptable_sfec.facture_finale', string="Facture Associée", required=True)
    date_paiement = fields.Date(string="Date de Paiement", default=fields.Date.today)
    montant = fields.Float(string="Montant Payé", required=True)
    mode_paiement = fields.Selection([
        ('espece', 'Espèces'),
        ('virement', 'Virement bancaire'),
        ('carte', 'Carte bancaire'),
        ('mobile_money', 'Mobile Money'),
        ('cheque', 'Chèque'),
        ('autre', 'Autre'),
    ], string="Mode de Paiement", required=True)
    reference = fields.Char(string="Référence / Justificatif")
