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
        day_works = self.env['ir.config_parameter'].get_param('hr_attendance_custom.day_works', '1,2,3,4,5')
        employee_id = vals['employee_id']
        check_in_date = res['check_in'].date()

        exist_overtime = self.env['hr.overtime'].search([('employee_id', '=', employee_id), ('date', '=', check_in_date), ('state', '=', 'approved')], limit=1)
        exist_leave = self.env['hr.leave'].search([('employee_id', '=', employee_id), ('request_date_from', '<=', check_in_date), ('request_date_to', '>=', check_in_date), ('state', '=', 'validate')], limit=1)
        # checkIn conflict in day off or holiday
        if exist_leave:
            raise ValidationError("Đã có đơn nghỉ phép cho ngày này")
        if str(check_in_date.weekday()) not in day_works and not exist_overtime:
            raise ValidationError("Ngày này không phải là ngày làm việc")
        lately = work_start_time - float(res['check_in'].hour)
        if lately < 0:
            res.late_minutes =  abs(lately)
        if res['check_out']:
            early = work_end_time - float(res['check_out'].hour) * 60 + float(res['check_out'].minute)
            if early < 0:
                res.early_minutes = abs(early)

        return res

    


