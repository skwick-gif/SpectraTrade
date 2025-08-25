from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse
import requests

app = FastAPI()

YAHOO_FINANCE_API = "https://query1.finance.yahoo.com/v7/finance/quote"

def get_stocks(symbols):
    params = {"symbols": ",".join(symbols)}
    r = requests.get(YAHOO_FINANCE_API, params=params)
    data = r.json()
    return data["quoteResponse"]["result"]

@app.get("/", response_class=HTMLResponse)
def home():
    html = """
    <h2>Stock Screener</h2>
    <form action='/screener' method='get'>
      <label>Symbols (comma separated):</label>
      <input name='symbols' value='AAPL,MSFT,GOOG' style='width:300px'>
      <button type='submit'>Scan</button>
    </form>
    """
    return html

@app.get("/screener")
def screener(symbols: str = Query(...)):
    symbol_list = [s.strip() for s in symbols.split(",")]
    stocks = get_stocks(symbol_list)
    return JSONResponse(content={"stocks": stocks})