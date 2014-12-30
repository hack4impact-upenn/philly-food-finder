from app import app
from flask import current_app
from flask.ext.wtf import Form
from wtforms.validators import InputRequired, Length, URL, Email, Optional, \
    ValidationError
from wtforms import TextField, TextAreaField, validators, PasswordField, \
    StringField, BooleanField, SubmitField, HiddenField, SelectField, \
    SelectField, FieldList, FormField
from flask_user.forms import RegisterForm, unique_email_validator
from flask_user.translations import lazy_gettext as _
from app.utils import *

class TimeSlotForm(Form):
    starts_at = SelectField(u'Opens at') 
    ends_at = SelectField(u'Closes at') 

    #def get_start_time(self):
        #return get_time_from_string

    #def get_end_time(self):

class IsOpenForm(Form):
    is_open = SelectField(u'Sunday', 
        choices=[('closed', 'Closed'), ('open', 'Open')])

    def set_label(self, label):
        is_open.label = label

class MultiTimeSlotForm(Form):
    timeslots = FieldList(FormField(TimeSlotForm), min_entries=1)

# Information about a new food resource. 
class AddNewFoodResourceForm(Form):
    food_resource_id = TextField() # Invisible to user
    location_type = SelectField(u'Food Resource Type', choices=[
        ('FARMERS_MARKET', "Farmers' Market"), 
        ('FOOD_CUPBOARD', 'Food Cupboard'),
        ('SENIOR_MEAL', 'Senior Meals'),
        ('SHARE', 'SHARE Host Site'), 
        ('SOUP_KITCHEN', 'Soup Kitchen'),
        ('WIC_OFFICE', 'WIC Office')])
    website = TextField(
        label = 'Food Resource Website', 
        validators = [
            #Optional(),
            #URL(True, "Invalid website URL.")
        ])
    name = TextField(
        label = 'Food Resource Name',
        validators = [
            InputRequired("Please provide the food resource's name.")
        ])
    phone_number = TextField(
        label = 'Phone Number')
    address_line1 = TextField(
        label = 'Address Line 1', 
        validators = [
            InputRequired("Please provide the food resource's address."),
            Length(1, 100) # same max length as in Address model.
        ])
    address_line2 = TextField(
        label = 'Address Line 2', 
        validators = [
            Length(0, 100) # Same max length as in Address model.
        ])
    address_city = TextField(
        label = 'City', 
        validators = [
            InputRequired("Please provide the food resource's city."),
            Length(1, 35) # Same max length as in Address model.
        ])
    address_state = TextField(
        label = 'State', 
        validators = [
            InputRequired("Please provide the food resource's state."),
            Length(1, 2) # Same max length as in Address model.
        ])
    address_zip_code = TextField(
        label = 'Zip Code', 
        validators = [
            InputRequired("Please provide the food resource's zip code."),
            Length(1, 5) # Same max length as in Address model.
        ])
    are_hours_available = SelectField(u'Are hours of operation available?', 
        choices=[('no', 'No'), ('yes', 'Yes')])

    # For each day of the week, is the food resource open or closed?
    is_open = FieldList(FormField(IsOpenForm), min_entries=7, max_entries=7)

    # If a food resource is open on a given day, input its hours of operation. 
    daily_timeslots = FieldList(FormField(MultiTimeSlotForm), 
        min_entries=7, max_entries=7)

    additional_information = TextAreaField(
        label = 'Any additional information?', 
        validators = [
            Length(0, 300)
        ])
    is_for_family_and_children = BooleanField('Check off if this food resource \
        is aimed towards family and children.')
    is_for_seniors = BooleanField('Check off if this food resource is aimed \
        towards seniors.')
    is_wheelchair_accessible = BooleanField('Check off if this food resource \
        is wheelchair accessible.')
    is_accepts_snap = BooleanField('Check off if this food resource accepts \
        SNAP.')

# All information from AddNewFoodResourceForm plus information 
# about the person submitting the food resource for evaluation. 
# Subclassed from 'AddNewFoodResourceForm'
class NonAdminAddNewFoodResourceForm(AddNewFoodResourceForm):
    your_name = TextField(
        label = 'Your Name', 
        validators = [
            InputRequired("Please provide your name."),
            Length(1, 150)
        ])
    your_email_address = TextField(
        label = 'Your Email Address', 
        validators = [
            InputRequired("Please provide an email address at which we can \
                contact you."), 
            Email("Invalid email address."),
            Length(1, 255)
        ])
    your_phone_number = TextField(
        label = 'Your Phone Number', 
        validators = [
            InputRequired("Please provide a phone number at which we can \
                contact you.")
        ])   

# Form to invite new admin.
# Subclassed from 'flask_user.forms.RegisterForm'
class InviteForm(RegisterForm):
    first_name = StringField(_('First Name'), validators=[
        validators.Required(_('First Name is required'))
        ])

    last_name = StringField(_('Last Name'), validators=[
        validators.Required(_('First Name is required'))
        ])

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
            Length(1, 35)
        ]
    )
    name_plural = TextField(
        label = 'Food Resource Type Name - Plural', 
        validators = [
            InputRequired("Please provide the plural version of the food \
                resource type's name."),
            Length(1, 35)
        ]
    )
    hex_color = TextField(
        label = 'Hexadecimal Color Code', 
        validators = [
            InputRequired("Please provide a 6-digit hexadecimal color code.")
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

    def validate_hex_color(form, field):
        hex_color = field.data.lower()
        a = re.compile("^[a-fA-F0-9]{6}$")
        if not a.match(hex_color):
            raise ValidationError('Hex color code must be a combination of six \
                digits 0-9 and A-F')
        existing_type = FoodResourceType.query.filter_by(hex_color=hex_color) \
            .first()
        if existing_type is not None and form.id.data is not existing_type.id:
            raise ValidationError('Another food resource type already has this \
                hex color code. Hex color codes names must be unique.')

