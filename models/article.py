from odoo import models, fields

class Article(models.Model):
    _name = 'gestion_comptable_sfec.article'
    _description = "Article / Produit en stock"

    name = fields.Char(string="Nom de l'article", required=True)
    reference = fields.Char(string="Référence", required=True)
    description = fields.Text(string="Description")
    quantite_stock = fields.Float(string="Quantité en stock", default=0.0)
    unite = fields.Selection([
        ('u', 'Unité'),
        ('kg', 'Kilogramme'),
        ('l', 'Litre'),
    ], string="Unité", default='u')
    prix_achat = fields.Float(string="Prix d'achat")
    prix_vente = fields.Float(string="Prix de vente")
    disponible = fields.Boolean(string="Disponible ?", default=True)
