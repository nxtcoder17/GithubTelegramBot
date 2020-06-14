import requests
import os

BOT_TOKEN = "1233261801:AAFamDNXezo-kdf370embNI0HRFSLXlGnIw"

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

if 'USER' in os.environ and os.environ['USER'] == "nxtcoder17":
    SERVER_URL = 'https://5190f17042cb.ngrok.io'
else:
    SERVER_URL = 'https://githubtelegrambot.herokuapp.com'


def init_webhook():
    print("SERVER URL:", SERVER_URL)
    resp = requests.get(f"{BASE_URL}/setWebhook?url={SERVER_URL}")
    return resp.status_code == 200


def send_message(chat_id, text):
    resp = requests.post(f"{BASE_URL}/sendMessage", json={"chat_id": chat_id, "text": text})
    return resp.status_code == 200


def send_formatted_message(chat_id, text):
    resp = requests.post(f"{BASE_URL}/sendMessage", json=dict(chat_id=chat_id, text=text,
                                                              parse_mode="MarkdownV2",
                                                              disable_web_page_preview=True))
    return resp.status_code == 200
