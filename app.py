from flask import Flask, jsonify
import requests, datetime
app = Flask(__name__)
BOT_TOKEN = "8760898163:AAEMgX69Z2tvXGuTw9_dmN4xIB0FVWJXNDA"

def get_levels():
    # Expiry - Next Thursday
    today = datetime.date.today()
    return {
        "BANK NIFTY": {"price": "52,340", "trend": "BULLISH", "strike": "52300 CE (CALL)", "action": "✅ 52300 CALL BUY KARO", "expiry": "06 Nov 2025 Expiry", "lot": "1 Lot (15 Qty)", "entry": "52340", "t1": "52500", "t2": "52800", "sl": "52100", "logic": "Bank Strong Hai - 52200 Support"},
        "NIFTY 50": {"price": "24,550", "trend": "BULLISH", "strike": "24500 CE (CALL)", "action": "✅ 24500 CALL BUY KARO", "expiry": "06 Nov 2025 Expiry", "lot": "1 Lot (75 Qty)", "entry": "24550", "t1": "24700", "t2": "24850", "sl": "24350", "logic": "24500 Ke Upar Strong Support"},
        "SENSEX": {"price": "80,120", "trend": "BEARISH", "strike": "80000 PE (PUT)", "action": "✅ 80000 PUT BUY KARO", "expiry": "06 Nov 2025 Expiry", "lot": "1 Lot (10 Qty)", "entry": "80120", "t1": "79800", "t2": "79500", "sl": "80300", "logic": "80200 Ke Neeche Selling Zone"}
    }

HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>ARIF PRO</title><style>body{background:#000;color:#fff;font-family:system-ui;padding:12px} .card{border:2px solid #222;border-radius:22px;padding:16px;margin:14px 0} .bull{border-color:#00ff88} .bear{border-color:#ff3b30} .opt{font-size:19px;font-weight:900;padding:10px 14px;border-radius:12px;display:inline-block;margin:8px 0} .cb{background:#00ff88;color:#000} .pb{background:#ff3b30;color:#fff} .info{background:#111;border-radius:12px;padding:10px;margin-top:8px;font-size:13px} .btn{width:100%;padding:15px;border-radius:50px;border:none;font-weight:900;margin:8px 0} .g{background:#00ff88} .b{background:#0088ff;color:#fff}</style></head><body><h2 style="text-align:center;color:#00ff88">● ARIF PRO BOT - LIVE</h2><h3 style="text-align:center">Owner: ARIF BHAI - Trade with Patel Sahab</h3><div id="box"></div><button class="btn g" onclick="load()">REFRESH KARO 🔄</button><button class="btn b" onclick="fetch('/send-telegram').then(r=>r.text()).then(a=>alert(a))">TELEGRAM PE BHEJO @Tradewithpatelsahab_AI_2026bot 🚀</button><script>function load(){fetch('/api/signals').then(r=>r.json()).then(d=>{let h='';for(let k in d){let v=d[k];let cls=v.trend=='BULLISH'?'bull':'bear';let optcls=v.strike.includes('CE')?'cb':'pb';h+=`<div class="card ${cls}"><div style="display:flex;justify-content:space-between"><b>${k}</b><b style="color:${v.trend=='BULLISH'?'#00ff88':'#ff3b30'}">${v.trend}</b></div><div style="font-size:30px;font-weight:900">${v.price}</div><div class="opt ${optcls}">${v.action}</div><div>Strike: <b>${v.strike}</b></div><div>Expiry: ${v.expiry} | ${v.lot}</div><div class="info">Entry: ${v.entry} | T1: ${v.t1} | T2: ${v.t2} | SL: <span style="color:#ff3b30">${v.sl}</span><br>Logic: ${v.logic}</div></div>`;}document.getElementById('box').innerHTML=h;});}load();</script></body></html>"""

@app.route('/')
def home(): return HTML
@app.route('/api/signals')
def signals(): return jsonify(get_levels())
@app.route('/send-telegram')
def send():
    levels=get_levels(); msg="🚀 TRADE WITH PATEL SAHAB 🚀\nOwner: ARIF BHAI\n";
    for k,v in levels.items(): msg+=f"\n{k} {v['trend']}\n➡️ {v['action']}\nStrike: {v['strike']}\nExp: {v['expiry']} | {v['lot']}\nEntry:{v['entry']} T1:{v['t1']} T2:{v['t2']} SL:{v['sl']}\n"
    try:
        r=requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates",timeout=5).json()
        if r['result']: 
            chat_id=r['result'][-1]['message']['chat']['id']
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",json={"chat_id":chat_id,"text":msg},timeout=5)
            return f"✅ Telegram Pe Bhej Diya!"
        else: return "❌ Pehle Telegram pe @Tradewithpatelsahab_AI_2026bot ko /start bhejo"
    except Exception as e: return f"Error: {e}"
if __name__=='__main__': app.run()
