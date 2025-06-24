from odoo import models, fields, api

class CustomClient(models.Model):
    _name = 'gestion_comptable_sfec.client'
    _description = 'Client de l’entreprise'

    name = fields.Char(string="Nom complet", required=True)
    lcc_number = fields.Char(string="Numéro LCC")
    contact = fields.Char(string="Contact")
    email = fields.Char(string="Email")
    address = fields.Text(string="Adresse")
    company_name = fields.Char(string="Entreprise liée")
    entreprise_id = fields.Many2one('gestion_comptable_sfec.entreprise', string="Entreprise liée")

    # 👉 Champs inspirés de res.partner
    parent_id = fields.Many2one('gestion_comptable_sfec.client', string="Client parent")
    street = fields.Char(string="Rue")

    # Statistiques de paiement
    total_paiements = fields.Float(string="Montant total payé", compute="_compute_total_paiements", store=True)
    nombre_paiements = fields.Integer(string="Nombre de paiements", compute="_compute_total_paiements", store=True)

    @api.depends('entreprise_id')
    def _compute_total_paiements(self):
        for client in self:
            paiements = self.env['gestion_comptable_sfec.paiement_client'].search([
                ('client_id', '=', client.id)
            ])
            client.total_paiements = sum(p.montant for p in paiements)
            client.nombre_paiements = len(paiements)
