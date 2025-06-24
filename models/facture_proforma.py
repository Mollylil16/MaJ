from odoo import models, fields, api

class FactureProforma(models.Model):
    _name = 'gestion_comptable_sfec.facture_proforma'
    _description = "Facture Proforma"

    name = fields.Char(string="Référence", required=True, copy=False, readonly=True, default='Nouveau')
    client_id = fields.Many2one('gestion_comptable_sfec.client', string="Client", required=True)
    bon_commande_id = fields.Many2one('gestion_comptable_sfec.bon_commande_client', string="Bon de commande lié")
    date_proforma = fields.Date(string="Date de la facture proforma", default=fields.Date.context_today)
    montant_total = fields.Float(string="Montant total", compute='_compute_montant_total', store=True)
    etat = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('envoyee', 'Envoyée'),
        ('acceptee', 'Acceptée'),
    ], string="État", default='brouillon')
    commentaire = fields.Text(string="Commentaire")

    ligne_facture_ids = fields.One2many(
        'gestion_comptable_sfec.ligne_facture_proforma',
        'facture_id',
        string='Lignes de facture'
    )

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals.get('name') == 'Nouveau':
            vals['name'] = self.env['ir.sequence'].next_by_code('gestion_comptable_sfec.facture_proforma') or 'Nouveau'
        return super().create(vals)

    @api.depends('ligne_facture_ids.quantite', 'ligne_facture_ids.prix_unitaire')
    def _compute_montant_total(self):
        for facture in self:
            total = 0.0
            for ligne in facture.ligne_facture_ids:
                total += ligne.quantite * ligne.prix_unitaire
            facture.montant_total = total
