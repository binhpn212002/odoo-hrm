# -*- coding: utf-8 -*-

import threading
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    work_start_time = fields.Float(
        string='Giờ bắt đầu làm việc',
        config_parameter='hr_attendance_custom.work_start_time',
        help='Giờ bắt đầu làm việc (ví dụ: 8.0 = 08:00)'
    )

    work_end_time = fields.Float(
        string='Giờ kết thúc làm việc',
        config_parameter='hr_attendance_custom.work_end_time',
        help='Giờ kết thúc làm việc (ví dụ: 17.5 = 17:30)'
    )

    day_works = fields.Char(string='Các ngày làm việc', default='1,2,3,4,5')

    # Ngày làm việc từ 1 đến 7, không được lặp lại
    @api.constrains('day_works')
    def _check_day_works(self):
        for rec in self:
            list_day_works = rec.day_works.split(',')
            if len(list_day_works) != len(set(list_day_works)):
                raise ValidationError("Các ngày làm việc phải là duy nhất (không trùng lặp)")
            for day in list_day_works:
                if day not in ['1', '2', '3', '4', '5', '6', '7']:
                    raise ValidationError("Các ngày làm việc phải nằm trong khoảng từ 1 đến 7")


    @api.constrains('work_start_time', 'work_end_time')
    def _check_work_time(self):
        for rec in self:
            if rec.work_start_time < 0 or rec.work_start_time > 24:
                raise ValidationError("Giờ bắt đầu làm việc phải nằm trong khoảng 0 đến 24")

            if rec.work_end_time < 0 or rec.work_end_time > 24:
                raise ValidationError("Giờ kết thúc làm việc phải nằm trong khoảng 0 đến 24")

            if rec.work_start_time >= rec.work_end_time:
                raise ValidationError("Giờ kết thúc làm việc phải lớn hơn giờ bắt đầu")