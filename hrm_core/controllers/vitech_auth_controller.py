# -*- coding: utf-8 -*-
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
import logging
from werkzeug.exceptions import BadRequest
import odoo
from odoo import http, tools, _
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.exceptions import UserError, AccessError, AccessDenied
from odoo.http import request, Response

_logger = logging.getLogger(__name__)
CORS = '*'


class VitechAuthController(AuthSignupHome):
  @http.route('/api/web/session/authenticate', type='json', auth="none")
  def authenticate(self, login, password,company, base_location=None):
    db = request.httprequest.headers.get("x-db")
    company_check = request.env['res.company'].search([('company_code', '=', company)])
    if(not company_check):
      return {"code": 403, "message": _("Company is invalid."), "data": None}
    try:
      pre_uid = request.session.authenticate(db, login, password)
      if pre_uid != request.session.uid:
        return {'uid': None}

      request.session.db = db
      registry = odoo.modules.registry.Registry(db)
      with registry.cursor() as cr:
        env = odoo.api.Environment(cr, request.session.uid, request.session.context)
        if not request.db:
          http.root.session_store.rotate(request.session, env)
          request.future_response.set_cookie(
            'session_id', request.session.sid,
            max_age=http.SESSION_LIFETIME, httponly=True
          )
        return {"code": 200, "message": _("Login successfully"), "data": env['ir.http'].session_info()}
    except AccessDenied as e:
      return {"code": 403, "message": _("Username or password invalid."), "data": None}

  @http.route('/api/auth/register', type='json', auth="public", sitemap=False, csrf=False)
  def api_register_user(self, *args, **kw):
    db = request.httprequest.headers.get("x-db")
    company_code = kw['company']
    qcontext = self.get_auth_signup_qcontext()
    if all(key not in qcontext for key in
           ['login', 'password', 'confirm_password', 'name']) and request.httprequest.method == 'POST':
      return {
        'register': True,
        'status_code': 200
      }
    if not qcontext.get('token') and not qcontext.get('signup_enabled'):
      return {
        'status_code': 400,
        'register': True,
        'message': 'Token invalid'
      }
    if 'error' not in qcontext and request.httprequest.method == 'POST':
      try:
        self.do_user_signup(qcontext, company_code)
        pre_uid = request.session.authenticate(db, qcontext['login'], qcontext['password'])
        return {
          'user_id': pre_uid,
          'register': True,
          'status_code': 200
        }
      except UserError as e:
        qcontext['error'] = e.args[0]
      except (SignupError, AssertionError) as e:
        if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
          qcontext["error"] = _("Another user is already registered using this email address.")
        else:
          _logger.warning("%s", e)
          qcontext['error'] = _("Could not create a new account.") + "\n" + str(e)
    return {
      'status_code': 400,
      'register': True,
      'message': qcontext['error']
    }

  def do_user_signup(self, qcontext, company_code):
    values = self._prepare_signup_values(qcontext)
    group_user = request.env.ref('base.group_user')
    real_estate_admin_group = request.env.ref('vitech_real_estate_core.real_estate_group_admin')
    if 'groups_id' not in values:
      values['groups_id'] = [(6, 0, [group_user.id, real_estate_admin_group.id])]
    company = request.env['res.company'].search([('company_code', '=', company_code)])
    values['company_ids'] = [company['id']]
    values['company_id'] = company['id']
    self._signup_with_values(qcontext.get('token'), values)
    request.env.cr.commit()

  @http.route('/api/remove/user', type='json', auth="user")
  def remove_user(self, password):
    try:
      user_remove = request.env.user
      db = request.env.cr.dbname
      login = user_remove['login']

      pre_uid = request.session.authenticate(db, login, password)
      if pre_uid != request.session.uid:
        return {"code": 403, "message": _("Password invalid."), "data": None}

      request.env.cr.execute("""
                      UPDATE res_users
                      SET active = False
                      WHERE id = %s
                  """, (user_remove.id,))
      request.env.cr.commit()
      return {"code": 200, "message": _("Remove user successfully"), "data": True}
    except AccessDenied as e:
      return {"code": 403, "message": _("Password invalid."), "data": None}
