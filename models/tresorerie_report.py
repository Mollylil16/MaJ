from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta

class TresorerieReport(models.TransientModel):
    _name = 'gestion_comptable_sfec.tresorerie.report'
    _description = 'Rapport de Trésorerie'

    date_debut = fields.Date(string="Date de début", required=True,
                            default=lambda self: fields.Date.to_string(datetime.now().replace(day=1)))
    date_fin = fields.Date(string="Date de fin", required=True,
                         default=lambda self: fields.Date.to_string(datetime.now()))
    company_id = fields.Many2one('res.company', string="Société", required=True,
                               default=lambda self: self.env.company)

    def get_tresorerie_data(self):
        data = {
            'date_debut': self.date_debut,
            'date_fin': self.date_fin,
            'company_id': self.company_id.id,
        }
        return data

    def print_report(self):
        data = self.get_tresorerie_data()
        return self.env.ref('gestion_comptable_sfec.tresorerie_report_template').report_action(self, data=data)
