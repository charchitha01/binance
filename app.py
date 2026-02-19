from flask import Flask, render_template, request
from client import BinanceClient
from logger import logger

app = Flask(__name__)

# Initialize Binance client
client = BinanceClient()


@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    if request.method == "POST":

        try:
            # Get form inputs
            symbol = request.form.get("symbol", "").upper().strip()
            side = request.form.get("side", "").upper().strip()
            order_type = request.form.get("type", "").upper().strip()

            quantity_raw = request.form.get("quantity", "").strip()
            price_raw = request.form.get("price", "").strip()

            # Validate inputs
            if not symbol:
                raise ValueError("Symbol is required")

            if side not in ["BUY", "SELL"]:
                raise ValueError("Side must be BUY or SELL")

            if order_type not in ["MARKET", "LIMIT"]:
                raise ValueError("Type must be MARKET or LIMIT")

            # Convert quantity
            quantity = float(quantity_raw)

            if quantity <= 0:
                raise ValueError("Quantity must be greater than 0")

            # Convert price if LIMIT
            price = None
            if order_type == "LIMIT":

                if not price_raw:
                    raise ValueError("Price required for LIMIT order")

                price = float(price_raw)

                if price <= 0:
                    raise ValueError("Price must be greater than 0")

            # Log request
            logger.info(
                f"Order request: symbol={symbol}, side={side}, type={order_type}, quantity={quantity}, price={price}"
            )

            # Place order
            response = client.place_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price
            )

            # Show FULL response for debugging
            result = f"FULL RESPONSE:\n{response}"

            logger.info(f"Binance response: {response}")

        except Exception as e:

            result = f"ERROR:\n{str(e)}"

            logger.error(f"Error placing order: {e}")

    return render_template("index.html", result=result)


if __name__ == "__main__":

    logger.info("Starting Flask Binance Futures Testnet App")

    app.run(debug=True)
