# -*- coding: utf-8 -*-

import threading
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class HrAttendancePenaltyRule(models.Model):
    _name = 'hr.attendance.penalty.rule'
    _description = 'HR Attendance Penalty Rule'


    from_minutes = fields.Integer("From Minutes", default=0)
    to_minutes = fields.Integer("To Minutes", default=0)
    penalty_amount = fields.Float("Penalty Amount", digits=(16, 2))
    currency_id = fields.Many2one('res.currency', string="Currency")

    