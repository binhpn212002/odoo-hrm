/** @odoo-module **/
import { useService } from "@web/core/utils/hooks";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { Constant } from "../../constant/constant";

const { useState, onMounted, onWillStart, useRef, Component } = owl;

export class AppMenu extends Component {
  setup() {
    this.menuService = useService("menu");
    this.router = useService("router");
    this.action = useService("action");
    this.menuRef = useRef("menuRef");
    this.orm = useService("orm");
    this.state = useState({
      menuApp: [],
      isMenu: false,
      hrmMenuService: useService("hrm_theme.hrm_menu_service"),
      mobile: false,
      hotline: "",
    });

    onWillStart(async () => {
      const listMenu = await this.menuService.getApps();
      const menuShow = listMenu.filter((menu) => {
        return menu.xmlid != Constant.XMLID_MENU_HOME;
      });
      this.state.menuApp = menuShow;
    });
    onMounted(async () => {
      const self = this.state;
      self.hrmMenuService.state.isSession = false;
      const dropdown = document.getElementById("dropdown");
      document.addEventListener("click", function (event) {
        if (!dropdown.contains(event.target)) {
          if (!self.mobile) {
            self.isMenu = false;
          }
        }
      });
    });
  }

  openWithWindow() {
    const self = this.state;
    self.mobile = false;
    self.isMenu = !self.isMenu;
  }

  async onNavBarDropdownItemSelection(menu) {
    if (menu) {
      await this.menuService.selectMenu(menu);
    }
    this.state.hrmMenuService.state.actionId = menu.actionID;
    this.state.isMenu = false;
    const { id } = menu;
    if (id) {
      await this.state.hrmMenuService.handleActiveMenuWhenClickReload(menu.id);
    }
  }
}

AppMenu.template = "hrm_theme.NavBar.AppsMenu";
AppMenu.components = {
  DropdownItem: DropdownItem,
};
AppMenu.props = {};
