from app import app, bot
from flask import request, Response
import json
from pprint import pprint


def parse_message(msg):
    if 'message' in msg:
        chat_id, text = msg['message']['chat']['id'], msg['message']['text']
    else:
        chat_id, text = msg['edited_message']['chat']['id'], msg['edited_message']['text']
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
        else:
            bot.send_message(chat_id, text)
    return Response('OK', status=200)


def parse_github_response(github_resp):
    return dict(
        email=github_resp['pusher']['email'],
        # name=github_resp['pusher']['name'],
        # repo_name=github_resp['repository']['full_name'],
        # repo_url=github_resp['repository']['html_url'],
        # message=github_resp['head_commit']['message'],
        # commit_url=github_resp['head_commit']['url'],
    )


@app.route('/<chat_id>/github', methods=['POST'])
def github_event(chat_id):
    print("I am here");
    pprint(request.json);
    if request.headers['content-type'] == 'application/json':
        data = parse_github_response(request.json)
        # email, name, repo_name, repo_url, message, commit_url = parse_github_response(request.json)

#         bot.send_formatted_message(chat_id, f"""
# 﫯 <b>{data['email']}</b>
#  <b>{data['name']}</b>
#  <b>{data['message']}</b>
# <a href="{data['repo_url']}">{data['repo_name']}</a>
# [![Generic badge](https://img.shields.io/badge/<SUBJECT>-<STATUS>-<COLOR>.svg)](https://shields.io/)
# """)
        email_msg = f"[![Generic badge](https://img.shields.io/badge/EMAIL-{data['email']}-green.svg)]" + \
                    "(https://shields.io/)"
        email_msg = f"﫯 <b>{data['email']}</b>"

        email_msg = f"<a src='https://img.shields.io/badge/EMAIL-{data['email']}-green.svg'>{data['email']}</a>"

        msg = r"""
{email}
<a src=https://img.shields.io/badge/EMAIL-nxtcoder17@gmail.com-green.svg>.</a>
"""

        bot.send_formatted_message(chat_id, msg.format(email=email_msg))
        # bot.send_formatted_message(chat_id, email_msg)
        print(msg.format(email=email_msg))
        return Response('OK', status=200)
    return json.dumps({"msg": "No Response"})
