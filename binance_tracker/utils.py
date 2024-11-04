from binance.client import Client
from datetime import datetime

class BinanceAPI:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)
    
    def get_candle_change(self, symbol):
        candles = self.client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=2)
        last_candle = candles[-1]
        open_price = float(last_candle[1])
        close_price = float(last_candle[4])
        timestamp = int(last_candle[0])  # Timestamp of the candle open time

        percent_change = ((close_price - open_price) / open_price) * 100
        is_green = close_price > open_price

        # Convert timestamp to readable time
        time_str = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')

        return {
            "symbol": symbol,
            "open_price": open_price,
            "close_price": close_price,
            "percent_change": percent_change,
            "is_green": is_green,
            "time": time_str

        }
