# -*- coding: utf-8 -*-
# from odoo import http


# class Tenrihotel(http.Controller):
#     @http.route('/tenrihotel/tenrihotel', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tenrihotel/tenrihotel/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tenrihotel.listing', {
#             'root': '/tenrihotel/tenrihotel',
#             'objects': http.request.env['tenrihotel.tenrihotel'].search([]),
#         })

#     @http.route('/tenrihotel/tenrihotel/objects/<model("tenrihotel.tenrihotel"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tenrihotel.object', {
#             'object': obj
#         })

from crypt import methods
import json


import json

from odoo import http, models, fields
from odoo.http import request


class TenriHotel(http.Controller):
    @http.route('/tenrihotel/getruangan', auth='public', method=['GET'])
    def getRuangan(self, **kw):
        # Mengambil semua barang dari table barang
        ruangan = request.env['tenrihotel.ruangan'].search([])
        items = []

        for item in barang:
            items.append({
                'nama_ruangan': item.name,
                'harga': item.harga,
                'jml_ruangan': item.jml_ruangan
            })
        
        return json.dumps(items)

	# Perubhannya di sini
    @http.route('/tenrihotel/gettiperuangan', auth='public', method=['GET'])
    def getTipeRuangan(self, **kw):
        supplier = request.env['tenrihotel.tiperuangan'].search([])
        items = []

        for item in tiperuangan:
            items.append({
                'nama': item.name,
                'kode_ruangan': item.kode_ruangan,
                'kode_lantai': item.kode_lantai,
                'ruangan_id': item.ruangan_id[0].name
            })
        
        return json.dumps(items)
