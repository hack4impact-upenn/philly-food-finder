from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField
from wtforms.validators import Required, Length
from app.models import User

class RequestNewFoodResourceForm(Form):
    # Information about the person submitting the food resource for evaluation. 
    first_name = TextField(
        label = 'First Name', 
        validators = [
            InputRequired("Please provide your first name.")
            Length(0, 35)
        ])
    last_name = TextField(
        label = 'Last Name', 
        validators = [
            InputRequired("Please provide your last name.")
            Length(0, 35)
        ])
    email_address = TextFile(
        label = 'Email Address', 
        validators = [
            InputRequired("Please provide an email address at which we can contact you."), 
            Email("Invalid email address.")
            Length(0, 35)
        ])
    phone_number = TextFile(
        label = 'Phone Number', 
        validators = [
            InputRequired("Please provide a phone number at which we can contact you.")
        ])

    # Information about the food resource itself. 
    food_resource_website = TextFile('Website', 
        validators = [
            URL(True, "Invalid website URL.")])
    food_resource_name = TextField('Food Resource Name')
    food_resource_type = TextField
    address_line1
    address_line2
    address_city
    address_state
    address_zip_code
    additional_information = TextAreaField

class AddNewFoodResourceForm(Form):



class LoginForm(Form):
  openid = TextField('openid', validators = [Required()])
  remember_me = BooleanField('remember_me', default = False)

class EditForm(Form):
    nickname = TextField('nickname', validators = [Required()])
    about_me = TextAreaField('about_me', validators = [Length(min = 0, max = 140)])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname = self.nickname.data).first()
        if user != None:
            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
            return False
        return True

class PostForm(Form):
    post = TextField('post', validators = [Required()])
