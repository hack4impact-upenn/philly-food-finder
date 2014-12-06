from app import app, db, utils
from utils import get_time
from models import *
from forms import AddNewFoodResourceForm, RequestNewFoodResourceForm
from flask import render_template, flash, redirect, session, url_for, request, \
    g, jsonify, current_app
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from variables import resources_info_singular, resources_info_plural, \
    days_of_week
from datetime import time
from utils import generate_password
from flask_user import login_required, signals
from flask_user.views import _endpoint_url, _send_registered_email
from flask_login import current_user, login_user, logout_user

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/map')
def map():
    return render_template('newmaps.html')

@app.route('/new', methods=['GET', 'POST'])
@app.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def new(id=None):
    form = AddNewFoodResourceForm(request.form)
    additional_errors = []
    if request.method == 'POST' and form.validate(): 
        # Create food resource's timeslots.
        timeslots = []
        is_timeslot_valid = True
        for i, day_of_week in enumerate(days_of_week): 
            if (request.form[day_of_week['id'] + '-open-or-closed'] == "open"):
                opening_time = request.form[day_of_week['id'] + '-opening-time']
                start_time = get_time(opening_time)
                closing_time = request.form[day_of_week['id'] + '-closing-time']
                end_time = get_time(closing_time)
                if start_time >= end_time: 
                    is_timeslot_valid = False
                    additional_errors.append("Opening time must be before closing time.")
                if is_timeslot_valid:
                    timeslot = TimeSlot(day_of_week = i, start_time = start_time, 
                        end_time = end_time)
                    db.session.add(timeslot)
                    timeslots.append(timeslot)
        # Create food resource's address.
        if is_timeslot_valid:
            address = Address(
                line1 = form.address_line1.data, 
                line2 = form.address_line2.data, 
                city = form.address_city.data, 
                state = form.address_state.data, 
                zip_code = form.address_zip_code.data)
            db.session.add(address)
            # Create food resource's phone number.
            phone_numbers = []
            phone_number = PhoneNumber(number = form.phone_number.data)
            db.session.add(phone_number)
            phone_numbers.append(phone_number)
            # Create food resource and store all data in it.
            food_resource = FoodResource(
                name = form.name.data, 
                phone_numbers = phone_numbers,
                description = form.additional_information.data,
                timeslots = timeslots,
                address = address)
            for resource_info in resources_info_singular:
                if (request.form['food-resource-type'] == resource_info['id']+'-option'):
                    food_resource.location_type = resource_info['enum']
            db.session.add(food_resource)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('add_resource.html', form=form, 
        days_of_week=days_of_week, resources_info=resources_info_singular, 
        additional_errors=additional_errors)

@app.route('/admin')
@login_required
def admin():
	resources = {}
	resources['farmers-markets'] = FoodResource.query.filter_by(location_type="FARMERS_MARKET")
	resources['meals-on-wheels'] = FoodResource.query.filter_by(location_type="MEALS_ON_WHEELS")  
	resources['food-cupboards'] = FoodResource.query.filter_by(location_type="FOOD_CUPBOARD")
	resources['share-host-sites'] = FoodResource.query.filter_by(location_type="SHARE")
	resources['soup-kitchens'] = FoodResource.query.filter_by(location_type="SOUP_KITCHEN")
	resources['wic-offices'] = FoodResource.query.filter_by(location_type="WIC_OFFICE")
	return render_template('admin_resources.html', resources_info=resources_info_plural, 
	    resources=resources, days_of_week=days_of_week)

@login_required
def invite():
	""" Display invite form and create new User."""
	user_manager =  current_app.user_manager
	db_adapter = user_manager.db_adapter

	next = request.args.get('next', _endpoint_url(user_manager.after_login_endpoint))
	reg_next = request.args.get('reg_next', _endpoint_url(user_manager.after_register_endpoint))

	login_form = user_manager.login_form()                      
	register_form = user_manager.register_form(request.form)   

	if request.method!='POST':
		login_form.next.data     = register_form.next.data     = next
		login_form.reg_next.data = register_form.reg_next.data = reg_next

	# Process valid POST
	if request.method=='POST' and register_form.validate():

		User = db_adapter.UserClass
		user_class_fields = User.__dict__
		user_fields = {}

		if db_adapter.UserEmailClass:
			UserEmail = db_adapter.UserEmailClass
			user_email_class_fields = UserEmail.__dict__
			user_email_fields = {}

		if db_adapter.UserAuthClass:
			UserAuth = db_adapter.UserAuthClass
			user_auth_class_fields = UserAuth.__dict__
			user_auth_fields = {}

		# Enable user account
		if db_adapter.UserProfileClass:
			if hasattr(db_adapter.UserProfileClass, 'active'):
				user_auth_fields['active'] = True
			elif hasattr(db_adapter.UserProfileClass, 'is_enabled'):
				user_auth_fields['is_enabled'] = True
			else:
				user_auth_fields['is_active'] = True
		else:
			if hasattr(db_adapter.UserClass, 'active'):
				user_fields['active'] = True
			elif hasattr(db_adapter.UserClass, 'is_enabled'):
				user_fields['is_enabled'] = True
			else:
				user_fields['is_active'] = True

		# For all form fields
		for field_name, field_value in register_form.data.items():	
			# Store corresponding Form fields into the User object and/or UserProfile object
			if field_name in user_class_fields:
				user_fields[field_name] = field_value
			if db_adapter.UserEmailClass:
				if field_name in user_email_class_fields:
					user_email_fields[field_name] = field_value
			if db_adapter.UserAuthClass:
				if field_name in user_auth_class_fields:
					user_auth_fields[field_name] = field_value

		# Generates temporary password
		password = generate_password(9)
		if db_adapter.UserAuthClass:
			user_auth_fields['password'] = password
		else:
			user_fields['password'] = password

		g.temp_password = password

		# Add User record using named arguments 'user_fields'
		user = db_adapter.add_object(User, **user_fields)
		if db_adapter.UserProfileClass:
			user_profile = user

		# Add UserEmail record using named arguments 'user_email_fields'
		if db_adapter.UserEmailClass:
			user_email = db_adapter.add_object(UserEmail,
					user=user,
					is_primary=True,
					**user_email_fields)
		else:
			user_email = None

		# Add UserAuth record using named arguments 'user_auth_fields'
		if db_adapter.UserAuthClass:
			user_auth = db_adapter.add_object(UserAuth, **user_auth_fields)
			if db_adapter.UserProfileClass:
				user = user_auth
			else:
				user.user_auth = user_auth
		db_adapter.commit()

		# Send 'invite' email and delete new User object if send fails
		if user_manager.send_registered_email:
			try:
				# Send 'invite' email
				_send_registered_email(user, user_email)
			except Exception as e:
				# delete new User object if send  fails
				db_adapter.delete_object(user)
				db_adapter.commit()
				raise e

		# Send user_registered signal
		signals.user_registered.send(current_app._get_current_object(), user=user)

		# Redirect if USER_ENABLE_CONFIRM_EMAIL is set
		if user_manager.enable_confirm_email:
			next = request.args.get('next', _endpoint_url(user_manager.after_register_endpoint))
			return redirect(next)

		# Auto-login after register or redirect to login page
		next = request.args.get('next', _endpoint_url(user_manager.after_confirm_endpoint))
		if user_manager.auto_login_after_register:
			return _do_login_user(user, reg_next)                     # auto-login
		else:
			return redirect(url_for('user.login')+'?next='+reg_next)  # redirect to login page

	# Process GET or invalid POST
	return render_template(user_manager.register_template,
			form=register_form,
			login_form=login_form,
			register_form=register_form)

@app.route('/_invite_sent')
def invite_sent():
	return render_template('invite_sent.html')

@app.route('/_admin')
def get_food_resource_data():
	farmers_markets = FoodResource.query.filter_by(location_type="FARMERS_MARKET")
	meals_on_wheels = FoodResource.query.filter_by(location_type="MEALS_ON_WHEELS")  
	food_cupboards = FoodResource.query.filter_by(location_type="FOOD_CUPBOARD")
	share_host_sites = FoodResource.query.filter_by(location_type="SHARE")
	soup_kitchens = FoodResource.query.filter_by(location_type="SOUP_KITCHEN")
	wic_offices = FoodResource.query.filter_by(location_type="WIC_OFFICE")
	names = FoodResource.query.all()
	return jsonify(farmers_markets=[i.serialize_name_only() for i in farmers_markets],
		meals_on_wheels=[i.serialize_name_only() for i in meals_on_wheels],
		food_cupboards=[i.serialize_name_only() for i in food_cupboards],
		share_host_sites=[i.serialize_name_only() for i in share_host_sites],
		soup_kitchens=[i.serialize_name_only() for i in soup_kitchens],
		wic_offices=[i.serialize_name_only() for i in wic_offices])

@app.route('/_map')
def address_food_resources():
    addresses = FoodResource.query.all()
    return jsonify(addresses=[i.serialize_map_list() for i in addresses])

@app.route('/_edit', methods=['GET', 'POST'])
def save_page():
    data = request.form.get('edit_data')
    name = request.form.get('page_name')
    if(data):
    	page = HTML.query.filter_by(page = name).first()
    	page.value = data
    	db.session.commit()
    return 'Added' + data + 'to database.'

#TODO: Remove this edit demo page once editing works on all others.
@app.route('/admin/edit')
def edit_content():
	return render_template('edit_content.html', html_string = HTML.query.filter_by(page = 'edit-page').first())

@app.route('/about')
def about():
	return render_template('about.html', html_string = HTML.query.filter_by(page = 'about-page').first())

@app.route('/faq')
def faq():
	return render_template('faq.html', html_string = HTML.query.filter_by(page = 'faq-page').first())

@app.route('/contact')
def contact():
	return render_template('contact.html', html_string = HTML.query.filter_by(page = 'contact-page').first())