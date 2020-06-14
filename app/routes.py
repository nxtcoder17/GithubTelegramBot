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
    return (
        github_resp['pusher']['email'],
        github_resp['pusher']['name'],
        github_resp['repository']['full_name'],
        github_resp['repository']['html_url'],
        github_resp['head_commit']['message'],
        github_resp['head_commit']['url'],
    )


@app.route('/<chat_id>/github', methods=['POST'])
def github_event(chat_id):
    if request.headers['content-type'] == 'application/json':
        email, name, repo_name, repo_url, message, commit_url = parse_github_response(request.json)

        bot.send_formatted_message(chat_id, f"""
﫯 <b>{email}</b>
 <b>{name}</b>
<a href="{repo_url}"><b>  {repo_name}</b></a>
 <b>{message}</b> <u>{commit_url}</u>
""")
        return Response('OK', status=200)
    return json.dumps({"msg": "No Response"})
