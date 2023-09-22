# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging

class ReportXlsx(models.AbstractModel):
    _name='report.purchase_book.report_purchase_xlsx'
    _inherit= 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        format1 = workbook.add_format({'font_size': 13, 'text_wrap':True, 'bold':True})
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
        
        sheet.write(0,0, 'Fecha de Libro', format1)
        sheet.write(0,1, partners.fecha_libro, format2)
        sheet.write(0,2, 'Descripcion', format1)
        sheet.write(0,3, partners.name, format2)
        sheet.write(0,4, 'Cantidad de Facturas', format1)
        sheet.write(0,5, partners.qty_invoice, format2)
        sheet.write(0,6, 'Monto Total', format1)
        sheet.write(0,7, partners.total, money_format)

        sheet.write(2,0, 'Linea', format1)
        sheet.write(2,1, 'Fecha de Factura', format1)
        sheet.write(2,2, 'Tipo de Documento', format1)
        sheet.write(2,3, 'No. de Serie', format1)
        sheet.write(2,4, 'No. de Factura', format1)
        sheet.write(2,5, 'NIT', format1)
        sheet.write(2,6, 'Nombre', format1)
        sheet.write(2,7, 'Compras', format1)
        sheet.write(2,8, 'Servicios', format1)
        sheet.write(2,9, 'Tasa Municipal', format1)
        sheet.write(2,10, 'Turismo por Hospedaje', format1)
        sheet.write(2,11, 'Timbre de Prensa', format1)
        sheet.write(2,12, 'IDP', format1)
        sheet.write(2,13, 'Combustibles', format1)
        sheet.write(2,14, 'Fac. de Pequeño Contribuyente compra', format1)
        sheet.write(2,15, 'Factura Especial', format1)
        sheet.write(2,16, 'IVA Credito', format1)
        sheet.write(2,17, 'Total', format1)


        for index, record in enumerate(partners.invoice_sheet_id, start=3):
            sheet.write(index+1, 0, str(index), format2)
            sheet.write(index+1, 1, record["fecha_documento"], date_format)
            sheet.write(index+1, 2, record["tipo_documento"], format2)
            sheet.write(index+1, 3, record["serie_factura"], format2)
            sheet.write(index+1, 4, record["no_factura"], format2)
            sheet.write(index+1, 5, record["nit"], format2)
            sheet.write(index+1, 6, record["proveedor_id"].name, format2)
            sheet.write(index+1, 7, record["compras"], money_format)
            sheet.write(index+1, 8, record["servicios"], money_format)
            sheet.write(index+1, 9, record["tasa_municipal"], money_format)
            sheet.write(index+1, 10, record["turismo_hospedaje"], money_format)
            sheet.write(index+1, 11, record["timbre_prensa"], money_format)
            sheet.write(index+1, 12, record["idp"], money_format)
            sheet.write(index+1, 13, record["combustible"], money_format)
            sheet.write(index+1, 14, record["fac_fpq"], money_format)
            sheet.write(index+1, 15, record["factura_especial"], money_format)
            sheet.write(index+1, 16, record["iva_credito"], money_format)
            sheet.write(index+1, 17, record["total"], money_format)
            

