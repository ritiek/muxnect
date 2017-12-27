import requests

class Client:
    def __init__(self, endpoint, defaults=None):
        self.defaults = None
        self.endpoint = endpoint

    def post(keys, data):
        if self.defaults:
            
        response = requests.post(self.endpoint, data=data)
        return response
