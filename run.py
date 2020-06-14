from app import app, bot
import os

if __name__ == '__main__':
    assert bot.init_webhook() is True, "WebHook not initialized"
    app.run(host="localhost" if 'HOST' in os.environ and os.environ['HOST'] == 'Baby' else '0.0.0.0',
            port=9999,
            debug=True)
