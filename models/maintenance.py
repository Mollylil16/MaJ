from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import UserError

class Maintenance(models.AbstractModel):
    _name = 'gestion_comptable_sfec.maintenance'
    _description = 'Scripts de maintenance'

    @api.model
    def cleanup_old_commands(self, days=60):
        """Nettoyage des commandes annulées plus vieilles que le nombre de jours spécifié"""
        threshold_date = datetime.now() - timedelta(days=days)
        old_commands = self.env['gestion_comptable_sfec.bon_commande_client'].search([
            ('state', '=', 'cancelled'),
            ('date_commande', '<=', threshold_date)
        ])
        
        if old_commands:
            old_commands.unlink()
            self.env.cr.commit()
            return f"{len(old_commands)} commandes annulées ont été supprimées."
        return "Aucune commande annulée à nettoyer."

    @api.model
    def cleanup_old_invoices(self, days=90):
        """Nettoyage des factures annulées plus vieilles que le nombre de jours spécifié"""
        threshold_date = datetime.now() - timedelta(days=days)
        old_invoices = self.env['gestion_comptable_sfec.facture_finale'].search([
            ('state', '=', 'cancelled'),
            ('date_facture', '<=', threshold_date)
        ])
        
        if old_invoices:
            old_invoices.unlink()
            self.env.cr.commit()
            return f"{len(old_invoices)} factures annulées ont été supprimées."
        return "Aucune facture annulée à nettoyer."

    @api.model
    def cleanup_old_payments(self, days=180):
        """Nettoyage des paiements annulés plus vieux que le nombre de jours spécifié"""
        threshold_date = datetime.now() - timedelta(days=days)
        old_payments = self.env['gestion_comptable_sfec.paiement_client'].search([
            ('state', '=', 'cancelled'),
            ('date_paiement', '<=', threshold_date)
        ])
        
        if old_payments:
            old_payments.unlink()
            self.env.cr.commit()
            return f"{len(old_payments)} paiements annulés ont été supprimés."
        return "Aucun paiement annulé à nettoyer."

    @api.model
    def check_stock_levels(self):
        """Vérification des niveaux de stock et création d'alertes si nécessaire"""
        low_stock_products = self.env['gestion_comptable_sfec.stock_mouvement'].search([
            ('stock_actuel', '<', 10),
            ('derniere_mouvement', '<=', datetime.now() - timedelta(days=30))
        ])
        
        if low_stock_products:
            for product in low_stock_products:
                self.env['mail.message'].create({
                    'model': 'gestion_comptable_sfec.stock_mouvement',
                    'res_id': product.id,
                    'body': f"Alerte : Le stock du produit {product.produit_id.name} est bas (stock actuel: {product.stock_actuel}).",
                    'message_type': 'notification',
                    'subtype_id': self.env.ref('mail.mt_comment').id
                })
            return f"{len(low_stock_products)} alertes de stock ont été générées."
        return "Aucune alerte de stock n'a été générée."

    @api.model
    def optimize_sequences(self):
        """Optimisation des séquences pour éviter les trous"""
        sequences = self.env['ir.sequence'].search([
            ('code', 'like', 'gestion_comptable_sfec%')
        ])
        
        for sequence in sequences:
            sequence.number_next = sequence.number_next_actual + 1
        
        return f"{len(sequences)} séquences ont été optimisées."

    @api.model
    def check_constraints(self):
        """Vérification des contraintes de données"""
        models = ['gestion_comptable_sfec.bon_commande_client',
                 'gestion_comptable_sfec.facture_finale',
                 'gestion_comptable_sfec.paiement_client']
        
        for model in models:
            records = self.env[model].search([])
            for record in records:
                if not record.name:
                    raise UserError(f"Le champ name est vide pour l'enregistrement {record.id} de {model}")
                if not record.date:
                    raise UserError(f"Le champ date est vide pour l'enregistrement {record.id} de {model}")
        
        return "Toutes les contraintes ont été vérifiées avec succès."

    @api.model
    def check_workflows(self):
        """Vérification des workflows"""
        models = ['gestion_comptable_sfec.bon_commande_client',
                 'gestion_comptable_sfec.facture_finale',
                 'gestion_comptable_sfec.paiement_client']
        
        for model in models:
            records = self.env[model].search([])
            for record in records:
                if record.state not in ['draft', 'confirmed', 'approved', 'cancelled']:
                    raise UserError(f"État invalide ({record.state}) pour l'enregistrement {record.id} de {model}")
        
        return "Tous les workflows ont été vérifiés avec succès."

    @api.model
    def check_emails(self):
        """Vérification des emails"""
        models = ['gestion_comptable_sfec.client', 'gestion_comptable_sfec.fournisseur']
        
        for model in models:
            records = self.env[model].search([])
            for record in records:
                if record.email and not record.email.strip():
                    record.email = False
                if record.email and '@' not in record.email:
                    raise UserError(f"Email invalide ({record.email}) pour l'enregistrement {record.id} de {model}")
        
        return "Tous les emails ont été vérifiés avec succès."
