### bot.py

"""
Simplified Binance Futures Testnet Bot
Features:
- MARKET, LIMIT, STOP-LIMIT orders
- View & Cancel open orders
- Simulated OCO Orders (Bonus)
- Logging
Author: Sujal Kalra
"""

import os
import logging
import time
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException

# ── ENV & LOGGER ────────────────────────────────────────────────────────────────
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ── BOT CLASS ───────────────────────────────────────────────────────────────────
class BasicBot:
    """Reusable Futures-Testnet helper"""

    def __init__(self, api_key: str, api_secret: str):
        try:
            self.client = Client(api_key, api_secret, testnet=True)
            self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
            # Test authentication with a simple ping
            self.client.futures_ping()
        except BinanceAPIException as e:
            logging.error(f"Invalid API credentials: {e.message}")
            raise ValueError("Invalid API credentials")

    # ----------  Order helpers  ----------
    def _notional_ok(self, price: float, qty: float) -> bool:
        notional = price * qty
        if notional < 100:
            print(f"❌ Order notional ${notional:.2f} < $100 minimum.")
            return False
        return True

    def market(self, symbol: str, side: str, qty: float):
        try:
            mark_price_data = self.client.futures_mark_price(symbol=symbol)
            mark_price = float(mark_price_data['markPrice'])
            if not self._notional_ok(mark_price, qty):
                return {"error": "Notional too low."}

            order = self.client.futures_create_order(
                symbol=symbol, side=side, type="MARKET", quantity=qty
            )
            print("✅ Market order placed!\n", order)
            logging.info(f"Market: {order}")
            return order
        except BinanceAPIException as e:
            logging.error(f"Market ERR: {e.message}")
            print("❌ Market order failed:", e.message)
            return {"error": e.message}

    def limit(self, symbol: str, side: str, qty: float, price: float):
        if not self._notional_ok(price, qty):
            return {"error": "Notional too low."}
        try:
            order = self.client.futures_create_order(
                symbol=symbol, side=side, type="LIMIT",
                timeInForce="GTC", quantity=qty, price=price
            )
            print("✅ Limit order placed!\n", order)
            logging.info(f"Limit: {order}")
            return order
        except BinanceAPIException as e:
            logging.error(f"Limit ERR: {e.message}")
            print("❌ Limit order failed:", e.message)
            return {"error": e.message}

    def stop_limit(self, symbol: str, side: str, qty: float,
                   stop_price: float, limit_price: float):
        if not self._notional_ok(limit_price, qty):
            return {"error": "Notional too low."}
        try:
            order = self.client.futures_create_order(
                symbol=symbol, side=side, type="STOP",
                timeInForce="GTC", quantity=qty,
                stopPrice=stop_price, price=limit_price
            )
            print("✅ Stop-Limit order placed!\n", order)
            logging.info(f"StopLimit: {order}")
            return order
        except BinanceAPIException as e:
            logging.error(f"StopLimit ERR: {e.message}")
            print("❌ Stop-Limit order failed:", e.message)
            return {"error": e.message}

    # ----------  Simulated OCO Order ----------
    def oco_simulated(self, symbol, side, quantity, take_profit_price, stop_price, stop_limit_price):
        try:
            mark_price_data = self.client.futures_mark_price(symbol=symbol)
            mark_price = float(mark_price_data['markPrice'])
            if not self._notional_ok(mark_price, quantity):
                return {"error": "Notional too low."}

            tp_order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                timeInForce="GTC",
                quantity=quantity,
                price=take_profit_price
            )
            logging.info(f"OCO-TakeProfit: {tp_order}")

            sl_order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="STOP",
                timeInForce="GTC",
                quantity=quantity,
                stopPrice=stop_price,
                price=stop_limit_price
            )
            logging.info(f"OCO-StopLoss: {sl_order}")

            while True:
                orders = self.client.futures_get_open_orders(symbol=symbol)
                open_ids = [o["orderId"] for o in orders]

                if tp_order["orderId"] not in open_ids:
                    self.cancel(symbol, sl_order["orderId"])
                    break
                elif sl_order["orderId"] not in open_ids:
                    self.cancel(symbol, tp_order["orderId"])
                    break

                time.sleep(1)

        except BinanceAPIException as e:
            logging.error(f"OCO Simulation Error: {e.message}")
            print("❌ Failed to simulate OCO:", e.message)
            return {"error": e.message}

    # ----------  Order management  ----------
    def open_orders(self, symbol: str):
        try:
            orders = self.client.futures_get_open_orders(symbol=symbol)
            logging.info(f"OpenOrders: {orders}")
            return orders
        except BinanceAPIException as e:
            logging.error(f"OpenOrders ERR: {e.message}")
            print("❌ Could not fetch open orders:", e.message)
            return {"error": e.message}

    def cancel(self, symbol: str, order_id: int):
        try:
            resp = self.client.futures_cancel_order(symbol=symbol, orderId=order_id)
            logging.info(f"Cancel: {resp}")
            return resp
        except BinanceAPIException as e:
            logging.error(f"Cancel ERR: {e.message}")
            print(f"❌ Cancel failed for {order_id}:", e.message)
            return {"error": e.message}
