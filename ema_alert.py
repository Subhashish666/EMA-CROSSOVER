import yfinance as yf
import pandas as pd
import requests
import os
import time

# Load token and chat_id from GitHub Secrets / Environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message: str):
    """Send message to Telegram bot"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Error sending Telegram message:", e)

def check_ema_touch():
    """Check if EMA9 and EMA21 touch in 15m timeframe"""
    data = yf.download("BTC-USD", interval="15m", period="2d")
    data["EMA9"] = data["Close"].ewm(span=9, adjust=False).mean()
    data["EMA21"] = data["Close"].ewm(span=21, adjust=False).mean()

    last_ema9 = data["EMA9"].iloc[-1]
    last_ema21 = data["EMA21"].iloc[-1]

    # Consider it a "touch" if the values are very close
    if abs(last_ema9 - last_ema21) <= 5:  # tolerance
        send_telegram_message("⚡ EMA Touch detected on BTC (15m)")

        # wait 5 min and send reminder
        time.sleep(300)
        send_telegram_message("⏰ Reminder: EMA Touch happened 5 min ago (BTC, 15m)")

if __name__ == "__main__":
    check_ema_touch()
