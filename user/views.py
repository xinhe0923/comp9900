from flask import Blueprint, render_template
from user.models import User


user_page = Blueprint('user_page',__name__)

@user_page.route('/login')
def login():

    # user = User(name = 'zeshi', password='123',email= 'email@gmail.com')
    # user.save
    #return "HI,{}!, Your email is {}".format(user.name,user.email)

    return render_template('user/login.html')


@user_page.route('/signup')
def signup():
    return render_template('user/signup.html')


