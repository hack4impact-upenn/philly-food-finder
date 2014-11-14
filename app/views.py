from app import app, db
from models import Address, FoodResource, TimeSlot, User
from forms import AddNewFoodResourceForm, RequestNewFoodResourceForm
from flask import render_template, flash, redirect, session, url_for, request, \
    g, jsonify
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from variables import resources_info_singular, resources_info_plural, \
    days_of_week
from datetime import time

@app.route('/')
def index():
    return "Hello World!"

@app.route('/new_food_resource', methods=['GET', 'POST'])
def new_food_resource():
    form = AddNewFoodResourceForm(request.form)
    if request.method == 'POST' and form.validate():
        timeslots = []
        for i, day_of_week in enumerate(days_of_week): 
            opening_time = request.form[day_of_week['id'] + '-opening-time']
            closing_time = request.form[day_of_week['id'] + '-closing-time']
            timeslot = TimeSlot(day_of_week = i, start_time = time(8,0), 
                end_time = time(18,30))
            db.session.add(timeslot)
            timeslots.append(timeslot)
        address = Address(
            line1 = form.address_line1.data, 
            line2 = form.address_line2.data, 
            city = form.address_city.data, 
            state = form.address_state.data, 
            zip_code = form.address_zip_code.data)
        db.session.add(address)
        food_resource = FoodResource(
            name = form.name.data, 
            phone_number = form.phone_number.data,
            description = form.additional_information.data,
            timeslots = timeslots,
            address = address)
        db.session.add(food_resource)
        db.session.commit()
        #food_resource = FoodResource()
        # user = User(form.username.data, form.email.data,
        #             form.password.data)
        # db_session.add(user)
        # flash('Thanks for registering')
        # return redirect(url_for('login'))
        return redirect(url_for('index'))
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