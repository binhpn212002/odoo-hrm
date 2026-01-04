from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    @api.model
    def create(self, vals):
       date_from = vals['request_date_from']
       holiday_vn_id = self.env['hr.holiday.vn'].search([('date_from', '<=', date_from), ('date_to', '>=', date_from)], limit=1)
       if holiday_vn_id:
            raise ValidationError("Ngày nghỉ không được trùng với ngày nghỉ lễ")
       res = super(HrLeave, self).create(vals)
       return res