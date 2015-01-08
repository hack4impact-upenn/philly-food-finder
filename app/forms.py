from app import app
from flask import current_app
from flask.ext.wtf import Form
from flask.ext.wtf.recaptcha import RecaptchaField
from wtforms.validators import InputRequired, Length, URL, Email, Optional, \
	ValidationError
from wtforms import TextField, TextAreaField, validators, PasswordField, \
	StringField, BooleanField, SubmitField, HiddenField, SelectField, \
	SelectField, FieldList, FormField, Label
from flask_user.forms import RegisterForm, unique_email_validator
from flask_user.translations import lazy_gettext as _
from app.utils import *

class BooleanForm(Form):
	value = SelectField(
		label = 'Default',
		choices = [('no', 'No'), ('yes', 'Yes')], 
		validators = [
			InputRequired("Please choose an option.")
		]
	)

	def set_label(self, label):
		self.value.label = Label(self.value.id, label)

class TimeSlotForm(Form):
	starts_at = SelectField(u'Opens at') 
	ends_at = SelectField(u'Closes at') 

class IsOpenForm(Form):
	is_open = SelectField(u'Sunday', 
		choices=[('closed', 'Closed'), ('open', 'Open')])

	def set_label(self, label):
		self.is_open.label = Label(self.is_open.id, label)

class MultiTimeSlotForm(Form):
	timeslots = FieldList(FormField(TimeSlotForm), min_entries=10, 
		max_entries=10)
	num_timeslots = TextField(
		label = 'Number of timeslots (1-10)',
		validators = [
			InputRequired("Please indicate a number of timeslots between 1 and \
				10.")
		], 
		default = 1
	)

	def validate_num_timeslots(form, field):
		regex = re.compile('^-?[0-9]+$')
		if len(str(field.data)) == 0 or not regex.match(str(field.data)) or \
			int(field.data) < 1 or int(field.data) > 10:
			raise ValidationError('Value must be an integer between 1 and 10.')

# Information about a new food resource. 
class AddNewFoodResourceForm(Form):
	food_resource_id = TextField() # Invisible to user
	location_type = SelectField(
		label = 'Food Resource Type', 
		validators = [
			InputRequired("Please indicate the food resource's type.")
		]
	)
	website = TextField(
		label = 'Food Resource Website', 
		validators = [
			#Optional(),
			#URL(True, "Invalid website URL.")
		], 
		description = "The website for the food resource or for the food \
			resource's organization."
	)
	name = TextField(
		label = 'Food Resource Name',
		validators = [
			InputRequired("Please provide the food resource's name.")
		]
	)
	phone_number = TextField(
		label = 'Phone Number')
	address_line1 = TextField(
		label = 'Address Line 1', 
		validators = [
			InputRequired("Please provide the food resource's address."),
			Length(1, 100) # same max length as in Address model.
		]
	)
	address_line2 = TextField(
		label = 'Address Line 2', 
		validators = [
			Length(0, 100) # Same max length as in Address model.
		]
	)
	address_city = TextField(
		label = 'City', 
		validators = [
			InputRequired("Please provide the food resource's city."),
			Length(1, 35) # Same max length as in Address model.
		]
	)
	address_state = TextField(
		label = 'State', 
		validators = [
			InputRequired("Please provide the food resource's state."),
			Length(1, 2) # Same max length as in Address model.
		]
	)
	address_zip_code = TextField(
		label = 'Zip Code', 
		validators = [
			InputRequired("Please provide the food resource's zip code."),
			Length(1, 5) # Same max length as in Address model.
		]
	)
	are_hours_available = SelectField(
		label = 'Are hours of operation available?', 
		choices = [('no', 'No'), ('yes', 'Yes')], 
		validators = [
			InputRequired("Please indicate whether hours of operation are \
				available or not.")
		]
	)

    # For each day of the week, is the food resource open or closed?
	is_open = FieldList(FormField(IsOpenForm), min_entries=7, max_entries=7)

    # If a food resource is open on a given day, input its hours of operation. 
	daily_timeslots = FieldList(FormField(MultiTimeSlotForm), 
		min_entries=7, max_entries=7)

	additional_information = TextAreaField(
		label = 'Any additional information?', 
		validators = [
			Length(0, 300)
		], 
		description = 'Any additional information that visitors to this food \
			resource might find useful. For example, "Open every second \
			Saturday of the month," "Referral required," or "Call for hours."'
	)
	booleans = FieldList(FormField(BooleanForm), min_entries=0)

	def generate_booleans(self):
		food_resource_booleans = get_food_resource_booleans()
		for i, food_resource_boolean in enumerate(food_resource_booleans):
			self.booleans.append_entry()
			self.booleans[i].set_label(food_resource_boolean.description_statement)

	def get_booleans(self):
		food_resource_booleans = get_food_resource_booleans()
		dict = {}
		for i, boolean in enumerate(self.booleans):
			key = food_resource_booleans[i].hyphenated_id
			value = False
			if boolean.value.data == 'yes':
				value = True
			dict[key] = value
		return dict

# All information from AddNewFoodResourceForm plus information 
# about the person submitting the food resource for evaluation. 
# Subclassed from 'AddNewFoodResourceForm'
class NonAdminAddNewFoodResourceForm(AddNewFoodResourceForm):
	your_name = TextField(
		label = 'Your Name', 
		validators = [
			InputRequired("Please provide your name."),
			Length(1, 150)
		],
		description = "Please provide your first AND last name. Your name will \
			not be displayed publicly on Philly Food Finder."
	)
	your_email_address = TextField(
		label = 'Your Email Address', 
		validators = [
			Length(0, 255)
		],
		description = "Please provide an email address at which we can contact \
			you if we have questions about your submitted food resource. Your \
			email address will not be used for any other purpose. Your email \
			address will not be displayed publicly on Philly Food Finder."
	)
	your_phone_number = TextField(
		label = 'Your Phone Number', 
		validators = [
			InputRequired("Please provide a phone number at which we can \
				contact you.")
		],
		description = "Please provide a phone number at which we can contact \
			you if we have questions about your submitted food resource. Your \
			phone number will not be displayed publicly on Philly Food Finder."
	)
	notes = TextAreaField(
		label = 'Notes', 
		validators = [
			Length(0, 500)
		], 
		description = 'Is there any additional information that you think we \
			should know as we review your food resource? For example, is your \
			site already in the database but its information is incorrect?'
	)   

	recaptcha = RecaptchaField() 

	def validate_your_email_address(form, field):
		regex = re.compile('^.+@[^.].*\.[a-z]{2,10}$')
		if len(str(field.data)) > 0 and not regex.match(str(field.data)):
			raise ValidationError('Invalid email address.')

# Form to invite new admin.
# Subclassed from 'flask_user.forms.RegisterForm'
class InviteForm(RegisterForm):
	first_name = StringField(_('First Name'), validators=[
		validators.Required(_('First Name is required'))
		]
	)

	last_name = StringField(_('Last Name'), validators=[
		validators.Required(_('First Name is required'))
		]
	)

	submit = SubmitField(_('Invite'))
    
    # Override RegisterForm's validate function so that a temporary password 
    # can be set 
	def validate(self):
        # remove certain form fields depending on user manager config
		user_manager =  current_app.user_manager
		delattr(self, 'password')
		delattr(self, 'retype_password')

		if not user_manager.enable_username:
			delattr(self, 'username')
		if not user_manager.enable_email:
			delattr(self, 'email')

        # Add custom username validator if needed
		if user_manager.enable_username:
			has_been_added = False
			for v in self.username.validators:
				if v==user_manager.username_validator:
					has_been_added = True
			if not has_been_added:
				self.username.validators.append(user_manager.username_validator)
        
        # Validate field-validators
		if not super(RegisterForm, self).validate():
			return False

		return True

class AddNewFoodResourceTypeForm(Form):
	id = TextField() # Hidden from user
	name_singular = TextField(
		label = 'Food Resource Type Name - Singular', 
		validators = [
			InputRequired("Please provide the singular version of the food \
				resource type's name."),
			Length(1, 200)
		], 
		description = 'The singular version of the name of the food resource \
			type. This name will be public-facing. Examples include "Farmers\' \
			Market," "Senior Meals," and "SHARE Host Site."'
	)
	name_plural = TextField(
		label = 'Food Resource Type Name - Plural', 
		validators = [
			InputRequired("Please provide the plural version of the food \
				resource type's name."),
			Length(1, 200)
		], 
		description = 'The plural version of the name of the food resource \
			type. This name will be public-facing. Examples include "Farmers\' \
			Markets," "Senior Meals," and "SHARE Host Sites."'
	)
	color = SelectField(u'Food Resource Color', 
		description = 'The color that will be associated with this food \
			resource type throughout the website. Each food resource type must \
			have a unique color. If there are no colors from which to choose, \
			then there are no more available colors. Please contact the \
			Hack4Impact team if you encounter this issue.',
		validators = [
			InputRequired("Please choose a color.")
		]
	)

	def validate_name_singular(form, field):
		name = field.data.lower()
		underscored_id_singular = get_underscored_string(name)
		existing_type = FoodResourceType.query \
			.filter_by(underscored_id_singular=underscored_id_singular).first()
		if (existing_type is not None) \
			and (form.id.data is not existing_type.id):
			raise ValidationError('Another food resource type already has this \
				singular name. Singular names must be unique.')

	def validate_name_plural(form, field):
		name = field.data.lower()
		underscored_name = get_underscored_string(name)
		existing_type = FoodResourceType.query \
			.filter_by(underscored_id_plural=underscored_name).first()
		if existing_type is not None and form.id.data is not existing_type.id:
			raise ValidationError('Another food resource type already has this \
				plural name. Plural names must be unique.')

