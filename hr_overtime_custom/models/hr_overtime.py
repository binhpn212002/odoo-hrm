from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrOvertime(models.Model):
    _name = "hr.overtime"
    _description = "HR Overtime"
    _inherit = ["hr.attendance.overtime"]

    ot_type_id = fields.Many2one("hr.ot.type.vn", string="Loại tăng ca", required=True)

    state = fields.Selection(
        [
            ("draft", "Nháp"),
            ("cancel", "Đã hủy"),
            ("approved", "Đã duyệt"),
        ],
        string="Trạng thái",
        default="draft",
        tracking=True,
    )
    start_time = fields.Float(string="Giờ bắt đầu", help="Ví dụ: 18.5 = 18h30")
    end_time = fields.Float(string="Giờ kết thúc", help="Ví dụ: 21.0 = 21h")

    @api.model
    def create(self, vals):
        end_work_time = float(
            self.env["ir.config_parameter"].get_param(
                "hr_attendance_custom.work_end_time", "0"
            )
        )
        max_ot_duration = float(
            self.env["ir.config_parameter"].get_param(
                "hr_overtime_custom.max_ot_duration", "0"
            )
        )

        # check application leave in the day
        ot_day = vals["date"]
        is_time_off = self.env["hr.leave"].search(
            [
                ("request_date_from", "<=", ot_day),
                ("request_date_to", ">=", ot_day),
                ("employee_id", "=", vals["employee_id"]),
                ("state", "=", "validate"),
            ],
            limit=1,
        )
        if is_time_off:
            raise ValidationError("Đã có đơn nghỉ phép cho ngày này")
        # check max overtime duration
        duration = vals["duration"]
        if duration > max_ot_duration or duration <= 0:
            raise ValidationError(
                "Giờ tăng ca vượt quá giờ tối đa tăng ca hoặc không hợp lệ"
            )
        res = super(HrOvertime, self).create(vals)
        res.start_time = end_work_time
        res.end_time = end_work_time + res.duration
        return res

    @api.onchange("duration")
    def _onchange_start_end_time(self):
        end_work_time = float(
            self.env["ir.config_parameter"].get_param(
                "hr_attendance_custom.work_end_time", "0"
            )
        )

        for rec in self:
            if rec.duration:
                rec.start_time = end_work_time
                rec.end_time = end_work_time + rec.duration

    def action_approve(self):
        for rec in self:
            rec.state = "approved"

    def action_cancel(self):
        for rec in self:
            rec.state = "cancel"
