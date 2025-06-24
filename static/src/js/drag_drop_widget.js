odoo.define('gestion_comptable_sfec.drag_drop_widget', function (require) {
    "use strict";

    const Widget = require('web.Widget');
    const core = require('web.core');
    const _t = core._t;

    class DragDropWidget extends Widget {
        constructor(parent, options) {
            super(parent, options);
            this.setupDragDrop();
        }

        setupDragDrop() {
            const dropZone = this.el.querySelector('.drop-zone');
            
            dropZone.addEventListener('dragover', (e) => {
                e.preventDefault();
                dropZone.classList.add('dragover');
            });

            dropZone.addEventListener('dragleave', () => {
                dropZone.classList.remove('dragover');
            });

            dropZone.addEventListener('drop', (e) => {
                e.preventDefault();
                dropZone.classList.remove('dragover');
                
                const files = e.dataTransfer.files;
                this.handleFiles(files);
            });
        }

        handleFiles(files) {
            const promises = Array.from(files).map(file => {
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
                .then(() => {
                    this.showSuccessMessage(_t('Fichiers importés avec succès'));
                })
                .catch(() => {
                    this.showErrorMessage(_t('Erreur lors de l\'import'));
                });
        }

        processFile(file, content) {
            // Traitement spécifique selon le type de fichier
            if (file.name.endsWith('.csv')) {
                this.processCSV(content);
            } else if (file.name.endsWith('.xlsx')) {
                this.processExcel(content);
            }
        }

        processCSV(content) {
            const lines = content.split('\n');
            const headers = lines[0].split(',');
            const records = lines.slice(1).map(line => {
                const values = line.split(',');
                return headers.reduce((obj, header, index) => {
                    obj[header] = values[index];
                    return obj;
                }, {});
            });
            this.saveRecords(records);
        }

        processExcel(content) {
            // À implémenter avec une bibliothèque comme xlsx
            // Pour le moment, on simule le traitement
            this.showSuccessMessage(_t('Traitement Excel en cours...'));
        }

        saveRecords(records) {
            this.trigger_up('save_records', { records });
        }

        showSuccessMessage(message) {
            const notification = new core.Notification(this, {
                title: _t('Succès'),
                message: message,
                type: 'success',
                sticky: false
            });
            notification.open();
        }

        showErrorMessage(message) {
            const notification = new core.Notification(this, {
                title: _t('Erreur'),
                message: message,
                type: 'danger',
                sticky: false
            });
            notification.open();
        }
    }

    core.action_registry.add('drag_drop_widget', DragDropWidget);
    return DragDropWidget;
});
