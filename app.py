import pyotp
from flask import Flask, jsonify

app = Flask(__name__)

API_KEY = "YmmvTd2T"
CLIENT_CODE = "A748605"
PASSWORD = "7233"
TOTP_SECRET = "G5SN3LR7LVJUYFUIQKIN2CQCJU"
TARGET_PCT = 30
STOPLOSS_PCT = 12

def get_totp():
    totp = pyotp.TOTP(TOTP_SECRET)
    return totp.now()

@app.route("/")
def home():
    return "Arif Option Bot is Live!"

@app.route("/api/totp")
def totp_api():
    return jsonify({"totp": get_totp(), "client_code": CLIENT_CODE})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
