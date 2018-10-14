
from flask import Blueprint, render_template, request,session, flash,redirect, url_for,abort
from user.models import User
from user.forms import RegistrationForm,LoginForm,EditForm
from user.decorator import login_required
import bcrypt

from utilities.storage import upload_image_file

user_page = Blueprint('user_page',__name__)

@user_page.route('/login', methods =['GET','POST'])
def login():

    # user = User(name = 'zeshi', password='123',email= 'email@gmail.com')
    # user.save
    #return "HI,{}!, Your email is {}".format(user.name,user.email)
    form = LoginForm(request.form)
    error = None

    if request.method == 'POST' and form.validate():
        user = User.objects.filter(email=form.email.data).first()
        if user: # if exit then verify psw
            if bcrypt.checkpw(form.password.data, user.password):
                session['email'] = user.email
                #session['username'] = user.name
                return redirect(request.args.get('next') or url_for('home_page.explore'))
            else:
                user = None
        if not user:
            error = 'Your email or psw was incrorect'

    return render_template('user/login.html', form=form)


@user_page.route('/logout')
@login_required
def logout():
  session.pop('email')
  #session.pop('username')
  return redirect(url_for('user_page.login'))



@user_page.route('/signup', methods =['GET','POST'])
def signup():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(form.password.data, salt)
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=hash_password

        )
        user.save()
        flash("Registered successfully")

        return '{} signup'.format(form.name.data)

    return render_template('user/signup.html', form =form)


@user_page.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    user = User.objects.filter(email=session['email']).first()
    if user:
        error = None
        message = None
        form = EditForm(obj=user)

        if request.method == 'POST' and form.validate():
            if user.email != form.email.data: #if change email
                if User.objects.filter(email=form.email.data).first():
                    error = "Email is already in use"
                else:
                    session['email'] = form.email.data.lower()
            if not error:
                form.populate_obj(user) # rewrite in to form
                image_url = upload_image_file(request.files.get('image'), 'proflie_image', str(user.id))
                if image_url:
                    user.profile_image = image_url

                user.save()
                message = "Profile updated"

        return render_template('user/edit.html', user=user,form=form,error =error, message=message)
    else:
        abort(404)
