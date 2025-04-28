# signal_alert_system.py

import yfinance as yf
import pandas as pd
import requests
from datetime import datetime

# --- CONFIG ---
TICKERS = {
    "ENR.DE": {"strategy": "ma", "fast": 9, "slow": 19, "name": "Siemens Energy AG"},
    "GLE.PA": {"strategy": "ma", "fast": 11, "slow": 21, "name": "Société Générale"},
    "INTC": {"strategy": "ma", "fast": 6, "slow": 15, "name": "Intel Corporation"},
    "AVGO": {"strategy": "ma", "fast": 10, "slow": 19, "name": "Broadcom Inc"},
    "UNH": {"strategy": "ma", "fast": 7, "slow": 15, "name": "UnitedHealth Group"},
    "UCG.MI": {"strategy": "ma", "fast": 7, "slow": 15, "name": "Unicredit SpA"},
    "HSBC": {"strategy": "ma", "fast": 7, "slow": 15, "name": "HSBC Holdings"}
}

PUSHOVER_USER_KEY = "ukjj19k3xndb93qeovzj2yk84v5yn2"
PUSHOVER_APP_TOKEN = "ab2ojh3egagcihiktn4ndx95x961yq"

START_HOUR = 9
END_HOUR = 22

# --- FUNCTIONS ---
def send_pushover(title, message):
    payload = {
        "token": PUSHOVER_APP_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "title": title,
        "message": message
    }
    requests.post("https://api.pushover.net/1/messages.json", data=payload)

def check_ma_signal(ticker, fast, slow):
    df = yf.download(ticker, period="7d", interval="5m", progress=False)
    if df.empty:
        return None
    df["fast_ma"] = df["Close"].rolling(fast).mean()
    df["slow_ma"] = df["Close"].rolling(slow).mean()
    df.dropna(inplace=True)
    df["position"] = (df["fast_ma"] > df["slow_ma"]).astype(int)
    if df["position"].iloc[-2] == 0 and df["position"].iloc[-1] == 1:
        return "BUY"
    elif df["position"].iloc[-2] == 1 and df["position"].iloc[-1] == 0:
        return "SELL"
    return None

def main():
    now = datetime.now()
    if not (START_HOUR <= now.hour < END_HOUR):
        return

    for ticker, params in TICKERS.items():
        if params["strategy"] == "ma":
            signal = check_ma_signal(ticker, params["fast"], params["slow"])
            if signal:
                title = f"{params['name']} ({ticker}) Signal: {signal}"
                if signal == "BUY":
                    message = "200er Rachehebel rein hier 🐮"
                elif signal == "SELL":
                    message = "Short Sell Everything, the 🐻 is coming"
                else:
                    message = f"{signal} signal detected for {params['name']} ({ticker}) (MA {params['fast']}/{params['slow']})"
                send_pushover(title, message)

if __name__ == "__main__":
    main()
