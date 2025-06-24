from odoo import models, fields, api
from datetime import date

class AccuseReception(models.Model):
    _name = 'gestion_comptable_sfec.accuse_reception'
    _description = "Accusé de Réception de la Facture Proforma"

    name = fields.Char(string="Référence", required=True, copy=False, readonly=True, default='New')
    client_id = fields.Many2one('gestion_comptable_sfec.client', string="Client", required=True)
    facture_proforma_id = fields.Many2one('gestion_comptable_sfec.facture_proforma', string="Facture Proforma", required=True)
    date_reception = fields.Date(string="Date de réception", default=fields.Date.today)
    remarques = fields.Text(string="Remarques / Observations")

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('accuse.reception') or 'New'
        return super().create(vals)
