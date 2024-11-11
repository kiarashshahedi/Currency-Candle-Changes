# binance_tracker/views.py
from django.shortcuts import render 
import re
from django.http import JsonResponse
from .utils import BinanceAPI
import requests




def send_telegram_notification(message):
    bot_token = '8110703357:AAEmAarnot50gxjhWXrrs3HUdYMGlOePabA'
    channel_id = '-1002405237232'
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': channel_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Raise an error on unsuccessful requests
    except requests.exceptions.RequestException as e:
        print(f"Error sending Telegram notification: {e}")


def notify_significant_changes(changes):
    if changes:  # Check if the list has items
        # Format each change to only include symbol and percent_change
        formatted_changes = "\n".join([f"- {change['symbol']}: {change['percent_change']:.2f}%" for change in changes])
        message = f"<b>Significant Decreases (> 1%)</b>:\n{formatted_changes}"
        send_telegram_notification(message)
    else:
        print("No significant changes to send.")




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
    "IOTXUSDT", "IOUSDT", "IQUSDT", "IRISUSDT", "JASMYUSDT", "JOEUSDT", "JSTUSDT", "JTOUSDT", "JUPUSDT",
    "JUVUSDT", "KAVAUSDT", "KDAUSDT", "KEYUSDT", "KLAYUSDT", "KMDUSDT", "KNCUSDT", "KP3RUSDT", "KSMUSDT",
    "LAZIOUSDT", "LDOUSDT", "LEVERUSDT", "LINAUSDT", "LINKUSDT", "LISTAUSDT", "LITUSDT", "LOKAUSDT", "LPTUSDT",
    "LQTYUSDT", "LRCUSDT", "LSKUSDT", "LTCUSDT", "LTOUSDT", "LUNAUSDT", "LUNCUSDT", "MAGICUSDT", "MANAUSDT",
    "MANTAUSDT", "MASKUSDT", "MATICUSDT", "MAVUSDT", "MBLUSDT", "MBOXUSDT", "MDTUSDT", "MEMEUSDT", "METISUSDT",
    "MINAUSDT", "MKRUSDT", "MLNUSDT", "MOVRUSDT", "MTLUSDT", "NEARUSDT", "NEOUSDT", "NEXOUSDT", "NFPUSDT",
    "NKNUSDT", "NMRUSDT", "NOTUSDT", "NTRNUSDT", "NULSUSDT", "OAXUSDT", "OGNUSDT", "OGUSDT", "OMNIUSDT",
    "OMUSDT", "ONEUSDT", "ONGUSDT", "ONTUSDT", "OOKIUSDT", "OPUSDT", "ORDIUSDT", "ORNUSDT", "OSMOUSDT",
    "OXTUSDT", "PAXGUSDT", "PDAUSDT", "PENDLEUSDT", "PEOPLEUSDT", "PEPEUSDT", "PERPUSDT", "PHAUSDT", "PHBUSDT",
    "PIVXUSDT", "PIXELUSDT", "POLYXUSDT", "PONDUSDT", "PORTALUSDT", "PORTOUSDT", "POWRUSDT", "PROMUSDT",
    "PROSUSDT", "PSGUSDT", "PUNDIXUSDT", "PYRUSDT", "PYTHUSDT", "QIUSDT", "QKCUSDT", "QNTUSDT", "QTUMUSDT",
    "QUICKUSDT", "RADUSDT", "RAREUSDT", "RAYUSDT", "RDNTUSDT", "REIUSDT", "RENDERUSDT", "RENUSDT", "REQUSDT",
    "REZUSDT", "RIFUSDT", "RLCUSDT", "RONINUSDT", "ROSEUSDT", "RPLUSDT", "RSRUSDT", "RUNEUSDT", "RVNUSDT",
    "SAGAUSDT", "SANDUSDT", "SANTOSUSDT", "SCRTUSDT", "SCUSDT", "SEIUSDT", "SFPUSDT", "SHIBUSDT", "SKLUSDT",
    "SLFUSDT", "SLPUSDT", "SNTUSDT", "SNXUSDT", "SOLUSDT", "SPELLUSDT", "SSVUSDT", "STEEMUSDT", "STGUSDT",
    "STMXUSDT", "STORJUSDT", "STPTUSDT", "STRAXUSDT", "STRKUSDT", "STXUSDT", "SUIUSDT", "SUNUSDT", "SUPERUSDT",
    "SUSHIUSDT", "SXPUSDT", "SYNUSDT", "SYSUSDT", "TAOUSDT", "TFUELUSDT", "THETAUSDT", "TIAUSDT", "TKOUSDT",
    "TLMUSDT", "TNSRUSDT", "TONUSDT", "TRBUSDT", "TROYUSDT", "TRUUSDT", "TRXUSDT", "TUSDT", "TUSDUSDT",
    "TWTUSDT", "UFTUSDT", "UMAUSDT", "UNFIUSDT", "UNIUSDT", "USDCUSDT", "USDPUSDT", "USTCUSDT", "UTKUSDT",
    "VANRYUSDT", "VETUSDT", "VGXUSDT", "VIDTUSDT", "VITEUSDT", "VOXELUSDT", "VTHOUSDT", "WAVESUSDT", "WAXUSDT",
    "WBTCUSDT", "WEMIXUSDT", "WINUSDT", "WOOUSDT", "WRXUSDT", "WSIUSDT", "WTCUSDT", "XECUSDT", "XEMUSDT",
    "XLMUSDT", "XMRUSDT", "XNOUSDT", "XRPUSDT", "XTZUSDT", "XVGUSDT", "XVSUSDT", "YFIUSDT", "YGGUSDT",
    "YUNUSDT", "ZECUSDT", "ZENUSDT", "ZILUSDT", "ZRXUSDT"
]



    candle_changes = []
    significant_changes = []  # Store changes > 0.5% decrease

    for symbol in symbols:
        try:
            candle_data = api.get_candle_change(symbol)
            if symbol not in last_candles or candle_data['close_price'] != last_candles[symbol]['close_price']:
                last_candles[symbol] = candle_data
                candle_changes.append(candle_data)

                if not candle_data['is_green'] and abs(candle_data['percent_change']) > 1:
                    significant_changes.append(candle_data)
                    # Send notification to Telegram
                    notify_significant_changes(significant_changes)

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

