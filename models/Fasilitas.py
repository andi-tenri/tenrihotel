from odoo import api, fields, models


class Fasilitas(models.Model):
    _name = 'tenrihotel.fasilitas'
    _description = 'New Description'

    name = fields.Selection([
        ('wash', 'Wash'),
        ('kolam renang', 'Kolam Renang'),
        ('fitnes  center', 'Fitnes Center')
    ], string='Nama Kelompok')

    kode_fasilitas = fields.Char(string='Kode Fasilitas')
    
    @api.onchange('name')
    def _onchange_kode_ruangan(self):
        if self.name == 'wash':
            self.kode_fasilitas = 'WASH01'
        elif self.name == 'kolam renang':
            self.kode_fasilitas = 'REG02'
        elif self.name == 'fitnes center':
            self.kode_fasilitas = 'FIT03'

    harga = fields.Integer(string='Harga')
    stok = fields.Integer(string='Stok')
    


   