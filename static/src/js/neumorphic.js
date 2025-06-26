/** @odoo-module **/

import { Widget } from "@web/core/widget";
import { registry } from "@web/core/registry";

export class NeumorphicWidget extends Widget {
    setup() {
        super.setup();
        this.setupAnimations();
    }

    setupAnimations() {
        document.querySelectorAll(".stat-number").forEach((el) => {
            const finalValue = parseInt(el.textContent);
            let counter = 0;
            const duration = 2000;
            const steps = 60;
            const stepTime = duration / steps;
            const increment = finalValue / steps;

            const interval = setInterval(() => {
                counter += increment;
                if (counter >= finalValue) {
                    el.textContent = finalValue;
                    clearInterval(interval);
                } else {
                    el.textContent = Math.ceil(counter);
                }
            }, stepTime);
        });

        document.querySelectorAll(".neumorphic-card").forEach((card, i) => {
            setTimeout(() => {
                card.classList.add("animated", "fadeInUp");
            }, i * 200);
        });

        document.querySelectorAll(".neumorphic-btn").forEach((btn) => {
            btn.addEventListener("mouseenter", () => btn.classList.add("hovered"));
            btn.addEventListener("mouseleave", () => btn.classList.remove("hovered"));
        });
    }

    addPulseEffect(element, duration = 1000) {
        element.style.animation = `pulse ${duration}ms ease-in-out infinite`;
    }

    addStatusChangeAnimation(element, newStatus) {
        const animation = newStatus === "success" ? "success" : "error";
        element.classList.add(`status-${animation}`);
        setTimeout(() => {
            element.classList.remove(`status-${animation}`);
        }, 1000);
    }
}

// Enregistrer l’action
registry.category("actions").add("neumorphic_dashboard", NeumorphicWidget);
