
from flask import Blueprint,render_template,request,session,redirect,url_for,abort,flash
from home.forms import BasicHomeForm, EditForm,CancelHomeForm
from user.decorator import login_required

from home.models import Home
from user.models import User
from utilities.storage import upload_image_file
import json
import bson


home_page = Blueprint('home_page',__name__)

@home_page.route('/create',methods=['GET','POST'])
@login_required
def create():
  form = BasicHomeForm()
  error = None
  if request.method == "POST" and form.validate():
    if form.end_datetime.data < form.start_datetime.data:
      error = "Available time must end after it starts!"
    if not error:
      user = User.objects.filter(email=session.get('email')).first()
      home = Home(
        name=form.name.data,
        place=form.place.data,
        location=[form.lng.data, form.lat.data],
        start_time=form.start_datetime.data,
        end_time=form.end_datetime.data,
        description=form.description.data,
        host=user.id,
        attendees=[user]
      )
      # image_url = upload_image_file(request.files.get('photo'), 'party_photo', str(party.id))
      # if image_url:
      #   party.party_photo = image_url

      home.save() #save to mdb
      return '{} created'.format(home.name)

  return render_template('home/create.html', form = form)


@home_page.route('/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
  try:
    home = Home.objects.filter(id=bson.ObjectId(id)).first()
  except bson.error.InvalidId:
    abort(404)

  user = User.objects.filter(email=session.get('email')).first()
  if home and home.host == user.id: # only host(admin) can modify
    error = None
    message = None
    form = EditForm(obj=home)
    if request.method == "POST" and form.validate():
      if not error:
        form.populate_obj(home)
        if form.lng.data and form.lat.data:
          home.location = [form.lng.data, form.lat.data]
        image_url = upload_image_file(request.files.get('photo'), 'party_photo', str(home.id))
        if image_url:
          home.party_photo = image_url
          home.save()
        message = "HOMe updated"
    return render_template('home/edit.html', form=form, error=error, message=message, home=home)
  else:
    abort(404)


@home_page.route('/<id>/cancel',methods=['GET','POST'])
@login_required
def cancel(id):
  try:
    home = Home.objects.filter(id=bson.ObjectId(id)).first()
  except bson.errors.InvalidId:
    return "None"
  user = User.objects.filter(email=session.get('email')).first()
  if home and home.host == user.id and home.cancel == False:
    error = None
    form = CancelHomeForm()
    if request.method=="POST" and form.validate():
      if form.confirm.data == 'yes':
        home.cancel = True
        home.save()
        return redirect(url_for('home_page.edit',id=home.id))
      else:
        error = "Say yes if you want to cancel"
    return render_template("home/cancel.html",form=form,error=error,home=home)
  else:
    return "None"


@home_page.route('/<id>',methods=['GET']) # review page
def public(id):
  try:
    home = Home.objects.filter(id=bson.ObjectId(id)).first()
  except bson.errors.InvalidId:
    return "None"
  if home:
    host = User.objects.filter(id=home.host).first()
    user = User.objects.filter(email=session.get('email')).first()
    return render_template('home/public.html',home=home,host=host,user=user)
  else:
    abort(404)


@home_page.route('/explore/<int:page>', methods=['GET'])
@home_page.route('/explore', methods=['GET'])
def explore(page=1):
  place = request.args.get('place') #encoding error
  # lng = float(request.args.get('lng')) # can not be empty
  # lat = float(request.args.get('lat'))

  # in the beginning when we open home/explore, it shows all homes which is display_home
  display_home = Home.objects(cancel=False).order_by('-start_time').paginate(page=page, per_page=4)

  #homes = Home.objects(cancel=False).order_by('-start_time').paginate(page=page, per_page=4)

  try:
    lng = float(request.args.get('lng'))
    lat = float(request.args.get('lat'))
    print(lng,lat)
    homes = Home.objects(location__near=[lng, lat], location__max_distance=10000,
                            cancel=False).order_by('-start_time').paginate(page=page, per_page=4)

    if homes : print("yes")
    print(homes)

    return render_template("home/explore.html", homes=homes, display_home=display_home, place= place,lng=lng,
                           lat=lat)
  except:

    return render_template('home/explore.html', place= place,display_home=display_home)


