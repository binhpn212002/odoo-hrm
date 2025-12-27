/** @odoo-module **/

import {
  Many2ManyBinaryField,
  many2ManyBinaryField,
} from "@web/views/fields/many2many_binary/many2many_binary_field";
import { registry } from "@web/core/registry";
import { useState } from "@odoo/owl";
import { useFileViewer } from "@web/core/file_viewer/file_viewer_hook";
import { useService } from "@web/core/utils/hooks";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";
import { url } from "@web/core/utils/urls";
import { CameraDialog } from "./camera_dialog";
import { AttachmentModel } from "../core/file_viewer/attachment_model";

export class Many2ManyImagePreview extends Many2ManyBinaryField {
  static template = "hrm_core.Many2ManyImagePreview";

  setup() {
    super.setup();
    console.log(this.files);
    this.ui = useState(useService("ui"));
    this.state = useState({
      hasCamera: false,
    });
    // Arbitrary high value, this is effectively a max-width.
    this.imagesWidth = 1920;
    this.imagesHeight = 200;
    this.fileViewer = useFileViewer();
    this.dialogService = useService("dialog");
    this.checkHasCamera();
  }

  onFileCamera = (ev) => {
    ev.stopPropagation();

    this.dialogService.add(CameraDialog, {
      parent: this,
      onUpload: (files) => this.onFileUploaded(files),
    });
  };
  checkHasCamera = async () => {
    try {
      // Check if the mediaDevices API is available
      if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) {
        return false;
      }

      // Get the list of media devices
      const devices = await navigator.mediaDevices.enumerateDevices();

      // Check if there is at least one video input device
      const hasCamera = devices.some((device) => device.kind === "videoinput");
      this.state.hasCamera = hasCamera;
    } catch (err) {
      console.error("Error checking for camera: ", err);
      this.state.hasCamera = false;
    }
  };

  get files() {
    return this.props.record.data[this.props.name].records.map((record) => {
      return Object.assign(new AttachmentModel(), {
        ...record.data,
        id: record.resId,
        modelOwner: record.data.model_owner,
      });
    });
  }

  getImageUrl(attachment) {
    if (attachment.uploading && attachment.tmpUrl) {
      return attachment.tmpUrl;
    }
    return url(attachment.urlRoute, {
      ...attachment.urlQueryParams,
      width: this.imagesWidth,
      height: this.imagesHeight,
    });
  }

  onClickDownload(attachment) {
    const downloadLink = document.createElement("a");
    downloadLink.setAttribute("href", attachment.downloadUrl);
    // Adding 'download' attribute into a link prevents open a new
    // tab or change the current location of the window. This avoids
    // interrupting the activity in the page such as rtc call.
    downloadLink.setAttribute("download", "");
    downloadLink.click();
  }

  onClickUnlink(attachment) {
    this.dialogService.add(ConfirmationDialog, {
      body: _t('Do you really want to delete "%s"?', attachment.name),
      cancel: () => {},
      confirm: () => this.onConfirmUnlink(attachment.id),
    });
  }

  onConfirmUnlink(deleteId) {
    this.onFileRemove(deleteId);
  }
}

export const many2ManyImagePreviewField = {
  ...many2ManyBinaryField,
  component: Many2ManyImagePreview,
  relatedFields: [...many2ManyBinaryField.relatedFields],
};

registry
  .category("fields")
  .add("many2many_image_preview", many2ManyImagePreviewField);
