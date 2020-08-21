'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
coin_api.py

Websocket for updates on crypto

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
from websocket import create_connection
import json
from invest import *
from config import *

pricing = [{
   "time": "2020-08-17T04:16:46.0182070Z",
   "asset_id_base": "BTC",
   "asset_id_quote": "USD",
   "rate": 11821.491440892429,
   "type": "exrate"
}]

bitcoin = Invest('/BTC/USD')

class CoinAPIv1_subscribe(object):
  def __init__(self, apikey):
    self.type = "hello"
    self.apikey = COIN_API_KEY
    self.heartbeat = False
    self.asset_id_base: "BTC"
    self.asset_id_quote: "USD"
    self.subscribe_data_type = ["exrate"]

ws = create_connection("wss://ws-sandbox.coinapi.io/v1/")
sub = CoinAPIv1_subscribe(COIN_API_KEY)
ws.send(json.dumps(sub.__dict__))
while True:
  msg =  ws.recv()
  exchange = json.loads(msg)
  # print(json.dumps(exchange, indent=3))
  if(exchange['asset_id_base'] == 'BTC' and exchange['asset_id_quote'] == 'USD'):
    if len(pricing) == 0:
      pricing.append((exchange['rate'], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1347517370))))
    else:
      change_in_price = pricing[-1]['rate'] - exchange['rate']
      # If the price changes by 2% send to server
      if abs(change_in_price) > bitcoin.watch_rate() :
          pricing.prepend((exchange['rate'], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1347517370))))
          th = threading.Thread(target=bitcoin.evaluate(pricing))
  
ws.close()
