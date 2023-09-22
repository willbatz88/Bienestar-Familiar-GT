from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests
import elementpath
import xml.etree.ElementTree as xml
from datetime import datetime
from pytz import timezone
import pytz
#import datetime

class account_move_inherit(models.Model):
    _inherit='account.move'

    validation_code = fields.Char(string='Codigo FEL', tracking=True)
    date_validation = fields.Datetime(string='Fecha de Validacion', tracking=True)

    def validate_invoice(self):
        URL_Token="https://felgttestaws.digifact.com.gt/gt.com.fel.api.v3/api/login/get_token"
        Params_token={"Username":"GT.000041545036.TESTUSER","Password":"j6C7&f5?"}
        response_token=requests.post(url=URL_Token, data=Params_token)
        resp= response_token.json()
        token= resp.get('Token')
        now_utc = datetime.now(timezone('UTC'))
        date= str(now_utc.astimezone(pytz.timezone('America/Guatemala')))
        date2= date.replace(' ', 'T')
        for rec in self:
            
            #Structure of the XML Format
            root = xml.Element("dte:GTDocumento", {'xmlns:xsi':"http://www.w3.org/2001/XMLSchema-instance", 'xmlns:dte':"http://www.sat.gob.gt/dte/fel/0.2.0", 'Version':"0.1"})
            f1= xml.SubElement(root, "dte:SAT",{'ClaseDocumento':"dte"})
            f11 = xml.SubElement(f1, "dte:DTE", {'ID':"DatosCertificados"})
            f2= xml.SubElement(f11, "dte:DatosEmision", {'ID':"DatosEmision"})
            f31= xml.SubElement(f2, "dte:DatosGenerales", {'Tipo':"FACT", 'FechaHoraEmision': date2[:19], 'CodigoMoneda': "GTQ"})
            f32= xml.SubElement(f2, "dte:Emisor", {'NITEmisor':"41545036", 'NombreEmisor':"Bienestar Familiar", 'CodigoEstablecimiento':"1", 'NombreComercial':"Bienestar Familiar", 'AfiliacionIVA':"GEN"})
            f321= xml.SubElement(f32, "dte:DireccionEmisor")
            f3211= xml.SubElement(f321, "dte:Direccion")
            f3211.text="Boulevard El Caminero 14-32, Zona 6 de Mixco"
            f3212= xml.SubElement(f321, "dte:CodigoPostal")
            f3212.text="01006"
            f3213=xml.SubElement(f321, "dte:Municipio")
            f3213.text="MIXCO"
            f3214=xml.SubElement(f321, "dte:Departamento")
            f3214.text="GUATEMALA"
            f3215=xml.SubElement(f321, "dte:Pais")
            f3215.text="GT"
            f33= xml.SubElement(f2, "dte:Receptor", {'NombreReceptor': rec.partner_id.name, 'CorreoReceptor':"sucorreo@gmail.com", 'IDReceptor':"CF"})
            f331= xml.SubElement(f33, "dte:DireccionReceptor")
            f3311= xml.SubElement(f331, "dte:Direccion")
            f3311.text="SECTOR 1 ESTANCIA DE LA VIRGEN"
            f3312= xml.SubElement(f331, "dte:CodigoPostal")
            f3312.text="01006"
            f3313=xml.SubElement(f331, "dte:Municipio")
            f3313.text="MIXCO"
            f3314=xml.SubElement(f331, "dte:Departamento")
            f3314.text="GUATEMALA"
            f3315=xml.SubElement(f331, "dte:Pais")
            f3315.text="GT"
            f34=xml.SubElement(f2, "dte:Frases")
            f341=xml.SubElement(f34, "dte:Frase", {'TipoFrase':"1", 'CodigoEscenario':"1"})
            Items=xml.SubElement(f2, "dte:Items")
            for item in rec.invoice_line_ids:
                Item= xml.SubElement(Items,'dte:Item', {'NumeroLinea':"1", 'BienOServicio':"B"})
                Cantidad= xml.SubElement(Item, 'dte:Cantidad')
                Cantidad.text= str(item.quantity)
                UnidadMedida= xml.SubElement(Item, 'dte:UnidadMedida')
                UnidadMedida.text= "CA"
                Descripcion= xml.SubElement(Item, 'dte:Descripcion')
                Descripcion.text= item.product_id.name
                PrecioUnitario= xml.SubElement(Item, 'dte:PrecioUnitario')
                PrecioUnitario.text= str(round(item.price_unit,2))
                Precio= xml.SubElement(Item, 'dte:Precio')
                price=(item.price_subtotal+(item.price_subtotal*(item.tax_ids.amount/100)))
                Precio.text= str(round(price,2))
                Descuento= xml.SubElement(Item, 'dte:Descuento')
                Descuento.text= "0"
                Impuestos =  xml.SubElement(Item, "dte:Impuestos")
                Impuesto = xml.SubElement(Impuestos, "dte:Impuesto")
                Nombre= xml.SubElement(Impuesto, "dte:NombreCorto")
                Nombre.text="IVA"
                CodigoUnidad= xml.SubElement(Impuesto, "dte:CodigoUnidadGravable")
                CodigoUnidad.text="1"
                MontoGravable = xml.SubElement(Impuesto, "dte:MontoGravable")
                MontoGravable.text = str(item.price_subtotal)
                MontoImpuesto = xml.SubElement(Impuesto, "dte:MontoImpuesto")
                tax= item.price_subtotal * (item.tax_ids.amount/100)
                MontoImpuesto.text = str(round(tax,2))
                Total =  xml.SubElement(Item, "dte:Total")
                Total.text = str(round(price,2))
            f36=xml.SubElement(f2, "dte:Totales")
            totalamount= rec.tax_totals.get('amount_total')
            untaxedTotal= rec.tax_totals.get('amount_untaxed')
            totalTax= totalamount-untaxedTotal
            TotalImpuestos= xml.SubElement(f36, "dte:TotalImpuestos")
            TotalImpuesto= xml.SubElement(TotalImpuestos, "dte:TotalImpuesto", {'NombreCorto': "IVA", 'TotalMontoImpuesto':str(round(totalTax,2))})
            GranTotal= xml.SubElement(f36, "dte:GranTotal")
            GranTotal.text= str(round(totalamount,2))
            tree= xml.tostring(root, encoding='utf8', method='xml', xml_declaration=True)
            
        URLCertificied= "https://felgttestaws.digifact.com.gt/gt.com.fel.api.v3/api/FelRequestV2"
        querystring = {"NIT":"000041545036","TIPO":"CERTIFICATE_DTE_XML_TOSIGN","FORMAT":"XML","USERNAME":"TESTUSER"}
        payload= tree
        header = {"Content-Type": "application/xml","Authorization": token}
        response = requests.post(url=URLCertificied, data=payload, headers=header, params=querystring)

        if response.status_code==200:
            response_autorizacion= response.json()
            gtm=pytz.timezone('America/Guatemala')
            utc= pytz.timezone('UTC')
            responsedate= response_autorizacion.get('Fecha_de_certificacion')
            date_time= datetime.strptime(responsedate, '%Y-%m-%dT%H:%M:%S')
            dategtm= gtm.localize(date_time)
            dateutc= dategtm.astimezone(utc)
            date_final= dateutc.strftime("%Y-%m-%d %H:%M:%S")
            autorizacion= response_autorizacion.get('Autorizacion')
            for rec in self:
                rec.date_validation= date_final
                rec.validation_code= autorizacion
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params':{
                        'title': _('Certificación Exitosa'),
                        'message': 'La factura ha sido certificada con Exito',
                        'sticky': False,
                    }
                }
        else:
            raise UserError(_('Ha ocurrido un error al ejecutar la operacion %s'%response.text))