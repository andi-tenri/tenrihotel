from odoo import api, fields, models


class Restoran(models.Model):
    _name = 'tenrihotel.restoran'
    _description = 'New Description'

    name = fields.Char(string='Nama Makanan')
    stok = fields.Integer(string='stok', required=True)
    harga = fields.Integer(string='Harga', required=True)

    restoranitem_id = fields.Many2one(comodel_name='tenrihotel.restoranitem',
                                        string='Jenis Makanan',
                                        ondelete='cascade')