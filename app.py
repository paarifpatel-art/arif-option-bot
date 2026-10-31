from flask import Flask, jsonify, request
import requests, datetime
app = Flask(__name__)

# ===== YOUR BOT =====
BOT_TOKEN = "8760898163:AAEMgX69Z2tvXGuTw9_dmN4xIB0FVWJXNDA"
BOT_USERNAME = "@Tradewithpatelsahab_AI_2026bot"

# Default Chat ID - niche setup se auto milega
CHAT_ID = None  

def get_levels():
    return {
        "NIFTY 50": {"price": "24,550.40", "trend": "BULLISH", "action": "BUY NIFTY 24500 CE", "entry": "24550", "target1": "24700", "target2": "24850", "sl": "24350", "logic": "Above 24500 - Strong Support"},
        "BANK NIFTY": {"price": "52,340.20", "trend": "BULLISH", "action": "BUY BANKNIFTY 52300 CE", "entry": "52340", "target1": "52500", "target2": "52800", "sl": "52100", "logic": "Bank Strong - Holding 52200"},
        "SENSEX": {"price": "80,120.85", "trend": "BEARISH", "action": "BUY SENSEX 80000 PE", "entry": "80120", "target1": "79800", "target2": "79500", "sl": "80300", "logic": "Below 80200 - Selling Zone"}
    }

def send_telegram_signal():
    global CHAT_ID
    levels = get_levels()
    msg = f"🚀 <b>TRADE WITH PATEL SAHAB - SOLID LEVELS</b> 🚀\n⏰ {datetime.datetime.now().strftime('%d-%m-%Y %I:%M %p')}\n\n"
    for k,v in levels.items():
        emoji = "🟢" if v['trend']=="BULLISH" else "🔴"
        msg += f"{emoji} <b>{k} - {v['trend']}</b>\n💰 Price: {v['price']}\n👉 <b>{v['action']}</b>\n📍 Entry: {v['entry']} | 🎯 T1: {v['target1']} | 🎯 T2: {v['target2']} | 🛑 SL: {v['sl']}\n💡 {v['logic']}\n\n"
    msg += "👑 Owner: ARIF BHAI\n🤖 Bot: @Tradewithpatelsahab_AI_2026bot\n✅ Status: GRANTED"

    # Try to auto-get chat id if not set
    if not CHAT_ID:
        try:
            r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates", timeout=5).json()
            if r['result']:
                CHAT_ID = r['result'][-1]['message']['chat']['id']
        except: pass
    
    if CHAT_ID:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=10)
            return True, CHAT_ID
        except Exception as e:
            return False, str(e)
    return False, "Chat ID nahi mila - Pehle /setup karo"

HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>ARIF PRO BOT</title><link rel="manifest" href="/manifest.json">
<style>
body{background:#000;color:#fff;font-family:system-ui;padding:12px;margin:0}
.header{text-align:center}
.live{color:#00ff88;font-weight:900;animation:blink 1s infinite}@keyframes blink{50%{opacity:0}}
.card{border:1.5px solid #1a1a1a;border-radius:22px;padding:16px;margin:14px 0;background:#0a0a0a}
.bull{border-color:#00ff88;box-shadow:0 0 18px #00ff8844}.bear{border-color:#ff3b30;box-shadow:0 0 18px #ff3b3044}
.price{font-size:30px;font-weight:900}.buy{background:#00ff88;color:#000;padding:8px 12px;border-radius:10px;font-weight:900;display:inline-block;margin:6px 0}
.sell{background:#ff3b30;color:#fff;padding:8px 12px;border-radius:10px;font-weight:900;display:inline-block;margin:6px 0}
.row{display:flex;justify-content:space-between;font-size:13px;margin:3px 0}.t{color:#00ff88}.sl{color:#ff3b30}
.btn{width:100%;padding:16px;border-radius:50px;border:none;font-weight:900;font-size:15px;margin:8px 0}
.g{background:#00ff88}.b{background:#0088ff;color:#fff}.d{background:#222;color:#fff}
</style></head><body>
<div class="header"><div class="live">● LIVE PRO - @Tradewithpatelsahab_AI_2026bot</div><h2>Owner: ARIF BHAI</h2><p id="time" style="opacity:0.5;font-size:12px"></p></div>
<div id="box">Loading...</div>
<button class="btn g" onclick="load()">REFRESH ALL - NIFTY/BANKNIFTY/SENSEX 🔄</button>
<button class="btn b" onclick="sendTG()">SEND TO TELEGRAM @Tradewithpatelsahab_AI_2026bot 🚀</button>
<button class="btn d">Bot ID: arif-option-bot | Telegram: GRANTED ✓</button>
<script>
function load(){
 fetch('/api/signals').then(r=>r.json()).then(d=>{
  let h='';for(let k in d){let v=d[k];let cls=v.trend=='BULLISH'?'bull':'bear';
   let btn=v.trend=='BULLISH'?`<div class="buy">${v.action}</div>`:`<div class="sell">${v.action}</div>`;
   h+=`<div class="card ${cls}"><div class="row"><b>${k}</b><span class="live">${v.trend}</span></div><div class="price">${v.price}</div>${btn}<div class="row"><span>Entry: ${v.entry}</span><span>${v.logic}</span></div><div class="row"><span class="t">T1: ${v.target1}</span><span class="t">T2: ${v.target2}</span><span class="sl">SL: ${v.sl}</span></div></div>`;}
  document.getElementById('box').innerHTML=h;
 });document.getElementById('time').innerText=new Date().toLocaleString();
}
function sendTG(){fetch('/send-telegram').then(r=>r.text()).then(a=>alert(a));}
load();
</script></body></html>
"""

@app.route('/')
def home(): return HTML
@app.route('/api/signals')
def signals(): return jsonify(get_levels())
@app.route('/setup')
def setup():
    try:
        r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates").json()
        return jsonify(r)
    except Exception as e:
        return str(e)

@app.route('/send-telegram')
def send():
    ok, info = send_telegram_signal()
    if ok:
        return f"✅ Bhej Diya Telegram Pe! Chat ID: {info}"
    else:
        return f"❌ Pehle Telegram Pe Bot Ko Message Karo! Error: {info}\n\n1. Telegram pe @{BOT_USERNAME} search karo\n2. /start bhejo\n3. Fir is link ko kholo: /setup - wahan chat id dikhega"

@app.route('/manifest.json')
def mani():
    return jsonify({"name":"ARIF PRO BOT","short_name":"ARIF BOT","start_url":"/","display":"standalone","background_color":"#000","theme_color":"#00ff88","icons":[{"src":"https://cdn-icons-png.flaticon.com/512/3135/3135715.png","sizes":"512x512","type":"image/png"}]})

if __name__=='__main__': app.run()
