from flask import Flask,redirect,url_for
from flask_mongoengine import MongoEngine

db = MongoEngine()

def create_app(config= None):
    app = Flask(__name__)
    if config is not None:
        app.config.from_object(config)
    db.init_app(app)

    @app.route("/")
    def hello():
        #return "home"
        return redirect(url_for('home_page.explore'))

    from user.views import user_page
    app.register_blueprint(user_page,url_prefix ="/user")

    from home.views import home_page
    app.register_blueprint(home_page, url_prefix="/home")

    return app