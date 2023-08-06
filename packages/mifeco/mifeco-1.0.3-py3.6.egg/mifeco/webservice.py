import base64
import requests
from requests.auth import HTTPBasicAuth
import sys, os, json
from urllib.parse import urlencode
from . login import Login
from . invoice import Invoice
from . note import Note
from . document_status import DocumentStatus
from . attach_rg import AttachRG
from . setters import DataSetter

class Webservice:
    is_production = False
    ssl_verify = True
    version = str('integrationAPI_2/')
    endpoint_test       = str('https://misfacturas.cenet.ws/')
    endpoint_production = str('https://www.misfacturas.com.co/')

    endpoints = {
                    'login_test':str(endpoint_test) + str(version) + str('api/login'), 
                    'login_production':str(endpoint_production) + str(version) + str('api/login'),

                    'invoice_test':str(endpoint_test) + str(version) + str('api/insertinvoice'), 
                    'invoice_production':str(endpoint_production) + str(version) + str('api/insertinvoice'),

                    'note_test':str(endpoint_test) + str(version) + str('api/insertnote'), 
                    'note_production':str(endpoint_production) + str(version) + str('api/insertnote'),

                    'document_status_test':str(endpoint_test) + str(version) + str('api/GetDocumentStatus'), 
                    'document_status_production':str(endpoint_production) + str(version) + str('api/GetDocumentStatus'),

                    'attach_rg_test':str(endpoint_test) + str(version) + str('api/AttachRG'), 
                    'attach_rg_production':str(endpoint_production) + str(version) + str('api/AttachRG'),

                    'contingency_test':str(endpoint_test) + str(version) + str('api/contingency'), 
                    'contingency_production':str(endpoint_production) + str(version) + str('api/contingency'),
                }   

    # Objects
    data_setter = None     
    
    def __init__(self, is_production, ssl_verify):
        self.is_production = is_production   
        self.ssl_verify = ssl_verify
        self.data_setter = DataSetter()
    
    def get_data_setter(self):        
        return self.data_setter

    def do_request(self, method, url_params = False, data = {}, headers={}, http_method="POST", is_file=False):
        response = None
        end_point = self.endpoints[str(method)]
        if(url_params):
            end_point = str(end_point) + str("?") + str(urlencode(url_params))  
             
        _request = requests.Request('POST', end_point, data=data)
        prepared = _request.prepare()
        _session = requests.Session()
        

        try:
            if(http_method=="POST"):
                if(is_file):                   
                    response = requests.post(end_point, headers=headers)
                    #return {'status':'success','response':response,"end_point":end_point}
                else:
                    response = requests.post(end_point, data=json.dumps(data), headers=headers)
                return {'status':'success','response':response.json()}
            else:
                return {'status':'fail','message':"Método HTTP no disponible: " +str("POST")}

        except Exception as e:
            xc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return {'status':'fail','message':str(getattr(e, 'message', repr(e)) + " ON LINE "+format(sys.exc_info()[-1].tb_lineno)) + str(" - ") + str(fname)}
        return response
    
    def call_login(self, params):
        _login = Login(params['username'], params['password'])
        method = str('login_production')
        if(not self.is_production):
            method = str('login_test')   
        headers =   {
                        "Content-Type":"application/json",
                    }           
        return self.do_request(method, url_params=_login.get_request_params(), data={},headers=headers)
    
    def call_invoice(self, params, data, token):
        _new_invoice = Invoice(params, data)
        method = str('invoice_production')
        if(not self.is_production):
            method = str('invoice_test')
        headers =   {
                        "Content-Type":"application/json",
                        "Authorization":"misfacturas " + str(token),
                        "Connection":"keep-alive",
                        "Accept-Encoding":"gzip, deflate, br",
                        "Accept":"*/*"
                    }
        return self.do_request(method, url_params=_new_invoice.get_request_params(), data=_new_invoice.get_request_data(), headers=headers)
    
    def call_note(self, params, data, token):
        _new_note = Note(params, data)
        method = str('note_production')
        if(not self.is_production):
            method = str('note_test')
        headers =   {
                        "Content-Type":"application/json",
                        "Authorization":"misfacturas " + str(token),
                        "Connection":"keep-alive",
                        "Accept-Encoding":"gzip, deflate, br",
                        "Accept":"*/*"
                    }
        return self.do_request(method, url_params=_new_note.get_request_params(), data=_new_note.get_request_data(), headers=headers)
    
    def call_document_status(self, params, data, token):
        _status = DocumentStatus(params, data)
        method = str('document_status_production')
        if(not self.is_production):
            method = str('document_status_test')
        headers =   {
                        "Content-Type":"application/json",
                        "Authorization":"misfacturas " + str(token),
                        "Connection":"keep-alive",
                        "Accept-Encoding":"gzip, deflate, br",
                        "Accept":"*/*"
                    }
        return self.do_request(method, url_params=_status.get_request_params(), data=_status.get_request_data(), headers=headers)

    def call_attach_rg(self, params, _file, file_name, token):    
        _attach_rg = AttachRG(params, {})
        method = str('attach_rg_production')
        if(not self.is_production):
            method = str('attach_rg_test')
        headers =   {
                        "Content-Type":"multipart/form-data",
                        "Authorization":"misfacturas " + str(token),
                        "Connection":"keep-alive",
                        "Accept-Encoding":"gzip, deflate, br",
                        "Accept":"*/*"
                    }
        
        return self.do_request(method, url_params=_attach_rg.get_request_params(), data=_attach_rg.get_request_data(), headers=headers, is_file=True)

    def fill_document_segment(self,segment_name,data):
        if('CustomerInformation' in str(segment_name)):
            return self.data_setter.fill_CustomerInformation(data)
            pass
        if('InvoiceGeneralInformation' in str(segment_name)):
            return self.data_setter.fill_InvoiceGeneralInformation(data)
            pass
        if('Delivery' in str(segment_name)):
            return self.data_setter.fill_Delivery(data)
            pass
        if('AdditionalDocuments' in str(segment_name)):
            return self.data_setter.fill_AdditionalDocuments(data)
            pass
        if('PaymentSummary' in str(segment_name)):
            return self.data_setter.fill_PaymentSummary(data)
            pass
        if('ItemInformation' in str(segment_name)):
            return self.data_setter.fill_ItemInformation(data)
            pass
        if('InvoiceTaxTotal' in str(segment_name)):
            return self.data_setter.fill_InvoiceTaxTotal(data)
            pass
        if('InvoiceAllowanceCharge' in str(segment_name)):
            return self.data_setter.fill_InvoiceAllowanceCharge(data)
            pass
        if('InvoiceTotal' in str(segment_name)):
            return self.data_setter.fill_InvoiceTotal(data)
            pass
        if('NoteGeneralInformation' in str(segment_name)):
            return self.data_setter.fill_NoteGeneralInformation(data)
            pass
        if('NoteTaxTotal' in str(segment_name)):
            return self.data_setter.fill_NoteTaxTotal(data)
            pass
        if('NoteTotal' in str(segment_name)):
            return self.data_setter.fill_NoteTotal(data)
            pass
        if('NoteAllowanceCharge' in str(segment_name)):
            return self.data_setter.fill_NoteAllowanceCharge(data)
            pass