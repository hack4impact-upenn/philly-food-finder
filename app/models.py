from app import app, db
from flask_user import UserMixin
import datetime
import utils
from pygeocoder import Geocoder
import time

class ColoredPin(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	color_name = db.Column(db.String(35), unique=True)
	hex_color = db.Column(db.String(6), unique=True)
	pin_image_name = db.Column(db.String(35), unique=True)
	food_resource = db.relationship(
		'FoodResourceType', # One-to-many relationship (one FoodResourceType with many FoodResource).
		backref='colored_pin', # Declare a new property of the FoodResource class.
		lazy='select', uselist=False)

	def serialize_colored_pin(self):
		return {
			'hex_color': self.hex_color, 
			'pin_image_name': self.pin_image_name
		}

class FoodResourceType(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	enum = db.Column(db.String(200), unique=True) # Should be singular
	name_singular = db.Column(db.String(200), unique=True)
	name_plural = db.Column(db.String(200), unique=True)
	hyphenated_id_singular = db.Column(db.String(200), unique=True)
	hyphenated_id_plural = db.Column(db.String(200), unique=True)
	underscored_id_singular = db.Column(db.String(200), unique=True)
	underscored_id_plural = db.Column(db.String(200), unique=True)
	colored_pin_id = db.Column(db.Integer, db.ForeignKey('colored_pin.id'))
	food_resources = db.relationship(
		'FoodResource', # One-to-many relationship (one FoodResourceType with many FoodResource).
		backref='food_resource_type', # Declare a new property of the FoodResource class.
		lazy='select', 
		uselist=True,
		order_by='FoodResource.name')

	def __init__(self, name_singular, name_plural, colored_pin):
		self.enum = utils.get_enum(name_singular)
		self.name_singular = name_singular
		self.name_plural = name_plural
		self.hyphenated_id_singular = utils \
			.get_hyphenated_string(name_singular)
		self.hyphenated_id_plural = utils \
			.get_hyphenated_string(name_plural)
		self.underscored_id_singular = utils \
			.get_underscored_string(name_singular)
		self.underscored_id_plural = utils \
			.get_underscored_string(name_plural)
		self.colored_pin = colored_pin

	def recreate_fields(self):
		self.enum = utils.get_enum(self.name_singular)
		self.hyphenated_id_singular = utils \
			.get_hyphenated_string(self.name_singular) 
		self.hyphenated_id_plural = utils \
			.get_hyphenated_string(self.name_plural)
		self.underscored_id_singular = utils \
			.get_underscored_string(self.name_singular)
		self.underscored_id_plural = utils \
			.get_underscored_string(self.name_plural)

	def serialize_food_resource_type(self):
		return {
			'id': self.id, 
			'enum': self.enum, 
			'name_singular': self.name_singular,
			'name_plural': self.name_plural, 
			'hyphenated_id_singular': self.hyphenated_id_singular,
			'hyphenated_id_plural': self.hyphenated_id_plural, 
			'underscored_id_singular': self.underscored_id_singular,
			'underscored_id_plural': self.underscored_id_plural,
			'colored_pin': self.colored_pin.serialize_colored_pin(),
			'food_resources': [i.serialize_food_resource(include_food_resource_type=False) for i in self.food_resources]
		}

class Address(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	line1 = db.Column(db.String(100))
	line2 = db.Column(db.String(100))
	city = db.Column(db.String(35))
	state = db.Column(db.String(2))
	zip_code = db.Column(db.String(5))
	latitude = db.Column(db.String(50))
	longitude = db.Column(db.String(50))
	valid_address = db.Column(db.Boolean, default=False)
	food_resource_id = db.Column(db.Integer, db.ForeignKey('food_resource.id'))

	def createLatAndLong(self):
		address_string = ""
		addressEvaluated = False
		while not addressEvaluated:
			try:
				address_string = str(self.line1) + ", "
				address_string += str(self.city) + ", " + str(self.state) + " " + str(self.zip_code)
				results = Geocoder.geocode(address_string)
				self.latitude = str(results[0].coordinates[0])
				self.longitude = str(results[0].coordinates[1])
				self.valid_address = True
				addressEvaluated = True
			except Exception as e:
				print "Invalid address"
				time.sleep(2)

	def serialize_address(self):
		return {
			'id': self.id,
			'line1': self.line1,
			'line2': self.line2,
			'city': self.city,
			'state': self.state,
			'zip_code': self.zip_code,
			'latitude': self.latitude, 
			'longitude': self.longitude,
			'food_resource_id': self.food_resource_id
		}

class TimeSlot(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	day_of_week = db.Column(db.Integer)
	start_time = db.Column(db.Time)
	end_time = db.Column(db.Time)
	food_resource_id = db.Column(db.Integer, db.ForeignKey('food_resource.id'))

	def serialize_timeslot(self, is_military_time=True):
		data = {
			'id': self.id,
			'day_of_week': self.day_of_week,
		}
		if is_military_time:
			data["start_time"] = self.start_time.isoformat()
			data["end_time"] = self.end_time.isoformat()
		else:
			data["start_time"] = self.start_time.strftime('%I:%M %p')
			data["end_time"] = self.end_time.strftime('%I:%M %p')
		return data

class PhoneNumber(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	number = db.Column(db.String(35))
	resource_id = db.Column(db.Integer, db.ForeignKey('food_resource.id'))

	def serialize_phone_numbers(self):
		return {
			'id': self.id,
			'number': self.number,
			'reource_id': self.resource_id
		}

class FoodResourceContact(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150))
	email = db.Column(db.String(255))
	phone_number = db.Column(db.String(35))
	food_resource = db.relationship('FoodResource', 
		backref='food_resource_contact', lazy='select', uselist=True)

class FoodResourceBoolean(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	value = db.Column(db.Boolean, default=False)
	description_question = db.Column(db.String(300))
	description_statement = db.Column(db.String(300))
	hyphenated_id = db.Column(db.String(300))
	food_resource_id = db.Column(db.Integer, db.ForeignKey('food_resource.id'))

	def __init__(self, description_question, description_statement):
		self.description_question = description_question
		self.description_statement = description_statement
		self.hyphenated_id = utils.get_hyphenated_string(description_question)

	def serialize_food_resource_boolean(self):
		return {
			'id': self.id,
			'value': self.value,
			'description_question': self.description_question,
			'description_statement': self.description_statement,
			'hyphenated_id': self.hyphenated_id
		}

	def serialize_food_resource_boolean_truncated(self):
		return {
			'value': self.valud,
			'hyphenated_id': self.hyphenated_id
		}

class FoodResource(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	phone_numbers = db.relationship('PhoneNumber', backref='food_resource', 
		lazy='select', uselist=True)
	url = db.Column(db.Text)
	description = db.Column(db.Text)
	food_resource_type_id = db.Column(db.Integer, 
		db.ForeignKey('food_resource_type.id'))
	address = db.relationship('Address', backref='food_resource', 
		lazy='select', uselist=False)

	# Hours of operation.
	are_hours_available = db.Column(db.Boolean, default=False)
	timeslots = db.relationship(
		'TimeSlot', # One-to-many relationship (one Address with many TimeSlots).
		backref='food_resource', # Declare a new property of the TimeSlot class.
		lazy='select', uselist=True, 
		order_by='TimeSlot.start_time')

	# Boolean fields.
	booleans = db.relationship(
		'FoodResourceBoolean', # One-to-many relationship (one FoodResource with many FoodResourceBooleans).
		backref='food_resource', # Declare a new property of the FoodResourceBoolean class.
		lazy='select', uselist=True)

	# Fields for when non-admins submit resources.
	is_approved = db.Column(db.Boolean(), default=True)
	food_resource_contact_id = db.Column(db.Integer, 
		db.ForeignKey('food_resource_contact.id'))
	notes = db.Column(db.String(500))

	# This is a workaround for a bug where the resource type
	# would not display for pending resources on the admin manage
	# page. This field is only used when a pending resource is 
	# created and displayed on the admin manage page. Once the 
	# resource is approved, this field is never used.
	resource_type_singular = db.Column(db.String(200))

	def __init__(self, *args, **kwargs):
		super(db.Model, self).__init__(*args, **kwargs)
		self.booleans = utils.get_food_resource_booleans()

	def serialize_name_only(self):
		return {
			'name': self.name, 
			'id': self.id
		}

	def serialize_food_resource(self, include_food_resource_type=True):
		dict = {
			'id': self.id, 
			'name': self.name, 
			'phone_number': self.phone_numbers[0].serialize_phone_numbers(),
			'url': self.url, 
			'description': self.description,
			'address': self.address.serialize_address(),
			'are_hours_available': self.are_hours_available, 
			'timeslots': [i.serialize_timeslot(False) for i in self.timeslots], 
			'booleans': [i.serialize_food_resource_boolean() for i in self.booleans]
		}
		if include_food_resource_type:
			dict["food_resource_type"] = self.food_resource_type.serialize_food_resource_type()
		return dict

	def serialize_map_list(self):
		return {
			'id': self.id,
			'name': self.name,
			'phone_number': self.phone_numbers[0].serialize_phone_numbers(),
			'description': self.description,
			'location_type': self.location_type,
			'address': self.address.serialize_address()
		}

class Role(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(100))
	role_type_enums = ('User','Admin')
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.Enum(*role_type_enums))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class UserRoles(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	user_id = db.Column(db.Integer(), db.ForeignKey('user.id', 
		ondelete='CASCADE'))
	role_id = db.Column(db.Integer(), db.ForeignKey('role.id', 
		ondelete='CASCADE'))
	
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)

	# User Authentication information
	password = db.Column(db.String(255), nullable=False, default='')
	reset_password_token = db.Column(db.String(100), nullable=False, default='')

	# User Email information
	email = db.Column(db.String(255), nullable=False, unique=True)
	confirmed_at = db.Column(db.DateTime())

	# User information
	is_enabled = db.Column(db.Boolean(), nullable=False, default=False)
	first_name = db.Column(db.String(50), nullable=False, default='')
	last_name = db.Column(db.String(50), nullable=False, default='')

	roles = db.relationship('Role', secondary='user_roles',
			backref=db.backref('users', lazy='dynamic'))

	def is_active(self):
		return self.is_enabled

	def verify_password(self, attept):
		return app.user_manager.verify_password(attept, self.password)

	# This function is only for the tests in tests.py
	def confirm_and_enable_debug(self):
		self.confirmed_at = datetime.datetime.now()
		self.is_enabled = True

	def __init__(self, email, password, is_enabled, first_name = '', last_name = '', roles = [Role(name = 'Admin')]):
		self.email = email
		self.password = app.user_manager.hash_password(password = password)
		self.first_name = first_name
		self.last_name = last_name
		self.roles = roles
		self.is_enabled = is_enabled

class HTML(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	page = db.Column(db.String(100), unique=True)
	value = db.Column(db.Text)

class ZipSearch(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	zip_code = db.Column(db.String(5))
	search_count = db.Column(db.Integer)
	date = db.Column(db.Date)

	def serialize_zip_search(self):
		return {
			'id': self.id,
			'zip_code': self.zip_code,
			'search_count': self.search_count,
			'date': str(self.date)
		}