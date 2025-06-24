# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.addons.web_tour.tour import Tour

class AccountingTour(Tour):
    _name = "accounting.tour"

    def start_invoice_process(self):
        return self.sequence(
            self.step("Bienvenue",
                     ".o_main_navbar",
                     "Bienvenue dans le module comptable SFEC. Ce guide vous accompagnera dans la création d'une facture."),
            self.step("Nouvelle facture",
                     "button[action='create_invoice']",
                     "Cliquez ici pour commencer une nouvelle facture"),
            self.step("Sélection client",
                     "div[name='partner_id'] input",
                     "Recherchez et sélectionnez le client")
        )

    def start_export_process(self):
        return self.sequence(
            self.step("Export des données",
                     "button[action='export_xlsx']",
                     "Cliquez ici pour exporter les données en Excel")
        )

    def start_advanced_features(self):
        return self.sequence(
            self.step("Filtres avancés", "button[data-key='advanced_search']", "Utilisez ces filtres pour des recherches complexes"),
            self.step("Tags personnalisés", ".custom_tags_container", "Créez des tags pour organiser vos documents"),
            self.step("Glisser-déposer", ".o_kanban_record", "Glissez les éléments pour les réorganiser")
        )

    def start_reporting(self):
        return self.sequence(
            self.step("Génération rapport", "button[action='generate_report']", "Générez un rapport personnalisé"),
            self.step("Export Excel", "button[action='export_xlsx']", "Exportez les données vers Excel"),
            self.step("Paramètres avancés", "a[data-toggle='export_settings']", "Configurez les options d'export")
        )

    def start_custom_widgets(self):
        return self.sequence(
            self.step("Sélecteur couleur", ".color-picker-widget", "Personnalisez les couleurs des éléments"),
            self.step("Graphiques", ".o_graph_renderer", "Interagissez avec les graphiques dynamiques")
        )
