from app import app, db
from models import Address, FoodResource, TimeSlot, User
from forms import RequestNewFoodResourceForm, LoginForm
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.user.forms import LoginForm as LoginForm2
from flask.ext.user.forms import Form as Form2

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        u = User.query.filter_by(username = form.username.data).first()
        if(u):
        	if(u.verify_password(candidate = form.password.data)):
        		print 'verified!'
        	else:
        		print 'password is wrong!'
        else:
        	print 'failed to login!'
    return render_template('login.html', form=form)

@app.route('/login2', methods=['GET', 'POST'])
def login2():
    login_form = LoginForm2()
    form = LoginForm2()
    return render_template('user/login_temp_rename.html',form=form, login_form=login_form)

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
