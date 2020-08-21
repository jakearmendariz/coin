'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
historical.py

Retrieves historical data about a cryptocurrency exchange rate over time from coinapi

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

from config import *
import json, datetime, requests, timedelta

class HistoricalData():
    def __init__(self):
        self.url = 'https://rest.coinapi.io/v1/ohlcv'
        self.type_of_request = '/history'
        self.headers = {'X-CoinAPI-Key' : COIN_API_KEY}
        return

    def specific_request(self, hours_back, period_id, exchange_type = '/BTC/USD'):
        today = datetime.datetime.now()
        days = 0
        # 2am 8 hours back -> - 1 day + 16 hrs -> (day = 1, hours_back = -16)
        if hours_back > today.hour:
            days = int(hours_back/24) + 1
            hours = 23 - today.hour + hours_back % 23
        else:
            hours = today.hour - hours_back
        time_start = today.replace(day = today.day - days, hour = hours).strftime("%Y-%m-%dT%H:%M:%S")
        return self.send_request(time_start, period_id, exchange_type)
    
    def get_data(self, window = 'day', exchange_type = '/BTC/USD'):
        today = datetime.datetime.now()
        if window == 'all':
            time_start = today.replace(year = today.year - 15).strftime("%Y-%m-%dT%H:%M:%S")
            period_id = '1YRS'
        elif window == 'year':
            time_start = today.replace(year = today.year - 1).strftime("%Y-%m-%dT%H:%M:%S")
            period_id = '1MTHS'
        elif window == 'month':
            time_start = today.replace(month = today.month - 1).strftime("%Y-%m-%dT%H:%M:%S")
            period_id = '1DAY'
        elif window == '2WK':
            time_start = today.replace(day = today.day - 14).strftime("%Y-%m-%dT%H:%M:%S")
            period_id = '1DAY'
        elif window == 'day':
            time_start = today.replace(day = today.day - 1).strftime("%Y-%m-%dT%H:%M:%S")
            period_id = '1HRS'
        elif window == 'hour':
            time_start = today.replace(hour = today.hour - 1).strftime("%Y-%m-%dT%H:%M:%S")
            period_id = '1MIN'
        else:
            return {"Error":"Invalid window: must be one of [day, month, year, all]"}
        
        return self.send_request(time_start, period_id, exchange_type)
        
    
    def send_request(self, time_start, period_id, exchange_type):
        url = self.url + exchange_type + self.type_of_request
        params = {
            'time_start':time_start,
            'period_id':period_id
        }
        response = requests.get(url, headers=self.headers, params = params)
        if(response.status_code is 200):
            return response.json()
        else:
            print("Error: status_code", response.status_code)
            return {}
    

if __name__ == "__main__":
    data = HistoricalData()
    print(json.dumps(data.get_data(), indent=3))

