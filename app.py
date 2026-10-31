from flask import Flask, jsonify, make_response
app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ARIF OPTION BOT</title>
<link rel="manifest" href="/manifest.json">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="ARIF BOT">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<link rel="apple-touch-icon" href="https://cdn-icons-png.flaticon.com/512/3135/3135715.png">
<style>
body{background:#000;color:#fff;font-family:system-ui;text-align:center;padding:20px}
.card{border:2px solid #00ff88;border-radius:20px;padding:20px;margin:20px 0;box-shadow:0 0 20px #00ff8855}
.btn{padding:18px 30px;border-radius:50px;border:none;font-weight:900;font-size:18px;width:90%;margin:10px}
.green{background:#00ff88;color:#000}
.gray{background:#333;color:#fff}
.live{color:#00ff88;animation:blink 1s infinite}
@keyframes blink{50%{opacity:0}}
</style>
</head>
<body>
<div class="live">● LIVE - PERMISSION GRANTED</div>
<h2>Owner: ARIF BHAI</h2>
<div class="card">
<h1 style="font-size:42px;margin:10px">52,340.20 <span style="color:#00ff88">UP 0.8%</span></h1>
<p>Target: 52,500 | SL: 52,100</p>
</div>
<button class="btn green" onclick="alert('NIFTY 50 CE BUY - 52,500 Target!')">GET TODAY SIGNAL 📈</button>
<button class="btn gray" onclick="location.reload()">REFRESH LIVE 🔄</button>
<p style="opacity:0.5;margin-top:20px">Bot ID: arif-option-bot<br>GitHub: paarifpatel-art<br>Status: GRANTED ✓</p>
<p style="margin-top:30px;font-size:12px;opacity:0.3">arif-option-bot.onrender.com</p>
<script>
if('serviceWorker' in navigator){navigator.serviceWorker.register('/sw.js')}
</script>
</body>
</html>
"""

@app.route('/')
def home(): return HTML

@app.route('/manifest.json')
def manifest():
    m = {
      "name": "ARIF OPTION BOT",
      "short_name": "ARIF BOT",
      "start_url": "/",
      "display": "standalone",
      "background_color": "#000000",
      "theme_color": "#00ff88",
      "icons": [{"src": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png","sizes": "512x512","type": "image/png"}]
    }
    return jsonify(m)

@app.route('/sw.js')
def sw():
    js = "self.addEventListener('fetch', function(e){})"
    r = make_response(js)
    r.headers['Content-Type'] = 'application/javascript'
    return r

if __name__ == '__main__':
    app.run()
