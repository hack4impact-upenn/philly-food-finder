from app import app, db
from models import Address, FoodResource, TimeSlot, User
from forms import RequestNewFoodResourceForm, LoginForm
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask_user import login_required
from flask_login import current_user, login_user, logout_user

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
    user_manager =  app.user_manager
    db_adapter = user_manager.db_adapter

    # Immediately redirect already logged in users
    if current_user.is_authenticated():
        return redirect('/admin')

    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = None
        user_email = None
        user, user_email = user_manager.find_user_by_email(form.email.data)

        if user:
            # Log user in
            login_user(user)
            redirect('/admin')

    return render_template('login.html', form=form)

def logout():
    """ Sign the user out."""
    user_manager =  current_app.user_manager

    # Send user_logged_out signal
    signals.user_logged_out.send(current_app._get_current_object(), user=current_user)

    # Use Flask-Login to sign out user
    logout_user()

    # Prepare one-time system message
    flash(_('You have signed out successfully.'), 'success')

    # Redirect to logout_next endpoint or '/'
    next = request.args.get('next', _endpoint_url(user_manager.after_logout_endpoint))  # Get 'next' query param
    return redirect(next)

@login_required
@app.route('/admin')
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
