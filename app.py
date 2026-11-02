from flask import Flask, jsonify, make_response
from flask_cors import CORS
import yfinance as yf
from datetime import datetime
import pytz

app = Flask(__name__)
CORS(app)

def get_ist():
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist).strftime("%d-%m %H:%M IST")

def get_live(symbol):
    try:
        df = yf.Ticker(symbol).history(period="1d", interval="15m")
        if df.empty:
            return 0
        return round(df['Close'].iloc[-1], 2)
    except:
        return 0

@app.route('/')
def home():
    return f"Bot LIVE - {get_ist()} - Go to /api/signal"

@app.route('/api/signal')
def signal():
    nifty = get_live("^NSEI")
    sensex = get_live("^BSESN")
    
    data = {
        "time": get_ist(),
        "nifty_spot": nifty,
        "sensex_spot": sensex,
        "status": "LIVE",
        "signals": [
            {"strike": "NIFTY 22950 CE", "price": 160, "target": 224, "sl": 96},
            {"strike": "NIFTY 23000 CE", "price": 129, "target": 181, "sl": 77}
        ]
    }
    resp = make_response(jsonify(data))
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
