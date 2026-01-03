# -*- coding: utf-8 -*-

import threading
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    max_ot_duration = fields.Float(
        string='Giờ tối đa tăng ca',
        config_parameter='hr_overtime_custom.max_ot_duration',
        help='Giờ tối đa tăng ca (ví dụ: 8.0 = 8h)'
    )

    @api.constrains('max_ot_duration')
    def _check_max_ot_duration(self):
        for rec in self:
            if rec.max_ot_duration <= 0 or rec.max_ot_duration > 5:
                raise ValidationError("Giờ tối đa tăng ca phải lớn hơn 0 và không vượt quá 5")
