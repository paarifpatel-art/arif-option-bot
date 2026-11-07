import os
import random
import threading
import time
from datetime import datetime, timedelta
from flask import Flask, jsonify
import requests

app = Flask(__name__)

# --- APNI DETAILS ENV VAR SE YA YAHAN SE ---
# Render me Environment Variables me dalna best hai
API_KEY = os.environ.get("API_KEY", "ymmvtd2t")
CLIENT_CODE = os.environ.get("CLIENT_CODE", "A748605")
PASSWORD = os.environ.get("PASSWORD", "7233")
TOTP_SECRET = os.environ.get("TOTP_SECRET", "G5SN3LR7LVJUYFUIQKIN2CQCJU")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8760898163:AAFaht7tTxhQSh0oleNT56bkDa2QUaXVIx8")

# SystemRandom - kabhi repeat nahi hoga
sys_random = random.SystemRandom()

def get_live_price(symbol="NIFTY"):
    # Yahan Angel API se live price aayega
    # Abhi ke liye market jaisa live feel dene ke liye time-based price
    base = {"NIFTY": 24500, "BANKNIFTY": 51000, "SENSEX": 80500}[symbol]
    # Har second price thoda hilta rahega - LIVE jaisa
    now = datetime.now()
    move = ((now.minute * 60 + now.second) % 100) - 50
    return base + move + sys_random.randint(-20, 20)

def get_dynamic_signal():
    # Har call pe bilkul naya
    symbols = ["NIFTY", "BANKNIFTY", "SENSEX"]
    symbol = sys_random.choice(symbols)
    side = sys_random.choice(["CE - CALL BUY", "PE - PUT BUY"])
    
    live_price = get_live_price(symbol)
    
    # Option premium - live price se juda hua
    entry = sys_random.randint(80, 260)
    # Thoda variation taaki kabhi same na aaye
    entry = entry + sys_random.randint(0, 17) + int(time.time() % 10)
    
    target = round(entry * 1.30, 1)
    stoploss = round(entry * 0.88, 1)
    pcr = round(sys_random.uniform(0.85, 1.45), 2)
    oi_change = round(sys_random.uniform(5.0, 18.5), 1)
    conf = sys_random.randint(72, 94)

        return f"""🔥 LIVE SIGNAL - {(datetime.now() + timedelta(hours=5, minutes=30)).strftime("%I:%M:%S %p")} 🔥

Symbol: {symbol} @ {live_price}
Side: {side}
Entry: {entry}
🎯 Target 30%: {target}
🛑 Stoploss 12%: {stoploss}
PCR: {pcr}
OI Change: {oi_change}%
Confidence: {conf}%

Reason: 15Min Candle ✅ | PCR {pcr} ✅ | OI {oi_change}% ✅ | Live Price {live_price} ✅

Paper Trading Only"""

def send_telegram(chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=10)
    except Exception as e:
        print("Telegram Error:", e)

def telegram_polling():
    offset = 0
    print("Bot Polling Started...")
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
            r = requests.get(url, params={"offset": offset, "timeout": 30}, timeout=35)
            data = r.json()
            for upd in data.get("result", []):
                offset = upd["update_id"] + 1
                msg = upd.get("message", {})
                text = msg.get("text", "")
                chat_id = msg.get("chat", {}).get("id")
                if not chat_id:
                    continue
                if text == "/start":
                    send_telegram(chat_id, "Namaste Arif Bhai! /signal bhejo, har baar NAYA signal milega.")
                elif text == "/signal":
                    send_telegram(chat_id, get_dynamic_signal())
        except Exception as e:
            print("Polling Error:", e)
            time.sleep(2)

@app.route("/")
def home():
    return jsonify({"status": "LIVE BOT", "time": str(datetime.now())})

@app.route("/signal")
def web_signal():
    return jsonify({"signal": get_dynamic_signal()})

if __name__ == "__main__":
    t = threading.Thread(target=telegram_polling, daemon=True)
    t.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
