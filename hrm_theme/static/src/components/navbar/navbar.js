/** @odoo-module **/
import { useService } from "@web/core/utils/hooks";
import { NavBar } from "@web/webclient/navbar/navbar";
import { AppMenu } from "./app_menu";

const { useState, onMounted, useRef } = owl;

export class HrmNavbar extends NavBar {
  setup() {
    super.setup();
    this.router = useService("router");
    this.appMenuRef = useRef("appMenuRef");
    this.menuRepo = useService("menu");
    this.state = useState({
      sessions: {},
      hrmMenuService: useService("hrm_theme.hrm_menu_service"),
    });
    onMounted(async () => {
      await this.state.hrmMenuService.handleActiveMenuWhenClickReload(
        this.router.current.hash.menu_id
      );
    });
  }

  onNavBarDropdownItemSelection(menu, vet) {
    this.state.hrmMenuService.state.vetId = 0;
    super.onNavBarDropdownItemSelection(menu);
    this.state.hrmMenuService.state.actionId = menu.actionID;
    const findVet = (m, menu) => {
      if (m.childrenTree) {
        if (m.children.includes(menu.id)) {
          this.state.hrmMenuService.state.vetId = vet;
          return;
        }
        m.childrenTree.forEach((s) => {
          findVet(s, menu);
        });
      }
    };
    this.menuService.getCurrentApp().childrenTree.forEach((m) => {
      if (m.children) {
        findVet(m, menu);
      }
    });
  }
}

HrmNavbar.template = "hrm_theme.navbar";
HrmNavbar.components = {
  ...NavBar.components,
  AppMenu: AppMenu,
};
