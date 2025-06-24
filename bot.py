from flask import Flask, request, jsonify
from binance.client import Client
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
client = Client(api_key, api_secret, testnet=True)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("📩 Přijatý signál:", data)

    action = data.get("action")
    symbol = data.get("symbol", "ETHUSDT")
    quantity = data.get("quantity", 0.01)

    if action == "buy":
        order = client.futures_create_order(
            symbol=symbol,
            side='BUY',
            type='MARKET',
            quantity=quantity
        )
        print("✅ BUY objednávka:", order)
        return jsonify({"status": "Buy order sent", "order": order})

    elif action == "sell":
        order = client.futures_create_order(
            symbol=symbol,
            side='SELL',
            type='MARKET',
            quantity=quantity
        )
        print("✅ SELL objednávka:", order)
        return jsonify({"status": "Sell order sent", "order": order})

    else:
        return jsonify({"error": "Invalid action"}), 400

if __name__ == "__main__":
    app.run(port=5000)
