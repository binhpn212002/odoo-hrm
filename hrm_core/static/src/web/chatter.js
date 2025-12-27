/* @odoo-module */
// @ts-nocheck

import { patch } from "@web/core/utils/patch";
import { Chatter } from "@mail/core/web/chatter";

Chatter.template = "hrm.Chatter";
patch(Chatter.props, [...Chatter.props, "hideAttachment?"]);
patch(Chatter.defaultProps, {
  ...Chatter.defaultProps,
  hideAttachment: false,
});

patch(Chatter.prototype, {
  toggleComposer(mode = false) {
    this.closeSearch();
    const toggle = () => {
      if (this.state.composerType === mode) {
        this.state.composerType = this.state.thread.composerType = false;
      } else {
        this.state.composerType = this.state.thread.composerType = mode;
      }
    };
    if (this.state.thread.id) {
      toggle();
    } else {
      this.onThreadCreated = toggle;
      this.props.saveRecord?.();
    }
  },
  onPostCallback() {
    if (this.props.hasParentReloadOnMessagePosted) {
      this.reloadParentView();
    }
    // hold chatter laị khi gửi message thành công
    // this.toggleComposer();
    this.state.jumpThreadPresent++;
    // Load new messages to fetch potential new messages from other users (useful due to lack of auto-sync in chatter).
    this.load(this.state.thread, [
      "followers",
      "messages",
      "suggestedRecipients",
    ]);
  },
});
