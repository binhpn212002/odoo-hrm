# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class IrUiMenuController(http.Controller):
    @http.route('/webclient/menu/<string:xml_id>', auth='public' , type="json")
    def _get_menu_by_xmlID(self, xml_id, lang=None):
      if lang:
        request.update_context(lang=lang)
      menus = request.env["ir.ui.menu"].load_menu_xml_id(request.session.debug, xml_id)
      return menus
