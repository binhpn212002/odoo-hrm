/* @odoo-module */
// @ts-nocheck
import {patch} from "@web/core/utils/patch";
import {Thread} from "@mail/core/common/thread_model";

patch(Thread.prototype, {
    get nonEmptyMessages() {
        if (this.composerType === "note") {
            return this.messages.filter((message) => {
                return !message.isEmpty && message.is_note && message.type === 'comment'
            });
        }
        return this.messages.filter((message) => !message.isEmpty && (!message.is_note || message.type === 'notification'));
    }
})