# -*- coding: utf-8 -*-

import threading
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class HrPenaltyRewardMonthlySummary(models.Model):
    _name = "hr.penalty.reward.monthly.summary"
    _description = "Penalty Reward Monthly Summary"


    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
        required=True,
    )
    month = fields.Integer(string="Month", required=True, compute="_compute_month")
    year = fields.Integer(string="Year", required=True, compute="_compute_year")
    penalty_reward_date = fields.Date(string="Penalty Reward Date", required=True)
    total_penalty = fields.Float(string="Total Penalty",  default=0)
    total_reward = fields.Float(string="Total Reward", default=0)
    total_penalty_reward = fields.Float(string="Total Penalty Reward",  default=0)
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
    )
    @api.depends('penalty_reward_date')
    def _compute_month(self):
        for record in self:
            if record.penalty_reward_date:
                record.month = record.penalty_reward_date.month
            else:
                record.month = 0
    
    @api.depends('penalty_reward_date')
    def _compute_year(self):
        for record in self:
            if record.penalty_reward_date:
                record.year = record.penalty_reward_date.year
            else:
                record.year = 0
    @api.constrains('month')
    def _check_month(self):
        for record in self:
            if record.month < 1 or record.month > 12:
                raise ValidationError(_("The month must be between 1 and 12."))
    @api.constrains('year')
    def _check_year(self):
        for record in self:
            if record.year < 1900 or record.year > 2100:
                raise ValidationError(_("The year must be between 1900 and 2100."))