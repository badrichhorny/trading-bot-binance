from flask import Flask, request
from binance.client import Client
import os

app = Flask(__name__)

# Získání API klíčů z Render proměnných
api_key = os.environ.get("BINANCE_API_KEY")
api_secret = os.environ.get("BINANCE_API_SECRET")

# Nastavení testnet klienta
client = Client(api_key, api_secret, testnet=True)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Přijatý požadavek:", data)

    action = data.get("action")
    symbol = data.get("symbol")
    quantity = float(data.get("quantity"))

    try:
        if action == "buy":
            order = client.futures_create_order(
                symbol=symbol,
                side="BUY",
                type="MARKET",
                quantity=quantity
            )
        elif action == "sell":
            order = client.futures_create_order(
                symbol=symbol,
                side="SELL",
                type="MARKET",
                quantity=quantity
            )
        else:
            return {"error": "Neznámá akce"}, 400

        return {"status": "úspěch", "order": order}, 200

    except Exception as e:
        print("Chyba při obchodování:", str(e))
        return {"error": str(e)}, 500

