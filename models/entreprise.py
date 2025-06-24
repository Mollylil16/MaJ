from odoo import models, fields

class Entreprise(models.Model):
    _name = 'gestion_comptable_sfec.entreprise'
    _description = "Entreprise des clients"

    name = fields.Char(string="Nom de l'entreprise", required=True)
    adresse = fields.Char(string="Adresse")
    contact = fields.Char(string="Contact")
    email = fields.Char(string="Email")
    clients_ids = fields.One2many('gestion_comptable_sfec.client', 'entreprise_id', string="Clients associés")
