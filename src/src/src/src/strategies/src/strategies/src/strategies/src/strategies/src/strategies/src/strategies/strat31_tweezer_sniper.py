import pandas_ta as ta

def approx_equal(a,b,tol): return abs(a-b) <= tol

def check_signal(df, symbol=None, timeframe="1h", config=None):
    df = df.copy()
    df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
    df['bb_low'] = ta.bbands(df['close'], length=20, std=2)['BBL_20_2']
    df['bb_up'] = ta.bbands(df['close'], length=20, std=2)['BBU_20_2']
    df['rsi'] = ta.rsi(df['close'], length=14)

    prev2 = df.iloc[-3]; prev1 = df.iloc[-2]
    tol = 0.1 * df['atr'].iloc[-2]
    # Tweezer Bottom
    if approx_equal(prev2['low'], prev1['low'], tol) and (prev1['close'] > prev1['open']):
        vol_avg5 = df['volume'].iloc[-7:-2].mean()
        if prev1['volume'] > vol_avg5 and prev1['rsi'] < 40 and prev1['low'] <= prev1['bb_low']*1.01:
            entry = float(df['open'].iloc[-1])
            wick = min(prev1['low'], prev2['low'])
            sl = wick - 0.5 * df['atr'].iloc[-2]
            tp1 = entry + 1.8*(entry - sl)
            return {"strategy":"Tweezer Sniper","symbol":symbol,"timeframe":timeframe,"signal":"BUY","entry":entry,"sl":sl,"tp":tp1,"reason":"Tweezer bottom + vol + RSI + BB touch"}
    # Tweezer Top
    if approx_equal(prev2['high'], prev1['high'], tol) and (prev1['close'] < prev1['open']):
        vol_avg5 = df['volume'].iloc[-7:-2].mean()
        if prev1['volume'] > vol_avg5 and prev1['rsi'] > 60 and prev1['high'] >= prev1['bb_up']*0.99:
            entry = float(df['open'].iloc[-1])
            wick = max(prev1['high'], prev2['high'])
            sl = wick + 0.5 * df['atr'].iloc[-2]
            tp1 = entry - 1.8*(sl - entry)
            return {"strategy":"Tweezer Sniper","symbol":symbol,"timeframe":timeframe,"signal":"SELL","entry":entry,"sl":sl,"tp":tp1,"reason":"Tweezer top + vol + RSI + BB touch"}
    return None
