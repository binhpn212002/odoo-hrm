from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    max_days_year = fields.Integer(
        string='Max Days Year',
        default=12,
        help='Max Days Year'
    )

    max_days_year_increment = fields.Integer(
        string='Max Days Year Increment',
        default=1,
        help='Max Days Year Increment'
    )