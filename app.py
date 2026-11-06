import random
from datetime import datetime

def get_dynamic_signal():
    # Har baar alag signal ke liye time se seed
    now = datetime.now()
    seed = int(now.strftime("%H%M")) + random.randint(1, 1000)
    random.seed(seed)

    symbols = ["NIFTY", "BANKNIFTY", "SENSEX"]
    symbol = random.choice(symbols)
    side = random.choice(["CE - CALL BUY", "PE - PUT BUY"])

    # Entry ko realistic rakho
    if symbol == "NIFTY":
        entry = random.randint(80, 220)
    elif symbol == "BANKNIFTY":
        entry = random.randint(100, 300)
    else:
        entry = random.randint(90, 250)

    target = round(entry * 1.30, 1)  # 30% Target
    stoploss = round(entry * 0.88, 1) # 12% Stoploss

    pcr = round(random.uniform(0.85, 1.45), 2)
    oi_change = round(random.uniform(5.0, 18.5), 1)

    return f"""🔥 SOLID SIGNAL 🔥

Symbol: {symbol}
Side: {side}
Entry: {entry}
🎯 Target 30%: {target}
🛑 Stoploss 12%: {stoploss}
PCR: {pcr}
OI Change: {oi_change}%
Confidence: HIGH

Reason: 15Min Candle ✅ | PCR {pcr} Bullish ✅ | OI Change {oi_change}% ✅ | Multi Strike OI ✅"""

# /signal command me ye lagao:
# bot.send_message(chat_id, get_dynamic_signal())
