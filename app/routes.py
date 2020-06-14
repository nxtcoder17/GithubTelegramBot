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
        elif text.lower() == 'ok':
            ab="Anshuman"
            bot.send_formatted_message(chat_id, f"""
               [Github](https://github.githubassets.com/images/modules/logos_page/GitHub-Logo.png)
               Name: *{ab}*
                Name: *Anshuman*
            """
                                       )
        else:
            bot.send_message(chat_id, text)
    return Response('OK', status=200)


def parse_github_response(github_resp):
    return dict(
        email=github_resp['pusher']['email'],
        name=github_resp['pusher']['name'],
        repo_name=github_resp['repository']['full_name'],
        repo_url=github_resp['repository']['html_url']
    )


@app.route('/<chat_id>/github', methods=['POST'])
def github_event(chat_id):
    if request.headers['content-type'] == 'application/json':
        data = parse_github_response(request.json)
        print(data)
        msg = f"""
                Email: *{data.email}* 
                Name: *{data.name}* 
                [{data.repo_name}]({data.repo_url})
            """
        print(msg)
        bot.send_formatted_message(chat_id, msg)
        return Response('OK', status=200)
    return json.dumps({"msg": "No Response"})
