/* @odoo-module */
import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

function HrmLogout(env) {
  const route = "/web/session/logout";
  return {
    type: "item",
    id: "logout",
    description: _t("Log out"),
    href: `${browser.location.origin}${route}`,
    callback: () => {
      if (window.ReactNativeWebView) {
        window.ReactNativeWebView.postMessage("log_out");
      }
      browser.location.href = route;
    },
    sequence: 70,
  };
}

export function HrmItem(env) {
  return {
    type: "item",
    id: "settings",
    description: _t("Preferences"),
    callback: async function () {
      const actionDescription = await env.services.orm.call(
        "res.users",
        "action_get"
      );
      actionDescription.res_id = env.services.user.userId;
      env.services.action.doAction(actionDescription);
      const event = new Event("closeBurger");
      window.dispatchEvent(event);
    },
    sequence: 50,
  };
}

export function removeUser(env) {
  return {
    type: "item",
    id: "remove_account",
    description: _t("Xóa tài khoản"),
    callback: async function () {
      const modalElement = $("#remove_account");
      if (modalElement.length) {
        modalElement.modal("show"); // Show the modal
      } else {
        console.error(
          "Modal element with ID 'remove_account_modal' not found."
        );
      }
    },
    sequence: 51,
  };
}

registry.category("user_menuitems").remove("log_out");
registry.category("user_menuitems").remove("documentation");
registry.category("user_menuitems").remove("odoo_account");
registry.category("user_menuitems").remove("support");
registry.category("user_menuitems").remove("profile");
registry.category("user_menuitems").add("log_out", HrmLogout);
registry.category("user_menuitems").add("profile", HrmItem);
registry.category("user_menuitems").add("remove_account", removeUser);
