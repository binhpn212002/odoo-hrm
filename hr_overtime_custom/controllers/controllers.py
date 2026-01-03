# -*- coding: utf-8 -*-
# from odoo import http


# class HrOvertimeCustom(http.Controller):
#     @http.route('/hr_overtime_custom/hr_overtime_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_overtime_custom/hr_overtime_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_overtime_custom.listing', {
#             'root': '/hr_overtime_custom/hr_overtime_custom',
#             'objects': http.request.env['hr_overtime_custom.hr_overtime_custom'].search([]),
#         })

#     @http.route('/hr_overtime_custom/hr_overtime_custom/objects/<model("hr_overtime_custom.hr_overtime_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_overtime_custom.object', {
#             'object': obj
#         })

