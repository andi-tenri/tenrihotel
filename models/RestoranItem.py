from odoo import api, fields, models


class RestoranItem(models.Model):
    _name = 'tenrihotel.restoranitem'
    _description = 'New Description'

    name = fields.Selection([
        ('breakfash', 'Breakfash'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner')
    ], string='Nama Kelompok')
    
    kode_kelompok = fields.Char(string='Kode Kelompok')

    @api.onchange('name')
    def _onchange_kode_kelompok(self):
        if self.name == 'breakfash':
            self.kode_kelompok = 'EAT01'
        elif self.name == 'lunch':
            self.kode_kelompok = 'EAT02'
        elif self.name == 'dinner':
            self.kode_kelompok = 'EAT01'

    restoran_ids = fields.One2many(comodel_name='tenrihotel.restoran',
                                inverse_name='restoranitem_id',
                                string='Daftar Keompok')

    jml_item = fields.Char(compute='_compute_jml_item', string='Jumlah Item')
    
    @api.depends('restoran_ids')
    def _compute_jml_item(self):
        for record in self:
            a = self.env['tenrihotel.restoran'].search([('restoranitem_id', '=', record.id)]).mapped('name')
            b = len(a)
            record.jml_item = b
            record.daftar = a
    
    daftar = fields.Char(string='Daftar isi')