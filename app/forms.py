from app import app
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, validators, PasswordField, StringField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, URL, Email

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

def password_validator(form, field):
    # Convert string to list of characters
    password = list(field.data)
    password_length = len(password)

    # Password must have one lowercase letter, one uppercase letter and one digit
    is_valid = password_length>=6
    if not is_valid:
        raise ValidationError('Password must have at least 6 characters')

def unique_email_validator(form, field):
    """ Email must be unique"""
    user_manager =  app.user_manager
    if not user_manager.email_is_available(field.data):
        raise ValidationError('This Email is already in use. Please try another one.')

class LoginForm(Form):
    email = StringField(('Email'), validators=[
        validators.Required('Email is required'),
        validators.Email('Invalid Email')
    ])
    password = PasswordField(('Password'), validators=[
        validators.Required('Password is required'),
    ])
    remember_me = BooleanField('Remember me')

    submit = SubmitField('Sign in')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def validate(self):
        user_manager =  app.user_manager

        # Validate field-validators
        if not super(LoginForm, self).validate():
            return False

        # Find user by username and/or email
        user = None
        user_email = None

        user, user_email = user_manager.find_user_by_email(self.email.data)

        # Handle successful authentication
        if user:
            if user.verify_password(self.password.data):
                return True                         # Successful authentication

        # Handle unsuccessful authentication
        self.email.errors.append('Incorrect Email and Password')
        self.password.errors.append('')
        return False             
