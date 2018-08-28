from app import db
from user.models import User


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

  #need one attribute ，"occupier" at specific time

  attendees = db.ListField(db.ReferenceField(User))

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
<<<<<<< HEAD
  # #attendees = db.ListField(db.ReferenceField(User))

=======
  # #attendees = db.ListField(db.ReferenceField(User))
>>>>>>> 39cd828dcebfc892011ed8b2deef98b4e9c8078c
