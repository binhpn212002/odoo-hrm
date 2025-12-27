from odoo.addons.mail.controllers.thread import ThreadController
from odoo import http
from odoo.http import request


class ExtThreadController(ThreadController):
  @http.route("/mail/thread/messages", methods=["POST"], type="json", auth="user")
  def mail_thread_messages(self, thread_model, thread_id, search_term=None, before=None, after=None, around=None,
                           message_chatter_type=None,
                           limit=30):
    note_id = request.env['ir.model.data'].sudo()._xmlid_to_res_id('mail.mt_note')
    com_id = request.env['ir.model.data'].sudo()._xmlid_to_res_id('mail.mt_comment')
    domain = [
      ("res_id", "=", int(thread_id)),
      ("model", "=", thread_model),
      ("message_type", "!=", "user_notification"),
      '|', '&',
      ("subtype_id", "=", note_id),
      ("create_uid", "=", request.env.uid)
      , ("subtype_id", "!=", note_id),
    ]

    res = request.env["mail.message"]._message_fetch(domain, search_term=search_term, before=before, after=after,
                                                     around=around, limit=limit)

    if not request.env.user._is_public():
      res["messages"].set_message_done()
    return {**res, "messages": res["messages"].message_format()}
