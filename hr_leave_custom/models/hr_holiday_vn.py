# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, timedelta

class HrHolidayVn(models.Model):
    _name = 'hr.holiday.vn'
    _description = 'HR Holiday VN'

    name = fields.Char(string='Name' , required=True)
    year = fields.Integer(string='Year' , compute='_compute_year')
    date_from = fields.Date(string='Date From' , required=True)
    date_to = fields.Date(string='Date To' , required=True)


    @api.constrains('date_from', 'date_to')
    def _check_date_range(self):
        for record in self:
            if record.date_from >= record.date_to:
                raise ValidationError("Ngày bắt đầu phải nhỏ hơn ngày kết thúc và không được trùng nhau")

    @api.depends('date_from')
    def _compute_year(self):
        for record in self:
            record.year = record.date_from.year

    @api.model
    def _cron_auto_generate_public_holidays(self):
        today = date.today()
        year = today.year
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)

        fixed_holidays = [
            ('01-01', 'Tết Dương lịch'),
            ('30-04', 'Giải phóng Miền Nam'),
            ('01-05', 'Quốc tế Lao động'),
            ('02-09', 'Quốc khánh'),
        ]
        # search exist holidays in the year
        exist_holidays = self.search([('date_from', '>=', start_date), ('date_from', '<=', end_date)])
        if exist_holidays:
            return

        for holiday in fixed_holidays:
            self.create({
                'name': holiday[1],
                'date_from': date(year, int(holiday[0].split('-')[1]), int(holiday[0].split('-')[0])),
                'date_to': date(year, int(holiday[0].split('-')[1]), int(holiday[0].split('-')[0])),
                'year': year,
            })