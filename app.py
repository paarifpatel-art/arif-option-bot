from flask import Flask, jsonify, render_template_string
import datetime

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ARIF OPTION BOT - LIVE</title>
<style>
body{background:#000;color:#fff;font-family:Arial;text-align:center;padding:20px;margin:0}
.card{background:linear-gradient(135deg,#0f0f0f,#1a1a1a);border:1px solid #00ff88;border-radius:20px;padding:20px;margin:15px auto;max-width:400px;box-shadow:0 0 20px #00ff8855}
.live{color:#00ff88;font-weight:bold;animation:blink 1s infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.3}}
.btn{background:#00ff88;color:#000;padding:15px 30px;border-radius:30px;border:none;font-weight:bold;font-size:18px;width:90%;max-width:300px;margin:10px;cursor:pointer}
h1{color:#00ff88}
.price{font-size:32px;font-weight:bold;margin:10px}
</style>
</head>
<body>
<h1>ARIF OPTION BOT</h1>
<div class="card">
<p class="live">● LIVE - PERMISSION GRANTED</p>
<p>Owner: <b>ARIF BHAI</b></p>
<p id="time"></p>
</div>
<div class="card">
<p>NIFTY 50</p>
<div class="price">24,568.75 UP 1.2%</div>
<p>Signal: <b style="color:#00ff88">BANKNIFTY 52000 CE BUY</b></p>
</div>
<div class="card">
<p>BANK NIFTY</p>
<div class="price">52,340.20 UP 0.8%</div>
<p>Target: <b>52,500</b> | SL: <b>52,100</b></p>
</div>
<button class="btn" onclick="alert('Signal Generated! BUY BANKNIFTY 52000 CE')">GET TODAY SIGNAL 📈</button>
<button class="btn" style="background:#fff" onclick="location.reload()">REFRESH LIVE 🔄</button>
<p style="margin-top:30px;color:#888">Bot ID: arif-option-bot<br>GitHub: paarifpatel-art<br>Status: GRANTED ✓</p>
<script>
function updateTime(){
 document.getElementById('time').innerText = new Date().toLocaleString('en-IN',{timeZone:'Asia/Kolkata'});
}
setInterval(updateTime,1000);
updateTime();
</script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/api')
def api():
    return jsonify({
        "bot": "arif-option-bot",
        "github": "paarifpatel-art",
        "owner": "ARIF BHAI",
        "permission": "GRANTED",
        "status": "LIVE",
        "time": datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
