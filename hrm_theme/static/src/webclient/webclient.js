/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { WebClient } from "@web/webclient/webclient";
import { HrmNavbar } from "../components/navbar/navbar";
import { SettingsFormController } from "@web/webclient/settings_form_view/settings_form_controller";

patch(WebClient, {
  components: {
    ...WebClient.components,
    HrmNavbar,
  },
});

SettingsFormController.template = "hrm_theme.SettingsFormView";
