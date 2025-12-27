/** @odoo-module **/
import {useService} from "@web/core/utils/hooks";
import {DropdownItem} from "@web/core/dropdown/dropdown_item";
import {Constant} from "../../constant/constant";


const {useState, onMounted, onWillStart, useRef, Component} = owl

export class VTAppMenu extends Component {
    setup() {
        this.menuService = useService("menu");
        this.router = useService("router");
        this.action = useService("action")
        this.menuRef = useRef("menuRef")
        this.orm = useService("orm")
        this.state = useState({
            menuApp: [],
            isMenu: false,
            vtMenuService: useService("hrm_theme.vt_menu_service"),
            mobile: false,
            hotline: "",
        })

        onWillStart(async () => {
            const listMenu = await this.menuService.getApps();
            const menuShow = listMenu.filter((menu) => {
                return menu.xmlid != Constant.XMLID_MENU_HOME
            })
            this.state.menuApp = menuShow
        })
        onMounted(async () => {
            const self = this.state
            self.vtMenuService.state.isSession = false
            const dropdown = document.getElementById('dropdown');
            document.addEventListener('click', function (event) {
                if (!dropdown.contains(event.target)) {
                    if (!self.mobile) {
                        self.isMenu = false
                    }
                }
            });
        })
    }

    openWithWindow() {
        const self = this.state
        self.mobile = false
        self.isMenu = !self.isMenu
    }

    backToHome() {
        const self = this.state
        self.mobile = true
        self.isMenu = true
        self.vtMenuService.state.showMenu = false
        this.action.doAction("hrm_theme.home_action")
    }

    openWithMobile() {
        const self = this.state
        self.mobile = true
        self.isMenu = true
    }

    async openProject() {
        //web_icon was match with menuitem web_icon. If change menuitem web_icon, must be change web_icon bellow
        this.state.isMenu = false
        let res = await this.orm.searchRead("ir.ui.menu", [["web_icon", "=", "vitech_bds_project,static/description/icon.png"]]);
        const menu = this.menuService.getMenu(res[0].id)
        this.menuService.setCurrentMenu(menu)
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: "Danh sách bảng hàng",
            res_model: 'vitech.real.estate.unit',
            views: [[false, 'tree']],
            target: 'current',
        })
        this.state.vtMenuService.state.actionId = menu.actionID
    }

    async openMail() {
        //web_icon was match with menuitem web_icon. If change menuitem web_icon, must be change web_icon bellow
        let res = await this.orm.searchRead("ir.ui.menu", [["web_icon", "=", "mail,static/description/icon.png"]]);
        const menu = this.menuService.getMenu(res[0].id)
        this.menuService.setCurrentMenu(menu)
        this.action.doAction("mail.action_discuss")
        this.state.isMenu = false
        this.menuService.setCurrentMenu(menu)
    }

    async onNavBarDropdownItemSelection(menu) {
        if (menu) {
            await this.menuService.selectMenu(menu);
        }
        this.state.vtMenuService.state.actionId = menu.actionID
        this.state.isMenu = false
        const {id} = menu
        if (id) {
            await this.state.vtMenuService.handleActiveMenuWhenClickReload(menu.id)
        }
    }
}

VTAppMenu.template = "hrm_theme.NavBar.AppsMenu"
VTAppMenu.components = {
    DropdownItem: DropdownItem
}
VTAppMenu.props = {}
