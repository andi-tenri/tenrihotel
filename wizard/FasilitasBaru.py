from odoo import api, fields, models


'''
Membuat model BarangDarang yang inherit
ke Transient Model, Odoo 14 ke atas harus
di daftarkan di security
'''
class FasilitasBaru(models.TransientModel):
    _name = 'tenrihotel.fasilitasbaru'

    fasilitas_id = fields.Many2one(comodel_name='tenrihotel.fasilitas', string='Nama Barang', required=True)
    jumlah = fields.Integer(string='Jumlah', required=False)

    def button_fasilitas_baru(self):
        for line in self:
            self.env['tenrihotel.fasilitas'].search([('id', '=', line.fasilitas_id.id)]).write(
                {'stok': line.fasilitas_id.stok +  line.jumlah}
            )