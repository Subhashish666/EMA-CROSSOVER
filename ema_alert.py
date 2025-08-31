import requests
import yfinance as yf
import pandas as pd

# 🔹 Your Telegram details
TELEGRAM_TOKEN = "8240031497:AAFTd0XwNR5obQLDGug2Zb2tW0z3p1lCeqc"
CHAT_ID = "1946138824"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram error:", e)

def main():
    # ✅ Always send a debug message when bot runs
    send_telegram_message("✅ Bot ran successfully, EMA check complete.")

    # Example: still fetch data so script runs correctly
    symbol = "AAPL"
    interval = "15m"
    period = "5d"

    df = yf.download(tickers=symbol, interval=interval, period=period)
    if not df.empty:
        df["EMA_9"] = df["Close"].ewm(span=9, adjust=False).mean()
        df["EMA_21"] = df["Close"].ewm(span=21, adjust=False).mean()

if __name__ == "__main__":
    main()
