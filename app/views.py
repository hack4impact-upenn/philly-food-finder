from app import app, db
from models import Address, FoodResource, TimeSlot, User
from forms import RequestNewFoodResourceForm
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required

@app.route('/')
def index():
    return "Hello World!"

@app.route('/new_food_resource', methods=['GET', 'POST'])
def register():
    form = RequestNewFoodResourceForm(request.form)
    if request.method == 'POST' and form.validate():
        # user = User(form.username.data, form.email.data,
        #             form.password.data)
        # db_session.add(user)
        # flash('Thanks for registering')
        # return redirect(url_for('login'))
        return "Hello World!"
    return render_template('add_resource.html', form=form)

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