# binance_tracker/views.py
from django.shortcuts import render 
import re
from django.http import JsonResponse
from .utils import BinanceAPI

api = BinanceAPI("S1XP1VKlOxfhGEuQoAxTX40XHxY2D4Cu4ILK1Go0glXgefUO0oUdLWfv6tzNoytK", "Qjdcx14iRfMLUBFjycDUQBwU1ZpcR1vzjduwMKCTqK5YqJ0RZo6lyrVBhR4VC1YT")

# Regex to validate valid Binance symbols
symbol_pattern = re.compile(r'^[A-Z0-9-_.]{1,20}$')

# Cache to store last candle data to avoid repetitions
last_candles = {}

def get_candles(request):
    symbols = [
    "1000SATSUSDT", "1INCHUSDT", "AAVEUSDT", "ACAUSDT", "ACEUSDT", "ACHUSDT", "ACMUSDT", "ADAUSDT", "ADXUSDT",
    "AERGOUSDT", "AEURUSDT", "AEVOUSDT", "AGLDUSDT", "AIUSDT", "AKROUSDT", "ALCXUSDT", "ALGOUSDT", "ALICEUSDT", 
    "ALPACAUSDT", "ALPHAUSDT", "ALPINEUSDT", "ALTUSDT", "AMBUSDT", "AMPUSDT", "ANKRUSDT", "APEUSDT", "API3USDT", 
    "APTUSDT", "ARBUSDT", "ARDRUSDT", "ARKMUSDT", "ARKUSDT", "ARPAUSDT", "ARUSDT", "ASRUSDT", "ASTRUSDT", 
    "ASTUSDT", "ATAUSDT", "ATMUSDT", "ATOMUSDT", "AUCTIONUSDT", "AUDIOUSDT", "AVAUSDT", "AVAXUSDT", "AXLUSDT", 
    "AXSUSDT", "BADGERUSDT", "BAKEUSDT", "BALUSDT", "BANANAUSDT", "BANDUSDT", "BARUSDT", "BATUSDT", "BBUSDT", 
    "BCHUSDT", "BEAMXUSDT", "BELUSDT", "BETAUSDT", "BICOUSDT", "BIFIUSDT", "BLURUSDT", "BLZUSDT", "BNBUSDT", 
    "BNTUSDT", "BNXUSDT", "BOMEUSDT", "BONKUSDT", "BSWUSDT", "BTCUSDT", "BTTCUSDT", "BURGERUSDT", "C98USDT", 
    "CAKEUSDT", "CELOUSDT", "CELRUSDT", "CFXUSDT", "CHESSUSDT", "CHRUSDT", "CHZUSDT", "CITYUSDT", "CKBUSDT", 
    "CLVUSDT", "COMBOUSDT", "COMPUSDT", "COSUSDT", "COTIUSDT", "CREAMUSDT", "CRVUSDT", "CTKUSDT", "CTSIUSDT", 
    "CTXCUSDT", "CVCUSDT", "CVXUSDT", "CYBERUSDT", "DARUSDT", "DASHUSDT", "DATAUSDT", "DCRUSDT", "DEGOUSDT", 
    "DENTUSDT", "DEXEUSDT", "DFUSDT", "DGBUSDT", "DIAUSDT", "DODOUSDT", "DOGEUSDT", "DOGSUSDT", "DOTUSDT", 
    "DUSKUSDT", "DYDXUSDT", "DYMUSDT", "EDUUSDT", "EGLDUSDT", "ELFUSDT", "ENAUSDT", "ENJUSDT", "ENSUSDT", 
    "EOSUSDT", "ERNUSDT", "ETCUSDT", "ETHFIUSDT", "ETHUSDT", "EURIUSDT", "EURUSDT", "FARMUSDT", "FDUSDUSDT", 
    "FETUSDT", "FIDAUSDT", "FILUSDT", "FIOUSDT", "FIROUSDT", "FISUSDT", "FLMUSDT", "FLOKIUSDT", "FLOWUSDT", 
    "FLUXUSDT", "FORTHUSDT", "FTMUSDT", "FTTUSDT", "FUNUSDT", "FXSUSDT", "GALAUSDT", "GASUSDT", "GFTUSDT", 
    "GHSTUSDT", "GLMRUSDT", "GLMUSDT", "GMTUSDT", "GMXUSDT", "GNOUSDT", "GNSUSDT", "GRTUSDT", "GTCUSDT", 
    "GUSDT", "HARDUSDT", "HBARUSDT", "HFTUSDT", "HIFIUSDT", "HIGHUSDT", "HIVEUSDT", "HOOKUSDT", "HOTUSDT", 
    "ICPUSDT", "ICXUSDT", "IDEXUSDT", "IDUSDT", "ILVUSDT", "IMXUSDT", "INJUSDT", "IOSTUSDT", "IOTAUSDT", 
    "IOTXUSDT", "IOUSDT", "IQUSDT", "IRISUSDT", "JASMYUSDT", "JOEUSDT", "JSTUSDT"
]



    candle_changes = []
    significant_changes = []  # Store changes > 0.5% decrease

    for symbol in symbols:
        try:
            candle_data = api.get_candle_change(symbol)
            if symbol not in last_candles or candle_data['close_price'] != last_candles[symbol]['close_price']:
                last_candles[symbol] = candle_data
                candle_changes.append(candle_data)
                
                # If the decrease is more than 0.5%
                if not candle_data['is_green'] and abs(candle_data['percent_change']) > 0.5:
                    significant_changes.append(candle_data)
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

    # If it's an AJAX request, return JSON data
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'candle_changes': candle_changes,
            'significant_changes': significant_changes
        })
    
    # Otherwise, render the template
    return render(request, 'candles.html', {})
