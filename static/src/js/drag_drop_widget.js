/** @odoo-module **/

import { Widget } from "@web/core/widget";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class DragDropWidget extends Widget {
    setup() {
        super.setup();
        this.notification = useService("notification");
        this.setupDragDrop();
    }

    setupDragDrop() {
        const dropZone = this.el.querySelector(".drop-zone");

        if (!dropZone) return;

        dropZone.addEventListener("dragover", (e) => {
            e.preventDefault();
            dropZone.classList.add("dragover");
        });

        dropZone.addEventListener("dragleave", () => {
            dropZone.classList.remove("dragover");
        });

        dropZone.addEventListener("drop", (e) => {
            e.preventDefault();
            dropZone.classList.remove("dragover");

            const files = e.dataTransfer.files;
            this.handleFiles(files);
        });
    }

    handleFiles(files) {
        const promises = Array.from(files).map((file) => {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const content = e.target.result;
                    this.processFile(file, content);
                    resolve();
                };
                reader.onerror = reject;
                reader.readAsText(file);
            });
        });

        Promise.all(promises)
            .then(() => this.showSuccessMessage("Fichiers importés avec succès"))
            .catch(() => this.showErrorMessage("Erreur lors de l'import"));
    }

    processFile(file, content) {
        if (file.name.endsWith(".csv")) {
            this.processCSV(content);
        } else if (file.name.endsWith(".xlsx")) {
            this.processExcel(content);
        }
    }

    processCSV(content) {
        const lines = content.trim().split("\n");
        const headers = lines[0].split(",");
        const records = lines.slice(1).map((line) => {
            const values = line.split(",");
            return headers.reduce((obj, header, index) => {
                obj[header] = values[index];
                return obj;
            }, {});
        });
        this.saveRecords(records);
    }

    processExcel(content) {
        // Tu peux importer xlsx ici plus tard si nécessaire
        this.showSuccessMessage("Traitement Excel en cours...");
    }

    saveRecords(records) {
        this.trigger("save_records", { records });
    }

    showSuccessMessage(message) {
        this.notification.add(message, { type: "success" });
    }

    showErrorMessage(message) {
        this.notification.add(message, { type: "danger" });
    }
}

// Optionnel : enregistrement de l'action
registry.category("actions").add("drag_drop_widget", DragDropWidget);
