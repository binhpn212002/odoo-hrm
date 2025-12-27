# -*- coding: utf-8 -*-
from odoo import models, fields, _


class HrmTheme(models.Model):
  _name = 'hrm.theme'
  _description = _('Vitech Theme')
  _rec_name = 'name'

  name = fields.Char(string=_("Name"))
  primary_color = fields.Selection([
    ('#434184', _('Black')),
    ('#D85959', _('Red')),
    ('#CECECE', _('Gray')),
    ('#9BEC00', _('Green')),
    ('#17AE92', _('Default')),
    ('#AA4585', _('Brown')),
    ('#3A30E2', _('Blue')),
    ('#7A19CA', _("Purple"))
  ], string=_("Primary Color"), default='#AA4585', help=_("Select the primary color for the user interface."))
  menuitem_color = fields.Selection([
    ('#A34484', _('Purple')),
    ('#CA19C1', _('Purple')),
    ('#D89959', _('Red')),
    ('#53aa45', _('Green')),
    ('#0B0D63', _('Default')),
  ], string=_("Menuitem Color"), default='#A34484', help=_("Select the primary color for the user interface."))

  secondary_color = fields.Selection([
    ('#FFDE00', _('Yellow')),
  ], string=_("Secondary Color"), default='#FFDE00', help=_("Select the primary color for the user interface."))

  info_color = fields.Selection([
    ('#006BFF', _('Sky')),
  ], string=_("Info color"), default='#006BFF', help=_("Select the primary color for the user interface."))

  dropdown_item_menu = fields.Selection([
    ('#FFFFFF', _('White')),
    ('#CECECE', _('Gray')),
  ], string=_("Menu List"), default='#FFFFFF', help=_("Select the primary color for the user interface."))