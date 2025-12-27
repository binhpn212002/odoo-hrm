# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ModelTestTheme(models.Model):
  _name = 'model.test.theme'
  _inherit = ["mail.thread"]
  _description = 'Description'

  name = fields.Char(string='name')
  age = fields.Integer(string='age')
  text_selection = fields.Selection(string='selection', selection=([('action', 'Action'),
                                                                    ('report', 'Report')]))
  test_many2many = fields.One2many(comodel_name='vitech_real_estate_theme', inverse_name='test_theme_id')
