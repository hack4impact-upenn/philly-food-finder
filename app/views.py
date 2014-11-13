from app import app, db
from models import Address, FoodResource, TimeSlot, User
from forms import RequestNewFoodResourceForm
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask_user import login_required
from flask_login import current_user, login_user, logout_user

@app.before_request
def load_users():
    if current_user.is_authenticated():
        g.user = current_user # return username in get_id()
        print 'here!' + current_user.email
    else:
        g.user = None # or 'some fake value', whatever

@app.route('/')
def index():
    return "Hello World!"

@app.route('/new_food_resource', methods = ['GET', 'POST'])
def add_resource():
    form = RequestNewFoodResourceForm(request.form)
    days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", 
        "Friday", "Saturday"]
    if request.method == 'POST' and form.validate():
        return "Hello World!"
    return render_template('add_resource.html', form=form)

@app.route('/admin')
@login_required
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
