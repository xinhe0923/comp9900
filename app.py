from flask import Flask,redirect,url_for,render_template
from flask_mongoengine import MongoEngine

from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms.fields import DateField

db = MongoEngine()

def create_app(config= None):
    app = Flask(__name__)
    if config is not None:
        app.config.from_object(config)
    db.init_app(app)
    Bootstrap(app)

    @app.route("/")
    def hello():
        #return "home"
        return redirect(url_for('home_page.explore'))


    # book s


    class MyForm(Form):
        date = DateField(id='datepick')

    @app.route('/index')
    def index():
        form = MyForm()
        return render_template('index.html', form=form)

    #book end


    from user.views import user_page
    app.register_blueprint(user_page,url_prefix ="/user")

    from home.views import home_page
    app.register_blueprint(home_page, url_prefix="/home")

    # from comment.views import comments
    # app.register_blueprint(comments, url_prefix="/comment")

    return app

