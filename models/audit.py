from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class AuditLog(models.Model):
    _name = 'gestion_comptable_sfec.audit'
    _description = 'Journal d\'audit des actions'
    _order = 'create_date desc'

    name = fields.Char('Description', required=True)
    user_id = fields.Many2one('res.users', 'Utilisateur', required=True)
    model = fields.Char('Modèle', required=True)
    record_id = fields.Integer('ID du Record')
    action_type = fields.Selection([
        ('create', 'Création'),
        ('write', 'Modification'),
        ('unlink', 'Suppression')
    ], string='Type d\'Action', required=True)
    date_action = fields.Datetime('Date de l\'Action', default=fields.Datetime.now)
    details = fields.Text('Détails')

    @api.model
    def log_action(self, model_name, record_id, action_type, description, details=None):
        # Ne pas logger si déjà en contexte "no_audit"
        if self.env.context.get('no_audit_logging'):
            return

        # Ne pas logger les écritures sur le modèle d'audit lui-même
        if model_name == 'gestion_comptable_sfec.audit':
            return

        self.with_context(no_audit_logging=True).create({
            'name': description,
            'user_id': self.env.user.id,
            'model': model_name,
            'record_id': record_id,
            'action_type': action_type,
            'details': details
        })
        _logger.info(f"AUDIT - {action_type}: {description}")


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def create(self, vals):
        record = super().create(vals)
        self.env['gestion_comptable_sfec.audit'].with_context(no_audit_logging=True).log_action(
            self._name,
            record.id,
            'create',
            f'Création de {self._name}'
        )
        return record

    def write(self, vals):
        result = super().write(vals)
        for rec in self:
            rec.env['gestion_comptable_sfec.audit'].with_context(no_audit_logging=True).log_action(
                rec._name,
                rec.id,
                'write',
                f'Modification de {rec._name}'
            )
        return result

    def unlink(self):
        for rec in self:
            rec.env['gestion_comptable_sfec.audit'].with_context(no_audit_logging=True).log_action(
                rec._name,
                rec.id,
                'unlink',
                f'Suppression de {rec._name}'
            )
        return super().unlink()
