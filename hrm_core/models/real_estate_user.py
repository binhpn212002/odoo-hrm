# -*- coding: utf-8 -*-
from pkg_resources import _

from odoo import models, fields, api, SUPERUSER_ID, Command
from odoo.exceptions import UserError
from odoo.tools import lazy_property


class RealEstateUser(models.Model):
  _name = 'res.users'
  _inherit = ['res.users']
  _description = 'real estate user'

  team_id = fields.Many2one('vitech.real.estate.team', string='Team')

  team_leader_ids = fields.One2many('vitech.real.estate.team', 'leader_id', string='Leader Team')
  branch_member_id = fields.Many2one(comodel_name='res.company', string='Chi nhánh')
  company_director_ids= fields.One2many(comodel_name='res.company',inverse_name='director_id',string='Company director')

  def _get_users_in_group_sale_director_domain(self):
    group_sale_director = self.env.ref('vitech_real_estate_core.real_estate_group_sale_director')
    return [('id', 'in', group_sale_director.users.ids)]

  def _get_only_users_in_group_sale_director_domain(self):
    group_sale_director = self.env.ref('vitech_real_estate_core.real_estate_group_sale_director')
    group_only_sale_director = group_sale_director.users - self.env.ref('vitech_real_estate_core.real_estate_group_admin').users
    return group_only_sale_director

  @api.model
  def _is_mkt(self):
    for user in self:
      return user.has_group('vitech_real_estate_core.real_estate_group_marketing') and not user.has_group(
        'vitech_real_estate_core.real_estate_group_sale')

  def _is_saler(self):
    for user in self:
      return user.has_group('vitech_real_estate_core.real_estate_group_sale') and not user.has_group(
        'vitech_real_estate_core.real_estate_group_admin')

  def _is_sale_director(self):
    for user in self:
      return user.has_group('vitech_real_estate_core.real_estate_group_sale_director') and not user.has_group(
        'vitech_real_estate_core.real_estate_group_admin')

  def _is_admin_bds(self):
    for user in self:
      return user.has_group('vitech_real_estate_core.real_estate_group_admin') and not user.has_group(
        'vitech_real_estate_core.real_estate_group_general')

  def _is_general(self):
    for user in self:
      return user.has_group('vitech_real_estate_core.real_estate_group_general') and not user.has_group(
        'vitech_real_estate_core.real_estate_group_super_admin')

  def get_team_id_leaded(self):
    team = self.sudo().env['vitech.real.estate.team'].search([('leader_id', '=', self.env.uid)], limit=1)
    return team

  def get_list_user_admin(self):
    return self.env.ref('vitech_real_estate_core.real_estate_group_admin').users


  @api.constrains('team_id')
  def _compute_team(self):
    for user in self:
      user.branch_member_id = user.team_id.branch_id

  def remove_team(self):
    for user in self:
      # if user.id == user.team_id.leader_id.id:
      #   user.team_id.leader_id = False
      team = user.team_id
      user.team_id = False
      notification = self.env['vitech.real.estate.notification'].contructor_notification(name='User',
                                                                                         body='Bạn đã rời khỏi team: ' + team.name,
                                                                                         model_id=user._name,
                                                                                         view_type='form',
                                                                                         view_ref='base.view_users_form',
                                                                                         date_time=fields.Datetime.now(),
                                                                                         display_name='Thông báo người dùng',
                                                                                         icon_src='/vitech_notification/static/img/employee.svg',
                                                                                         is_muted=False, is_read=False,
                                                                                         is_hide=False,
                                                                                         user_id=user.id,
                                                                                         type_display='user',
                                                                                         record_id=user.id)
      self.env['vitech.real.estate.notification'].create(notification)
