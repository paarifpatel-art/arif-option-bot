import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>✅ ARIF OPTION BOT LIVE HAI!</h1>
    <h3>Permission System Active</h3>
    <p>Bot Status: RUNNING</p>
    <p>Owner: paarifpatel-art</p>
    <p>Render Deploy: SUCCESS</p>
    <br>
    <a href='/status'>Check Status</a>
    """

@app.route('/status')
def status():
    return jsonify({
        "bot": "arif-option-bot",
        "status": "LIVE",
        "owner": "ARIF BHAI",
        "permission": "GRANTED",
        "github": "paarifpatel-art"
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
