from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
import os
from config import basedir
from flask_mail import Mail

# Use a Class-based config
class ConfigClass(object):
    # Flask settings
    SECRET_KEY =              os.getenv('SECRET_KEY',       'development key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',     'sqlite:///basic_app.sqlite')
    CSRF_ENABLED = True

    # Flask-Mail settings
    MAIL_USERNAME =           os.getenv('MAIL_USERNAME',        'email@example.com')
    MAIL_PASSWORD =           os.getenv('MAIL_PASSWORD',        'password')
    MAIL_DEFAULT_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',  '"MyApp" <noreply@example.com>')
    MAIL_SERVER =             os.getenv('MAIL_SERVER',          'smtp.gmail.com')
    MAIL_PORT =           int(os.getenv('MAIL_PORT',            '465'))
    MAIL_USE_SSL =        int(os.getenv('MAIL_USE_SSL',         True))

    # Flask-User settings
    USER_ENABLE_EMAIL              = True
    USER_ENABLE_LOGIN_WITHOUT_CONFIRM           = True
    USER_REQUIRE_INVITATION        = True
    USER_ENABLE_USERNAME           = False
    USER_ENABLE_CHANGE_USERNAME    = False
    USER_ENABLE_FORGOT_PASSWORD    = True
    USER_ENABLE_CHANGE_PASSWORD    = True
    USER_APP_NAME        = 'AppName'                # Used by email templates
    USER_PASSWORD_HASH		= 'sha512_crypt'
    USER_PASSWORD_HASH_MODE          = 'passlib'

app = Flask(__name__)
app.config.from_object(__name__+'.ConfigClass')
app.config.from_object('config')

db = SQLAlchemy(app) 	# Initialize Flask-SQLAlchemy
mail = Mail(app)		# Initialize Flask-Mail

from app import views, models, forms
from app.models import User
from flask_user import SQLAlchemyAdapter, UserManager

db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
user_manager = UserManager(db_adapter, app)     # Initialize Flask-User
