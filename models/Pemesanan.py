from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class Pemesanan(models.Model):
    _name = 'tenrihotel.pemesanan'
    _description = 'Pemesanan'

    name = fields.Char(string='No. Nota')
    nama_pembeli = fields.Char(string='Nama Pembeli')
    tgl_checkin = fields.Datetime(
        string='Tanggal Check-in',
        default=fields.Datetime.now())
    total_bayar = fields.Integer(
        string='Total Pembayaran',
        compute='_compute_totalbayar')
    detailpemesanan_ids = fields.One2many(
        comodel_name='tenrihotel.detailpemesanan',
        inverse_name='pemesanan_id',
        string='Detail Pemesanan')
        
    @api.depends('detailpemesanan_ids')
    def _compute_totalbayar(self):
        for line in self:
            result = sum(self.env['tenrihotel.detailpemesanan'].search(
                [('pemesanan_id', '=', line.id)]).mapped('subtotal'))
            line.total_bayar = result
    
    # @api.ondelete(at_uninstall=False)
    # def __ondelete_pemesanan(self):
    #     if self.detailpemesanan_ids:
    #         pemesanan = []
    #         for line in self:
    #             pemesanan = self.env['tenrihotel.detailpemesanan'].search(
    #                 [('pemesanan_id', '=', line.id)])
    #             print(pemesanan)

    #         for ob in pemesanan:
    #             print(str(ob.ruangan_id.name) + ' ' + str(ob.qty))
    #             ob.ruangan_id.jml_ruangan += ob.qty

    def unlink(self):
        if self.detailpemesanan_ids:
            pemesanan = []
            for line in self:
                pemesanan = self.env['tenrihotel.detailpemesanan'].search(
                    [('pemesanan_id', '=', line.id)])
                print(pemesanan)

            for ob in pemesanan:
                print(str(ob.ruangan_id.name) + ' ' + str(ob.qty))
                ob.ruangan_id.jml_ruangan += ob.qty

        line = super(Pemesanan, self).unlink()
    
    def write(self, vals):
        for line in self:
            pemesanan = self.env['tenrihotel.detailpemesanan'].search([('pemesanan_id','=', line.id)])
            print(pemesanan)
            for data in pemesanan:
                print(str(data.ruangan_id.name)+ ' ' +str(data.qty)+ ' ' +str(data.ruangan_id.jml_ruangan))
                data.ruangan_id.jml_ruangan += data.qty
        line = super(Pemesanan,self).write(vals)
        for line in self:
            pemesanan_brg = self.env['tenrihotel.detailpemesanan'].search([('pemesanan_id','=', line.id)])
            print(pemesanan_brg)
            print(pemesanan)
            for databaru in pemesanan_brg:
                if databaru in pemesanan:
                    print(str(databaru.ruangan_id.name)+ ' ' +str(databaru.qty)+ ' ' +str(databaru.ruangan_id.jml_ruangan))
                    databaru.ruangan_id.jml_ruangan -= databaru.qty
                else:
                    pass
        return line
    
    _sql_constraints = [
    ('no_nota_unik', 'unique (name)', 'Nomor Nota tidak boleh sama!')
    ]

class DetailPemesanan(models.Model):
    _name = 'tenrihotel.detailpemesanan'
    _description = 'Detail'

    name = fields.Char(string='Nama')
    pemesanan_id = fields.Many2one(
        comodel_name='tenrihotel.pemesanan',
        string='Detail')
    ruangan_id = fields.Many2one(
        comodel_name='tenrihotel.ruangan',
        string='List Ruangan')
    fasilitas_id = fields.Many2one(
        comodel_name='tenrihotel.fasilitas',
        string='List fasilitas')
    restoran_id = fields.Many2one(
        comodel_name='tenrihotel.restoran',
        string='List restoran')
    hrg_ruangan = fields.Integer(
        string='Harga ruangan',
        onchange='_onchange_ruangan_id')
    hrg_fasilitas = fields.Integer(
        string='Harga fasilitas',
        onchange='_onchange_fasilitas_id')
    hrg_restoran = fields.Integer(
        string='Harga fasilitas',
        onchange='_onchange_restoran_id')
    qty = fields.Integer(string='Qty ruangan')
    qty01 = fields.Integer(string='Qty fasilitas')
    qty02 = fields.Integer(string='Qty restoran')
    subtotal = fields.Integer(compute='_compute_subtotal', string='Subtotal')

    @api.depends('hrg_ruangan', 'hrg_fasilitas', 'hrg_restoran', 'qty', 'qty01', 'qty02')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.qty * line.hrg_ruangan + line.hrg_fasilitas * line.qty01 + line.qty02 * line.hrg_restoran

    @api.onchange('ruangan_id')
    def _onchange_ruangan_id(self):
        if self.ruangan_id.harga:
            self.hrg_ruangan = self.ruangan_id.harga
    
    @api.onchange('fasilitas_id')
    def _onchange_fasilitas_id(self):
        if self.fasilitas_id.harga:
            self.hrg_fasilitas = self.fasilitas_id.harga
    
    @api.onchange('restoran_id')
    def _onchange_restoran_id(self):
        if self.restoran_id.harga:
            self.hrg_restoran = self.restoran_id.harga
    
    
    @api.model
    def create(self, vals):
        line = super(DetailPemesanan, self).create(vals)
        if line.qty:
            # Mendapatkan data berdasarkan ID pada barang_id
            self.env['tenrihotel.ruangan'].search(
                [('id', '=', line.ruangan_id.id)]
            ).write({'jml_ruangan': line.ruangan_id.jml_ruangan - line.qty})
        return line

    @api.constrains('qty')
    def check_quantity(self):
        for line in self:
            if line.qty < 1:
                raise ValidationError('Jumlah pemesanan Ruangan harus minimal 1, silahkan input dengan benar!')
            elif line.ruangan_id.jml_ruangan < line.qty:
                raise ValidationError('Jumlah Ruangan tersedia saat ini tidak mencukupi.')
    