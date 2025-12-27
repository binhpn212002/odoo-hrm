# controllers/main.py
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.home import  Home

XML_ID_HOME_ACTION ="hrm_theme.hrm_theme_home"


class VitechHomeHontroller(Home):

    @http.route()
    def web_login(self, redirect=None, **kw):
        # Call the parent method to handle the actual login process
        response = super(VitechHomeHontroller, self).web_login(redirect=redirect, **kw)
        if request.session.uid:
            return request.redirect("/web#action="+XML_ID_HOME_ACTION)
        return response
