import yfinance as yf
import pandas as pd

def timeframe_to_yf_interval(tf):
    if tf == "1h": return "60m"
    if tf == "4h": return "120m"
    if tf == "30m": return "30m"
    return "60m"

def fetch_ohlcv(config, symbol_key, timeframe="1h", lookback=200):
    try:
        sym_cfg = config['symbols'][symbol_key]
        ticker = sym_cfg.get('ticker', symbol_key)
        interval = timeframe_to_yf_interval(timeframe)
        period = "60d"
        df = yf.download(ticker, period=period, interval=interval, progress=False)
        if df is None or df.empty:
            return None
        df = df.rename(columns={"Open":"open","High":"high","Low":"low","Close":"close","Volume":"volume"})
        df = df[['open','high','low','close','volume']].dropna()
        df.index = pd.to_datetime(df.index)
        return df.tail(lookback)
    except Exception as e:
        print("Data fetch error:", e)
        return None
