/** @odoo-module */

import { Dialog } from "@web/core/dialog/dialog";
import {
  useState,
  useRef,
  Component,
  onMounted,
  onWillUnmount,
  useEffect,
} from "@odoo/owl";
import { checkFileSize } from "@web/core/utils/files";
import { useService } from "@web/core/utils/hooks";
import { FileInput } from "@web/core/file_input/file_input";
import { isLandscape } from "../utils/screen_resolution";

/**
 * creating a dialogue to show camera
 */
export class CameraDialog extends Component {
  setup() {
    super.setup();
    this.http = useService("http");
    this.notification = useService("notification");
    this.video = useRef("video");
    this.image = useRef("image");
    this.state = useState({
      url: false,
      file: false,
    });

    onMounted(async () => {
      this.video.el.srcObject = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: isLandscape() ? 1920 : 1080 },
          height: { ideal: isLandscape() ? 1080 : 1920 },
          facingMode: "environment",
        },
        audio: false,
      });
    });
    onWillUnmount(() => {
      this.stopCamera();
      console.log("onWillUnmount call");
    });
  }

  /**
   * Closes the camera
   */
  _cancel() {
    this.env.dialogData.close();
    this.stopCamera();
  }

  /**
   * Saves the Image
   */
  _confirm() {
    let video = this.video.el;
    let image = this.image.el;
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const canvasContext = canvas.getContext("2d");
    canvasContext.drawImage(video, 0, 0);
    canvas.toBlob((blob) => {
      // Convert the Blob to a File
      const file = new File([blob], performance.now() + ".jpg", {
        type: "image/jpeg",
      });
      // For demonstration, let's show the captured image in an img element
      this.state.url = URL.createObjectURL(file);
      this.state.file = file;
      video.classList.add("d-none");
      image.classList.remove("d-none");
      image.src = URL.createObjectURL(file);
    }, "image/jpeg");
  }

  get httpParams() {
    const { resId, resModel } = this.props.parent.props.record;
    const params = {
      csrf_token: odoo.csrf_token,
      ufile: [this.state.file],
    };
    if (resModel) {
      params.model = resModel;
    }
    if (resId !== undefined) {
      params.id = resId;
    }
    return params;
  }

  async uploadFiles(params) {
    if ((params.ufile && params.ufile.length) || params.file) {
      const fileSize =
        (params.ufile && params.ufile[0].size) || params.file.size;
      if (!checkFileSize(fileSize, this.notification)) {
        return null;
      }
    }
    const fileData = await this.http.post(this.props.route, params, "text");
    const parsedFileData = JSON.parse(fileData);
    if (parsedFileData.error) {
      throw new Error(parsedFileData.error);
    }
    return parsedFileData;
  }

  /**
   * Updates the image
   */
  async _save() {
    console.log(this.props);
    console.log(this.state.url);
    const parsedFileData = await this.uploadFiles(this.httpParams);
    console.log(parsedFileData);

    if (parsedFileData) {
      this.props.onUpload(parsedFileData);
    }
    this.props.parent.state.isValid = true;
    this.props.parent.rawCacheKey = null;
    this.env.dialogData.close();
    this.stopCamera();
  }

  /**
   * Resets the Image
   */
  _reset() {
    this.state.file = false;
    this.state.url = false;
    this.video.el.classList.remove("d-none");
    this.image.el.classList.add("d-none");
  }

  /**
   * Closes camera
   */
  _close() {
    this.stopCamera();
  }

  /**
   * Stop camera
   */
  stopCamera() {
    this.video.el.srcObject.getVideoTracks().forEach((track) => {
      track.stop();
    });
  }
}

CameraDialog.template = "hrm.camera_dialog";
CameraDialog.components = { Dialog };
CameraDialog.defaultProps = {
  title: "Máy ảnh",
  route: "/web/binary/upload_attachment",
  onUpload: () => {},
};
