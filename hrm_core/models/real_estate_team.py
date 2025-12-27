# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RealEstateTeam(models.Model):
  _name = 'vitech.real.estate.team'
  _description = 'real estate team'

  name = fields.Char(required=True)

  member_ids = fields.One2many('res.users', 'team_id', string='Thành viên',
                               domain="[('groups_id', 'in', [ref('vitech_real_estate_core.real_estate_group_sale')])]")

  calc_member_ids = fields.Many2many(
    'res.users', string='Thành viên',
    domain=lambda self: self._get_member_ids_domain(),
    compute='_compute_member_ids', inverse='_inverse_member_ids', search='_search_member_ids',
    help="Users assigned to this team.")
  leader_id = fields.Many2one('res.users', string='Leader', domain=lambda self: self._get_combined_domain(), required=True)

  branch_id = fields.Many2one(comodel_name='res.company',string='Company', required=True, default=lambda self:self.env.company, domain=lambda self:[('id','in',self.env.companies.ids)])

  def _get_combined_domain(self):
    domain_group_sale_director = self.env['res.users']._get_only_users_in_group_sale_director_domain()
    sale_director = domain_group_sale_director.filtered(lambda s: (s.company_id.id == self.env.company.id) and(not s.team_id))
    # domain_share_false = [('share', '=', False),('team_id','=',False)]
    return [('id','in', sale_director.ids)]

  def _get_member_ids_domain(self):
    domain = self.env.ref('vitech_real_estate_core.real_estate_group_sale').users - self.env.ref('vitech_real_estate_core.real_estate_group_sale_director').users
    sale = domain.filtered(lambda u: (u.company_id.id == self.env.company.id) and (not u.team_id))
    return [('id','in', sale.ids)]

  @api.depends('member_ids.active')
  def _compute_member_ids(self):
    for team in self:
      team.calc_member_ids = team.member_ids

  def _inverse_member_ids(self):
    for team in self:
      # pre-save value to avoid having _compute_member_ids interfering
      # while building membership status
      memberships = team.member_ids
      users_current = team.calc_member_ids
      users_new = users_current - memberships.user_id

      # add missing memberships
      for user in users_new:
        user.write({'team_id': team.id})

  def _search_member_ids(self, operator, value):
    return [('member_ids.user_id', operator, value)]

  @api.constrains('leader_id')
  def _constraint_add_leader_into_team(self):
    for team in self:
      team.calc_member_ids += team.leader_id
    return {
      'type': 'ir.actions.client',
      'tag': 'reload',
    }



