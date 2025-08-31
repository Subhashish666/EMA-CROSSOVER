import yfinance as yf
import pandas as pd
import requests
import time

# Telegram bot setup
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"   # Replace with your actual chat ID
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Fetch data function
def get_data(symbol="BTC-USD", interval="15m", period="2d"):
    df = yf.download(tickers=symbol, interval=interval, period=period)
    df.dropna(inplace=True)
    return df

# Send Telegram message
def send_telegram(msg):
    try:
        requests.post(BASE_URL, data={"chat_id": CHAT_ID, "text": msg})
    except Exception as e:
        print("Telegram error:", e)

def main():
    df = get_data()

    # Calculate EMA
    df["EMA7"] = df["Close"].ewm(span=7, adjust=False).mean()
    df["EMA21"] = df["Close"].ewm(span=21, adjust=False).mean()

    last_ema7 = df["EMA7"].iloc[-1]
    last_ema21 = df["EMA21"].iloc[-1]
    prev_ema7 = df["EMA7"].iloc[-2]
    prev_ema21 = df["EMA21"].iloc[-2]

    # Check if EMAs touched/crossed
    if (prev_ema7 < prev_ema21 and last_ema7 >= last_ema21) or \
       (prev_ema7 > prev_ema21 and last_ema7 <= last_ema21):
        
        # Instant notification
        send_telegram("⚡ EMA Touch/ Cross Detected")

        # Reminder after 5 min
        time.sleep(300)
        send_telegram("⏰ Reminder: EMA Touch/ Cross Happened 5 min ago")

if __name__ == "__main__":
    main()
