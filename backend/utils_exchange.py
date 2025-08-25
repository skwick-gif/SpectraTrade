import requests
from loguru import logger

class ExchangeConnector:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_price(self, symbol):
        # דמו – מחזיר מחיר רנדומלי
        import random
        price = round(100 + random.uniform(-5, 5), 2)
        logger.info(f"Fetched price for {symbol}: {price}")
        return price

    def execute_order(self, symbol, action, amount, price):
        # דמו – מחזיר תוצאה פיקטיבית, אפשר להחליף ל־API אמיתי
        logger.info(f"Order executed: {action} {amount} {symbol} at {price}")
        return {"status": "success", "filled_price": price}