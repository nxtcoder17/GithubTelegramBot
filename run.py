from app import app
import os

app.run(host="localhost" if os.environ['HOST'] == 'Baby' else '0.0.0.0',
        port=9999,
        debug=True)
