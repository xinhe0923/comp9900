from app import db
from user.models import User
from comment.models import Comment


class Renant(db.Document):
    name = db.StringField(required=True)
    place = db.StringField(required=True)
    location = db.PointField(required=True)
    start_time = db.DateTimeField(required=True)
    end_time = db.DateTimeField(required=True)
    home_photo = db.StringField()
    description = db.StringField(min_length=20, required=True)
    host = db.ObjectIdField(required=True)  # link to USER DB
    cancel = db.BooleanField(default=False)
    capacity = db.StringField()
    price = db.StringField()
    contact = db.StringField()
    comments = db.ListField(db.ReferenceField(Comment))