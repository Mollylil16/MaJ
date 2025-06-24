from odoo import models, fields, api

class StockMouvement(models.Model):
    _name = 'gestion_comptable_sfec.stock_mouvement'
    _description = 'Mouvements de stock (entrées et sorties)'

    article_id = fields.Many2one('gestion_comptable_sfec.article', string="Article", required=True)
    date_mouvement = fields.Datetime(string="Date du mouvement", default=fields.Datetime.now)
    type_mouvement = fields.Selection([
        ('entree', 'Entrée en stock'),
        ('sortie', 'Sortie de stock')
    ], string="Type", required=True)
    quantite = fields.Float(string="Quantité", required=True)
    note = fields.Text(string="Note complémentaire")

    @api.model
    def create(self, vals):
        article = self.env['gestion_comptable_sfec.article'].browse(vals['article_id'])
        if vals['type_mouvement'] == 'entree':
            article.quantite_stock += vals['quantite']
        elif vals['type_mouvement'] == 'sortie':
            article.quantite_stock -= vals['quantite']
        article.sudo().write({'disponible': article.quantite_stock > 0})
        return super(StockMouvement, self).create(vals)
