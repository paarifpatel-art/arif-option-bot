import pyotp
from flask import Flask, jsonify
from SmartApi import SmartConnect
import datetime
app = Flask(__name__)
API_KEY = "YmmvTd2T"
CLIENT_CODE = "A748605"
PASSWORD = "7233"
TOTP_SECRET = "TOTP_SECRET = "G5SN3LR7LVJUYFUIQKIN2CQCJU"
TARGET_PCT = 30
STOPLOSS_PCT = 12
def get_totp():
    return pyotp.TOTP(TOTP_SECRET).now()
def get_login():
    smart = SmartConnect(api_key=API_KEY)
    data = smart.generateSession(CLIENT_CODE, PASSWORD, get_totp())
    return smart, data
@app.route('/')
def home():
    return "Arif Solid Bot Running - 15min + OI + PCR"
@app.route('/api/totp')
def totp_api():
    return jsonify({"bot_totp": get_totp(), "client_code": CLIENT_CODE})
@app.route('/api/signal')
def signal():
    try:
        smart, login_data = get_login()
        if login_data.get('status') == False:
            return jsonify({"angel_login": "FAILED", "error": login_data.get('message'), "bot_totp_used": get_totp()})
        try:
            ltp_data = smart.ltpData("NSE", "NIFTY", "26000")
            nifty_ltp = ltp_data['data']['ltp']
        except:
            nifty_ltp = 0
        return jsonify({"angel_login": "LOGIN SUCCESS", "nifty_ltp": nifty_ltp, "signal": "WAIT - 15min + OI + PCR Check", "target_30pct": "30% on Premium", "stoploss_12pct": "12% on Premium", "bot_totp_used": get_totp()})
    except Exception as e:
        return jsonify({"angel_login": "FAILED", "error": str(e)})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
