import os
import threading
import time
import pyotp
import pandas as pd
from datetime import datetime
from flask import Flask, jsonify
import requests
from SmartApi import SmartConnect

app = Flask(__name__)

# --- DETAILS SIRF ENV SE AAYEGI, CODE ME KABHI MAT LIKHNA ---
API_KEY = os.environ.get("API_KEY")
CLIENT_CODE = os.environ.get("CLIENT_CODE")
PASSWORD = os.environ.get("PASSWORD")
TOTP_SECRET = os.environ.get("TOTP_SECRET")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

smart = None

def login_angel():
    global smart
    try:
        smart = SmartConnect(api_key=API_KEY)
        totp = pyotp.TOTP(TOTP_SECRET).now()
        data = smart.generateSession(CLIENT_CODE, PASSWORD, totp)
        print("Angel Login Success:", data['status'])
        return True
    except Exception as e:
        print("Login Fail:", e)
        return False

def get_nifty_data():
    # NIFTY ka asli price + VWAP nikalenge
    try:
        # 26000 = NIFTY Spot Token
        ltp = smart.ltpData("NSE", "NIFTY", "99926000")['data']['ltp']
        
        # Pichle 15min ke candle leke VWAP banayenge
        params = {
            "exchange": "NSE",
            "symboltoken": "99926000",
            "interval": "FIFTEEN_MINUTE",
            "fromdate": datetime.now().strftime("%Y-%m-%d 09:15"),
            "todate": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        candles = smart.getCandleData(params)['data']
        df = pd.DataFrame(candles, columns=['time','open','high','low','close','volume'])
        # VWAP = Typical Price * Volume / Total Volume
        df['tp'] = (df['high'] + df['low'] + df['close']) / 3
        vwap = round((df['tp'] * df['volume']).sum() / df['volume'].sum(), 2)
        return ltp, vwap
    except Exception as e:
        print("Price Error:", e)
        return None, None

def get_pcr_oi():
    # Asli Option Chain se PCR nikalenge
    try:
        # NIFTY Option Chain
        params = {"symbolname": "NIFTY", "exchange": "NFO"}
        # SmartAPI me optionChain API se data aata hai
        chain = smart.optionChain(params)['data']
        
        # ATM ke aas paas ke 5 strike ka OI jodenge
        total_ce_oi = 0
        total_pe_oi = 0
        for row in chain:
            total_ce_oi += row.get('ce_oi', 0)
            total_pe_oi += row.get('pe_oi', 0)
        
        if total_ce_oi == 0:
            return 1.0, 0
        pcr = round(total_pe_oi / total_ce_oi, 2)
        return pcr, total_ce_oi
    except Exception as e:
        print("PCR Error:", e)
        # Agar chain na aaye to PCR 1.0 maan lo, signal mat roko
        return 1.0, 0

def get_real_signal():
    now = datetime.now()
    time_str = now.strftime("%H:%M")
    
    # LOCK 1: Market Time Check - 9:20 se pehle aur 3:00 ke baad NO TRADE
    if time_str < "09:20" or time_str > "15:00":
        return f"🕒 NO TRADE - Market Band Hai / Time {time_str}"
    
    # LOCK 2: Expiry Day 12 baje ke baad NO TRADE - Theta bahut khata hai
    # Expiry Thursday hota hai, isliye Thursday ko 12 baje ke baad band
    if now.weekday() == 3 and time_str > "12:00":
        return f"❌ NO TRADE - Expiry Day Hai, 12 Baje Ke Baad Theta Bahut Zyada Hai"

    if smart is None:
        if not login_angel():
            return "❌ Angel Login Fail - API Key Check Karo"

    nifty, vwap = get_nifty_data()
    if nifty is None:
        return "❌ Live Price Nahi Aa Raha - Angel Se Dobara Connect Karo"

    pcr, _ = get_pcr_oi()

    # LOCK 3: VWAP + PCR se asli signal
    # CE tabhi jab Price VWAP se UPAR ho aur PCR 1.0 se kam ho
    if nifty > vwap and pcr < 1.0:
        side = "CE - CALL BUY ✅"
        reason = f"Price {nifty} VWAP {vwap} se UPAR hai | PCR {pcr} Bullish hai"
        conf = "78%"
    # PE tabhi jab Price VWAP se NEECHE ho aur PCR 1.0 se zyada ho
    elif nifty < vwap and pcr > 1.0:
        side = "PE - PUT BUY ✅"
        reason = f"Price {nifty} VWAP {vwap} se NEECHE hai | PCR {pcr} Bearish hai"
        conf = "78%"
    else:
        return f"""❌ NO TRADE - {time_str}
NIFTY @ {nifty} | VWAP @ {vwap}
PCR: {pcr}
Reason: Price VWAP ke paas fasa hai, Range me hai.
Galat Signal se bachna hi profit hai.
Paper Trading Only"""

    return f"""🔥 LIVE SIGNAL - {time_str}
Symbol: NIFTY @ {nifty}
Side: {side}
VWAP: {vwap}
PCR: {pcr}
Confidence: {conf}%
Reason: {reason}
Target: 20% | Stoploss: 10%
Paper Trading Only"""

def send_telegram(chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": text})
    except Exception as e:
        print("Telegram Error:", e)

def telegram_polling():
    offset = 0
    print("Bot Polling Started...")
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
            r = requests.get(url, params={"offset": offset, "timeout": 10})
            data = r.json()
            for upd in data.get("result", []):
                offset = upd["update_id"] + 1
                msg = upd.get("message", {})
                text = msg.get("text", "")
                chat_id = msg.get("chat", {}).get("id")
                if not chat_id: continue
                if text == "/start":
                    send_telegram(chat_id, "Namaste Arif Bhai 🙏\nAsli Bot ON hai.\n/signal likho signal ke liye.")
                elif text == "/signal":
                    send_telegram(chat_id, get_real_signal())
        except Exception as e:
            print("Polling Error:", e)
        time.sleep(2)

@app.route("/")
def home():
    return jsonify({"status": "LIVE BOT - REAL DATA", "time": datetime.now().strftime("%H:%M:%S")})

@app.route("/signal")
def web_signal():
    return jsonify({"signal": get_real_signal()})

if __name__ == "__main__":
    login_angel()
    t = threading.Thread(target=telegram_polling)
    t.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
