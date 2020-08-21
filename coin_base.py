'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
coin_base.py

Buying and selling cryptocurrency

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase
from config import *

API_URL = 'https://api.pro.coinbase.com/'

# Create custom authentication for Exchange
class Coinbase(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or b'').decode()
        print('method:', request.method, 'req.url:', request.path_url, 'body:', (request.body or b'').decode())
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode()

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request
    
    #  balance USD, BTC, ETH
    def get_balance(self):
        usd, btc, eth = 0,0,0
        response = requests.get(API_URL + 'accounts', auth=Coinbase(COIN_BASE_KEY, COIN_BASE_SECRET, COIN_BASE_PASS)).json()
        for currency in response:
            if(currency['currency'] == 'USD'):
                usd = currency['balance']
            if(currency['currency'] == 'BTC'):
                btc = currency['balance']
            if(currency['currency'] == 'ETH'):
                eth = currency['balance']
        return usd, btc, eth

    def place_order(self, size, price, type, product_id, cancel_after='min'):
        order = {
            'size': size,
            'price': price,
            'side': type,
            'product_id': product_id,
            'cancel_after':cancel_after
        }
        r = requests.post(api_url + 'orders', json=order, auth=Coinbase(COIN_BASE_KEY, COIN_BASE_SECRET, COIN_BASE_PASS))


# api_url = 'https://api.pro.coinbase.com/'
# auth = Coinbase(COIN_BASE_KEY, COIN_BASE_SECRET, COIN_BASE_PASS)

# # Get accounts
# r = requests.get(api_url + 'accounts', auth=auth)
# print(json.dumps(r.json(), indent=3))

# Place an order
# order = {
#     'size': 0.00000,
#     'price': 1.0,
#     'side': 'buy',
#     'product_id': 'ETH-USD',
#     'cancel_after':'min'
# }
# r = requests.post(api_url + 'orders', json=order, auth=auth)
# print(r.json())
# {"id": "0428b97b-bec1-429e-a94c-59992926778d"}