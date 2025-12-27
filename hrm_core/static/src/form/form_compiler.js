/* @odoo-module */
import {evaluateExpr} from "@web/core/py_js/py";
import {append, createElement, setAttributes} from "@web/core/utils/xml";
import {registry} from "@web/core/registry";

const originalChatterCompiler = registry.category("form_compilers").get("chatter_compiler").fn;

function extendedChatterCompiler(node, params) {
    let chatterContainerHookXml = originalChatterCompiler(node, params);
    // Adding custom logic to handle hideAttachments
    for (const childNode of node.children) {
        const options = evaluateExpr(childNode.getAttribute("options") || "{}");
        if (childNode.getAttribute("name") === "message_ids") {
            const hideAttachment = options["hide_attachment"];
            setAttributes(chatterContainerHookXml.querySelector('[t-component="__comp__.mailComponents.Chatter"]'), {
                hideAttachment,
            });
        }
    }
    return chatterContainerHookXml;
}

registry.category("form_compilers").get("chatter_compiler").fn = extendedChatterCompiler
// Override the existing compiler with the extended one
// registry.category("form_compilers").add("chatter_compiler", {
//     selector: "div.oe_chatter",
//     fn: extendedChatterCompiler,
// }, {force: true});