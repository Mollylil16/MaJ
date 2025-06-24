from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class PartenariatExclusif(models.Model):
    _name = 'gestion_comptable_sfec.partenariat_exclusif'
    _description = 'Partenariat Exclusif'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nom du Partenariat', required=True)
    fournisseur_id = fields.Many2one('gestion_comptable_sfec.fournisseur', string='Fournisseur', required=True)
    date_debut = fields.Date(string='Date de Début', required=True)
    date_fin = fields.Date(string='Date de Fin')
    active = fields.Boolean(string='Actif', default=True)
    conditions = fields.Text(string='Conditions Particulières')
    type_partenariat = fields.Selection([
        ('spirax', 'SPIRAX SARCO'),
        ('approtech', 'APPROTECH')
    ], string='Type de Partenariat', required=True)
    
    # Statistiques
    nb_commandes = fields.Integer(string='Nombre de Commandes', compute='_compute_stats')
    montant_total = fields.Float(string='Montant Total', compute='_compute_stats')
    
    @api.model
    def create(self, vals):
        # Vérifier si le fournisseur est déjà partenaire exclusif
        existing = self.env['gestion_comptable_sfec.partenariat_exclusif'].search([
            ('fournisseur_id', '=', vals['fournisseur_id']),
            ('active', '=', True)
        ])
        if existing:
            raise models.ValidationError('Ce fournisseur est déjà partenaire exclusif')
            
        res = super(PartenariatExclusif, self).create(vals)
        
        # Créer un groupe de notification
        channel = self.env['mail.channel'].create({
            'name': f'Notifications {res.name}',
            'channel_type': 'group',
            'public': 'private',
            'email_send': True
        })
        
        # Créer une activité de suivi
        self.env['mail.activity'].create({
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
            'summary': 'Suivi Partenariat Exclusif',
            'note': f'Nouveau partenariat exclusif avec {res.fournisseur_id.name}',
            'date_deadline': datetime.now() + relativedelta(days=7),
            'user_id': self.env.user.id,
            'res_id': res.id,
            'res_model_id': self.env['ir.model'].search([('model', '=', 'gestion_comptable_sfec.partenariat_exclusif')]).id
        })
        
        return res

    def write(self, vals):
        if 'active' in vals and not vals['active']:
            # Envoyer une notification quand le partenariat n'est plus actif
            self.env['mail.thread'].message_post(
                body=f'Le partenariat exclusif avec {self.fournisseur_id.name} a été désactivé',
                subject='Statut Partenariat Exclusif',
                subtype_xmlid='mail.mt_comment'
            )
            
            # Créer une activité de suivi
            self.env['mail.activity'].create({
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'summary': 'Partenariat Inactif',
                'note': f'Partenariat avec {self.fournisseur_id.name} désactivé',
                'date_deadline': datetime.now() + relativedelta(days=7),
                'user_id': self.env.user.id,
                'res_id': self.id,
                'res_model_id': self.env['ir.model'].search([('model', '=', 'gestion_comptable_sfec.partenariat_exclusif')]).id
            })
        
        return super(PartenariatExclusif, self).write(vals)

    def _compute_stats(self):
        for rec in self:
            commandes = self.env['gestion_comptable_sfec.bon_commande_fournisseur'].search([
                ('fournisseur_id', '=', rec.fournisseur_id.id),
                ('date_commande', '>=', rec.date_debut),
                ('date_commande', '<=', rec.date_fin)
            ])
            rec.nb_commandes = len(commandes)
            rec.montant_total = sum(commandes.mapped('montant_total'))

    @api.constrains('date_debut', 'date_fin')
    def _check_dates(self):
        for rec in self:
            if rec.date_fin and rec.date_fin < rec.date_debut:
                raise models.ValidationError('La date de fin ne peut pas être antérieure à la date de début')
            
            # Vérifier les chevauchements
            overlaps = self.env['gestion_comptable_sfec.partenariat_exclusif'].search([
                ('fournisseur_id', '=', rec.fournisseur_id.id),
                ('id', '!=', rec.id),
                ('active', '=', True),
                '|',
                '&', ('date_debut', '<=', rec.date_fin), ('date_fin', '>=', rec.date_fin),
                '&', ('date_debut', '<=', rec.date_debut), ('date_fin', '>=', rec.date_debut)
            ])
            if overlaps:
                raise models.ValidationError('Ce partenariat chevauche un autre partenariat actif')

    def action_valider_commande(self, commande_id):
        """Valider automatiquement les commandes des partenaires exclusifs"""
        commande = self.env['gestion_comptable_sfec.bon_commande_fournisseur'].browse(commande_id)
        if commande.fournisseur_id.id == self.fournisseur_id.id:
            commande.write({'state': 'validate'})
            # Envoyer une notification
            self.env['mail.thread'].message_post(
                body=f'Commande {commande.name} automatiquement validée pour le partenaire exclusif {self.fournisseur_id.name}',
                subject='Validation Commande Partenaire Exclusif',
                subtype_xmlid='mail.mt_comment'
            )
            return True
        return False
