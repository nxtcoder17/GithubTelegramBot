from app import app
import os

if __name__ == '__main__':
    app.run(host="localhost" if 'HOST' in os.environ and os.environ['HOST'] == 'Baby' else '0.0.0.0',
            port=9999,
            debug=True)
