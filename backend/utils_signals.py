from datetime import datetime, timedelta
from loguru import logger

def process_signal(signal, config):
    # עיבוד איתות: הגדרת SL/TP, לוג, אימות תדירות
    signal.sl = signal.sl or config['trading']['default_sl'] * signal.price
    signal.tp = signal.tp or config['trading']['default_tp'] * signal.price
    signal.status = 'pending'
    logger.info(f"Signal processed for {signal.symbol} at {signal.price} (SL: {signal.sl}, TP: {signal.tp})")
    return signal

def validate_signal_frequency(user_signals, config):
    # הגנה על תדירות איתותים
    now = datetime.utcnow()
    last_minute_signals = [s for s in user_signals if (now - s.created_at).total_seconds() < 60]
    if len(last_minute_signals) >= config['trading']['max_signal_per_min']:
        logger.warning("Signal frequency exceeded for user!")
        return False
    return True