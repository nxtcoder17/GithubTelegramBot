from flask import Flask

app = Flask(__name__)

from app import telegram_bot as bot
from app import routes


