import pandas_ta as ta
from src.utils import compute_sl_tp

def check_signal(df, symbol=None, timeframe="1h", config=None):
    df = df.copy()
    bb = ta.bbands(df['close'], length=10, std=1.5)
    df['bb_up'] = bb['BBU_10_1.5']
    df['bb_low'] = bb['BBL_10_1.5']
    df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
    df['bandwidth'] = df['bb_up'] - df['bb_low']

    last = df.iloc[-6:-1]
    if (last['bandwidth'] < last['atr']*0.8).all():
        prev = df.iloc[-2]
        vol_avg3 = df['volume'].iloc[-4:-1].mean()
        if prev['close'] > prev['bb_up'] and prev['volume'] > vol_avg3 and prev['atr'] > df['atr'].iloc[-6:-1].mean():
            entry = float(prev['close'])
            sl = float(prev['low'])
            tp = entry + 2*(entry-sl)
            return {"strategy":"BB Squeeze","symbol":symbol,"timeframe":timeframe,"signal":"BUY","entry":entry,"sl":sl,"tp":tp,"reason":"Breakout after squeeze"}
        if prev['close'] < prev['bb_low'] and prev['volume'] > vol_avg3 and prev['atr'] > df['atr'].iloc[-6:-1].mean():
            entry = float(prev['close'])
            sl = float(prev['high'])
            tp = entry - 2*(sl-entry)
            return {"strategy":"BB Squeeze","symbol":symbol,"timeframe":timeframe,"signal":"SELL","entry":entry,"sl":sl,"tp":tp,"reason":"Breakout after squeeze"}
    return None
