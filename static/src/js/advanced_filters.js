/** @odoo-module **/

import { ListView } from "@web/views/list/list_view";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n";
import { useService } from "@web/core/utils/hooks";

export class AdvancedFilterListView extends ListView {
    setup() {
        super.setup();
        this.notification = useService("notification");
        this.advancedFilters = this._setupAdvancedFilters();
    }

    _setupAdvancedFilters() {
        return [
            {
                name: "date_range",
                label: _t("Période"),
                type: "date_range",
                fields: ["date_facture", "date_paiement"]
            },
            {
                name: "amount_range",
                label: _t("Montant"),
                type: "numeric_range",
                field: "montant_total"
            },
            {
                name: "status",
                label: _t("Statut"),
                type: "selection",
                field: "statut",
                options: [
                    { value: "en_attente", label: _t("En Attente") },
                    { value: "valide", label: _t("Validée") },
                    { value: "payee", label: _t("Payée") }
                ]
            },
            {
                name: "partner",
                label: _t("Partenaire"),
                type: "many2one",
                field: "partner_id"
            }
        ];
    }

    onFiltersChanged(filters) {
        super.onFiltersChanged?.(filters);
        const domains = [];

        for (const filter of this.advancedFilters) {
            const value = filters[filter.name];
            if (value) {
                domains.push(...this._createFilterDomain(filter, value));
            }
        }

        this.model.load({ domain: [...this.model.domain, ...domains] });
    }

    _createFilterDomain(filter, value) {
        switch (filter.type) {
            case "date_range":
                return [
                    [filter.fields[0], ">=", value.start],
                    [filter.fields[0], "<=", value.end]
                ];
            case "numeric_range":
                return [
                    [filter.field, ">=", value.min],
                    [filter.field, "<=", value.max]
                ];
            case "selection":
                return [[filter.field, "=", value]];
            case "many2one":
                return [[filter.field, "in", value]];
            default:
                return [];
        }
    }

    doExportData(format) {
        const fields = this.model.config.fields;
        const records = this.model.root.records;

        const data = records.map((record) => {
            return Object.keys(fields).reduce((obj, key) => {
                obj[key] = record.data[key];
                return obj;
            }, {});
        });

        if (format === "csv") this._exportCSV(data);
        else if (format === "excel") this._exportExcel(data);
    }

    _exportCSV(data) {
        const headers = Object.keys(data[0]);
        const csvContent = [
            headers.join(","),
            ...data.map((record) => headers.map((h) => record[h]).join(","))
        ].join("\n");

        const blob = new Blob([csvContent], { type: "text/csv" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "factures.csv";
        a.click();
        URL.revokeObjectURL(url);
    }

    _exportExcel(data) {
        this.notification.add(_t("Export Excel en cours..."), { type: "success" });
        // Tu peux intégrer xlsx ici
    }
}

// Enregistrement de ta vue
registry.category("views").add("advanced_list", {
    ...ListView,
    Component: AdvancedFilterListView,
});
