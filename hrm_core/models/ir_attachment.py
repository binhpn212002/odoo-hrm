from odoo import models, fields, api


class IrAttachment(models.Model):
  _inherit = 'ir.attachment'

  model_owner = fields.Boolean(string='Model Owner', default=False)
