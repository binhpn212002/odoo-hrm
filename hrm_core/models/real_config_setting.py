from odoo import models, fields


class RealEstateSettings(models.TransientModel):
  _name = 'res.config.settings'
  _inherit = 'res.config.settings'

  hotline = fields.Char('HotLine', config_parameter='vitech_real_estate_core.hotline', default='')

