from odoo import models, fields, api
from datetime import date

class ReceptionFournisseur(models.Model):
    _name = 'gestion_comptable_sfec.reception_fournisseur'
    _description = "Réception de commande fournisseur"

    bon_commande_id = fields.Many2one('gestion_comptable_sfec.bon_commande_fournisseur', string="Bon de commande", required=True)
    date_reception = fields.Date(string="Date de réception", default=date.today)
    notes = fields.Text(string="Remarques")
    reception_ligne_ids = fields.One2many('gestion_comptable_sfec.ligne_reception_fournisseur', 'reception_id', string="Articles réceptionnés")

    @api.model
    def create(self, vals):
        reception = super().create(vals)
        # Mise à jour du stock à la réception
        for ligne in reception.reception_ligne_ids:
            if ligne.article_id:
                ligne.article_id.quantite_stock += ligne.quantite_recue
        return reception
