from odoo import models, fields
from datetime import date

class PaiementFournisseur(models.Model):
    _name = 'gestion_comptable_sfec.paiement_fournisseur'
    _description = "Paiement Fournisseur"

    facture_id = fields.Many2one('gestion_comptable_sfec.facture_fournisseur', string="Facture", required=True)
    fournisseur_id = fields.Many2one('gestion_comptable_sfec.fournisseur', string="Fournisseur", required=True)  # <-- ajouté
    date_paiement = fields.Date(string="Date du paiement", default=date.today)
    montant_paye = fields.Float(string="Montant payé", required=True)
    mode_paiement = fields.Selection([
        ('caisse', 'Caisse'),
        ('banque', 'Banque'),
        ('credit', 'Crédit'),
    ], string="Mode de paiement", default='caisse')
    reference = fields.Char(string="Référence du paiement")
