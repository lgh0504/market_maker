# Wrapper for the Bittrex public api
# Created on September 25, 2017
# By Izak Fritz

import urllib.request
from urllib.parse import urlencode
import hmac
import hashlib
import json
import requests
import time

class bittrex_wrapper:
    def __init__(self):
        private_data = open("keys.txt", "r")
        key = private_data.readline().rstrip('\n')
        secret = private_data.readline().rstrip('\n')

        self.key = key
        self.secret = secret
        self.url = 'https://bittrex.com/api/v1.1/{req_type}/{cmnd}?'

    def process_command(self, cmnd, req_type, args={}):
        # Process public commands below
        nonce = str(int(time.time() * 1000))
        request_url = self.url.format(req_type=req_type, cmnd=cmnd)

        if req_type != 'public':
            request_url = "{0}apikey={1}&nonce={2}&".format(
                request_url, self.key, nonce)

        request_url += urlencode(args)

        apisign = hmac.new(self.secret.encode(),
                           request_url.encode(),
                           hashlib.sha512).hexdigest()

        return requests.get(request_url, headers={"apisign": apisign}).json()
