#!/usr/bin/env python3
import time, logging, importlib
from src.data_fetcher import fetch_ohlcv
from src.notifier import TelegramNotifier
from src.utils import load_local_config, pretty_signal

cfg = load_local_config()
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
notifier = TelegramNotifier(cfg['telegram']['bot_token'], cfg['telegram']['chat_id'])

# strategy module names (files in src/strategies)
STRATS = [
    'strat01_bb_squeeze','strat02_rsi_exhaustion','strat03_ema_overextension',
    'strat04_macd_pullback','strat05_multi_confirmation','strat31_tweezer_sniper'
]
STRATEGIES = [importlib.import_module(f"src.strategies.{s}") for s in STRATS]

SYMBOLS = list(cfg['symbols'].keys())
TIMEFRAMES = cfg['timeframes']
MIN_BETWEEN = cfg['bot'].get('min_time_between_signals_sec',300)
last_signal = {}

def scan_once():
    logging.info("Starting scan cycle")
    for sym in SYMBOLS:
        for tf in TIMEFRAMES:
            df = fetch_ohlcv(cfg, sym, tf, lookback=200)
            if df is None or df.empty:
                logging.warning(f"No data for {sym} {tf}")
                continue
            for strat in STRATEGIES:
                try:
                    res = strat.check_signal(df, symbol=sym, timeframe=tf, config=cfg)
                    if res and res.get('signal') in ('BUY','SELL'):
                        key = f"{sym}-{tf}"
                        now = time.time()
                        if now - last_signal.get(key,0) < MIN_BETWEEN:
                            logging.info(f"Throttling {key}")
                            continue
                        last_signal[key] = now
                        msg = pretty_signal(res)
                        notifier.send(msg)
                        logging.info(f"Sent {res.get('signal')} {sym} {tf} by {res.get('strategy')}")
                        break
                except Exception as e:
                    logging.exception(f"Strategy error for {sym} {tf}: {e}")
    logging.info("Scan cycle complete")

if __name__ == "__main__":
    scan_once()
    while True:
        time.sleep(60)
        scan_once()
