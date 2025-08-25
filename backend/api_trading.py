from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from models import Signal, Trade, User
from utils.signals import process_signal, validate_signal_frequency
from utils.exchange import ExchangeConnector
from utils.notifications import send_notification
from sqlalchemy.orm import Session
from datetime import datetime
import yaml

router = APIRouter()
with open('config.yaml') as f:
    config = yaml.safe_load(f)
exchange = ExchangeConnector(config['api_keys']['exchange'])

@router.post("/signal")
def create_signal(symbol: str, action: str, price: float, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=403, detail="User not found or inactive")
    user_signals = db.query(Signal).filter(Signal.user_id == user_id).all()
    if not validate_signal_frequency(user_signals, config):
        raise HTTPException(status_code=429, detail="Signal frequency exceeded")
    signal = Signal(symbol=symbol, action=action, price=price, user_id=user_id)
    process_signal(signal, config)
    db.add(signal)
    db.commit()
    db.refresh(signal)
    send_notification(user.email, f"Signal created for {symbol} {action} at {price}")
    return signal

@router.post("/trade")
def execute_trade(user_id: int, signal_id: int, amount: float, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    signal = db.query(Signal).filter(Signal.id == signal_id).first()
    if not user or not signal: raise HTTPException(status_code=404, detail="User or signal not found")
    price = exchange.get_price(signal.symbol)
    order = exchange.execute_order(signal.symbol, signal.action, amount, price)
    commission = price * amount * config['trading']['commission']
    profit = (price - signal.price if signal.action == 'buy' else signal.price - price) * amount - commission
    trade = Trade(user_id=user_id, signal_id=signal_id, status='closed', executed_price=price,
                  closed_at=datetime.utcnow(), profit=profit, commission=commission, sl=signal.sl, tp=signal.tp)
    db.add(trade)
    db.commit()
    db.refresh(trade)
    send_notification(user.email, f"Trade executed for {signal.symbol} {signal.action} at {price}")
    return trade

@router.get("/signal")
def list_signals(db: Session = Depends(get_db)):
    return db.query(Signal).all()