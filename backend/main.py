from fastapi import FastAPI
from db import Base, engine
import api.trading, api.users, api.stats
from loguru import logger
import yaml

with open('config.yaml') as f:
    config = yaml.safe_load(f)

logger.add("spectra.log", level=config['logging']['level'])

Base.metadata.create_all(bind=engine)
app = FastAPI(title="SpectraTrade API", description="מערכת מסחר בזמן אמת")

app.include_router(api.trading.router, prefix="/trading", tags=["Trading"])
app.include_router(api.users.router, prefix="/users", tags=["Users"])
app.include_router(api.stats.router, prefix="/stats", tags=["Statistics"])