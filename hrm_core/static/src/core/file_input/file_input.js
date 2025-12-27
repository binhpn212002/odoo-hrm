/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import {FileInput} from "@web/core/file_input/file_input";

// @ts-ignore
patch(FileInput.prototype, {
    get httpParams() {
        const {resId, resModel, modelOwner} = this.props;
        const params = {
            csrf_token: odoo.csrf_token,
            ufile: [...this.fileInputRef.el.files],
        };
        if (resModel) {
            params.model = resModel;
        }
        if (resId !== undefined) {
            params.id = resId;
        }
        if (modelOwner !== undefined) {
            params.model_owner = modelOwner;
        }
        return params;
    }
})