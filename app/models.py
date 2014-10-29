from app import db
from flask_user import UserMixin

class Address(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	line1 = db.Column(db.String(100))
	line2 = db.Column(db.String(100))
	city = db.Column(db.String(35))
	state = db.Column(db.String(2))
	zip_code = db.Column(db.String(5))
	resource_id = db.Column(db.Integer, db.ForeignKey('food_resource.id'))

class TimeSlot(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	day_of_week = db.Column(db.Integer)
	start_time = db.Column(db.Time)
	end_time = db.Column(db.Time)
	resource_id = db.Column(db.Integer, db.ForeignKey('food_resource.id'))

class FoodResource(db.Model):
	food_resource_type_enums = ('FARMERS_MARKET','MEALS_ON_WHEELS','FOOD_CUPBOARD','SHARE','SOUP_KITCHEN','WIC_OFFICE')
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50))
	address = db.relationship('Address', backref='food_resource', lazy='select', uselist=False)
	phone = db.Column(db.String(35))
	timeslots = db.relationship('TimeSlot', backref='food_resource', lazy='select', uselist=True)
	description = db.Column(db.String(500))
	location_type = db.Column(db.Enum(*food_resource_type_enums))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)

	# User Authentication information
	username = db.Column(db.String(50), nullable=False, unique=True)
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

class Role(db.Model):
	role_type_enums = ('User','Admin')
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.Enum(*role_type_enums))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class UserRoles(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
	role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))
