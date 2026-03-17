import requests
from app.config import settings

def send_newsletter(newsletter):

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": newsletter
    }

    response = requests.post(url, json=payload)

    print("📩 Telegram response:", response.text)