from odoo import fields, models, api


class VitechSlider(models.Model):
    _name = 'vitech.slider'
    _description = 'Vitech Slider'


    name = fields.Char(string="Tiêu đề", required=True)
    image = fields.Image(string="Image", required=True)
    description = fields.Text(string="Mô tả")
    sequence = fields.Integer(string="Thứ tự sắp xếp", default=10)
    active = fields.Boolean(string="Kích hoạt", default=True)
    company_id = fields.Many2one(comodel_name='res.company',string='Company', required=True, default=lambda self:self.env.company, domain=lambda self: [('id', '=', self.env.company.id)])

