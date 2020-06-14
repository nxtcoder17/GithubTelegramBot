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
        elif text.lower() == '/github':
            bot.send_message(chat_id, f"{bot.SERVER_URL}/{chat_id}/github")
        elif text.lower() == 'google':
            bot.send_message(chat_id, )
        else:
            bot.send_message(chat_id, text)
    return Response('OK', status=200)


def parse_github_response(github_resp):
    pusher_email, pusher_name = github_resp['pusher']['email'], github_resp['pusher']['name']
    sender_img = github_resp['sender']['avatar_url']
    return pusher_email, pusher_name, sender_img


@app.route('/<chat_id>/github', methods=['POST'])
def github_event(chat_id):
    if request.headers['content-type'] == 'application/json':
        pprint(request.json)
        email, name, img = parse_github_response(request.json)
        msg = f"""Email: *{email}* Name: *{name}* []({img})"""
        print(msg)
        bot.send_formatted_message(chat_id, msg)
        return Response('OK', status=200)
    return json.dumps({"msg": "No Response"})

