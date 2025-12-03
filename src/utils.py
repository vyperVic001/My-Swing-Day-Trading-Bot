import json, os
def load_local_config():
    # load local config.py (not committed)
    try:
        import config
        return config.CONFIG
    except Exception as e:
        raise RuntimeError("Missing local config.py. Create it from config.example.json and don't push it.") from e

def pretty_signal(sig: dict) -> str:
    lines = []
    lines.append(f"{sig.get('strategy')} | {sig.get('symbol')} | {sig.get('timeframe')}")
    lines.append(f"{sig.get('signal')} ENTRY: {sig.get('entry'):.2f}")
    lines.append(f"SL: {sig.get('sl'):.2f}  TP: {sig.get('tp'):.2f}")
    lines.append(f"Reason: {sig.get('reason','')}")
    return "\n".join(lines)

def compute_sl_tp(entry, side, atr_val, wick_size=None, rr=2.0):
    if side == "BUY":
        sl = entry - max(atr_val, (wick_size or 0))
        tp = entry + rr * (entry - sl)
    else:
        sl = entry + max(atr_val, (wick_size or 0))
        tp = entry - rr * (sl - entry)
    return float(sl), float(tp)
