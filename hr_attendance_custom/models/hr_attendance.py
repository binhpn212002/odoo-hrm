# -*- coding: utf-8 -*-

import threading
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    late_minutes = fields.Integer("Late Minutes", default=0)
    early_minutes = fields.Integer("Early Minutes", default=0)

    @api.model
    def create(self, vals):
        res = super(HrAttendance, self).create(vals)
        work_start_time = float(self.env['ir.config_parameter'].get_param('hr_attendance_custom.work_start_time', '0'))
        work_end_time = float(self.env['ir.config_parameter'].get_param('hr_attendance_custom.work_end_time', '0'))
        lately = work_start_time - float(res['check_in'].hour)
        if lately < 0:
            res.late_minutes =  abs(lately)
        if res['check_out']:
            early = work_end_time - float(res['check_out'].hour) * 60 + float(res['check_out'].minute)
            if early < 0:
                res.early_minutes = abs(early)

        return res

    


