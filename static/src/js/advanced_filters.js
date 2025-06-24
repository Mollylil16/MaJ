odoo.define('gestion_comptable_sfec.advanced_filters', function (require) {
    "use strict";

    const ListView = require('web.ListView');
    const core = require('web.core');
    const _t = core._t;

    ListView.include({
        init: function () {
            this._super.apply(this, arguments);
            this.advancedFilters = [];
            this.setupAdvancedFilters();
        },

        setupAdvancedFilters() {
            // Ajout des filtres avancés pour les factures
            this.advancedFilters = [
                {
                    name: 'date_range',
                    label: _t('Période'),
                    type: 'date_range',
                    fields: ['date_facture', 'date_paiement']
                },
                {
                    name: 'amount_range',
                    label: _t('Montant'),
                    type: 'numeric_range',
                    field: 'montant_total'
                },
                {
                    name: 'status',
                    label: _t('Statut'),
                    type: 'selection',
                    field: 'statut',
                    options: [
                        { value: 'en_attente', label: _t('En Attente') },
                        { value: 'valide', label: _t('Validée') },
                        { value: 'payee', label: _t('Payée') }
                    ]
                },
                {
                    name: 'partner',
                    label: _t('Partenaire'),
                    type: 'many2one',
                    field: 'partner_id'
                }
            ];
        },

        on_filters_changed: function (filters) {
            this._super.apply(this, arguments);
            
            // Ajout des filtres avancés
            const advancedFilters = this.advancedFilters.map(filter => {
                const value = filters[filter.name];
                if (value) {
                    return this.createFilterDomain(filter, value);
                }
                return [];
            }).flat();

            this.domain = [...this.domain, ...advancedFilters];
            this.reload();
        },

        createFilterDomain(filter, value) {
            switch (filter.type) {
                case 'date_range':
                    return [
                        ['date_facture', '>=', value.start],
                        ['date_facture', '<=', value.end]
                    ];
                case 'numeric_range':
                    return [
                        [filter.field, '>=', value.min],
                        [filter.field, '<=', value.max]
                    ];
                case 'selection':
                    return [[filter.field, '=', value]];
                case 'many2one':
                    return [[filter.field, 'in', value]];
                default:
                    return [];
            }
        },

        // Ajout des actions d'export
        do_export_data: function (format) {
            const self = this;
            const fields = this.fields;
            const records = this.data.records;

            const data = records.map(record => {
                return Object.keys(fields).reduce((obj, field) => {
                    obj[field] = record[field];
                    return obj;
                }, {});
            });

            switch (format) {
                case 'csv':
                    this.exportCSV(data);
                    break;
                case 'excel':
                    this.exportExcel(data);
                    break;
            }
        },

        exportCSV: function (data) {
            const headers = Object.keys(data[0]);
            const csvContent = [
                headers.join(','),
                ...data.map(record => headers.map(h => record[h]).join(','))
            ].join('\n');

            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'factures.csv';
            a.click();
            window.URL.revokeObjectURL(url);
        },

        exportExcel: function (data) {
            // À implémenter avec une bibliothèque comme xlsx
            // Pour le moment, on simule l'export
            this.showSuccessMessage(_t('Export Excel en cours...'));
        },

        showSuccessMessage: function (message) {
            const notification = new core.Notification(this, {
                title: _t('Succès'),
                message: message,
                type: 'success',
                sticky: false
            });
            notification.open();
        }
    });

    return ListView;
});
