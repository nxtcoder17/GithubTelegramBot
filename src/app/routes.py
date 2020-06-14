from app import app


@app.route('/')
def index():
    print("Flask, Web server is UP")
    return "Flask is running"


@app.route('/github', methods=['POST'])
def github_event(req):
    if req.headers['content-type'] == 'application/json':
        print(req.json)
        return req.json
    return req
