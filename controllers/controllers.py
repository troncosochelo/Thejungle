# -*- coding: utf-8 -*-
from odoo import http

# class Restaurante(http.Controller):
#     @http.route('/restaurante/restaurante/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/restaurante/restaurante/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('restaurante.listing', {
#             'root': '/restaurante/restaurante',
#             'objects': http.request.env['restaurante.restaurante'].search([]),
#         })

#     @http.route('/restaurante/restaurante/objects/<model("restaurante.restaurante"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('restaurante.object', {
#             'object': obj
#         })