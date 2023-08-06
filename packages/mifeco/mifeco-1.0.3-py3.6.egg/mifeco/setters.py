import base64
import requests
import sys

class DataSetter:
    def __init__(self):
        pass
    
    # SETTERS FOR ELECTRONIC INVOICES

    def fill_InvoiceGeneralInformation(self, data):
        invoice_general_information =  {
                                            "InvoiceAuthorizationNumber": data['dian']['autorizacion']['codigo'],
                                            #"PreinvoiceNumber": 1, (opcional) Número de prefectura si el emisor no maneja la numeración de factura.
                                            "InvoiceNumber": str(data['numero']),
                                            "DaysOff": str(data['diasVencimiento']),
                                            "Currency": str(data['tipoMoneda']),                                            
                                            "SalesPerson": str(data['vendedor']),
                                            "Note": str(self.get_document_note(data)) + str(" ") + str(data['tipoMoneda'])
                                        }

        if(str(data["exportacion"]["exportation"]["es_exportacion"]) == str("True")):        
                invoice_general_information["ExchangeRate"] = str(data["exportacion"]["exportation"]["calculo_rate"])
                invoice_general_information["ExchangeRateDate"] = str(data["exportacion"]["exportation"]["calculation_date"])
          
        return invoice_general_information
    
    def fill_NoteGeneralInformation(self, data):
        note_general_information = {
                                        "NoteNumber": str(data['numero']),
                                        "CUFE": str(data['documentoOrigenCUFE']),
                                        "ReferenceID": str(data['documentoOrigen']),
                                        "IssueDate": str(data['fechaEmision'])+str("T00:00:00"),
                                        "DiscrepancyCode": str(data['notaDiscrepanciaCode']),
                                        "Currency": str(data['tipoMoneda'])
                                    }
        return note_general_information

    def fill_CustomerInformation(self, data):
        customer_information =  {
                                    "IdentificationType": str(data['receptor']['tipo_documento']),
                                    "Identification": str(data['receptor']['nro']),
                                    "DV": str(data['receptor']['vat_dv']),
                                    "RegistrationName": str(data['receptor']['nombre']),
                                    "CountryCode": str(data['receptor']['codigoPais']),
                                    "CountryName": str(data['receptor']['nombrePais']),
                                    "SubdivisionCode": str(data['receptor']['municipio_code'])[:2],
                                    "SubdivisionName": str(data['receptor']['departamento']),
                                    "CityCode": str(data['receptor']['municipio_code']),
                                    "CityName": str(data['receptor']['municipio']),
                                    "AddressLine": str(data['receptor']['direccion']),
                                    "Telephone": str(data['receptor']['telefono']),
                                    "Email": str(data['receptor']['correo_electronico']),
                                    "CustomerCode": str(data['receptor']['id_platform']), # custom
                                    "AdditionalAccountID": str(data["receptor"]["tipo_persona"]),
                                    "TaxLevelCodeListName": str(data["receptor"]["regimen"])
                                }
        return customer_information       
    
    def fill_Delivery(self, data):        
        delivery =  {
                        "AddressLine": str(data['receptor']['ubicacion_entrega']['direccion']),
                        "CountryCode": str(data['receptor']['ubicacion_entrega']['codigoPais']),
                        "CountryName": str(data['receptor']['ubicacion_entrega']['nombrePais']),
                        "SubdivisionCode": str(data['receptor']['ubicacion_entrega']['municipio_code'])[:2],
                        "SubdivisionName": str(data['receptor']['departamento']),
                        "CityCode": str(data['receptor']['ubicacion_entrega']['municipio_code']),
                        "CityName": str(data['receptor']['ubicacion_entrega']['municipio']),
                        "ContactPerson": str(data['receptor']['ubicacion_entrega']['nombre']),
                    }

        if('envio' in data):
            if(data['envio']):
                if('fecha' in data['envio']):
                    delivery['DeliveryDate'] = data['envio']['fecha']
                if('transportista' in data['envio']):
                    delivery['DeliveryCompany'] = data['envio']['transportista']

        return delivery
    
    def fill_AdditionalDocuments(self, data):
        additional_documents = {}
        if(data['documento_origen']):
            additional_documents["ReceiptDocumentReference"] = data['documento_origen']
        
        return additional_documents
    
    def fill_PaymentSummary(self, data):
        if('pago' not in data):
            return {}
        payment_summary =  {
                                "PaymentType": str(data['pago']['dian_payment_means_id']),
                                "PaymentMeans": str(data['pago']['payment_means_code']),
                                "PaymentNote": str(data['pago']['payment_reference'])
                            }
        return payment_summary
    
    def fill_ItemInformation(self, data):
        _items = []
        items = data["items"]
        for item in items:
            _item = {
                        "ItemReference": str(item['id']),
                        "Name": str(item['descripcion']),
                        "Quatity": str(item['cantidad']),
                        "Price": str(item['precioUnidad']),
                        "LineAllowanceTotal": self.fill_LineAllowanceTotal(item), # discount 
                        #"LineChargeTotal": 0, # charge
                        "LineTotalTaxes": self.fill_LineTotalTaxes(item),
                        "LineTotal": self.get_money(item['totalVenta']),
                        "LineExtensionAmount": self.get_money(item['subTotalVenta']),
                        "MeasureUnitCode": str(item['unidadMedida']),
                        "FreeOFChargeIndicator": "false", # True si el ítem es un regalo que no genera contraprestación y por ende no es una venta. False si no es un regalo.                    }
                        "AdditionalReference": [],
                        "AdditionalProperty": [],
                        "TaxesInformation": self.fill_TaxesInformation(item), 
                        "AllowanceCharge": self.fill_ItemAllowanceCharge(item), # ChargeIndicator True si se trata de un cargo False si se trata de un descuento
                    }
            _items.append(_item)
            
        return _items
    
    def fill_ItemAllowanceCharge(self, item):  
        item_allowance_charge = []     
        if('descuento' not in item):
            return item_allowance_charge
        descuento = item['descuento']
        if('codigo' not in descuento):
            return item_allowance_charge
        _discount = {
                        "Id": str(descuento['codigo']),
                        "ChargeIndicator": "false",
                        "AllowanceChargeReason": str(descuento['razon']),
                        "MultiplierFactorNumeric":str(descuento['porcentaje']),
                        "Amount": self.get_money(descuento['monto']),
                        "BaseAmount": self.get_money(float(item['cantidad']) * float(item['precioUnidad']))
                    }
        # espacio para cargos
        item_allowance_charge.append(_discount)
        return item_allowance_charge
    
    def fill_LineAllowanceTotal(self, item):   
        if('descuento' not in item):
            return str(0.0)
        descuento = item['descuento']
        if('codigo' not in descuento):
            return str(0.0)
        return self.get_money(descuento['monto'])
    
    def fill_InvoiceTaxTotal(self, data):        
        return self.get_TaxTotal(data) 
    
    def fill_InvoiceAllowanceCharge(self, data):
        _allowance_charge = []
        if('descuentos' not in data):
            return _allowance_charge
        descuentos = data['descuentos']['globales']
        for descuento in descuentos:
            _descuento =   {
                                "Id": str(descuento['codigo']),
                                "ChargeIndicator": "false",
                                "AllowanceChargeReason": str(descuento['razon']),
                                "MultiplierFactorNumeric": str(descuento['porcentaje']),
                                "Amount": self.get_money(descuento['monto']),
                                "BaseAmount": self.fill_AllowanceChargeBaseAmount(data)
                            }
            _allowance_charge.append(_descuento)
        # espacio para cargos
        return _allowance_charge
    
    def fill_AllowanceChargeBaseAmount(self, data):
        base_amount = 0.0
        items = data["items"]
        for item in items:
            base_amount += (float(item['cantidad']) * float(item['precioUnidad']))
        return self.get_money(base_amount)
    
    def fill_TaxesInformation(self, item):
        _tributos = []

        if('tributos' not in item):
            return float(0.0)
        tributos = item["tributos"]
        
        for tributo in tributos:
            _tributo = {
                            "Id": str(tributo['codigo']),
                            "TaxEvidenceIndicator": "false",
                            "TaxableAmount": self.get_money(tributo['total_venta']),
                            "TaxAmount": self.get_money(tributo['montoAfectacionTributo']),
                            "Percent": str(tributo['porcentaje'])
                        }

            if(str(tributo['codigo']) == str("22")):
                    _tributo['BaseUnitMeasure'] = str(tributo['unidadMedida'])
                    _tributo['PerUnitAmount'] = str(tributo['porcentaje'])
            else:
                _tributo['Percent'] = str(tributo['porcentaje'])
                
            if(float(self.get_money(tributo['montoAfectacionTributo']))>0):
                _tributos.append(_tributo)
        return _tributos

    def fill_LineTotalTaxes(self, item):
        total_taxes = float(0.0)
        if('tributos' not in item):
            return float(0.0)
        tributos = item["tributos"]
        for tributo in tributos:
            total_taxes += float(tributo['montoAfectacionTributo'])
        return format(float(total_taxes), '.2f')
    
    def fill_InvoiceTotal(self, data):
        invoice_total = {
                            "LineExtensionAmount": self.fill_Total_LineExtensionAmount(data),
                            "TaxExclusiveAmount": self.fill_Total_TaxExclusiveAmount(data),
                            "TaxInclusiveAmount": self.fill_Total_TaxInclusiveAmount(data),
                            "AllowanceTotalAmount": self.fill_AllowanceTotalAmount(data), # descuentos
                            #"ChargeTotalAmount": 10000.00,  # cargo
                            # "PrePaidAmount": 0.0, # Total anticipios o prepagos
                            "PayableAmount": self.fill_PayableAmount(data)
                        }
        return invoice_total 

    def fill_AllowanceTotalAmount(self, data):  
        _total = float(0)
        if('descuentos' not in data):
            return _total
        descuentos = data['descuentos']['globales']
        for descuento in descuentos:
            _total = float(_total) + float(descuento['monto'])
         
        return self.get_money(_total)

    def fill_PayableAmount(self, data):
        total_a_pagar = 0.0
        total_con_impuestos = self.fill_Total_TaxInclusiveAmount(data)
        total_a_pagar += float(total_con_impuestos)
        # agregar descuentos y cargos para completar el total a pagar
        return self.get_money(total_a_pagar)
    
    def fill_Total_TaxExclusiveAmount(self, data):
        items = data["items"]
        tributes_per_item = []
        for item in items:
            tributes_per_item.append(self.fill_TaxesInformation(item))
        
        total_tax_exclusive_amount = float(0.0)
        for _tribute_per_item in tributes_per_item:
                for _tributo in _tribute_per_item:
                    total_tax_exclusive_amount += float(_tributo['TaxableAmount'])
        return self.get_money(total_tax_exclusive_amount)

    def fill_Total_TaxInclusiveAmount(self, data):
        items = data["items"]
        tributes_per_item = []
        for item in items:
            tributes_per_item.append(self.fill_TaxesInformation(item))
        
        total_tax_inclusive_amount = float(0.0)
        for _tribute_per_item in tributes_per_item:
                for _tributo in _tribute_per_item:
                    total_tax_inclusive_amount += float(_tributo['TaxAmount'])
        
        total_tax_exclusive_amount = float(self.fill_Total_TaxExclusiveAmount(data))
        total_tax_inclusive_amount += float(total_tax_exclusive_amount)
        return self.get_money(total_tax_inclusive_amount)

    def fill_Total_LineExtensionAmount(self, data):
        total_line_extension_amount = float(0.0)
        items = data["items"]
        for item in items:
            total_line_extension_amount += float(self.get_money(item['subTotalVenta']))
        return self.get_money(total_line_extension_amount)

    
    def fill_NoteTaxTotal(self, data):
        return self.get_TaxTotal(data)
    
    def fill_NoteTotal(self, data):
        note_total =    {
                            "LineExtensionAmount": self.fill_Total_LineExtensionAmount(data),
                            "TaxExclusiveAmount": self.fill_Total_TaxExclusiveAmount(data),
                            "TaxInclusiveAmount": self.fill_Total_TaxInclusiveAmount(data),
                            "AllowanceTotalAmount": self.fill_AllowanceTotalAmount(data),
                            #"ChargeTotalAmount": 10000.00,  # cargo
                            # "PrePaidAmount": 0.0, # Total anticipios o prepagos
                            "PayableAmount": self.fill_PayableAmount(data)
                        }
        return note_total
    
    def fill_NoteAllowanceCharge(self, data):
        return self.fill_InvoiceAllowanceCharge(data)       
    
    def get_TaxTotal(self, data):
        if('tributos' not in data):
            return float(0.0)
        tributos_globales = data['tributos']
        _tributo_Taxes_Information = []
        for tributo_code in tributos_globales:
            lista_tributos = tributos_globales[str(tributo_code)]
            for _tributo in lista_tributos: 

                _tributo_Tax_Information = {
                                                "Id": str(_tributo['codigo']),
                                                # "TaxEvidenceIndicator": "false", # True si se trata de una retención False si se trata de un impuesto.
                                                "TaxableAmount": self.get_money(_tributo['total_venta']),
                                                "TaxAmount": self.get_money(_tributo['sumatoria']),
                                            }
                
                if(str(_tributo['codigo']) == str("22")):
                    _tributo_Tax_Information['BaseUnitMeasure'] = str(_tributo['unidadMedida'])
                    _tributo_Tax_Information['PerUnitAmount'] = str(_tributo['porcentaje'])
                else:
                    _tributo_Tax_Information['Percent'] = str(_tributo['porcentaje'])

                if(float(self.get_money(_tributo['sumatoria']))>0):
                    _tributo_Taxes_Information.append(_tributo_Tax_Information)
        return _tributo_Taxes_Information     
    
    def get_money(self, value):
        return format(float(value), '.2f')

    def get_document_note(self, data):
        return str(self.total_en_letras(data["totalVentaGravada"]))    
    
    def total_en_letras(self, numero):
        indicador = [("", ""), ("MIL", "MIL"), ("MILLON", "MILLONES"),
                     ("MIL", "MIL"), ("BILLON", "BILLONES")]
        entero = int(numero)
        decimal = int(round((numero - entero)*100))
        # print 'decimal : ',decimal
        contador = 0
        numero_letras = ""
        while entero > 0:
            a = entero % 1000
            if contador == 0:
                en_letras = self.total_en_letras_algoritmo(a, 1).strip()
            else:
                en_letras = self.total_en_letras_algoritmo(a, 0).strip()
            if a == 0:
                numero_letras = en_letras+" "+numero_letras
            elif a == 1:
                if contador in (1, 3):
                    numero_letras = indicador[contador][0]+" "+numero_letras
                else:
                    numero_letras = en_letras+" " + \
                        indicador[contador][0]+" "+numero_letras
            else:
                numero_letras = en_letras+" " + \
                    indicador[contador][1]+" "+numero_letras
            numero_letras = numero_letras.strip()
            contador = contador + 1
            entero = int(entero / 1000)
        numero_letras = numero_letras
        return numero_letras

    def total_en_letras_algoritmo(self, numero, sw):
        lista_centana = ["", ("CIEN", "CIENTO"), "DOSCIENTOS", "TRESCIENTOS", "CUATROCIENTOS",
                         "QUINIENTOS", "SEISCIENTOS", "SETECIENTOS", "OCHOCIENTOS", "NOVECIENTOS"]
        lista_decena = ["", ("DIEZ", "ONCE", "DOCE", "TRECE", "CATORCE", "QUINCE", "DIECISEIS", "DIECISIETE", "DIECIOCHO", "DIECINUEVE"),
                        ("VEINTE", "VEINTI"), ("TREINTA",
                                               "TREINTA Y "), ("CUARENTA", "CUARENTA Y "),
                        ("CINCUENTA", "CINCUENTA Y "), ("SESENTA", "SESENTA Y "),
                        ("SETENTA", "SETENTA Y "), ("OCHENTA", "OCHENTA Y "),
                        ("NOVENTA", "NOVENTA Y ")
                        ]
        lista_unidad = ["", ("UN", "UNO"), "DOS", "TRES",
                        "CUATRO", "CINCO", "SEIS", "SIETE", "OCHO", "NUEVE"]
        centena = int(numero / 100)
        decena = int((numero - (centena * 100))/10)
        unidad = int(numero - (centena * 100 + decena * 10))
        # print "centena: ",centena, "decena: ",decena,'unidad: ',unidad

        texto_centena = ""
        texto_decena = ""
        texto_unidad = ""

        # Validad las centenas
        texto_centena = lista_centana[centena]
        if centena == 1:
            if (decena + unidad) != 0:
                texto_centena = texto_centena[1]
            else:
                texto_centena = texto_centena[0]

        # Valida las decenas
        texto_decena = lista_decena[decena]
        if decena == 1:
            texto_decena = texto_decena[unidad]
        elif decena > 1:
            if unidad != 0:
                texto_decena = texto_decena[1]
            else:
                texto_decena = texto_decena[0]
        # Validar las unidades
        # print "texto_unidad: ",texto_unidad
        if decena != 1:
            texto_unidad = lista_unidad[unidad]
            if unidad == 1:
                texto_unidad = texto_unidad[sw]

        return "%s %s %s" % (texto_centena, texto_decena, texto_unidad)