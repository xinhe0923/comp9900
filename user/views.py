from flask import Blueprint, render_template,request
from user.models import User
from user.forms import RegistrationForm


user_page = Blueprint('user_page',__name__)

@user_page.route('/login')
def login():

    # user = User(name = 'zeshi', password='123',email= 'email@gmail.com')
    # user.save
    #return "HI,{}!, Your email is {}".format(user.name,user.email)

    return render_template('user/login.html')


@user_page.route('/signup', methods=['GET','POST'])
def signup():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(form.password.data, salt)
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=hash_password
            # password= form.password.data # hahh, we can see the detailed psw, but it seems illegal :)

        )
        user.save()
        flash("Registered successfully")

        return '{} signup'.format(form.name.data)

    return render_template('user/signup.html', form=form)







