from odoo import models, fields,api

class LigneFactureFournisseur(models.Model):
    _name = 'gestion_comptable_sfec.ligne_facture_fournisseur'
    _description = "Ligne de facture fournisseur"

    facture_id = fields.Many2one('gestion_comptable_sfec.facture_fournisseur', string="Facture")
    article_id = fields.Many2one('gestion_comptable_sfec.article', string="Article", required=True)
    quantite = fields.Float(string="Quantité", required=True)
    prix_unitaire = fields.Float(string="Prix unitaire", required=True)
    montant_total = fields.Float(string="Total", compute="_compute_total", store=True)

    @api.depends('quantite', 'prix_unitaire')
    def _compute_total(self):
        for rec in self:
            rec.montant_total = rec.quantite * rec.prix_unitaire
