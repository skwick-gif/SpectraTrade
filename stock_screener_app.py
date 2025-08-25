import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse
import requests

app = FastAPI(title="Stock Screener", description="סריקת מניות פוטנציאליות בזמן אמת")

# קריטריונים אפשריים לסריקה
DEFAULT_CRITERIA = {
    "min_price": 5,
    "max_price": 150,
    "min_volume": 100000,
    "max_change_pct": 5
}

# דוגמת רשימת מניות לסריקה (אפשר להרחיב או לייבא רשימה אמיתית)
STOCK_LIST = ["AAPL", "MSFT", "GOOG", "TSLA", "AMZN", "NVDA", "AMD", "META", "NFLX", "BABA", "JPM", "DIS"]

# קבלת נתוני מניה מ-API ציבורי (Yahoo, דמו)
def get_stock_data(symbol):
    base_url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
    resp = requests.get(base_url)
    if resp.status_code != 200:
        return None
    data = resp.json()
    try:
        stock = data["quoteResponse"]["result"][0]
        return {
            "symbol": symbol,
            "price": stock.get("regularMarketPrice"),
            "volume": stock.get("regularMarketVolume"),
            "change_pct": stock.get("regularMarketChangePercent"),
            "name": stock.get("shortName", symbol)
        }
    except Exception:
        return None

@app.get("/", response_class=HTMLResponse)
def home():
    return '''
    <html>
    <head>
        <title>Stock Screener</title>
        <meta charset=\"UTF-8\">
    </head>
    <body>
        <h1>סריקת מניות פוטנציאליות</h1>
        <form method=\"get\" action=\"/scan\">
            מחיר מינימלי: <input type=\"number\" name=\"min_price\" value=\"5\"><br>
            מחיר מקסימלי: <input type=\"number\" name=\"max_price\" value=\"150\"><br>
            מחזור מינימלי: <input type=\"number\" name=\"min_volume\" value=\"100000\"><br>
            שינוי יומי מקסימלי (%): <input type=\"number\" step=\"0.1\" name=\"max_change_pct\" value=\"5\"><br>
            <button type=\"submit\">סרוק</button>
        </form>
    </body>
    </html>
    '''

@app.get("/scan", response_class=HTMLResponse)
def scan(
    min_price: float = Query(DEFAULT_CRITERIA["min_price"]),
    max_price: float = Query(DEFAULT_CRITERIA["max_price"]),
    min_volume: int = Query(DEFAULT_CRITERIA["min_volume"]),
    max_change_pct: float = Query(DEFAULT_CRITERIA["max_change_pct"])
):
    results = []
    for symbol in STOCK_LIST:
        stock_data = get_stock_data(symbol)
        if not stock_data:
            continue
        if (
            stock_data["price"] is not None and
            stock_data["volume"] is not None and
            min_price <= stock_data["price"] <= max_price and
            stock_data["volume"] >= min_volume and
            abs(stock_data["change_pct"] or 0) <= max_change_pct
        ):
            results.append(stock_data)
    html = '''
    <html>
    <head>
    <title>תוצאות סריקה</title>
    <meta charset=\"UTF-8\">
    </head>
    <body>
        <h2>מניות פוטנציאליות:</h2>
        <table border=\"1\" cellpadding=\"4\" style=\"border-collapse:collapse\">
            <tr>
                <th>סימבול</th>
                <th>שם</th>
                <th>מחיר</th>
                <th>מחזור</th>
                <th>שינוי יומי (%)</th>
            </tr>
    '''
    for stock in results:
        html += f"""<tr>
            <td>{stock["symbol"]}</td>
            <td>{stock["name"]}</td>
            <td>{stock["price"]}</td>
            <td>{stock["volume"]}</td>
            <td>{stock["change_pct"]:.2f}</td>
        </tr>"""
    html += '''
        </table>
        <br><a href=\"/\">חזור</a>
    </body>
    </html>
    '''
    return HTMLResponse(content=html)

@app.get("/api/scan", response_class=JSONResponse)
def api_scan(
    min_price: float = Query(DEFAULT_CRITERIA["min_price"]),
    max_price: float = Query(DEFAULT_CRITERIA["max_price"]),
    min_volume: int = Query(DEFAULT_CRITERIA["min_volume"]),
    max_change_pct: float = Query(DEFAULT_CRITERIA["max_change_pct"])
):
    results = []
    for symbol in STOCK_LIST:
        stock_data = get_stock_data(symbol)
        if not stock_data:
            continue
        if (
            stock_data["price"] is not None and
            stock_data["volume"] is not None and
            min_price <= stock_data["price"] <= max_price and
            stock_data["volume"] >= min_volume and
            abs(stock_data["change_pct"] or 0) <= max_change_pct
        ):
            results.append(stock_data)
    return JSONResponse(content=results)

if __name__ == \"__main__\":
    uvicorn.run("stock_screener_app:app", host="0.0.0.0", port=8000, reload=True)
