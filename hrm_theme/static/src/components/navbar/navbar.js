/** @odoo-module **/
import {NavBar} from "@web/webclient/navbar/navbar";
import {useService} from "@web/core/utils/hooks";
import {VTAppMenu} from "./app_menu";

const {useState, onMounted, onWillStart, useRef} = owl

export class VTNavbar extends NavBar {
    setup() {
        super.setup();
        this.router = useService("router");
        this.appMenuRef = useRef('appMenuRef')
         this.menuRepo = useService("menu");
        this.state = useState({
            sessions: {},
            vtMenuService: useService("hrm_theme.vt_menu_service"),
        })
        onMounted(async () => {
            await this.state.vtMenuService.handleActiveMenuWhenClickReload(this.router.current.hash.menu_id)
        })
    }

    onNavBarDropdownItemSelection(menu, vet) {
        this.state.vtMenuService.state.vetId = 0
        super.onNavBarDropdownItemSelection(menu)
        this.state.vtMenuService.state.actionId = menu.actionID
        const findVet = (m, menu) => {
            if (m.childrenTree) {
                if (m.children.includes(menu.id)) {
                    this.state.vtMenuService.state.vetId = vet
                    return
                }
                m.childrenTree.forEach(s => {
                    findVet(s, menu)
                })
            }
        }
        this.menuService.getCurrentApp().childrenTree.forEach((m) => {
            if (m.children) {
                findVet(m, menu)
            }
        })
    }
}

VTNavbar.template = "hrm_theme.navbar"
VTNavbar.components = {
    ...NavBar.components,
    VTAppMenu: VTAppMenu,
}
