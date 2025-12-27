/** @odoo-module */
import {registry} from "@web/core/registry";
import {reactive} from "@odoo/owl";

const VTMenuService = {
    dependencies: ["router", 'menu', 'orm'],
    start(env, {router, menu, orm}) {
        const state = reactive({
            sessions: {},
            actionId: router.current.hash.action,
            vetId: 0,
            isSession : true,
            showMenu: false
        });

        const setVetId = (menu, vet, menu_id) => {
            if (menu.childrenTree) {
                if (menu.children.includes(menu_id)) {
                    state.vetId = vet
                    return
                }
                menu.childrenTree.forEach((m) => {
                    setVetId(m, vet, menu_id)
                })
            }
        }

        const setVet = async (menu_id) => {
            const crrMenu = await menu.getMenu(menu_id)
            if (crrMenu) {
                const appMenu = await menu.getMenuAsTree(crrMenu.appID)
                appMenu.childrenTree.forEach((menu) => {
                    let vet = menu.id
                    setVetId(menu, vet, menu_id,)
                })
            }
        }
        const handleAutoSelectMenuActive = async () => {
            const {menu_id} = router.current.hash;
            await setVet(menu_id)
        }

        const handleActiveMenuWhenClickReload = async (menu_id) => {
            let menu = await orm.searchRead("ir.ui.menu", [["id", "=", menu_id]]);
            if (menu[0] && menu[0]?.id && menu[0].id == menu_id) {
                state.vetId = menu[0]?.child_id[0]
                return
            }
            if (menu) {
                state.vetId = menu[0]?.parent_path.split("/")[1]
            }
        }
        const getMenuItemHref = (payload) => {
            const parts = [`menu_id=${payload.id}`];
            if (payload.actionID) {
                parts.push(`action=${payload.actionID}`);
            }
            return "#" + parts.join("&");
        }

        return {
            state,
            handleAutoSelectMenuActive,
            getMenuItemHref,
            handleActiveMenuWhenClickReload
        };
    },
};

registry.category("services").add("hrm_theme.vt_menu_service", VTMenuService);
