from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, validators
from wtforms.validators import InputRequired, Length, URL, Email

class RequestNewFoodResourceForm(Form):
    # Information about the person submitting the food resource for evaluation. 
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

    # Information about the food resource itself. 
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
        label = 'State', 
        validators = [
            InputRequired("Please provide the food resource's zip code."),
            Length(1, 5) # Same max length as in Address model.
        ])
    additional_information = TextAreaField(
        label = 'Any additional information?', 
        validators = [
            InputRequired("Please provide the food resource's zip code."),
            Length(1, 5) # Same max length as in Address model.
        ])

#class AddNewFoodResourceForm(Form):



# class LoginForm(Form):
#   openid = TextField('openid', validators = [Required()])
#   remember_me = BooleanField('remember_me', default = False)

# class EditForm(Form):
#     nickname = TextField('nickname', validators = [Required()])
#     about_me = TextAreaField('about_me', validators = [Length(min = 0, max = 140)])

#     def __init__(self, original_nickname, *args, **kwargs):
#         Form.__init__(self, *args, **kwargs)
#         self.original_nickname = original_nickname

#     def validate(self):
#         if not Form.validate(self):
#             return False
#         if self.nickname.data == self.original_nickname:
#             return True
#         user = User.query.filter_by(nickname = self.nickname.data).first()
#         if user != None:
#             self.nickname.errors.append('This nickname is already in use. Please choose another one.')
#             return False
#         return True

# class PostForm(Form):
#     post = TextField('post', validators = [Required()])
