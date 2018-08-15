from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import Form, StringField,PasswordField,validators, ValidationError,FileField #biao dan
from wtforms.fields.html5 import EmailField
from user.models import User

from wtforms.widgets import TextArea

class BaseUserForm(FlaskForm):
    name = StringField('Username', [validators.DataRequired(),validators.Length(min=3, max=25),])
    email = EmailField('Email address', [ validators.DataRequired(), validators.Email() ])


class EditForm(BaseUserForm):
    image = FileField("Profile image",
                      validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'bmp'], "Only allow .jpg .png files")])
    bio = StringField("Bio", widget= TextArea(),
                      validators=[validators.Length(max=200)])



class RegistrationForm(BaseUserForm):
    # name = StringField('Your name' , [validators.DataRequired(), validators.Length(min=2,max=30)])
    # email = EmailField('Email Address', [validators.DataRequired(), validators.Email()])
    #
    password = PasswordField ('New Password', [ validators.DataRequired(),
                                                validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

    def validate_email(Form, field): # if the mail ready exit,
        if User.objects.filter(email=field.data).first():
            raise ValidationError("Email already in use")


class LoginForm(FlaskForm):
    email = EmailField("Email", [validators.DataRequired(),validators.Email()])
    password = PasswordField('Password', [ validators.DataRequired(),validators.Length(max=80)])