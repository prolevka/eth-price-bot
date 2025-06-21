import time
import requests
from telegram import Bot
import os
from dotenv import load_dotenv
load_dotenv()


TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)

CHECK_INTERVAL = 60  # каждые 60 секунд
STEP = 50  # шаг в долларах
last_alert_price = None


def get_eth_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "ethereum", "vs_currencies": "usd"}
    response = requests.get(url, params=params)
    return response.json()["ethereum"]["usd"]


def send_alert(price):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"🚨 Цена ETH: ${price:.2f}")


def main():
    global last_alert_price
    print("⏳ Старт отслеживания...")

    while True:
        try:
            price = get_eth_price()
            print(f"Текущая цена ETH: ${price:.2f}")

            if last_alert_price is None:
                last_alert_price = round(price / STEP) * STEP
                send_alert(price)
            elif abs(price - last_alert_price) >= STEP:
                last_alert_price = round(price / STEP) * STEP
                send_alert(price)

        except Exception as e:
            print("❌ Ошибка:", e)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
