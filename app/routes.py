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
    added = set()
    modified = set()
    removed = set()
    for commit in github_resp['commits']:
        message = commit['message']
        for path in commit['added']:
            added.add(path)

        for path in commit['removed']:
            modified.add(path)

        for path in commit['modified']:
            removed.add(path)

    return dict(
        email=github_resp['pusher']['email'],
        name=github_resp['pusher']['name'],
        repo_name=github_resp['repository']['full_name'],
        repo_url=github_resp['repository']['html_url'],
        message=github_resp['head_commit']['message'],
        commit_url=github_resp['head_commit']['url'],
        added = added,
        removed = removed,
        modified = removed,
    )


@app.route('/<chat_id>/github', methods=['POST'])
def github_event(chat_id):
    print("I am here");
    pprint(request.json);
    if request.headers['content-type'] == 'application/json':
        data = parse_github_response(request.json)
        email_msg = f"﫯 <b>{data['email']}</b>"
        name_msg = f" <b>{data['name']}</b>"
        commit_msg = f" <b>{data['message']}</b>"
        commit_url = f"{data['commit_url']}"
        repo = f"""<a href="{data['repo_url']}">&#x02026;</a>"""

        files = "&#x0000A;&#x00009;a&#x02026;".join(data['modified']),

        msg = r"""
{email}
{name}
{repo}
{commit}
{commit_url}

Modified Files
{files}
"""

        bot.send_formatted_message(chat_id, msg.format(email=email_msg, name=name_msg,
                                                       repo=repo,
                                                       commit=commit_msg, commit_url=commit_url,
                                                       files=files))
        # bot.send_formatted_message(chat_id, email_msg)
        print(msg.format(email=email_msg))
        return Response('OK', status=200)
    return json.dumps({"msg": "No Response"})
