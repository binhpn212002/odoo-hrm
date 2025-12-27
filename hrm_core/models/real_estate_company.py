from odoo import fields, models, api


class RealEstateCompany(models.Model):
    _name = 'res.company'
    _inherit = ['res.company']
    _description = 'real estate company'


    director_id = fields.Many2one(comodel_name='res.users', string='Director',required=True, domain=lambda self: self._get_combined_domain())
    team_ids = fields.One2many('vitech.real.estate.team', 'branch_id', string='Teams')
    company_code = fields.Char(string='Code')
    member_ids = fields.One2many(comodel_name="res.users", inverse_name='branch_member_id', string='Member')
    director_branch_id = fields.Many2one(comodel_name='res.users', string='Director branch',related='parent_id.director_id')

    def _get_combined_domain(self):
        domain_group_super_admin = self._get_users_in_group_super_admin_domain()
        # domain_share_false = [('share', '=', False)]
        return domain_group_super_admin

    def _get_users_in_group_super_admin_domain(self):
        group_general = self.env.ref('vitech_real_estate_core.real_estate_branch_general')
        return [('id', 'in', group_general.users.ids)]
    #
    # def _get_users_in_group_general_domain(self):
    #     branch_general = self.env.ref('vitech_real_estate_core.real_estate_branch_general')
    #     return [('id', 'in', branch_general.users.ids)]
