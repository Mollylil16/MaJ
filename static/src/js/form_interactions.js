/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Widget } from "@web/core/widget";

class FormWidget extends Widget {
    constructor(parent, options) {
        super(parent, options);
        this.setupFormInteractions();
    }

    setupFormInteractions() {
        document.querySelectorAll('.neumorphic-input').forEach((input) => {
            input.addEventListener('focus', () => input.classList.add('focused'));
            input.addEventListener('blur', () => input.classList.remove('focused'));
            input.addEventListener('input', () => {
                const value = input.value;
                const field = input.dataset.field;

                if (field === 'email') {
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    const messageElem = input.nextElementSibling;
                    if (!emailRegex.test(value)) {
                        input.classList.add('invalid');
                        if (messageElem) messageElem.textContent = 'Format email invalide';
                    } else {
                        input.classList.remove('invalid');
                        if (messageElem) messageElem.textContent = '';
                    }
                }
            });
        });

        document.querySelectorAll('.status-value').forEach((el) => {
            const status = el.textContent.trim();
            el.classList.add(status.toLowerCase());
        });

        document.querySelectorAll('.neumorphic-btn').forEach((btn) => {
            btn.addEventListener('mouseenter', () => btn.classList.add('hovered'));
            btn.addEventListener('mouseleave', () => btn.classList.remove('hovered'));
        });

        document.querySelectorAll('.neumorphic-btn[name="save"]').forEach((btn) => {
            btn.addEventListener('click', () => {
                const form = btn.closest('form');
                const message = document.createElement('div');
                message.className = 'status-message success';
                message.textContent = 'Sauvegarde en cours...';
                form.appendChild(message);

                setTimeout(() => {
                    message.textContent = 'Sauvegarde réussie !';
                    setTimeout(() => {
                        message.style.display = 'none';
                    }, 2000);
                }, 1000);
            });
        });
    }

    updateStatus(element, newStatus) {
        const statusElement = element.querySelector('.status-value');
        if (statusElement) {
            statusElement.textContent = newStatus;
            statusElement.className = 'status-value ' + newStatus.toLowerCase();
        }
    }

    showValidationMessage(element, message, isError = false) {
        const messageElement = document.createElement('div');
        messageElement.className = 'validation-message';
        if (isError) messageElement.classList.add('error');
        messageElement.textContent = message;
        element.parentNode.insertBefore(messageElement, element.nextSibling);

        setTimeout(() => {
            messageElement.style.display = 'none';
        }, 3000);
    }
}

// Optionnel : enregistrement dans un service ou action_registry si nécessaire
registry.category('actions').add('form_interactions', FormWidget);
