from sqlalchemy.orm import Query
from loguru import logger

def trade_statistics(trades):
    total = len(trades)
    wins = sum(1 for t in trades if t.profit > 0)
    losses = sum(1 for t in trades if t.profit <= 0)
    avg_profit = sum(t.profit for t in trades) / total if total > 0 else 0
    win_rate = wins / total if total > 0 else 0
    max_drawdown = min([t.profit for t in trades] + [0])
    logger.info(f"Computed stats: total={total}, wins={wins}, losses={losses}, avg={avg_profit}")
    return {
        "total_trades": total,
        "wins": wins,
        "losses": losses,
        "avg_profit": avg_profit,
        "win_rate": win_rate,
        "max_drawdown": max_drawdown
    }