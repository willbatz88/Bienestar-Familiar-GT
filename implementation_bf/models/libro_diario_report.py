# -*- coding: utf-8 -*-
from odoo import models
from itertools import groupby
from operator import itemgetter
import datetime

class ReportXlsx(models.AbstractModel):
    _name='report.implementation_bf.report_libro_diario_xlsx'
    _inherit= 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, seat):

        format1 = workbook.add_format({'font_size': 13, 'text_wrap':True, 'bold':True})
        format2 = workbook.add_format({'font_size': 10, 'text_wrap':True})     
        money_format = workbook.add_format({'font_size': 10, 'num_format': '#,##0.00'})
        date_format = workbook.add_format({'font_size': 10, 'num_format': 'dd/mm/yyyy'})
        format1.set_align('center')
        format1.set_align('vcenter')

        format2.set_align('center')
        format2.set_align('vcenter')

        date_format.set_align('center')
        date_format.set_align('vcenter')

        money_format.set_align('center')
        money_format.set_align('vcenter')
        sheet= workbook.add_worksheet('Asientos Contables')

        sheet.set_column('A:L', 25)

        date = datetime.date.today()

        values = data['accounts']
        form_data = data['form_data']
        sheet.merge_range(1, 1, 1, 4, 'BIENESTAR FAMILIAR, S.A.', format1)
        sheet.write(1,5, date, date_format)
        sheet.merge_range(3, 1, 3, 4, 'Libro Diario', format1)

        sheet.write(4,0, 'Periodo', format1)
        sheet.write(4,1, 'Desde', format1)
        sheet.write(4,2, form_data['date_begin'], date_format)
        sheet.write(4,3, 'Hasta', format1)
        sheet.write(4,4, form_data['date_end'], date_format)

        row = 6
        col = 1
        sheet.write(row, col, 'Fecha', format1)
        sheet.write(row, col + 1, 'Cuenta Contable', format1)
        sheet.write(row, col + 2, 'Debe', format1)
        sheet.write(row, col + 3, 'Haber', format1)

        values = sorted(values, key= itemgetter('asiento'))
        total_credit = 0
        total_debit = 0
 
        for key, account in groupby(values, key = itemgetter('asiento')):
            row += 1
            total_credit = 0
            total_debit = 0
            comentario = ''
            move_type = ''
            
            if key:
                sheet.merge_range(row, col, row, col + 4, key, format1)
            else:
                sheet.merge_range(row, col, row, col + 4, account['move_id'][1], format1)
            for value in account:
                row += 1
                sheet.write(row, col, value['date'], date_format)
                sheet.write(row, col + 1, value['account_id'][1], format2)
                sheet.write(row, col + 2, value['debit'], money_format)
                sheet.write(row, col + 3, value['credit'], money_format)
                total_credit += value['credit']
                total_debit += value['debit']
                move_type = value['move_type']
                comentario = value['comentario']
            row += 1
           
            if move_type == 'out_invoice':
                sheet.write(row, col, 'Factura de Cliente', format2)
            elif move_type == 'out_refund':
                sheet.write(row, col, 'Nota de Debito', format2)
            elif move_type == 'in_invoice':
                sheet.write(row, col, 'Factura de Proveedor', format2)
            elif move_type == 'in_refund':
                sheet.write(row, col, 'Nota de Credito', format2)
                
            sheet.write(row, col + 1, comentario, format2)
            sheet.write(row, col + 2, total_debit, money_format)
            sheet.write(row, col + 3, total_credit, money_format)
            row += 1