odoo.define('gestion_comptable_sfec.form_interactions', function (require) {
    "use strict";

    const core = require('web.core');
    const Widget = require('web.Widget');

    class FormWidget extends Widget {
        constructor(parent, options) {
            super(parent, options);
            this.setupFormInteractions();
        }

        setupFormInteractions() {
            // Animation des champs de formulaire
            $('.neumorphic-input').on('focus', function() {
                $(this).addClass('focused');
            }).on('blur', function() {
                $(this).removeClass('focused');
            });

            // Validation en temps réel
            $('.neumorphic-input').on('input', function() {
                const value = $(this).val();
                const field = $(this).data('field');
                
                // Validation spécifique selon le champ
                if (field === 'email') {
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailRegex.test(value)) {
                        $(this).addClass('invalid');
                        $(this).next('.validation-message').text('Format email invalide');
                    } else {
                        $(this).removeClass('invalid');
                        $(this).next('.validation-message').text('');
                    }
                }
            });

            // Gestion des statuts
            $('.status-value').each(function() {
                const status = $(this).text();
                $(this).addClass(status.toLowerCase());
            });

            // Animation des boutons
            $('.neumorphic-btn').on('mouseenter', function() {
                $(this).addClass('hovered');
            }).on('mouseleave', function() {
                $(this).removeClass('hovered');
            });

            // Messages de confirmation
            $('.neumorphic-btn[name="save"]').on('click', function() {
                const form = $(this).closest('form');
                const message = $('<div class="status-message success">Sauvegarde en cours...</div>');
                form.append(message);
                
                // Simulation de sauvegarde
                setTimeout(() => {
                    message.text('Sauvegarde réussie !');
                    setTimeout(() => {
                        message.fadeOut();
                    }, 2000);
                }, 1000);
            });
        }

        // Fonction pour mettre à jour le statut
        updateStatus(element, newStatus) {
            const statusElement = element.find('.status-value');
            statusElement.text(newStatus);
            statusElement.removeClass();
            statusElement.addClass('status-value');
            statusElement.addClass(newStatus.toLowerCase());
        }

        // Fonction pour afficher un message de validation
        showValidationMessage(element, message, isError = false) {
            const messageElement = $('<div class="validation-message"></div>');
            if (isError) {
                messageElement.addClass('error');
            }
            messageElement.text(message);
            element.after(messageElement);
            
            setTimeout(() => {
                messageElement.fadeOut();
            }, 3000);
        }
    }

    // Enregistrement du widget
    core.action_registry.add('form_interactions', FormWidget);

    return FormWidget;
});
