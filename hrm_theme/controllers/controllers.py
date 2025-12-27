# -*- coding: utf-8 -*-
# from odoo import http


# class VitechRealEstateTheme(http.Controller):
#     @http.route('/vitech_real_estate_theme/vitech_real_estate_theme', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vitech_real_estate_theme/vitech_real_estate_theme/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('vitech_real_estate_theme.listing', {
#             'root': '/vitech_real_estate_theme/vitech_real_estate_theme',
#             'objects': http.request.env['vitech_real_estate_theme.vitech_real_estate_theme'].search([]),
#         })

#     @http.route('/vitech_real_estate_theme/vitech_real_estate_theme/objects/<model("vitech_real_estate_theme.vitech_real_estate_theme"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vitech_real_estate_theme.object', {
#             'object': obj
#         })

