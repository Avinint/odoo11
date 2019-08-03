# -*- coding: utf-8 -*-
from odoo import http

# class Geography(http.Controller):
#     @http.route('/geography/geography/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/geography/geography/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('geography.listing', {
#             'root': '/geography/geography',
#             'objects': http.request.env['geography.geography'].search([]),
#         })

#     @http.route('/geography/geography/objects/<model("geography.geography"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('geography.object', {
#             'object': obj
#         })