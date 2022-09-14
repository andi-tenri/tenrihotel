from odoo import models, fields


class PartnerXlsx(models.AbstractModel):
    _name = 'report.tenrihotel.report_ruangan_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    tgl_laporan = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, ruangan):
        # One sheet by partner
        sheet = workbook.add_worksheet('Daftar Ruangan')
        # Menambahkan informasi tanggal laporan
        sheet.write(0, 0, str(self.tgl_laporan))
        sheet.write(1, 0, 'Nama Ruangan')
        sheet.write(1, 1, 'Jumlah orang')
        sheet.write(1, 2, 'Jumlah ruangan')
        sheet.write(1, 3, 'Harga')
        
        row = 2
        col = 0
        for obj in ruangan:
            col = 0
            # Text style bold, jjika tidak perlu bisa dihapus
            # bold = workbook.add_format({'bold': True})

            # write(row, col, title, style)
            # style bersifat opsional
            # sheet.write(0, 0, obj.name, bold)
            sheet.write(row, col, obj.name)
            sheet.write(row, col + 1, obj.jml_orang)
            sheet.write(row, col + 2, obj.jml_ruangan)
            sheet.write(row, col + 3, obj.harga)

            for item in obj.tiperuangan_id:
                sheet.write(row, col + 4, item.name)
                col += 1
            row += 1