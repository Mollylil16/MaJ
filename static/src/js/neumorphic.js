odoo.define('gestion_comptable_sfec.neumorphic', function (require) {
    "use strict";

    const core = require('web.core');
    const Widget = require('web.Widget');

    class NeumorphicWidget extends Widget {
        constructor(parent, options) {
            super(parent, options);
            this.setupAnimations();
        }

        setupAnimations() {
            // Animation des statistiques
            $('.stat-number').each(function() {
                const $this = $(this);
                const finalValue = parseInt($this.text());
                $this.prop('Counter', 0).animate({
                    Counter: finalValue
                }, {
                    duration: 2000,
                    easing: 'swing',
                    step: function(now) {
                        $this.text(Math.ceil(now));
                    }
                });
            });

            // Animation des cartes
            $('.neumorphic-card').each(function(i) {
                setTimeout(() => {
                    $(this).addClass('animated fadeInUp');
                }, i * 200);
            });

            // Hover effect sur les boutons
            $('.neumorphic-btn').on('mouseenter', function() {
                $(this).addClass('hovered');
            }).on('mouseleave', function() {
                $(this).removeClass('hovered');
            });
        }

        // Effet de pulsation pour les notifications importantes
        addPulseEffect(element, duration = 1000) {
            element.style.animation = `pulse ${duration}ms ease-in-out infinite`;
        }

        // Animation douce pour les changements de statut
        addStatusChangeAnimation(element, newStatus) {
            const animation = newStatus === 'success' ? 'success' : 'error';
            element.classList.add(`status-${animation}`);
            setTimeout(() => {
                element.classList.remove(`status-${animation}`);
            }, 1000);
        }
    }

    // Enregistrement du widget
    core.action_registry.add('neumorphic_dashboard', NeumorphicWidget);

    return NeumorphicWidget;
});
