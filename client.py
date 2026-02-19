from binance.client import Client
from config import API_KEY, API_SECRET, BASE_URL
from logger import logger


class BinanceClient:

    def __init__(self):

        try:
            # Initialize client
            self.client = Client(API_KEY, API_SECRET)

            # Set Futures Testnet URL
            self.client.FUTURES_URL = BASE_URL + "/fapi"

            logger.info("Connected to Binance Futures Testnet")

        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise e


    def place_order(self, symbol, side, order_type, quantity, price=None):

        try:

            params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity,
            }

            if order_type == "LIMIT":

                params["price"] = price
                params["timeInForce"] = "GTC"

            logger.info(f"Sending order: {params}")

            response = self.client.futures_create_order(**params)

            logger.info(f"Received response: {response}")

            return response

        except Exception as e:

            logger.error(f"Order failed: {e}")

            return {
                "error": str(e)
            }
