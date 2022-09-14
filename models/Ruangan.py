from odoo import api, fields, models


class Ruangan(models.Model):
    _name = 'tenrihotel.ruangan'
    _description = 'New Description'

    name = fields.Char(string='Nama Ruangan')
    jml_orang = fields.Integer(string='Jumlah Orang', required=True)
    jml_ruangan = fields.Integer(string='Jumlah Ruangan')

    kode_lantai = fields.Selection([
        ('lantai 1', 'Lantai 1'),
        ('lantai 2', 'Lantai 2'),
        ('lantai 3', 'Lantai 3')
    ], string='kode_lantai')

    harga = fields.Integer(string='Harga', required=True)
    

    tiperuangan_id = fields.Many2one(comodel_name='tenrihotel.tiperuangan',
                                        string='Tipe Ruangan',
                                        ondelete='cascade')