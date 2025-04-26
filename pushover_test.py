import yfinance as yf
import pandas as pd
import requests
from datetime import datetime

# --- Pushover Credentials ---
PUSHOVER_USER_KEY = "ukjj19k3xndb93qeovzj2yk84v5yn2"
PUSHOVER_APP_TOKEN = "ab2ojh3egagcihiktn4ndx95x961yq"

# --- Pushover Nachricht Funktion ---
def send_pushover(message):
    url = "https://api.pushover.net/1/messages.json"
    data = {
        "user": PUSHOVER_USER_KEY,
        "token": PUSHOVER_APP_TOKEN,
        "message": message
    }
    requests.post(url, data=data)

# --- Parameter ---
ticker = 'RHM.DE'  # Rheinmetall
fast_ma_period = 10
slow_ma_period = 20

# --- Daten laden ---
data = yf.download(ticker, period='5d', interval='15m')  # letzte 5 Tage, 15 Minuten Intervalle
data['fast_ma'] = data['Close'].rolling(window=fast_ma_period).mean()
data['slow_ma'] = data['Close'].rolling(window=slow_ma_period).mean()

# --- Aktueller Wert ---
latest = data.iloc[-1]  # letzte Zeile
close_price = latest['Close'].item()
fast_ma = latest['fast_ma'].item()
slow_ma = latest['slow_ma'].item()

# --- Entscheidungslogik ---
if close_price > fast_ma and close_price > slow_ma:
    send_pushover(f"{ticker}: 🛡️ HOLD THE LINE!")
elif close_price < fast_ma and close_price < slow_ma:
    send_pushover(f"{ticker}: 😱 KOMPLETTE PANIK ALLES LOSWERDEN!")
else:
    send_pushover(f"{ticker}:🔥🔥 THIS IS FINE 🔥🔥", ticker)

print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Nachricht verschickt.")