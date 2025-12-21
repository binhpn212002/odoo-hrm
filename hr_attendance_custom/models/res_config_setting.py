# -*- coding: utf-8 -*-

import threading
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    work_start_time = fields.Float(
        string='Work Start Time',
        config_parameter='hr_attendance_custom.work_start_time',
        help='Giờ bắt đầu làm việc (ví dụ: 8.0 = 08:00)'
    )

    work_end_time = fields.Float(
        string='Work End Time',
        config_parameter='hr_attendance_custom.work_end_time',
        help='Giờ kết thúc làm việc (ví dụ: 17.5 = 17:30)'
    )


    @api.constrains('work_start_time', 'work_end_time')
    def _check_work_time(self):
        for rec in self:
            if rec.work_start_time < 0 or rec.work_start_time > 24:
                raise ValidationError("Work Start Time must be between 0 and 24")

            if rec.work_end_time < 0 or rec.work_end_time > 24:
                raise ValidationError("Work End Time must be between 0 and 24")

            if rec.work_start_time >= rec.work_end_time:
                raise ValidationError("Work End Time must be greater than Work Start Time")