import json

from odoo import http
from odoo.http import request

class SliderController(http.Controller):
    @http.route('/slider/images', type='json', auth='public')
    def get_slider_images(self):
        user = request.env.user
        current_company = user.company_id
        images = request.env['vitech.slider'].search([('active', '=', True),('company_id','=',current_company.id)], order='sequence asc')
        return [{'name': img.name, 'url': '/web/image/vitech.slider/%d/image' % img.id, 'description': img.description} for img in images]