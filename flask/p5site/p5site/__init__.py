from flask import Flask
from .views import article
from .views import account

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings.TestConfig")

    app.register_blueprint(account.ac)
    app.register_blueprint(article.art)

    return app

