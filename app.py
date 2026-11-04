import pyotp
from flask import Flask, jsonify
from SmartApi import SmartConnect
import datetime

app = Flask(__name__)

# ===== FINAL CONFIG =====
API_KEY = "YmmvTd2T"
CLIENT_CODE = "A748605"
PASSWORD = "7233"
TOTP_SECRET = "G5SN3LR7LVJYUFUIQKIN2CQCJU"

# ===== SOLID STRATEGY SETTINGS =====
TARGET_PCT = 30  # 30% Target
STOPLOSS_PCT = 12 # 12% Stoploss
MAX_TRADES_PER_DAY = 3
TIMEFRAME = "15minute"
# ================================

def get_totp():
    return pyotp.TOTP(TOTP_SECRET).now()

def get_login():
    smart = SmartConnect(api_key=API_KEY)
    data = smart.generateSession(CLIENT_CODE, PASSWORD, get_totp())
    return smart, data

def get_15min_trend(smart, symbol_token, exchange="NSE"):
    # 15min candle analysis
    try:
        to_date = datetime.datetime.now()
        from_date = to_date - datetime.timedelta(days=2)
        params = {
            "exchange": exchange,
            "symboltoken": symbol_token,
            "interval": "FIFTEEN_MINUTE",
            "fromdate": from_date.strftime("%Y-%m-%d %H:%M"),
            "todate": to_date.strftime("%Y-%m-%d %H:%M")
        }
        candles = smart.getCandleData(params)
        if not candles or not candles.get('data'):
            return "SIDEWAYS", 0
        data = candles['data']
        last = data[-1]  # [time, open, high, low, close, volume]
        prev = data[-2]
        last_close = last[4]
        prev_close = prev[4]
        # VWAP jaisa simple trend: last 3 candle up/down
        last_3 = [c[4] for c in data[-3:]]
        if last_3[2] > last_3[1] > last_3[0] and last_close > prev_close:
            return "BULLISH", last_close
        elif last_3[2] < last_3[1] < last_3[0] and last_close < prev_close:
            return "BEARISH", last_close
        else:
            return "SIDEWAYS", last_close
    except Exception as e:
        return "SIDEWAYS", 0

def get_pcr_and_oi(smart, symbol="NIFTY"):
    # Option Chain se PCR + OI Bias
    try:
        # Angel One Option Chain
        params = {"symbolname": symbol, "exchange": "NFO"}
        chain = smart.optionChain(params)
        if not chain or not chain.get('data'):
            return 1.0, "NEUTRAL", 0
        
        data = chain['data']
        total_ce_oi = 0
        total_pe_oi = 0
        total_ce_change = 0
        total_pe_change = 0
        
        # ATM ke aas paas ki 5-5 strike hi lenge - Multi Strike OI
        for item in data[:11]:
            ce = item.get('CE', {})
            pe = item.get('PE', {})
            total_ce_oi += ce.get('openInterest', 0)
            total_pe_oi += pe.get('openInterest', 0)
            total_ce_change += ce.get('changeinOpenInterest', 0)
            total_pe_change += pe.get('changeinOpenInterest', 0)
        
        if total_ce_oi == 0:
            return 1.0, "NEUTRAL", 0
        
        pcr = total_pe_oi / total_ce_oi if total_ce_oi else 1.0
        
        # OI Change se bias
        # PE me zyada OI badh raha = Bullish, CE me zyada = Bearish
        if total_pe_change > total_ce_change and pcr > 1.0:
            bias = "BULLISH"
        elif total_ce_change > total_pe_change and pcr < 0.9:
            bias = "BEARISH"
        else:
            bias = "NEUTRAL"
            
        return round(pcr, 2), bias, total_pe_change - total_ce_change
    except:
        return 1.0, "NEUTRAL", 0

@app.route('/')
def home():
    return "Arif Solid Bot Running - 15min + OI + PCR"

@app.route('/api/signal')
def signal():
    try:
        smart, login_data = get_login()
        if login_data.get('status') == False:
            return jsonify({"angel_login": "FAILED", "error": login_data.get('message')})
        
        # 1. NIFTY 15min Trend - Token 26000
        trend, ltp = get_15min_trend(smart, "26000", "NSE")
        
        # 2. PCR + OI
        pcr, oi_bias, oi_diff = get_pcr_and_oi(smart, "NIFTY")
        
        # 3. SOLID FILTER - Teeno ek saath hona chahiye warna NO TRADE
        final_signal = "NO TRADE"
        reason = ""
        option_type = ""
        entry = 0
        target = 0
        stoploss = 0
        
        # CALL ke liye solid condition
        if trend == "BULLISH" and oi_bias == "BULLISH" and pcr >= 1.0:
            final_signal = "BUY CALL - SOLID"
            option_type = "CE"
            reason = f"15min BULLISH + PCR {pcr} Bullish + PE OI Badh Raha"
        
        # PUT ke liye solid condition
        elif trend == "BEARISH" and oi_bias == "BEARISH" and pcr <= 0.9:
            final_signal = "BUY PUT - SOLID"
            option_type = "PE"
            reason = f"15min BEARISH + PCR {pcr} Bearish + CE OI Badh Raha"
        else:
            reason = f"Wait - Trend:{trend} | PCR:{pcr} | OI Bias:{oi_bias} - Teenon match nahi hue, isliye NO TRADE"
        
        # Entry / Target / SL - Option Premium pe
        # LTP se ATM strike nikal ke uska premium lenge
        if final_signal != "NO TRADE":
            # Example: NIFTY ATM premium assume 100 se calculate karenge, live me optionChain se ayega
            # Yahan hum NIFTY LTP se ATM nikalte hai
            atm = round(ltp / 50) * 50
            # ATM option ka LTP lene ki koshish
            try:
                # Symbol token ke liye option chain se premium lena best hai, abhi demo ke liye
                entry = 100  # Isko live option LTP se replace hoga
                target = round(entry * (1 + TARGET_PCT/100), 2)
                stoploss = round(entry * (1 - STOPLOSS_PCT/100), 2)
            except:
                entry = 0
                target = 0
                stoploss = 0

        return jsonify({
            "angel_login": "LOGIN SUCCESS",
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "index": "NIFTY",
            "nifty_ltp": ltp,
            "15min_trend": trend,
            "pcr": pcr,
            "oi_bias": oi_bias,
            "oi_diff": oi_diff,
            "signal": final_signal,
            "option_type": option_type,
            "entry": entry,
            "target_30pct": target,
            "stoploss_12pct": stoploss,
            "reason": reason,
            "max_trades_today": MAX_TRADES_PER_DAY,
            "note": "Sirf SOLID signal pe trade lo, NO TRADE matlab paisa bach gaya"
        })
    except Exception as e:
        return jsonify({"angel_login": "FAILED", "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
