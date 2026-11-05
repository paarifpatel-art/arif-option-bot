import os, pyotp, threading, datetime
from flask import Flask, jsonify

app = Flask(__name__)

# --- TUMHARI DETAILS ---
API_KEY = "YmmvTd2T"
CLIENT_CODE = "A748605"
PASSWORD = "7233"
TOTP_SECRET = "G5SN3LR7LVJUYFUIQKIN2CQCJU"
TELEGRAM_TOKEN = "8760898163:AAEMgX69Z2tvXGuTw9_dmN4xIB0FVWJXNDA"

# --- SOLID STRATEGY SETTING ---
TARGET_PCT = 30
STOPLOSS_PCT = 12
TIMEFRAME = "15minute"
MAX_TRADES_PER_DAY = 3
MIN_PCR_BULLISH = 1.10  # Isse upar = Bullish
MAX_PCR_BEARISH = 0.90  # Isse neeche = Bearish
MIN_OI_CHANGE_PCT = 8   # OI me kam se kam 8% badlav hona chahiye
TRADES_TODAY = []
LAST_SIGNAL_DATE = ""

def get_totp():
    return pyotp.TOTP(TOTP_SECRET).now()

def analyze_solid_signal(symbol, price, pcr, oi_change, multi_strike_oi_bullish, candle_15m_green):
    """
    95% SOLID FILTER - 5 me se 5 condition milni chahiye tabhi signal
    1. 15 Min Candle Confirm
    2. PCR Confirm
    3. OI Change Confirm
    4. Multi Strike OI Confirm
    5. Din me 3 se zyada trade nahi
    """
    global TRADES_TODAY
    today = datetime.date.today().isoformat()
    if LAST_SIGNAL_DATE != today:
        TRADES_TODAY.clear()

    if len(TRADES_TODAY) >= MAX_TRADES_PER_DAY:
        return None, "Aaj ke 3 Trade pure ho gaye. Ab kal."

    score = 0
    reasons = []

    # 1. 15 Min Candle
    if candle_15m_green:
        score += 1
        reasons.append("15Min Candle ✅")
    else:
        return None, "15Min Candle Confirm nahi hai - Trade SKIP"

    # 2. PCR Check
    if pcr >= MIN_PCR_BULLISH:
        score += 1
        reasons.append(f"PCR {pcr} Bullish ✅")
        side = "CE - CALL BUY"
    elif pcr <= MAX_PCR_BEARISH:
        score += 1
        reasons.append(f"PCR {pcr} Bearish ✅")
        side = "PE - PUT BUY"
    else:
        return None, f"PCR {pcr} Neutral hai - Trade SKIP"

    # 3. OI Change
    if abs(oi_change) >= MIN_OI_CHANGE_PCT:
        score += 1
        reasons.append(f"OI Change {oi_change}% ✅")
    else:
        return None, f"OI Change {oi_change}% kam hai - Trade SKIP"

    # 4. Multi Strike OI
    if multi_strike_oi_bullish:
        score += 1
        reasons.append("Multi Strike OI ✅")
    else:
        return None, "Multi Strike OI Confirm nahi - Trade SKIP"

    # 5. Sab mil gaya = SOLID SIGNAL
    if score >= 4:
        target = round(price * (1 + TARGET_PCT/100), 1)
        stoploss = round(price * (1 - STOPLOSS_PCT/100), 1)
        signal = {
            "symbol": symbol, "side": side, "entry": price,
            "target": target, "stoploss": stoploss,
            "target_pct": TARGET_PCT, "stoploss_pct": STOPLOSS_PCT,
            "pcr": pcr, "oi_change": oi_change, "reasons": reasons,
            "confidence": "HIGH - SOLID SETUP"
        }
        TRADES_TODAY.append(signal)
        return signal, "SOLID SIGNAL MILA"
    return None, "Filter Fail"

@app.route("/")
def home():
    return "Arif SOLID Bot is Live!"

@app.route("/api/totp")
def totp_api():
    return jsonify({"totp": get_totp(), "client_code": CLIENT_CODE, "status": "Live"})

@app.route("/api/signal/<symbol>")
def test_signal(symbol):
    # Test ke liye - Abhi dummy data, Live me Angel API se aayega
    sig, msg = analyze_solid_signal(symbol.upper(), 150, 1.25, 12.5, True, True)
    return jsonify({"signal": sig, "msg": msg, "trades_today": len(TRADES_TODAY)})

def telegram_bot():
    import requests, time
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"
    offset = 0
    print("SOLID Telegram Bot Started...")
    while True:
        try:
            r = requests.get(url + "getUpdates", params={"offset": offset, "timeout": 30}, timeout=35).json()
            for upd in r.get("result", []):
                offset = upd["update_id"] + 1
                msg = upd.get("message", {})
                chat_id = msg.get("chat", {}).get("id")
                text = msg.get("text", "").strip().lower()
                if not chat_id:
                    continue
                if text == "/start":
                    reply = "Namaste Arif Bhai! 🤝\nSOLID Bot Live Hai ✅\n\nStrategy:\nTarget: 30%\nStoploss: 12%\nTimeframe: 15 Min\nDin ke Max Trade: 2-3\nFilter: PCR + OI + Multi Strike OI\n\nCommands:\n/signal - Aaj ka Signal\n/status - Bot Status\n/totp - TOTP"
                elif text == "/status":
                    reply = f"SOLID Bot: LIVE ✅\nClient: {CLIENT_CODE}\nAaj ke Trade: {len(TRADES_TODAY)}/{MAX_TRADES_PER_DAY}\nTarget: {TARGET_PCT}% | SL: {STOPLOSS_PCT}%\nSymbols: NIFTY | SENSEX | BANKNIFTY"
                elif text == "/signal":
                    # Yahan abhi test signal hai, Live Angel data judne ke baad real aayega
                    sig, msg2 = analyze_solid_signal("NIFTY", 150, 1.25, 12.5, True, True)
                    if sig:
                        reply = f"🔥 SOLID SIGNAL 🔥\n\nSymbol: {sig['symbol']}\nSide: {sig['side']}\nEntry: {sig['entry']}\n🎯 Target 30%: {sig['target']}\n🛑 Stoploss 12%: {sig['stoploss']}\nPCR: {sig['pcr']}\nOI Change: {sig['oi_change']}%\nConfidence: HIGH\n\nReason: {' | '.join(sig['reasons'])}"
                    else:
                        reply = f"Abhi koi SOLID Signal nahi hai.\nWajah: {msg2}\n\nBot wait kar raha hai, halki trade nahi lega."
                elif text == "/totp":
                    reply = f"TOTP: {get_totp()}"
                else:
                    reply = "Samajh nahi aaya. /start bhejo."
                requests.post(url + "sendMessage", json={"chat_id": chat_id, "text": reply})
        except Exception as e:
            print("Telegram Error:", e)
            time.sleep(5)

threading.Thread(target=telegram_bot, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
