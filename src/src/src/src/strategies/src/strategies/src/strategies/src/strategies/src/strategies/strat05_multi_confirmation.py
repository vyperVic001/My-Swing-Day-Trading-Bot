import pandas_ta as ta
from src.utils import compute_sl_tp

def check_signal(df, symbol=None, timeframe="1h", config=None):
    df = df.copy()
    df['ema20'] = ta.ema(df['close'], 20)
    df['ema50'] = ta.ema(df['close'], 50)
    df['ema200'] = ta.ema(df['close'], 200)
    df['rsi'] = ta.rsi(df['close'], 14)
    df['atr'] = ta.atr(df['high'], df['low'], df['close'], 14)
    df['bb_up'] = ta.bbands(df['close'], length=20, std=2)['BBU_20_2']
    df['bb_low'] = ta.bbands(df['close'], length=20, std=2)['BBL_20_2']

    prev = df.iloc[-2]
    body = abs(prev['close'] - prev['open'])
    candle_size = prev['high'] - prev['low']
    is_pin = ( (prev['low'] <= prev['open'] and prev['low'] <= prev['close']) and (((prev['high']-max(prev['open'],prev['close']))/candle_size) > 0.6) )

    bull_div = (df['low'].rolling(3).min().iloc[-2] < df['low'].rolling(6).min().iloc[-5]) and (df['rsi'].rolling(3).min().iloc[-2] > df['rsi'].rolling(6).min().iloc[-5])
    bear_div = (df['high'].rolling(3).max().iloc[-2] > df['high'].rolling(6).max().iloc[-5]) and (df['rsi'].rolling(3).max().iloc[-2] < df['rsi'].rolling(6).max().iloc[-5])

    opt_count_buy = 0
    if prev['ema20'] > prev['ema50'] and prev['ema50'] > prev['ema200']: opt_count_buy += 1
    if prev['close'] <= df['bb_low'].iloc[-2]: opt_count_buy += 1
    if prev['atr'] > df['atr'].rolling(5).mean().iloc[-2]: opt_count_buy += 1

    if (is_pin or body>0) and bull_div and opt_count_buy >= 2:
        entry = prev['close']
        sl, tp = compute_sl_tp(entry, "BUY", prev['atr'])
        return {"strategy":"Multi Confirmation","symbol":symbol,"timeframe":timeframe,"signal":"BUY","entry":entry,"sl":sl,"tp":tp,"reason":"Reversal + divergence + filters"}
    if (is_pin or body>0) and bear_div and opt_count_buy >= 2:
        entry = prev['close']
        sl, tp = compute_sl_tp(entry, "SELL", prev['atr'])
        return {"strategy":"Multi Confirmation","symbol":symbol,"timeframe":timeframe,"signal":"SELL","entry":entry,"sl":sl,"tp":tp,"reason":"Reversal + divergence + filters"}
    return None
