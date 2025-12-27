/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import {WebClient} from "@web/webclient/webclient";
import {VTNavbar} from "../components/navbar/navbar";
import {VTAction} from "../components/action/vt_action";
import {
    SettingsFormController
} from "@web/webclient/settings_form_view/settings_form_controller";


patch(WebClient, {
    components: {
        ...WebClient.components,
        VTNavbar,
        VTAction,
    },
});

SettingsFormController.template = 'vitech.web.SettingsFormView'
