from odoo import models, fields, api

class FactureFinale(models.Model):
    _name = 'gestion_comptable_sfec.facture_finale'
    _description = "Facture Finale"

    name = fields.Char(string="Référence", required=True, copy=False, readonly=True, default='New')
    client_id = fields.Many2one('gestion_comptable_sfec.client', string="Client", required=True)
    date_facture = fields.Date(string="Date de Facturation", default=fields.Date.today)
    montant_total = fields.Float(string="Montant Total", required=True)
    statut = fields.Selection([
        ('en_attente', 'En attente'),
        ('payee', 'Payée'),
        ('partiellement_payee', 'Partiellement payée'),
    ], string="Statut", default='en_attente')
    notes = fields.Text(string="Notes supplémentaires")

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('facture.final') or 'New'
        return super().create(vals)

    def marquer_comme_payee(self):
        for facture in self:
            facture.statut = 'payee'
