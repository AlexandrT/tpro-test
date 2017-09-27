import requests
import logging
import json
import re

from config import settings

logger = logging.getLogger('public_api')

class ApiRequest:
    methods = ("get", "put", "post", "delete")
    payload = {}
    headers = {}
    reqType = ""
    url = ""

    def _dump_request(fn):
        def magic(self, url, reqType):
            req = fn(self, url, reqType)

            output = f"{self.reqType.upper()}-request will be send to {self.url}"

            headers = json.dumps(self.headers)
            if len(self.headers) == 0:
                output += f" without any headers"
            else:
                output += f" with headers {headers}"

            payload = json.dumps(self.payload)
            if len(self.payload) != 0:
                output += f" with payload {payload}"

            logger.info(output)
            return req
        return magic

    def _dump_response(fn):
        def magic(self):
            response = fn(self)
            logger.info(f'Response {response.text} with headers {response.headers}')
            return response
        return magic

    def set_data(self, payload):
        self.payload = payload

    @_dump_request
    def prepare_request(self, url, reqType):
        self.reqType = reqType
        self.url = url

        reqType = reqType.lower()

        if reqType not in self.methods:
            print ("[ERROR] Unknown request type")
            raise Exception(f"Unknown request type {reqType}")


    @_dump_response
    def send(self):
        attr = self.reqType.lower()
        method = getattr(requests, attr)
        r = method(self.url, headers=self.headers, json=self.payload)

        return r

    def add_headers(self, headers):
        self.headers = {**self.headers, **headers}

    def build(self, request_type, request_path, **kwargs):
        uri = url(request_path)
        uri += get_query(**kwargs) if kwargs is not None else None
        self.prepare_request(uri, request_type)

        r = self.send()

        return r

    def auth(self):
        pass

def url(request_path):
    return settings.API_URL + request_path

def get_query(**kwargs):
    output = f"?"

    for param in kwargs:
        output += f"{param}={kwargs[param]}&"

    output = re.sub('[&, ?]*$', '', output)

    return output
