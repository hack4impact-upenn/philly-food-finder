from app import app, db
from flask_user import UserMixin
from datetime import datetime
import utils

class ColoredPin(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	hex_color = db.Column(db.String(6), unique=True)
	pin_image_name = db.Column(db.String(35), unique=True)
	food_resources = db.relationship(
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
	enum = db.Column(db.String(35), unique=True) # Should be singular
	name_singular = db.Column(db.String(35), unique=True)
	name_plural = db.Column(db.String(35), unique=True)
	hyphenated_id_singular = db.Column(db.String(35), unique=True)
	hyphenated_id_plural = db.Column(db.String(35), unique=True)
	underscored_id_singular = db.Column(db.String(35), unique=True)
	underscored_id_plural = db.Column(db.String(35), unique=True)
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
		self.hyphenated_id_singular = utils.get_hyphenated_string(name_singular)
		self.hyphenated_id_plural = utils.get_hyphenated_string(name_plural)
		self.underscored_id_singular = utils.get_underscored_string(name_singular)
		self.underscored_id_plural = utils.get_underscored_string(name_plural)
		self.colored_pin = colored_pin

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
	food_resource_id = db.Column(db.Integer, db.ForeignKey('food_resource.id'))

	def serialize_address(self):
		return {
			'id': self.id,
			'line1': self.line1,
			'line2': self.line2,
			'city': self.city,
			'state': self.state,
			'zip_code': self.zip_code,
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

# Represents a start and end month for a resource. 
# For example OpenMonthPair(3,5) means the resource is open from March to May.
class OpenMonthPair(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	start_month = db.Column(db.Integer)
	end_month = db.Column(db.Integer)
	resource_id = db.Column(db.Integer, db.ForeignKey('food_resource.id'))

	def serialize_open_month_pair(self):
		return {
			'id': self.id, 
			'start_month': self.start_month, 
			'end_month': self.end_month, 
			'resource_id': self.resource_id
		}

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

class FoodResource(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50))
	phone_numbers = db.relationship('PhoneNumber', backref='food_resource', 
		lazy='select', uselist=True)
	url = db.Column(db.Text)
	open_month_pairs = db.relationship('OpenMonthPair', backref='food_resource', 
		lazy='select', uselist=True)
	exceptions = db.Column(db.Text)
	description = db.Column(db.Text)
	location_type = db.Column(db.String(100))
	food_resource_type_id = db.Column(db.Integer, 
		db.ForeignKey('food_resource_type.id'))
	address = db.relationship('Address', backref='food_resource', 
		lazy='select', uselist=False)

	# Hours of operation.
	are_hours_available = db.Column(db.Boolean, default=False)
	timeslots = db.relationship(
		'TimeSlot', # One-to-many relationship (one Address with many TimeSlots).
		backref='food_resource', # Declare a new property of the TimeSlot class.
		lazy='select', uselist=True)

	# Boolean fields
	is_for_family_and_children = db.Column(db.Boolean, default=False)
	is_for_seniors = db.Column(db.Boolean, default=False)
	is_wheelchair_accessible = db.Column(db.Boolean, default=False)
	is_accepts_snap = db.Column(db.Boolean, default=False)

	# Fields for when non-admins submit resources
	is_approved = db.Column(db.Boolean(), default=True)
	food_resource_contact_id = db.Column(db.Integer, 
		db.ForeignKey('food_resource_contact.id'))

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
			'open_month_pairs': 
				[i.serialize_open_month_pair() for i in self.open_month_pairs],
			'exceptions': self.exceptions, 
			'description': self.description,
			'location_type': self.location_type,
			'address': self.address.serialize_address(),
			'are_hours_available': self.are_hours_available, 
			'timeslots': [i.serialize_timeslot(False) for i in self.timeslots], 
			'is_for_family_and_children': self.is_for_family_and_children, 
			'is_for_seniors': self.is_for_seniors, 
			'is_wheelchair_accessible': self.is_wheelchair_accessible, 
			'is_accepts_snap': self.is_accepts_snap 
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
		self.confirmed_at = datetime.now()
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
