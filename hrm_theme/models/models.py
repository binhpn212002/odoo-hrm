# -*- coding: utf-8 -*-

from odoo import models, fields, api


class vitech_real_estate_theme(models.Model):
  _name = 'vitech_real_estate_theme'
  _description = 'vitech_real_estate_theme.vitech_real_estate_theme'

  name = fields.Char()
  value = fields.Integer()
  value2 = fields.Float(compute="_value_pc", store=True)
  description = fields.Text()
  test_theme_id = fields.Many2one(comodel_name='model.test.theme')

  @api.depends('value')
  def _value_pc(self):
    for record in self:
      record.value2 = float(record.value) / 100
