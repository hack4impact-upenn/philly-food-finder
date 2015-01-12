from app import app, db, utils
from utils import *
from models import *
from forms import *
from flask import render_template, flash, redirect, session, url_for, request, \
	g, jsonify, current_app, Response
from flask.ext.login import login_user, logout_user, current_user, \
	login_required
from variables import *
from datetime import time
from utils import generate_password, import_file
from flask_user import login_required, signals
from flask_user.emails import send_email
from flask_user.views import _endpoint_url, _send_registered_email
from flask_login import current_user, login_user, logout_user
from tempfile import NamedTemporaryFile
import csv, time

@app.route('/admin/new', methods=['GET', 'POST'])
@app.route('/admin/edit/<id>', methods=['GET', 'POST'])
@login_required
def new(id=None):
	form = AddNewFoodResourceForm(request.form)

	# Set timeslot choices.
	for timeslots in form.daily_timeslots:
		for timeslot in timeslots.timeslots:
			timeslot.starts_at.choices=get_possible_opening_times()
			timeslot.ends_at.choices=get_possible_closing_times()

	# Set food resource type choices.
	food_resource_types = FoodResourceType.query \
		.order_by(FoodResourceType.name_plural).all()
	food_resource_types_choices = []
	for food_resource_type in food_resource_types:
		food_resource_types_choices.append(
			(food_resource_type.enum, 
			food_resource_type.name_singular)
		)
	form.location_type.choices = food_resource_types_choices

	# Create a new food resource. 
	if id is None:
		title = "Add New Food Resource"
		food_resource_type = food_resource_types_choices[0][0]
	# Edit an existing food resource.
	else:
		title = "Edit Food Resource"

	# GET request.
	if request.method == 'GET':
		if id is not None:
			# Populate form with information about existing food resource. 
			food_resource = FoodResource.query.filter_by(id=id).first()
			if food_resource is None:
				return render_template('404.html')

			# Data that can be directly retrieved from the database.
			form.name.data = food_resource.name
			form.address_line1.data = food_resource.address.line1
			form.address_line2.data = food_resource.address.line2
			form.address_city.data = food_resource.address.city
			form.address_state.data = food_resource.address.state
			form.address_zip_code.data = food_resource.address.zip_code
			form.phone_number.data = food_resource.phone_numbers[0].number
			form.website.data = food_resource.url
			form.additional_information.data = food_resource.description
			form.is_for_family_and_children.data = \
				food_resource.is_for_family_and_children
			form.is_for_seniors.data = food_resource.is_for_seniors
			form.is_wheelchair_accessible.data = \
				food_resource.is_wheelchair_accessible
			form.is_accepts_snap.data = food_resource.is_accepts_snap
			form.location_type.data = food_resource.food_resource_type.enum

			# Data that must be interpreted before being rendered.
			if food_resource.are_hours_available == True:
				form.are_hours_available.data = "yes"
			else:
				form.are_hours_available.data = "no"

			num_timeslots_per_day = [0] * 7
			for timeslot in food_resource.timeslots:
				day_of_week_index = timeslot.day_of_week
				timeslot_index = num_timeslots_per_day[timeslot.day_of_week]
				num_timeslots_per_day[timeslot.day_of_week] += 1
				start_time = timeslot.start_time
				end_time = timeslot.end_time
				form.daily_timeslots[day_of_week_index] \
					.timeslots[timeslot_index].starts_at.data = \
						start_time.strftime("%H:%M")
				form.daily_timeslots[day_of_week_index] \
					.timeslots[timeslot_index].ends_at.data = \
						end_time.strftime("%H:%M")
				form.is_open[day_of_week_index].is_open.data = "open"
				form.daily_timeslots[day_of_week_index].num_timeslots.data = \
					num_timeslots_per_day[timeslot.day_of_week]

	# POST request.
	additional_errors = []
	if request.method == 'POST' and form.validate(): 
		food_resource = create_food_resource_from_form(form, additional_errors)

		if (len(additional_errors) == 0):
			# If a food resource is being edited, remove its old verion from the 
			# database.
			if id is not None:
				fr = FoodResource.query.filter_by(id=id).first()
				if fr:
					for phone_number in fr.phone_numbers:
						db.session.delete(phone_number)
					for timeslot in fr.timeslots:
						db.session.delete(timeslot)
					db.session.delete(fr.address)
					db.session.delete(fr)

			# Commit all database changes. 
			db.session.add(food_resource)
			db.session.commit()
			return redirect(url_for('admin'))

	# If GET request is received or POST request fails due to invalid timeslots, 
	# render the page. 
	return render_template('add_resource.html', form=form, 
		days_of_week=days_of_week,  
		additional_errors=additional_errors, title=title)

# Allows non-admins to add food resources
@app.route('/propose-resource', methods=['GET', 'POST'])
def guest_new_food_resource():
	form = NonAdminAddNewFoodResourceForm(request.form)

	# Set timeslot choices.
	for timeslots in form.daily_timeslots:
		for timeslot in timeslots.timeslots:
			timeslot.starts_at.choices=get_possible_opening_times()
			timeslot.ends_at.choices=get_possible_closing_times()

	# Set food resource type choices.
	food_resource_types = FoodResourceType.query \
		.order_by(FoodResourceType.name_plural).all()
	food_resource_types_choices = []
	for food_resource_type in food_resource_types:
		food_resource_types_choices.append(
			(food_resource_type.enum, 
			food_resource_type.name_singular)
		)
	form.location_type.choices = food_resource_types_choices

	# Initialize location type.
	if request.method == 'GET':
		form.location_type.data = food_resource_types_choices[0][0]

	additional_errors = []
	if request.method == 'POST' and form.validate(): 
		# Check if this guest has added resources in the past. If not,
		# create a new FoodResourceContact.
		guest_name = form.your_name.data
		guest_email = form.your_email_address.data
		guest_phone_number = form.your_phone_number.data

		# Check to see if this contact exists.
		contact = FoodResourceContact.query \
			.filter_by(email=guest_email, name=guest_name).first()

		if contact is None:
			contact = FoodResourceContact(name=guest_name, 
				email=guest_email, phone_number=guest_phone_number)
			db.session.add(contact)

		food_resource = create_food_resource_from_form(form, additional_errors)

		if (len(additional_errors) == 0):
			# Additional fields that are relevant for pending resources.
			food_resource.is_approved = False
			food_resource.food_resource_contact = contact
			food_resource.notes = form.notes.data

			# Commit all database changes. 
			db.session.add(food_resource)
			db.session.commit()
			return redirect(url_for('post_guest_add'))

	# If GET request is received or POST request fails due to invalid timeslots, 
	# render the page. 
	return render_template('guest_add_resource.html', form=form, 
		days_of_week=days_of_week,  
		additional_errors=additional_errors)

@app.route('/_thank-you')
def post_guest_add():
	return render_template('thank_you.html')

@app.route('/admin/manage-resources')
@login_required
def admin():
	food_resource_types = FoodResourceType.query \
		.order_by(FoodResourceType.name_plural).all()
	for food_resource_type in food_resource_types:
		for food_resource in list(food_resource_type.food_resources):
			if food_resource.is_approved == False:
				food_resource_type.food_resources.remove(food_resource)

	contacts = FoodResourceContact.query.all()

	return render_template('admin_resources.html', 
		food_resource_contacts=contacts, 
		days_of_week=days_of_week,
		food_resource_types=food_resource_types)

@app.route('/admin')
def admin_redirect():
	return redirect(url_for('admin'))

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
			# Store corresponding Form fields into the User object and/or 
			# UserProfile object
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
@login_required
def invite_sent():
	return render_template('invite_sent.html')

@app.route("/_admin_remove_filters")
@login_required
def get_all_food_resource_data():
	food_resource_types = FoodResourceType.query \
		.order_by(FoodResourceType.name_plural).all()
	for food_resource_type in food_resource_types:
		for food_resource in list(food_resource_type.food_resources):
			if food_resource.is_approved == False:
				food_resource_type.food_resources.remove(food_resource)

	return jsonify(days_of_week=days_of_week, 
		food_resource_types=[i.serialize_food_resource_type() for i in \
			food_resource_types])

@app.route('/_admin_apply_filters')
@login_required
def get_filtered_food_resource_data():
	# Collect boolean paramaters passed via JSON.
	has_zip_code_filter = request.args.get('has_zip_code_filter', 0, type=int)
	zip_code = request.args.get('zip_code', 0, type=int)
	has_families_and_children_filter = request.args.get(
		'has_families_and_children_filter', 0, type=int) 
	has_seniors_filter = request.args.get('has_seniors_filter', 0, type=int) 
	has_wheelchair_accessible_filter = request.args.get(
		'has_wheelchair_accessible_filter', 0, type=int) 
	has_accepts_snap_filter = request.args.get(
		'has_accepts_snap_filter', 0, type=int) 
	has_open_now_filter = request.args.get(
		'has_open_now_filter', 0, type=int) 

	# Create empty arrays to hold food resources.
	all_resources = []
	food_resource_types = FoodResourceType.query \
		.order_by(FoodResourceType.name_plural).all()

	# Zip code is one of the filters.
	if has_zip_code_filter:

		# Iterate through all food resource types.
		for i, food_resource_type in enumerate(food_resource_types):

			# Filter for each kind of food resource with a specific zip code.
			all_resources.append([])
			get_food_resources_by_location_type_and_zip_code(
				all_resources[i], # List to populate.
				food_resource_type, # Location type by which to filter.
				zip_code # Zip code by which to filter.
			)

	# Zip code is not one of the filters. 
	else: 

		# Iterate through all food resource types.
		for i, food_resource_type in enumerate(food_resource_types):

			# Filter for each kind of food resource without a specific zip code.
			all_resources.append([])
			get_food_resources_by_location_type(
				all_resources[i], # List to populate.
				food_resource_type # Location type by which to filter.
			)

	# Filter each list by other boolean criteria.
	for list_to_filter in all_resources:
		filter_food_resources(list_to_filter, has_families_and_children_filter, 
			has_seniors_filter, has_wheelchair_accessible_filter,
			has_accepts_snap_filter, has_open_now_filter)

	json = []
	for i, list in enumerate(all_resources):
		json.append([])
		for food_resource in list:
			json[i].append(food_resource.serialize_food_resource())

	return jsonify(days_of_week=days_of_week, food_resources=json)

@app.route('/')
@app.route('/map')
def map():
	food_resource_types = FoodResourceType.query \
		.order_by(FoodResourceType.name_singular).all()
	return render_template('newmaps.html', 
		food_resource_types=food_resource_types)

@app.route('/_map')
def address_food_resources():
	zip_code = request.args.get('zip_code', 0, type=int)
	food_resources = db.session.query(FoodResource) \
		.join(FoodResource.address) \
		.filter(Address.zip_code==zip_code, FoodResource.is_approved==True) \
		.order_by(FoodResource.name).all()
	return jsonify(addresses=[i.serialize_food_resource() for i in food_resources])

@app.route('/_edit', methods=['GET', 'POST'])
@login_required
def save_page():
	data = request.form.get('edit_data')
	name = request.form.get('page_name')
	if(data):
		page = HTML.query.filter_by(page = name).first()
		page.value = data
		db.session.commit()
	return 'Added' + data + 'to database.'

@app.route('/_remove_food_resource_type')
def remove_food_resource_type():
	id = request.args.get("id", type=int)
	food_resource_type = FoodResourceType.query.filter_by(id=id).first()

	# Remove the food resoures and their timeslots, address, and phone numbers 
	# from the database.
	for food_resource in food_resource_type.food_resources:
		for timeslot in food_resource.timeslots:
			db.session.delete(timeslot)
		for phone_number in food_resource.phone_numbers:
			db.session.delete(phone_number)
		db.session.delete(food_resource.address)
		db.session.delete(food_resource)

	# Remove the food resource type from the database.
	db.session.delete(food_resource_type)
	db.session.commit()
	return jsonify(success="success")


@app.route('/_search_query', methods=['GET', 'POST'])
def save_search_query():
	# Only record searches for regular users
	if(current_user.is_authenticated()):
		return
	zip_code = request.form.get('zipCode')
	if(zip_code):
		zip_requested = ZipSearch.query.filter_by(zip_code = zip_code).first()
		if(zip_requested):
			zip_requested.search_count = zip_requested.search_count + 1
		else:
			zip_requested = ZipSearch(zip_code = zip_code, search_count = 1)
			db.session.add(zip_requested)
		db.session.commit()
	return 'Recorded a search for' + zip_code

@app.route('/_remove')
@login_required
def remove():
	id = request.args.get("id", type=int)
	food_resource = FoodResource.query.filter_by(id=id).first()
	if not food_resource:
		return jsonify(message="failed")

	# Determine whether the food resource being removed is approved or pending.
	# Needed for front-end update after food resource is removed.
	is_approved = False
	if (food_resource.is_approved):
		is_approved = True

	contact = food_resource.food_resource_contact

	if contact and contact.email:
		send_email(
			recipient = contact.email, 
			subject = food_resource.name + ' has been rejected',
			html_message = 'Dear ' + contact.name + ', \
				<p>Your proposed resource <b>' + food_resource.name + 
				'</b> was rejected. Please contact an admin to find out why.\
				</p><br> Sincerely,<br>' + app.config['USER_APP_NAME'],
			text_message = 'Your proposed resource ' + food_resource.name + 
				' was rejected. Please contact an admin to find out why.'
		)

	# If the food resource has a contact and its contact has submitted no other 
	# food resources to the database, remove him/her from the database.
	if contact and len(contact.food_resource) <= 1:
		db.session.delete(contact)

	# Remove the food resoure and its timeslots, address, and phone numbers 
	# from the database.
	for timeslot in food_resource.timeslots:
			db.session.delete(timeslot)
	for phone_number in food_resource.phone_numbers:
		db.session.delete(phone_number)
	db.session.delete(food_resource.address)
	db.session.delete(food_resource)
	db.session.delete(food_resource)
	db.session.commit()
	return jsonify(is_approved=is_approved)

@app.route('/_approve')
@login_required
def approve():
	id = request.args.get("id", type=int)
	food_resource = FoodResource.query.filter_by(id=id).first()
	contact = food_resource.food_resource_contact

	if contact.email:
		send_email(
			recipient = contact.email, 
			subject = food_resource.name + ' has been approved',
			html_message = 'Dear ' + contact.name + ',\
			<p>Good news! Your proposed resource <b>' + food_resource.name + 
				'</b> was approved. Thanks so much!</p><br> Sincerely,<br>' + 
				app.config['USER_APP_NAME'],
			text_message = 'Good news! Your proposed resource ' + 
				food_resource.name + ' was approved. Thanks so much!'
		)

	if len(contact.food_resource) <= 1:
		db.session.delete(contact)
	else:
		contact.food_resource.remove(food_resource)

	food_resource.is_approved = True
	db.session.commit()
	return jsonify(message="success")

@app.route('/about')
def about():
	return render_template('about.html', 
		html_string = HTML.query.filter_by(page = 'about-page').first())

@app.route('/admin/analytics')
@login_required
def analytics():
	zip_codes_all_query = ZipSearch.query.order_by(ZipSearch.search_count.desc())
	zip_codes_all = ZipSearch.query.order_by(ZipSearch.search_count.desc()).all()
	zip_codes_limit = zip_codes_all_query.limit(10)
	return render_template('charts.html', zip_codes_all = zip_codes_all, zip_codes_limit = zip_codes_limit)

@app.route('/contact')
def contact():
	return render_template('contact.html', 
		html_string = HTML.query.filter_by(page = 'contact-page').first())

@app.route('/resources/wic')
def wic():
	return render_template('wic_info.html', 
		html_string = HTML.query.filter_by(page = 'wic-info-page').first())

@app.route('/resources/snap')
def snap():
	return render_template('snap_info.html', 
		html_string = HTML.query.filter_by(page = 'snap-info-page').first())

@app.route('/resources/summer-meals')
def summer_meals():
	return render_template('summer_meals.html', 
		html_string = HTML.query.filter_by(page = 'summer-info-page').first())

@app.route('/resources/seniors')
def seniors():
	return render_template('seniors_info.html', 
		html_string = HTML.query.filter_by(page = 'seniors-info-page').first())

@app.route('/resources/farmers')
def farmers():
	return render_template('farmers_info.html', 
		html_string = HTML.query.filter_by(page = 'farmers-info-page').first())

@app.route('/resources/neighborhood')
def neighborhood():
	return render_template('neighborhood_info.html', 
		html_string = HTML.query.filter_by(page = 'neighborhood-info-page').first())

@app.route('/resources/share')
def share():
	return render_template('share_info.html', 
		html_string = HTML.query.filter_by(page = 'share-info-page').first())

@app.route('/admin/files')
@login_required
def files():
	return render_template('file_inputoutput.html')

@app.route('/_csv_input', methods=['GET', 'POST'])
@login_required
def csv_input():
	file = request.files['file']
	path = '.csv_input.csv'
	file.save(path)

	if file:
		try:
			errors = import_file(path)
		except Exception as e:
			errors = [str(e)]

		if errors is None or len(errors) is 0:
			return jsonify(message = "success")
		else:
			response = jsonify({
				'status': 500,
				'errors': errors
			})
			response.status_code = 500
			return response

@app.route('/_csv_download')
@login_required
def download():
	outfile = open('.mydump.csv', 'wb')
	outcsv = csv.writer(outfile)

	resources = FoodResource.query.filter_by(is_approved = True).all()

	outcsv.writerow(['Table 1'])
	data = ['','Type (' + get_string_of_all_food_resource_types() + ')',
		'Name', 'Address - Line 1', 'Address - Line 2 (optional)', 'City', 
		'State', 'Zip Code', 'Phone Number (optional)', 
		'Website (optional)', 'Description (optional)', 
		'Families and children? (either \'Yes\' or leave blank)', 
		'Seniors? (either \'Yes\' or leave blank)', 
		'Wheelchair accessible? (either \'Yes\' or leave blank)', 
		'Accepts SNAP? (either \'Yes\' or leave blank)', 
		'Accepts FMNP Vouchers? (either \'Yes\' or leave blank)', 
		'Accepts Philly Food Bucks? (either \'Yes\' or leave blank)', 
		'Hours Available? (either \'Yes\' or leave blank)', 
		'Open Sunday? (either \'Yes\' or leave blank)', 
		'Open Monday? (either \'Yes\' or leave blank)', 
		'Open Tuesday? (either \'Yes\' or leave blank)',
		'Open Wednesday? (either \'Yes\' or leave blank)', 
		'Open Thursday? (either \'Yes\' or leave blank)', 
		'Open Friday? (either \'Yes\' or leave blank)', 
		'Open Saturday? (either \'Yes\' or leave blank)']
	for day_of_week in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", 
		"Friday", "Saturday"]:
		for i in range(1, 11): 
			data.append(str(day_of_week) + ' Opening Time #' + str(i) + 
				' (military time - e.g., 8:00 or 17:00)') 
			data.append(str(day_of_week) + ' Closing Time #' + str(i) + 
				' (military time - e.g., 8:00 or 17:00)')
	outcsv.writerow(data)

	for i, resource in enumerate(resources):
		# 2-dimensional array to hold all timeslots.
		# Index 0 corresponds to a list of Sunday's timeslots, 
		# index 1 corresponds to a list of Monday's timeslots, etc.
		all_timeslots = [None] * 7
		for j in range(0, 7):
			all_timeslots[j] = []
		for timeslot in resource.timeslots:
			all_timeslots[timeslot.day_of_week].append(timeslot)
		data = [
			str(i + 1), 
			resource.food_resource_type.enum, 
			resource.name, 
			resource.address.line1, 
			resource.address.line2, 
			resource.address.city, 
			resource.address.state, 
			resource.address.zip_code, 
			resource.phone_numbers[0].number, 
			resource.url, 
			resource.description, 
			'Yes' if resource.is_for_family_and_children else '', 
			'Yes' if resource.is_for_seniors else '', 
			'Yes' if resource.is_wheelchair_accessible else '', 
			'Yes' if resource.is_accepts_snap else '', 
			'Accepts FMNP Vouchers?', 
			'Accepts Philly Food Bucks?', 
			'Yes' if resource.are_hours_available else '', 
			'Yes' if len(all_timeslots[0]) != 0 else '', 
			'Yes' if len(all_timeslots[1]) != 0 else '', 
			'Yes' if len(all_timeslots[2]) != 0 else '', 
			'Yes' if len(all_timeslots[3]) != 0 else '', 
			'Yes' if len(all_timeslots[4]) != 0 else '', 
			'Yes' if len(all_timeslots[5]) != 0 else '', 
			'Yes' if len(all_timeslots[6]) != 0 else '']
		for day_of_week_timeslots in all_timeslots: # 7 days of the week.
			for j in range (0, 10): # [0, 10) - 10 possible timeslots per day.
				if j >= len(day_of_week_timeslots) or \
					day_of_week_timeslots[j] is None:
					data.append('') # Start time is empty.
					data.append('') # End time is empty.
				else:
					data.append(day_of_week_timeslots[j] \
						.start_time.strftime('%H:%M'))
					data.append(day_of_week_timeslots[j] \
						.end_time.strftime('%H:%M'))
		outcsv.writerow(data)

	def generate():
		with open('.mydump.csv', 'rb') as f:
			for line in f:
				yield line
	
	response = Response(generate(), mimetype='text/csv')
	filename = 'resources_generated_at_' + str(datetime.now()) + '.csv'
	response.headers["Content-Disposition"] = "attachment; filename="+filename
	return response

@app.route('/admin/food-resource-types')
@login_required
def view_food_resource_types():
	food_resource_types = FoodResourceType.query \
		.order_by(FoodResourceType.name_singular).all()
	return render_template('food_resource_types.html', 
		food_resource_types=food_resource_types)

@app.route('/admin/new-food-resource-type', methods=['GET', 'POST'])
@app.route('/admin/edit-food-resource-type/<id>', methods=['GET', 'POST'])
@login_required
def new_food_resource_type(id=None):
	form = AddNewFoodResourceTypeForm(request.form)
	form.id.data = None

	# Show unused colors.
	choices = []
	unused_pins = ColoredPin.query.filter_by(food_resource=None) \
		.order_by(ColoredPin.color_name).all()
	for unused_pin in unused_pins:
		choices.append((unused_pin.color_name, unused_pin.color_name))
	if id is not None:
		food_resource_type = FoodResourceType.query.filter_by(id=id).first()
		if food_resource_type:
			choices.insert(0, (food_resource_type.colored_pin.color_name, 
				food_resource_type.colored_pin.color_name))
	form.color.choices = choices

	# Create a new food resource. 
	if id is None:
		title = "Add New Food Resource Type"
	# Edit an existing food resource.
	else:
		title = "Edit Food Resource Type"
		food_resource_type = FoodResourceType.query.filter_by(id=id).first()
		if food_resource_type is not None:
			form.id.data = food_resource_type.id

	# GET request.
	if request.method == 'GET' and id is not None:

		# Retrieve existing food resource type. 
		food_resource_type = FoodResourceType.query.filter_by(id=id).first()
		if food_resource_type is None:
			return render_template('404.html')
		print "merp"

		# Pre-populate form fields with data from database.
		form.name_singular.data = food_resource_type.name_singular
		form.name_plural.data = food_resource_type.name_plural

	if request.method == 'POST' and form.validate():
		colored_pin = ColoredPin.query.filter_by(color_name=form.color.data) \
			.first()

		# Edit an existing food resource type.
		if id is not None:
			food_resource_type = FoodResourceType.query.filter_by(id=id).first()
			if food_resource_type:
				food_resource_type.name_singular = form.name_singular.data
				food_resource_type.name_plural = form.name_plural.data
				food_resource_type.colored_pin = colored_pin
				food_resource_type.recreate_fields()
		
		# Create a new food resource type.
		else:
			food_resource_type = FoodResourceType(
				name_singular = form.name_singular.data, 
				name_plural = form.name_plural.data, 
				colored_pin = colored_pin
			)

		# Save and commit database changes.
		db.session.add(food_resource_type)
		db.session.commit()

		return redirect(url_for('view_food_resource_types'))

	return render_template('add_resource_type.html', form=form, title=title)
