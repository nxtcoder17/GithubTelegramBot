from app import app, bot
from flask import request, Response
import json
from pprint import pprint


def parse_message(msg):
    chat_id, text = msg['message']['chat']['id'], msg['message']['text']
    return chat_id, text


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.json
        pprint(msg)
        # return Response('OK', status=200)
        chat_id, text = parse_message(msg)
        if text.upper() == 'HI':
            bot.send_message(chat_id, "Fuck it dude")
        else:
            bot.send_message(chat_id, text)
    return Response('OK', status=200)


@app.route('/github', methods=['POST'])
def github_event():
    if request.headers['content-type'] == 'application/json':
        pprint(request.json)
        bot.send_message('847119416', 'hello from github')
        bot.send_message('847119416', str(request.json))
        return request.json
    return json.dumps({"msg": "No Response"})
