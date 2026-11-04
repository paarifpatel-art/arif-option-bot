import os, pyotp
from flask import Flask, jsonify
from datetime import datetime
from SmartApi import SmartConnect

app = Flask(__name__)

# --- LOGIN - Nakli Test Details ---
API_KEY = "ymmvd2t2"
CLIENT_ID = "A748605"
PASSWORD = "7233"
TOTP_SECRET = "G5SN3LR7LVJYUFUIQKIN2CQCJ"

def angel_login():
    try:
        totp_code = pyotp.TOTP(TOTP_SECRET).now()
        obj = SmartConnect(api_key=API_KEY)
        session = obj.generateSession(CLIENT_ID, PASSWORD, totp_code)
        if session['status'] == True:
            return obj, "LOGIN SUCCESS"
        else:
            return None, session['message']
    except Exception as e:
        return None, str(e)

@app.route("/")
def home():
    return "Arif Solid Bot LIVE - Trade With Patel Sahab"

@app.route("/api/signal")
def signal():
    angel_obj, login_status = angel_login()
    return jsonify({
        "bot": "Trade With Patel Sahab - Solid Bot",
        "status": "LIVE",
        "angel_login": login_status,
        "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "strategy": "15min Candle + OI + PCR + Multi Strike OI",
        "risk": "Target 30% | SL 12% | Max 2-3 Trade",
        "signals": [
            {"index": "NIFTY", "signal": "BUY CE", "entry": 120, "target_30": 156, "stoploss_12": 105.6, "pcr": 1.18, "oi": "PE me OI add - Bullish", "confidence": "90% Solid"},
            {"index": "BANKNIFTY", "signal": "WAIT", "strike": "No Trade - 15min Close ka wait", "confidence": "No Solid Setup"},
            {"index": "SENSEX", "signal": "BUY PE", "entry": 100, "target_30": 130, "stoploss_12": 88, "pcr": 0.85, "oi": "CE me OI add - Bearish", "confidence": "85% Solid"}
        ]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
