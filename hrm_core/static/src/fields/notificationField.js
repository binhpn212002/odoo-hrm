/** @odoo-module */
import {CharField} from "@web/views/fields/char/char_field";
import {registry} from "@web/core/registry";
import {charField} from "@web/views/fields/char/char_field";


export class NotificationField extends CharField {
    setup(){
        super.setup()
    }
};

NotificationField.template = "vitech.NotificationField";
export const notificationField = {
    ...charField,
    component: NotificationField,
};
registry.category("fields").add("NotificationField", notificationField);
