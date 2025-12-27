from odoo import models, fields


class RealEstateSettings(models.TransientModel):
  _name = 'res.config.settings'
  _inherit = 'res.config.settings'

  hotline = fields.Char('HotLine', config_parameter='hrm_core.hotline', default='')

