from odoo import models, fields

class LigneCommandeClient(models.Model):
    _name = 'gestion_comptable_sfec.ligne_commande_client'
    _description = 'Ligne de commande client'

    commande_id = fields.Many2one('gestion_comptable_sfec.bon_commande_client', string="Bon de commande")
    article_id = fields.Many2one('gestion_comptable_sfec.article', string="Article", required=True)
    quantite = fields.Float(string="Quantité", required=True)
    prix_unitaire = fields.Float(string="Prix unitaire", required=True)
