# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResUserSettings(models.Model):
  _inherit = 'res.users'

  theme_id = fields.Many2one('vitech.theme', string=_('Theme'), help='Select a theme for the user')

  primary_color = fields.Selection(related="theme_id.primary_color", string=_("Primary Color"),
                                   help=_("Select the primary color for the user interface."))
  dropdown_item_menu = fields.Selection(related="theme_id.dropdown_item_menu",string=_("Menu List"),
                                   help=_("Select the primary color for the user interface."))
  secondary_color = fields.Char(string=_("Secondary color"))
  info_color = fields.Char(string=_("Info color"))
