from odoo import api, fields, models


class TipeRuangan(models.Model):
    _name = 'tenrihotel.tiperuangan'
    _description = 'New Description'

    name = fields.Selection([
        ('standart', 'Standart'),
        ('suporior', 'Suporior'),
        ('luxury', 'Luxury')
    ], string='Nama Kelompok')

    kode_ruangan = fields.Char(string='Kode Ruangan')
    
    @api.onchange('name')
    def _onchange_kode_ruangan(self):
        if self.name == 'standart':
            self.kode_ruangan = 'STAND01'
        elif self.name == 'suporior':
            self.kode_ruangan = 'SUP02'
        elif self.name == 'luxury':
            self.kode_ruangan = 'LUX01'

    ruangan_ids = fields.One2many(comodel_name='tenrihotel.ruangan',
                                inverse_name='tiperuangan_id',
                                string='Daftar Ruangan')
    
    jml_item = fields.Char(compute='_compute_jml_item', string='Jml Item')
    
	# Perubahannya di sini
    @api.depends('ruangan_ids')
    def _compute_jml_item(self):
        for record in self:
            a = self.env['tenrihotel.ruangan'].search([('tiperuangan_id', '=', record.id)]).mapped('name')
            b = len(a)
            record.jml_item = b
            record.daftar = a
    
    daftar = fields.Char(string='Daftar isi')