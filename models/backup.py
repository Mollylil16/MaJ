from odoo import models, fields, api
from datetime import datetime, timedelta
import os
import shutil

class Backup(models.Model):
    _name = 'gestion_comptable_sfec.backup'
    _description = 'Gestion des Sauvegardes'

    name = fields.Char(string="Nom", required=True)
    date = fields.Datetime(string="Date de création", default=fields.Datetime.now)
    type = fields.Selection([
        ('daily', 'Quotidienne'),
        ('weekly', 'Hebdomadaire'),
        ('monthly', 'Mensuelle')
    ], string="Type", default='daily', required=True)
    file_path = fields.Char(string="Chemin du fichier")
    size = fields.Float(string="Taille (MB)")
    state = fields.Selection([
        ('pending', 'En attente'),
        ('done', 'Terminée'),
        ('failed', 'Échouée')
    ], string="État", default='pending')
    error_message = fields.Text(string="Message d'erreur")

    @api.model
    def create_backup(self, backup_type):
        """Création d'une sauvegarde automatique"""
        try:
            # Création du nom du fichier
            backup_name = f"backup_{backup_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            backup_path = os.path.join('/var/odoo/backups', backup_name)

            # Création de la sauvegarde
            self.env.cr.execute("""
                SELECT pg_start_backup('daily_backup', true);
            """)
            
            # Copie des fichiers
            shutil.copytree('/var/odoo/filestore', os.path.join('/var/odoo/backups', 'filestore'))
            
            self.env.cr.execute("""
                SELECT pg_stop_backup();
            """)

            # Compression
            shutil.make_archive(backup_path, 'zip', '/var/odoo/backups')

            # Création de l'enregistrement
            backup = self.create({
                'name': backup_name,
                'type': backup_type,
                'file_path': backup_path,
                'size': os.path.getsize(backup_path) / (1024 * 1024),
                'state': 'done'
            })

            return backup

        except Exception as e:
            self.create({
                'name': backup_name,
                'type': backup_type,
                'state': 'failed',
                'error_message': str(e)
            })
            raise e

    def cleanup_old_backups(self, days=30):
        """Suppression des sauvegardes anciennes"""
        threshold_date = datetime.now() - timedelta(days=days)
        old_backups = self.search([
            ('date', '<=', threshold_date),
            ('state', '=', 'done')
        ])
        
        for backup in old_backups:
            if os.path.exists(backup.file_path):
                os.remove(backup.file_path)
            backup.unlink()

    def get_latest_backup(self):
        """Récupération de la dernière sauvegarde"""
        return self.search([
            ('state', '=', 'done')
        ], order='date desc', limit=1)
