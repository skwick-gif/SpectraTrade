from fastapi import APIRouter, Depends
from db import get_db
from models import Trade, Signal, User
from utils.analytics import trade_statistics
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/user/{user_id}")
def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    trades = db.query(Trade).filter(Trade.user_id == user_id).all()
    stats = trade_statistics(trades)
    return stats

@router.get("/signal/{signal_id}")
def get_signal_stats(signal_id: int, db: Session = Depends(get_db)):
    trades = db.query(Trade).filter(Trade.signal_id == signal_id).all()
    stats = trade_statistics(trades)
    return stats

@router.get("/global")
def get_global_stats(db: Session = Depends(get_db)):
    trades = db.query(Trade).all()
    return trade_statistics(trades)