/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import {WebClient} from "@web/webclient/webclient";
import {BurgerMenu} from "@web/webclient/burger_menu/burger_menu";

const {useState, onMounted, useRef} = owl
patch(BurgerMenu.prototype, {
    setup(...args) {
        super.setup(...args);
        onMounted(() => {
            window.addEventListener('closeBurger', (e) => {
                this.state.isUserMenuOpened = false;
                this.state.isBurgerOpened = false;
            });
        })
    },
});
