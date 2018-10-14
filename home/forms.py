from flask_wtf import FlaskForm
from wtforms import StringField, validators, DateTimeField, FloatField
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileAllowed


class BasicHomeForm(FlaskForm):
    name = StringField('Home Title Name', validators=[validators.DataRequired(), validators.Length(min=2, max=80)])
    gplace = StringField('GOOGLE Places API TEST')
    lng = FloatField("Longtitude", validators=[validators.Optional()])
    lat = FloatField("Latitude", validators=[validators.Optional()])
    place = StringField('Place', validators=[validators.DataRequired()], widget=TextArea())
    capacity = StringField('People', validators=[validators.DataRequired()])
    price = StringField('Price $', validators=[validators.DataRequired()])
    contact = StringField('Contact', validators=[validators.DataRequired()])
    # avaiblable period
    start_datetime = DateTimeField('Avaiblable From', validators=[validators.DataRequired()], format='%Y-%m-%d')
    end_datetime = DateTimeField('Avaiblable By', validators=[validators.DataRequired()], format='%Y-%m-%d')
    description = StringField('Discription', widget=TextArea(), validators=[validators.Length(min=20)])


class CancelHomeForm(FlaskForm):
    confirm = StringField("Are you sure you want to cancel?", validators=[validators.DataRequired()])


class EditForm(BasicHomeForm):
    photo = FileField("Home Photo",
                      validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'bmp'], "Only allow .jpg .png .gif files"),
                                  validators.Optional()])



