from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import csv
import io
import logging

_logger = logging.getLogger(__name__)

class ImportData(models.TransientModel):
    _name = 'gestion_comptable_sfec.import_data'
    _description = 'Import de Données'

    file = fields.Binary(string='Fichier', required=True)
    filename = fields.Char(string='Nom du Fichier')
    import_type = fields.Selection([
        ('csv', 'CSV'),
        ('excel', 'Excel')
    ], string='Type d\'Import', required=True, default='csv')

    def _get_default_import_type(self):
        """Récupère le type d'import par défaut"""
        return self.env.context.get('default_import_type', 'csv')

    def _get_default_model(self):
        """Récupère le modèle cible par défaut"""
        return self.env.context.get('default_model', False)

    def import_data(self):
        """Import des données selon le type de fichier"""
        if not self.file:
            raise ValidationError('Aucun fichier sélectionné')

        try:
            if self.import_type == 'csv':
                self._import_csv()
            elif self.import_type == 'excel':
                self._import_excel()

            # Log l'action dans le système d'audit
            self.env['gestion_comptable_sfec.audit'].log_action(
                'gestion_comptable_sfec.import_data',
                self.id,
                'write',
                f'Import de données {self.import_type}'
            )

            # Retourne une action pour recharger la vue
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

        except Exception as e:
            _logger.error(f"Erreur lors de l'import: {str(e)}")
            raise ValidationError(str(e))

    def _import_csv(self):
        """Import des données CSV"""
        try:
            content = base64.b64decode(self.file)
            input = io.StringIO(content.decode('utf-8'))
            reader = csv.DictReader(input)
            
            for row in reader:
                self._process_row(row)

        except Exception as e:
            _logger.error(f"Erreur lors de l'import CSV: {str(e)}")
            raise ValidationError(f"Erreur lors de l'import CSV: {str(e)}")

    def _import_excel(self):
        """Import des données Excel"""
        raise ValidationError('Import Excel non implémenté')

    def _process_row(self, row):
        """Traitement d'une ligne d'import"""
        try:
            # Récupère le modèle cible
            model = self.env.context.get('default_model')
            if not model:
                raise ValidationError('Modèle non spécifié')

            # Prépare les données pour la création
            values = {}
            for key, value in row.items():
                if value:
                    values[key] = value

            # Création du record
            record = self.env[model].create(values)
            
            # Log la création du record
            self.env['gestion_comptable_sfec.audit'].log_action(
                model,
                record.id,
                'create',
                f'Création via import: {record.display_name}'
            )

        except Exception as e:
            _logger.error(f"Erreur lors du traitement de la ligne: {str(e)}")
            raise ValidationError(f"Erreur lors du traitement de la ligne: {str(e)}")

    def init_model(self):
        """Initialisation du modèle"""
        # Création des groupes d'utilisateurs si nécessaire
        if not self.env.ref('gestion_comptable_sfec.group_import_data', raise_if_not_found=False):
            self.env['res.groups'].create({
                'name': 'Gestionnaire Import',
                'category_id': self.env.ref('base.module_category_accounting').id,
                'implied_ids': [(4, self.env.ref('base.group_user').id)]
            })

        # Création des droits d'accès
        if not self.env.ref('gestion_comptable_sfec.access_import_data', raise_if_not_found=False):
            self.env['ir.model.access'].create({
                'name': 'Import Data Access',
                'model_id': self.env['ir.model'].search([('model', '=', 'gestion_comptable_sfec.import_data')]).id,
                'perm_read': True,
                'perm_write': True,
                'perm_create': True,
                'perm_unlink': True,
                'group_id': self.env.ref('gestion_comptable_sfec.group_import_data').id
            })
