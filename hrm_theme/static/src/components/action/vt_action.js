/** @odoo-module **/
import {useService} from "@web/core/utils/hooks";
import {Constant} from "@hrm_theme/constant/constant";

const {useState, onWillStart, useEffect, Component} = owl

export class VTAction extends Component {
    setup() {
        this.action = useService("action")
        this.menuService = useService("menu")
        this.router = useService('router')
    }

    backToHome() {
        this.menuService.setCurrentMenu({})
        this.action.doAction(Constant.MENU_HOME_ACTION)
    }

    goToDiscuss() {
        this.menuService.setCurrentMenu({})
        this.action.doAction(Constant.MENU_DISCUSS_ACTION)
    }
}

VTAction.template = "hrm_theme.vt_action"
VTAction.props={}
