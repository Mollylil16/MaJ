from odoo import models, fields, api

class Fournisseur(models.Model):
    _name = 'gestion_comptable_sfec.fournisseur'
    _description = "Fournisseur de l’entreprise"

    name = fields.Char(string="Nom du fournisseur", required=True)
    entreprise = fields.Char(string="Entreprise")
    email = fields.Char(string="Email")
    contact = fields.Char(string="Contact")
    address = fields.Text(string="Adresse")

    # Nouveau champ pour le statut
    status = fields.Selection([
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
    ], string="Statut", default='actif')

    # Statistiques de paiement
    total_paiements = fields.Float(string="Montant total payé", compute="_compute_total_paiements", store=True)
    nombre_paiements = fields.Integer(string="Nombre de paiements", compute="_compute_total_paiements", store=True)

    @api.depends('name')
    def _compute_total_paiements(self):
        for f in self:
            paiements = self.env['gestion_comptable_sfec.paiement_fournisseur'].search([
                ('fournisseur_id', '=', f.id)
            ])
            f.total_paiements = sum(p.montant for p in paiements)
            f.nombre_paiements = len(paiements)
