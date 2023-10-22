"""
This runs the app
"""
from flask import Flask


app = Flask(__name__, static_url_path = '/static', static_folder='static')

from routes import confirmation
from routes import profile
from routes import register_login_front
from routes import dashboard

if __name__ == "__main__":
    app.run()
