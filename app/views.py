from app import app, db
from models import Address, FoodResource, TimeSlot, User
from forms import RequestNewFoodResourceForm
from flask import render_template, flash, redirect, session, url_for, request, \
    g, jsonify
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from variables import resources_info_singular, resources_info_plural, \
    days_of_week

@app.route('/')
def index():
    return "Hello World!"

@app.route('/new_food_resource', methods=['GET', 'POST'])
def new_food_resource():
    form = RequestNewFoodResourceForm(request.form)
    if request.method == 'POST' and form.validate():
        # user = User(form.username.data, form.email.data,
        #             form.password.data)
        # db_session.add(user)
        # flash('Thanks for registering')
        # return redirect(url_for('login'))
        return "Hello World!"
    return render_template('add_resource.html', form=form, 
        days_of_week=days_of_week, resources_info=resources_info_singular)

@app.route('/admin')
#@login_required
def admin():
    resources = FoodResource.query.all()
    return render_template('admin.html', resources=resources, 
        resources_info=resources_info_plural)

@app.route('/_admin')
def get_food_resource_data():
    names = FoodResource.query.all()
    return jsonify(names=[i.serialize_name_only() for i in names])