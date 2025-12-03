import pandas_ta as ta
from src.utils import compute_sl_tp

def is_bull_div(df):
    return df['low'].iloc[-2] < df['low'].iloc[-3] and df['rsi'].iloc[-2] > df['rsi'].iloc[-3]

def is_bear_div(df):
    return df['high'].iloc[-2] > df['high'].iloc[-3] and df['rsi'].iloc[-2] < df['rsi'].iloc[-3]

def check_signal(df, symbol=None, timeframe="1h", config=None):
    df = df.copy()
    df['rsi'] = ta.rsi(df['close'], length=14)
    df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
    prev = df.iloc[-2]
    if prev['rsi'] < 30 and is_bull_div(df) and prev['close'] > prev['open']:
        entry = prev['close']
        sl, tp = compute_sl_tp(entry, "BUY", prev['atr'])
        return {"strategy":"RSI Exhaustion","symbol":symbol,"timeframe":timeframe,"signal":"BUY","entry":entry,"sl":sl,"tp":tp,"reason":"RSI <30 + divergence + bullish candle"}
    if prev['rsi'] > 70 and is_bear_div(df) and prev['close'] < prev['open']:
        entry = prev['close']
        sl, tp = compute_sl_tp(entry, "SELL", prev['atr'])
        return {"strategy":"RSI Exhaustion","symbol":symbol,"timeframe":timeframe,"signal":"SELL","entry":entry,"sl":sl,"tp":tp,"reason":"RSI >70 + divergence + bearish candle"}
    return None
