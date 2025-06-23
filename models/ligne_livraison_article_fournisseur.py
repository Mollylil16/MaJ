from odoo import models, fields, api

class LigneLivraisonArticleFournisseur(models.Model):
    _name = 'custom.accounting.livraison_article_fournisseur'
    _description = "Lignes de livraison fournisseur"

    article_id = fields.Many2one('custom.accounting.article', string="Article", required=True)
    quantite_livree = fields.Float(string="Quantité livrée", required=True)
    bon_commande_id = fields.Many2one('custom.accounting.bon_commande_fournisseur', string="Bon de commande lié")

    @api.model
    def create(self, vals):
        record = super().create(vals)
        # Mettre à jour le stock de l'article livré
        if record.article_id and record.quantite_livree:
            record.article_id.quantite_stock += record.quantite_livree
        return record
