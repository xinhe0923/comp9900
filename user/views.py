from flask import Blueprint, render_template
from user.models import User


user_page = Blueprint('user_page',__name__)

@user_page.route('/login')
def login():
    # just for test
    # user = User(name = 'zeshi', password='123',email= 'email@gmail.com')
    # user.save
    # return "HI,{}!, Your email is {}".format(user.name,user.email)
    return render_template('base.html')

