from app import app, db
from models import Address, FoodResource, TimeSlot, User
from forms import RequestNewFoodResourceForm
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/new_food_resource', methods=['GET', 'POST'])
def register():
    form = RequestNewFoodResourceForm(request.form)
    days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", 
        "Friday", "Saturday"]
    if request.method == 'POST' and form.validate():
        # user = User(form.username.data, form.email.data,
        #             form.password.data)
        # db_session.add(user)
        # flash('Thanks for registering')
        # return redirect(url_for('login'))
        return "Hello World!"
    return render_template('add_resource.html', form=form, 
        days_of_week=days_of_week)

@app.route('/admin')
#@login_required
def admin():
    resources = FoodResource.query.all()
    resources_info = [
        ["farmers-markets", "Farmers' Markets"], 
        ["food-cupboards", "Food Cupboards"], 
        ["meals-on-wheels", "Meals On Wheels"], 
        ["share-host-sites", "SHARE Host Sites"], 
        ["soup-kitchens", "Soup Kitchens"],
        ["wic-offices", "WIC Offices"]]
    return render_template('admin.html', resources=resources, 
        resources_info=resources_info)

@app.route('/_admin')
def get_food_resource_data():
    names = FoodResource.query.all()
    return jsonify(names=[i.serialize_name_only() for i in names])
