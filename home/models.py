from app import db
from user.models import User
from comment.models import Comment


class Home(db.Document):
  name = db.StringField(required=True)
  place = db.StringField(required=True)
  location = db.PointField(required=True)
  start_time = db.DateTimeField(required=True)
  end_time = db.DateTimeField(required=True)
  home_photo = db.StringField()
  description = db.StringField(min_length=20,required=True)
  host = db.ObjectIdField(required=True) #link to USER DB
  cancel = db.BooleanField(default=False)

  occupy = db.BooleanField(default=False)
  capacity = db.StringField()
  price = db.StringField()
  contact=  db.StringField()



  #need one attribute ，"occupier" at specific time

  attendees = db.ListField(db.ReferenceField(User))

  comments = db.ListField(db.ReferenceField(Comment))

  # xuyue modify
  # event_name = db.StringField(required=True)
  # venue = db.StringField(required=True)
  # location = db.PointField(required=True)
  # #start_time = db.DateTimeField(required=True)
  # #end_time = db.DateTimeField(required=True)
  # #party_photo = db.StringField()
  # description = db.StringField(min_length=20, required=True)
  # #host = db.ObjectIdField(required=True)
  # #cancel = db.BooleanField(default=False)

  # rooms_booked = int(rooms_booked)

  # bookname = db.StringField('姓名', required=True)
  # bopokphone = db.StringField('电话', required=True)
  # bookphotoset = db.SelectField('套系', choices=[('SET1', '1'), ('SET2', '2')])
  # bookdate = db.DateField('预约时间', default='', required=True, format='%Y/%m/%d', widget=DatePickerWidget())
  # booksubmit = db.SubmitField("预定")

