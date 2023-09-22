# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging

class ReportXlsx(models.AbstractModel):
    _name='report.purchase_book.report_sale_xlsx'
    _inherit= 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        format1 = workbook.add_format({'font_size': 13, 'bold':True})
        format2 = workbook.add_format({'font_size': 10, 'text_wrap':True})
        
        money_format = workbook.add_format({'font_size': 10, 'num_format': '#,##0.00'})
        date_format = workbook.add_format({'font_size': 10, 'num_format': 'dd/mm/yyyy'})
        sheet= workbook.add_worksheet(partners.name)

        format1.set_align('center')
        format1.set_align('vcenter')

        format2.set_align('center')
        format2.set_align('vcenter')

        date_format.set_align('center')
        date_format.set_align('vcenter')

        money_format.set_align('center')
        money_format.set_align('vcenter')

        sheet.set_column('A:L', 25)

        sheet.write(0,2, 'Fecha de Libro', format1)
        sheet.write(0,3, partners.fecha_libro, format2)
        sheet.write(0,0, 'Descripcion', format1)
        sheet.write(0,1, partners.name, format2)
        sheet.write(0,4, 'Cantidad de Facturas', format1)
        sheet.write(0,5, partners.qty_invoice, format2)
        sheet.write(0,6, 'Monto Total', format1)
        sheet.write(0,7, partners.total, money_format)

        sheet.write(2,0, 'No.', format1)
        sheet.write(2,1, 'Fecha de Factura', date_format)
        sheet.write(2,2, 'NIT', format1)
        sheet.write(2,3, 'Cliente', format1)
        sheet.write(2,4, 'Serie de Factura', format1)
        sheet.write(2,5, 'Numero de Factura', format1)
        sheet.write(2,6, 'Bienes', format1)
        sheet.write(2,7, 'Servicios', format1)
        sheet.write(2,8, 'Exportaciones', format1)
        sheet.write(2,9, 'Ventas no Afectas', format1)
        sheet.write(2,10, 'IVA', format1)
        sheet.write(2,11, 'Total', format1)

        for index, record in enumerate(partners.invoice_sheet_id, start=2):
            sheet.write(index+1, 0, str(index), format2)
            sheet.write(index+1, 1, record["fecha_documento"], date_format)
            sheet.write(index+1, 2, record["nit"], format2)
            sheet.write(index+1, 3, record["cliente_id"].name, format2)
            sheet.write(index+1, 4, record["serie_factura"], format2)
            sheet.write(index+1, 5, record["no_factura"], format2)
            sheet.write(index+1, 6, record["bienes"], money_format)
            sheet.write(index+1, 7, record["servicios"], money_format)
            sheet.write(index+1, 8, record["exportaciones"], money_format)
            sheet.write(index+1, 9, record["ventas"], money_format)
            sheet.write(index+1, 10, record["iva"], money_format)
            sheet.write(index+1, 11, record["total"], money_format)
            

