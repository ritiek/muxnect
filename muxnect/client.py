import requests

class Client:
    def __init__(self, endpoint, default_data=None):
        self.default_data = default_data
        self.endpoint = endpoint

    def send(self, keys, data={}):
        data['keys'] = keys

        if isinstance(self.default_data, dict):
            override = self.default_data
            for item, value in data.items():
                override[item] = value
            data = override

        response = requests.post(self.endpoint, data=data)
        return response
