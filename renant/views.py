
from flask import Blueprint,render_template,request,session,redirect,url_for,abort,flash
from renant.forms import BasicHomeForm, CancelHomeForm
from user.decorator import login_required

from renant.models import Renant
from user.models import User
from utilities.storage import upload_image_file
import json
import bson


renant_page = Blueprint('renant_page',__name__)

@renant_page.route('/create',methods=['GET','POST'])
@login_required
def create():
  form = BasicHomeForm()
  error = None
  if request.method == "POST" and form.validate():
    if form.end_datetime.data < form.start_datetime.data:
      error = "Available time must end after it starts!"
    if not error:
      user = User.objects.filter(email=session.get('email')).first()
      renant = Renant(
        name=form.name.data,
        place=form.place.data,
        location=[form.lng.data, form.lat.data],
        start_time=form.start_datetime.data,
        end_time=form.end_datetime.data,
        description=form.description.data,
        contact= form.contact.data,
        host=user.id,
        attendees=[user]

      )
      renant.save()         #save to mdb
      return '{} created'.format(renant.name)
  return render_template('renant/create.html', form = form)


@renant_page.route('/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
  try:
    renant = Renant.objects.filter(id=bson.ObjectId(id)).first()
  except bson.error.InvalidId:
    abort(404)

  user = User.objects.filter(email=session.get('email')).first()
  if renant and renant.host == user.id: # only host(admin) can modify
    error = None
    message = None
    form = EditForm(obj=home)
    if request.method == "POST":
      if not error:
        form.populate_obj(renant)
        if form.lng.data and form.lat.data:
          renant.location = [form.lng.data, form.lat.data]
          home.save()
        message = "Renant updated"
    return render_template('renant/edit.html', form=form, error=error, message=message, renant=renant)
  else:
    abort(404)

@renant_page.route('/<id>/cancel',methods=['GET','POST'])
@login_required
def cancel(id):
  try:
    renant = Renant.objects.filter(id=bson.ObjectId(id)).first()
  except bson.errors.InvalidId:
    return "None"
  user = User.objects.filter(email=session.get('email')).first()
  if renant and renant.host == user.id and home.cancel == False:
    error = None
    form = CancelRenantForm()
    if request.method=="POST" and form.validate():
      if form.confirm.data == 'yes':
        renant.cancel = True
        renant.save()
        return redirect(url_for('renant_page.edit',id=renant.id))
      else:
        error = "Say yes if you want to cancel"
    return render_template("renant/cancel.html",form=form,error=error,renant=renant)
  else:
    return "None"


@renant_page.route('/<id>',methods=['GET'])
def public(id):
  try:
    renant = Renant.objects.filter(id=bson.ObjectId(id)).first()
  except bson.errors.InvalidId:
    return "None"
  if renant:
    host = User.objects.filter(id=renant.host).first()
    user = User.objects.filter(email=session.get('email')).first()
    return render_template('renant/public.html',renant=renant,host=host,user=user)
  else:
    abort(404)


@renant_page.route('/explore/<int:page>', methods=['GET'])
@renant_page.route('/explore', methods=['GET'])
def explore(page=1):
  place = request.args.get('place') #encoding error
  display_renant = Renant.objects(cancel=False).order_by('-start_time').paginate(page=page, per_page=4)


  try:
    lng = float(request.args.get('lng'))
    lat = float(request.args.get('lat'))
    print(lng,lat)
    renants = Renant.objects(location__near=[lng, lat], location__max_distance=10000,
                            cancel=False).order_by('-start_time').paginate(page=page, per_page=4)

    if renants : print("yes")
    print(renants)

    return render_template("renant/explore.html", renants=renants, display_renant=display_renant, place= place,lng=lng,
                           lat=lat)
  except:

    return render_template('renant/explore.html', place= place,display_renant=display_renant)


@renant_page.route('/<id>/leave')
@login_required
def leave(id):
  user = User.objects.filter(email=session.get('email')).first()
  try:
    renant = Renant.objects.filter(id=bson.ObjectId(id)).first()
  except bson.errors.InvalidId:
    return abort(404)
  if user and renant:
    if user in renant.attendees:
      home.attendees.remove(user)
      flash("Quit this party successfully")
      renant.save()
      return redirect(url_for('renant_page.public', id=id))
  else:
    abort(404)


@renant_page.route('/<id>/join', methods=['GET'])
@login_required
def join(id):
  user = User.objects.filter(email=session.get('email')).first()
  try:
    renant = Renant.objects.filter(id=bson.ObjectId(id)).first()
  except bson.errors.InvalidId:
    return abort(404)
  if user and renant:
    if user not in renant.attendees:
      renant.attendees.append(user)
      flash("Join this party successfully!")
      renant.save()
    return redirect(url_for('renant_page.public', id=id))
  else:
    abort(404)