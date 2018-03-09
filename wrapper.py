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

    # Define functions for each command
    def getticker(self, pair):
        return self.process_command("getticker", "public",
                                    {'market': str(pair)})

    def getmarketsummaries(self):
        return self.process_command("getmarketsummaries", "public")

    def getmarketsummary(self, pair):
        return self.process_command("getmarketsummary", "public",
                                    {'market': str(pair)})

    # Booktype must be 'sell', 'buy', or 'both'
    def getorderbook(self, pair, booktype):
        return self.process_command("getorderbook", "public",
                                    {'market': str(pair),
                                     'type': booktype})

    def buylimit(self, pair, quantity, rate):
        return self.process_command("buylimit", "market",
                                    {'market': str(pair),
                                     'quantity': quantity,
                                     'rate': rate})

    def selllimit(self, pair, quantity, rate):
        return self.process_command("selllimit", "market",
                                    {'market': str(pair),
                                     'quantity': quantity,
                                     'rate': rate})

    def cancel(self, order_id):
        return self.process_command("cancel", "market",
                                    {'uuid': order_id})

    def getopenorders(self, pair):
        return self.process_command("getopenorders", "market",
                                    {'market': str(pair)})

    def getorderhistory(self, pair):
        return self.process_command("getorderhistory", "account")

    def getbalances(self):
        return self.process_command("getbalances", "account")

    def getbalance(self, pair):
        return self.process_command("getbalance", "account",
                                    {'currency': str(pair)})

    def getorder(self, order_id):
        return self.process_command("getorder", "account",
                                    {'uuid': order_id})
