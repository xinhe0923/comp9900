from flask import Flask
from flask_mongoengine import MongoEngine

db= MongoEngine()

def create_app(config = None):
    app = Flask(__name__)
    if config is not None:
        app.config.from_object(config)

    db.init_app(app)

    @app.route("/")
    def hello():
        return "hello world"

    from user.views import user_page
    app.register_blueprint(user_page,url_prefix="/user") #e.g. air/user/login

    return app