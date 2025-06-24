from odoo import models, fields, api

class FactureFinale(models.Model):
    _name = 'gestion_comptable_sfec.facture_finale'
    _description = "Facture Finale"

    name = fields.Char(string="Référence", required=True, copy=False, readonly=True, default='New')
    client_id = fields.Many2one('gestion_comptable_sfec.client', string="Client", required=True)
    date_facture = fields.Date(string="Date de Facturation", default=fields.Date.today)
    date_echeance = fields.Date(string="Date d'Échéance")
    montant_total = fields.Float(string="Montant Total", required=True)
    statut = fields.Selection([
    ('brouillon', 'Brouillon'),
    ('en_attente', 'En attente'),
    ('payee', 'Payée'),
    ('partiellement_payee', 'Partiellement payée'),
   ], string="Statut", default='brouillon')
    notes = fields.Text(string="Notes supplémentaires")

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('facture.final') or 'New'
        return super().create(vals)

    def marquer_comme_payee(self):
        for facture in self:
            facture.statut = 'payee'

    def action_valider(self):
      for facture in self:
        facture.statut = 'en_attente'  # Nouveau statut après validation
        # Message automatique dans le fil de discussion
        facture.message_post(
            body="La facture a été validée avec succès.",
            subtype_xmlid="mail.mt_note"
        )
        # Appel d'une méthode d'impression automatique (fictive ici)
        return {
            'type': 'ir.actions.report',
            'report_name': 'gestion_comptable_sfec.report_facture_finale',
            'report_type': 'qweb-pdf',
            'res_id': facture.id,
            'res_model': 'gestion_comptable_sfec.facture_finale',
        }  # ou 'valide' si tu ajoutes cet état
    def action_imprimer(self):
       self.ensure_one()
       return self.env.ref('gestion_comptable_sfec.report_facture_finale').report_action(self)
      
