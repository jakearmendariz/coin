'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
invest.py

Decision making for investing

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
from historical import *
import threading
import time
class Invest():
    def __init__(self, exchange_type = '/BTC/USD'):
        self.history = HistoricalData()
        self.exchange_type = exchange_type
        # self.low, self.high, self.data = self.get_low_and_high(self.history.get_data('all'))
        # self.year_low, self.year_high, self.year_data = self.get_low_and_high(self.history.get_data('year'))
        self.month_low, self.month_high, self.month_data = self.get_low_and_high(self.history.get_data('month))
        self.watch_rate = (self.month_low + self.month_high)/2 * 0.02
        print("Invest class setup complete")

    def get_low_and_high(self, data):
        low = 100000
        high = 0
        for obj in data:
            if obj['price_high'] > high:
                high = obj['price_high']
            if obj['price_low'] < low:
                low = obj['price_low']
        return low, high, data

    def rate_of_change(self, hours, period):
        data = self.history.specific_request(hours, period, exchange_type = self.exchange_type)
        derivative = []
        prev_price = data[0]['price_close']
        for i in range(1, len(data)):
            derivative.append(data[i]['price_close'] - prev_price)
            prev_price = data[i]['price_close']

        return derivative

    def rsi(self, current_price):
        data = self.history.get_data('2WK', self.exchange_type)
        prev_day = data[0]['price_close']
        increase = 0
        decrease = 0
        for i in range(1, len(data)):
            if prev_day > data[i]['price_close']:
                increase = ( prev_day - data[i]['price_close'] ) / prev_day
            else:
                decrease = ( data[i]['price_close'] - prev_day ) / prev_day
            
            prev_data = data[i]
        
        if prev_day > current_price:
            increase = ( prev_day - current_price ) / prev_day
        else:
            decrease = ( current_price - prev_day ) / prev_day
        
        return 100 - 100/(1 + increase/decrease)
    
    def advise(self, current_price):
        today_change = [x/current_price for x in self.rate_of_change(24, '1HRS')]
        two_hour_change = [x/current_price for x in self.rate_of_change(2, '4MIN')]
        thirty_min_change = two_hour_change[22:]

        accel_today = sum(today_change)/24
        accel_recent = sum(two_hour_change)/30
        thirty_min_change = sum(thirty_min_change)/8
        
        print("accel today:", accel_today,'accel two hour',accel_recent,'accel 30 minute' ,thirty_min_change)
        change_predictor = (150 + (accel_today + accel_recent +  thirty_min_change)*30000 )/3
        print("Change predictor", change_predictor)
        result = ( change_predictor * 2 + self.rsi(current_price) ) / 3
        print("result:", result)
        return result

    def print_analysis(self, current_price):
        print("Exchange rates for " + self.exchange_type)
        # print("all:", self.low, self.high)
        # print("year:", self.year_low, self.year_high)
        # print("month:", self.month_low, self.month_high)
        today_change = self.rate_of_change(24, '1HRS')
        recent_change = self.rate_of_change(2, '4MIN')
        accel_today = sum(today_change)/24
        accel_recent = sum(recent_change)/30
        print("rate of change for a day:", today_change, accel_today)
        print("rate of change for 3 hours:", recent_change, accel_recent)
        print("RSI", self.rsi(current_price))
        print("current price:", current_price)

    # Every element in list is 2% off from the others
    def evaluate(self, pricing):
        if(price[0][0] > price[1][0]): # If price is increasing
            self.consider_buying(pricing)
        else:                           # If price is decreasing
            self.consider_selling(pricing)

    def consider_buying(self, pricing): 
        i = 1
        while i < len(pricing):
            if(pricing[i][0] < pricing[i-1][0]):
                # Decreasing towards localmin
                i += 1
            else:
                break
        # i * 2 % of pure desent
        i += 1
        while i < len(pricing):
            if(pricing[i][0] < pricing[i-1][0]):
                # Decreasing towards localmin
                i += 1
            else:
                break
        # In case of one off step
        i -=1

        
        pass 
    
    def consider_selling(self, pricing):
        pass
    
    def watch_rate(self):
        return self.watch_rate

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

ideal buy:
    local-minimum was the last step
    increasing price average

ideal sell:
    local maximum was the last step
    increasing since then


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

