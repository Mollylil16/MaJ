from odoo import models, fields, api

class Fournisseur(models.Model):
    _name = 'gestion_comptable_sfec.fournisseur'
    _description = "Fournisseur de l’entreprise"

    name = fields.Char(string="Nom du fournisseur", required=True)
    entreprise = fields.Char(string="Entreprise")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Téléphone")
    address = fields.Text(string="Adresse")

    # Statistiques de paiement
    total_paiements = fields.Float(string="Montant total payé", compute="_compute_total_paiements", store=True)
    nombre_paiements = fields.Integer(string="Nombre de paiements", compute="_compute_total_paiements", store=True)

    @api.depends('name')  # tu peux aussi mettre 'email' ou 'entreprise'
    def _compute_total_paiements(self):
        for f in self:
            paiements = self.env['gestion_comptable_sfec.paiement_fournisseur'].search([
                ('fournisseur_id', '=', f.id)
            ])
            f.total_paiements = sum(p.montant for p in paiements)
            f.nombre_paiements = len(paiements)
