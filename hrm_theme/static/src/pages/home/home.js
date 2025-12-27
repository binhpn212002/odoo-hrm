/** @odoo-module **/
import {registry} from "@web/core/registry"
import {useService} from "@web/core/utils/hooks";
import {Constant} from "../../constant/constant";
import {Slider} from "../slider/slider"

const {useState, onWillStart, onMounted, useRef, Component} = owl

export class Home extends Component {
    setup() {
        this.menuService = useService('menu')
        this.action = useService("action")
        this.router = useService('router')
        this.ui = useService("ui")
        this.state = useState({
            menuApp: [],
            isSmall: this.ui.isSmall,
            vtMenuService: useService("hrm_theme.vt_menu_service"),
        })
        this.navSectionRef = useRef('navSectionRef')
        onWillStart(async () => {
            const listMenu = await this.menuService.getApps();
            const menuShow = listMenu.filter((menu) => {
                return menu.xmlid != Constant.XMLID_MENU_HOME
            })
            this.state.menuApp = menuShow
            const width = window.innerWidth;
            if (width > 768) {
                const estateAction = listMenu.find((a) => a.xmlid == Constant.MENU_BDS_PROJECT_ACTION)
                if (
                    estateAction
                ) {
                    this.state.vtMenuService.state.actionId = estateAction.actionID
                    await this.menuService.selectMenu(estateAction);
                }
            }
        })
        onMounted(() => {
            this.state.vtMenuService.state.isSession = false
        })
    }

    computesAlignmentClass(menu_index) {
        switch (menu_index % 3) {
            case 0:
                return 'text-start text-md-center'
            case 1:
                return 'text-center text-md-center'
            default:
                return 'text-end text-md-center'
        }
    }

    async openApp(menu) {
        let params = this.state.vtMenuService.getMenuItemHref(menu)
        let actionId = params.split("action=")[1].split("&")[0]
        this.state.vtMenuService.state.actionId = actionId
        if (menu) {
            await this.menuService.selectMenu(menu);
        }
        const {id} = menu
        if (id) {
            await this.state.vtMenuService.handleActiveMenuWhenClickReload(menu.id)
        }
        this.state.vtMenuService.state.isSession = true
        this.state.vtMenuService.state.showMenu = true
    }
}

Home.template = "hrm_theme.home"
Home.components = {Slider}
registry.category("actions").add("hrm_theme.home_action", Home)
