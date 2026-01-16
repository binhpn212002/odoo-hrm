import threading

from ebaysdk.utils import parse_yaml

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    overtime_ids = fields.One2many(
        'hr.overtime',
        'employee_id',
        string='Overtimes'
    )