

import os.path
from app import create_app, socketio

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

app = create_app(BASE_DIR, DB_PATH)
app.host = '0.0.0.0'
app.debug = True


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
