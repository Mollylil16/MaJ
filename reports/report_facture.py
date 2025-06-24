from odoo import api, models,fields
from odoo.tools import date_utils
import logging

_logger = logging.getLogger(__name__)

class ReportFacture(models.AbstractModel):
    _name = 'report.gestion_comptable_sfec.report_facture'
    _description = 'Rapport de Factures'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['gestion_comptable_sfec.facture_finale'].browse(docids)
        
        # Calcul des statistiques
        total_factures = len(docs)
        montant_total = sum(doc.montant_total for doc in docs)
        moyenne_factures = montant_total / total_factures if total_factures else 0
        
        # Groupe par statut
        factures_par_statut = {}
        for doc in docs:
            factures_par_statut[doc.statut] = factures_par_statut.get(doc.statut, 0) + 1
        
        # Préparation des données pour le graphique
        graph_data = {
            'labels': list(factures_par_statut.keys()),
            'values': list(factures_par_statut.values())
        }
        
        return {
            'doc_ids': docids,
            'doc_model': 'gestion_comptable_sfec.facture_finale',
            'docs': docs,
            'total_factures': total_factures,
            'montant_total': montant_total,
            'moyenne_factures': moyenne_factures,
            'graph_data': graph_data,
            'date_generation': fields.Date.today()
        }

class ReportPartenariat(models.AbstractModel):
    _name = 'report.gestion_comptable_sfec.report_partenariat'
    _description = 'Rapport de Partenariats'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['gestion_comptable_sfec.partenariat'].browse(docids)
        
        # Statistiques par type de partenariat
        stats = {
            'spirax': 0,
            'aprotech': 0,
            'total': 0
        }
        
        for doc in docs:
            stats['total'] += 1
            if doc.type_partenariat == 'spirax':
                stats['spirax'] += 1
            else:
                stats['aprotech'] += 1
        
        return {
            'doc_ids': docids,
            'doc_model': 'gestion_comptable_sfec.partenariat',
            'docs': docs,
            'stats': stats,
            'date_generation': fields.Date.today()
        }
