# models/hr_ot_type_vn.py
from odoo import models, fields


class HrOTTypeVN(models.Model):
    _name = "hr.ot.type.vn"
    _description = "Vietnam OT Type"
    _order = "sequence"
    _rec_name = "name"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    sequence = fields.Integer(default=10)

    rate = fields.Float(string="OT Rate (%)", required=True, help="VD: 150 = 150%")

    is_night = fields.Boolean(string="Night OT")
    is_public_holiday = fields.Boolean(string="Public Holiday")
    is_weekend = fields.Boolean(string="Weekend")
    active = fields.Boolean(default=True)
    overtime_ids = fields.One2many("hr.overtime", "ot_type_id", string="Overtimes")

    _sql_constraints = [
        (
            "uniq_code_company",
            "unique(code, company_id)",
            "OT Type code must be unique per company",
        )
    ]
