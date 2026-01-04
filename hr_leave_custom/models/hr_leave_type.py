# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    is_paid = fields.Boolean(string='Có lương', default=False)
    affect_bhxh = fields.Boolean(string='Tính BHXH', default=False)