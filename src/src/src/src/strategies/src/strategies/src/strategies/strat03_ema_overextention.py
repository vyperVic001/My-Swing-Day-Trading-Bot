import pandas_ta as ta
from src.utils import compute_sl_tp

def check_signal(df, symbol=None, timeframe="1h", config=None):
    df = df.copy()
    df['ema20'] = ta.ema(df['close'], length=20)
    df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
    prev = df.iloc[-2]
    if (prev['ema20'] - prev['close']) > 2 * prev['atr'] and (prev['close'] > prev['open']):
        entry = prev['close']
        sl, tp = compute_sl_tp(entry, "BUY", prev['atr'])
        return {"strategy":"EMA Overextension","symbol":symbol,"timeframe":timeframe,"signal":"BUY","entry":entry,"sl":sl,"tp":tp,"reason":"Price far below EMA20 then small bull candle"}
    if (prev['close'] - prev['ema20']) > 2 * prev['atr'] and (prev['close'] < prev['open']):
        entry = prev['close']
        sl, tp = compute_sl_tp(entry, "SELL", prev['atr'])
        return {"strategy":"EMA Overextension","symbol":symbol,"timeframe":timeframe,"signal":"SELL","entry":entry,"sl":sl,"tp":tp,"reason":"Price far above EMA20 then small bear candle"}
    return None
