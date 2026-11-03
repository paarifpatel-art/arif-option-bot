import os
from flask import Flask, jsonify

app = Flask(__name__)

# Angel One credentials from Render Environment
API_KEY = os.environ.get("API_KEY"ymmvtd2t")
CLIENT_ID = os.environ.get("CLIENT_ID"A748605")
PASSWORD = os.environ.get("PASSWORD"7233")
TOTP_SECRET = os.environ.get("TOTP_SECRET"G5SN3LR7LVJUYFUIQKIN2CQCJ")

@app.route("/")
def home():
    return "Arif Option Bot is LIVE!"

@app.route("/api/signal")
def signal():
    # Dummy signal for testing - real logic baad me
    return jsonify({
        "status": "success",
        "live_data": True,
        "message": "Bot is running!",
        "signal": "No trade"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
