import base64
import requests
import sys

class Login:
    username = None
    password = None

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def get_request_params(self):
        return {'username':self.username,'password':self.password}