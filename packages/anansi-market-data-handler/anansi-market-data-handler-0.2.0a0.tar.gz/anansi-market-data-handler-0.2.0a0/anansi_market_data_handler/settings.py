class TimeFrames:
    seconds_dict = {
        "1m": 60,
        "3m": 180,
        "5m": 300,
        "15m": 900,
        "30m": 1800,
        "1h": 3600,
        "2h": 7200,
        "4h": 14400,
        "6h": 21600,
        "12h": 43200,
        "1d": 86400,
        "1w": 604800,
    }

    def __init__(self):
        pass

    def seconds_in(self, time_frame):
        return self.seconds_dict[time_frame]


klines_desired_info = [
    "Open_time",
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
]  # , "Close_time"]


# TODO: API key and secret from get os.environment ou default = None
class Binance_:
    api_key = None
    api_secret = None
    DateTimeFmt = 'timestamp'
    DateTimeUnit = 'milliseconds'
    _base_endpoint = "https://api.binance.com/api/v3/"
    _ping_endpoint = _base_endpoint + "ping"
    _time_endpoint = _base_endpoint + "time"
    _klines_endpoint = _base_endpoint + "klines?symbol={}&interval={}"
    _request_weight_per_minute = 1100  # Default: 1200/min/IP
    records_per_request = 500  # Default: 500 | Limit: 1000 samples/response

    kline_information_map = [
        # Que informações (em ordem) são retornadas pela Binance em cada candle
        "Open_time",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Close_time",
        "Quote_asset_volume",
        "Number_of_trades",
        "Taker_buy_base_asset_volume",
        "Taker_buy_quote_asset_volume",
        "Ignore",
    ]
