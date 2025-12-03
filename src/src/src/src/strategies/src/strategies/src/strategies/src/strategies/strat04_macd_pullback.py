import pandas_ta as ta
from src.utils import compute_sl_tp

def check_signal(df, symbol=None, timeframe="1h", config=None):
    df = df.copy()
    macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
    df['macd_hist'] = macd['MACDh_12_26_9']
    df['ma20'] = ta.sma(df['close'], length=20)
    prev = df.iloc[-2]
    if df['ma20'].iloc[-2] < df['ma20'].iloc[-1]:  # uptrend
        if (df['macd_hist'].iloc[-2] < df['macd_hist'].iloc[-3]) and (df['macd_hist'].iloc[-2] > 0):
            prev_body = abs(df['close'].iloc[-3] - df['open'].iloc[-3]) if len(df) > 3 else None
            cur_body = abs(prev['close'] - prev['open'])
            if prev_body and cur_body < 0.33 * prev_body and prev['close'] > prev['open']:
                entry = prev['close']
                sl, tp = compute_sl_tp(entry, "BUY", prev['atr'] if 'atr' in prev else 0.0)
                return {"strategy":"MACD Pullback Pop","symbol":symbol,"timeframe":timeframe,"signal":"BUY","entry":entry,"sl":sl,"tp":tp,"reason":"MACD pullback then break"}
    if df['ma20'].iloc[-2] > df['ma20'].iloc[-1]:  # downtrend
        if (df['macd_hist'].iloc[-2] > df['macd_hist'].iloc[-3]) and (df['macd_hist'].iloc[-2] < 0):
            prev_body = abs(df['close'].iloc[-3] - df['open'].iloc[-3]) if len(df) > 3 else None
            cur_body = abs(prev['close'] - prev['open'])
            if prev_body and cur_body < 0.33 * prev_body and prev['close'] < prev['open']:
                entry = prev['close']
                sl, tp = compute_sl_tp(entry, "SELL", prev['atr'] if 'atr' in prev else 0.0)
                return {"strategy":"MACD Pullback Pop","symbol":symbol,"timeframe":timeframe,"signal":"SELL","entry":entry,"sl":sl,"tp":tp,"reason":"MACD pullback then break"}
    return None
