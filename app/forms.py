from app import app
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, validators, PasswordField, StringField, BooleanField, SubmitField, HiddenField
from wtforms.validators import InputRequired, Length, URL, Email
from flask_user.forms import RegisterForm, unique_email_validator
from flask_user.translations import lazy_gettext as _

# Information about a new food resource. 
class AddNewFoodResourceForm(Form):
    website = TextField(
        label = 'Food Resource Website', 
        validators = [
            URL(True, "Invalid website URL.")
        ])
    name = TextField(
        label = 'Food Resource Name',
        validators = [
            InputRequired("Please provide the food resource's name.")
        ])
    address_line1 = TextField(
        label = 'Address Line #1', 
        validators = [
            InputRequired("Please provide the food resource's address."),
            Length(1, 100) # same max length as in Address model.
        ])
    address_line2 = TextField(
        label = 'Address Line #1', 
        validators = [
            Length(1, 100) # Same max length as in Address model.
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
    additional_information = TextAreaField(
        label = 'Any additional information?', 
        validators = [
            Length(1, 300)
        ])

# Information about the person submitting the food resource for evaluation. 
# Subclassed from 'AddNewFoodResourceForm'
class RequestNewFoodResourceForm(AddNewFoodResourceForm):
    first_name = TextField(
        label = 'Your First Name', 
        validators = [
            InputRequired("Please provide your first name."),
            Length(0, 35)
        ])
    last_name = TextField(
        label = 'Your Last Name', 
        validators = [
            InputRequired("Please provide your last name."),
            Length(0, 35)
        ])
    email_address = TextField(
        label = 'Your Email Address', 
        validators = [
            InputRequired("Please provide an email address at which we can contact you."), 
            Email("Invalid email address."),
            Length(1, 35)
        ])
    phone_number = TextField(
        label = 'Your Phone Number', 
        validators = [
            InputRequired("Please provide a phone number at which we can contact you.")
        ])   

class InviteForm(RegisterForm):
    password_validator_added = False

    next = HiddenField()        # for login_or_register.html
    reg_next = HiddenField()    # for register.html

    email = StringField(_('Email'), validators=[
        validators.Required(_('Email is required')),
        validators.Email(_('Invalid Email')),
        unique_email_validator])

    first_name = StringField(_('First Name'), validators=[
        validators.Required(_('First Name is required'))
        ])

    last_name = StringField(_('Last Name'), validators=[
        validators.Required(_('First Name is required'))
        ]
        
    submit = SubmitField(_('Invite'))