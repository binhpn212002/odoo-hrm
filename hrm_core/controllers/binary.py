from odoo.addons.web.controllers.binary import Binary, clean
import json
import unicodedata
import logging

try:
  from werkzeug.utils import send_file
except ImportError:
  from odoo.tools._vendor.send_file import send_file

from odoo import _, http
from odoo.exceptions import AccessError, UserError
from odoo.http import request

_logger = logging.getLogger(__name__)


class ExtBinary(Binary):
  @http.route('/web/binary/upload_attachment', type='http', auth="user")
  def upload_attachment(self, model, id, model_owner, ufile, callback=None):
    files = request.httprequest.files.getlist('ufile')
    Model = request.env['ir.attachment']
    out = """<script language="javascript" type="text/javascript">
                      var win = window.top.window;
                      win.jQuery(win).trigger(%s, %s);
                  </script>"""
    args = []
    for ufile in files:

      filename = ufile.filename
      if request.httprequest.user_agent.browser == 'safari':
        # Safari sends NFD UTF-8 (where é is composed by 'e' and [accent])
        # we need to send it the same stuff, otherwise it'll fail
        filename = unicodedata.normalize('NFD', ufile.filename)

      try:
        attachment = Model.create({
          'name': filename,
          'raw': ufile.read(),
          'res_model': model,
          'res_id': int(id),
          'model_owner': True if model_owner == 'true' else False,
        })
        attachment._post_add_create()
      except AccessError:
        args.append({'error': _("You are not allowed to upload an attachment here.")})
      except Exception:
        args.append({'error': _("Something horrible happened")})
        _logger.exception("Fail to upload attachment %s", ufile.filename)
      else:
        args.append({
          'filename': clean(filename),
          'mimetype': attachment.mimetype,
          'id': attachment.id,
          'size': attachment.file_size
        })
    return out % (json.dumps(clean(callback)), json.dumps(args)) if callback else json.dumps(args)
