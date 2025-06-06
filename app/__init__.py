from flask import Flask
from .routes import bp
def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp, url_prefix='/api')
    return app
