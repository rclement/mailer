import json


class JsonRequest:
    def __init__(self, data):
        self.json = json.dumps(data)
        self.content_type = "application/json"
