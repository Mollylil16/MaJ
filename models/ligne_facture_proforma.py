from odoo import models, fields, api

class LigneFactureProforma(models.Model):
    _name = 'gestion_comptable_sfec.ligne_facture_proforma'
    _description = 'Ligne de facture proforma'

    facture_id = fields.Many2one('gestion_comptable_sfec.facture_proforma', string="Facture")
    article_id = fields.Many2one('gestion_comptable_sfec.article', string="Article", required=True)
    quantite = fields.Float(string="Quantité", required=True)
    prix_unitaire = fields.Float(string="Prix unitaire", required=True)
    total = fields.Float(string="Total", compute='_compute_total', store=True)

    @api.depends('quantite', 'prix_unitaire')
    def _compute_total(self):
        for ligne in self:
            ligne.total = ligne.quantite * ligne.prix_unitaire
