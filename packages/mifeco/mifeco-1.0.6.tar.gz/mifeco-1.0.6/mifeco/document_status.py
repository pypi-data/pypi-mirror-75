import base64
import requests
import sys

class DocumentStatus:
    params = {}
    data = {}

    def __init__(self, params, data):
        self.params = params
        self.data = data
        pass
    
    def get_request_params(self):
        return self.params

    def get_request_data(self):
        return self.data