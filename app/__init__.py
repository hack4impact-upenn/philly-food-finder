from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
from celery import Celery
from flask.ext.cache import Cache
from flask.ext.compress import Compress
import os
from flask_mail import Mail
from flask_user import SQLAlchemyAdapter, UserManager
from raygun4py.middleware import flask as flask_raygun

basedir = os.path.abspath(os.path.dirname(__file__))


# Use a Class-based config to config flask and extensions
class ConfigClass(object):
    # Flask settings
    SECRET_KEY =              os.getenv('SECRET_KEY',       'not so secret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',     
        'sqlite:///' + os.path.join(basedir, 'app.db'))

    CSRF_ENABLED = True

    # Flask-Mail settings
    MAIL_USERNAME =           os.getenv('MAIL_USERNAME',        
        'phillyhungercoalition@gmail.com')
    MAIL_PASSWORD =           os.getenv('MAIL_PASSWORD',        
        'not so secret')
    DEFAULT_MAIL_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',
        '"Philly Food Finder" <phillyhungercoalition@gmail.com>')
    MAIL_DEFAULT_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',
        '"Philly Food Finder" <phillyhungercoalition@gmail.com>')
    MAIL_SERVER =             os.getenv('MAIL_SERVER',          
        'smtp.gmail.com')
    MAIL_PORT =           int(os.getenv('MAIL_PORT',            '465'))
    MAIL_USE_SSL =        int(os.getenv('MAIL_USE_SSL',         True))

    # Flask-User settings
    USER_ENABLE_EMAIL              = True
    USER_REQUIRE_INVITATION        = True
    USER_ENABLE_USERNAME           = False
    USER_ENABLE_CHANGE_USERNAME    = False
    USER_ENABLE_FORGOT_PASSWORD    = True
    USER_ENABLE_CHANGE_PASSWORD    = True
    USER_APP_NAME        = 'Philly Food Finder'                
    USER_PASSWORD_HASH		= 'sha512_crypt'
    USER_PASSWORD_HASH_MODE          = 'passlib'
    USER_CONFIRM_EMAIL_EXPIRATION    = 9223372036854775807
    USER_RESET_PASSWORD_EXPIRATION   = 9223372036854775807

    USER_AUTO_LOGIN_AFTER_REGISTER = False
    USER_AUTO_LOGIN_AFTER_CONFIRM = True

    USER_CHANGE_PASSWORD_URL      = '/admin/change-password'
    USER_CHANGE_USERNAME_URL      = '/admin/change-username'
    USER_CONFIRM_EMAIL_URL        = '/admin/confirm-email/<token>'
    USER_EMAIL_ACTION_URL         = '/admin/email/<id>/<action>'     
    USER_FORGOT_PASSWORD_URL      = '/admin/forgot-password'
    USER_LOGIN_URL                = '/admin/login'
    USER_LOGOUT_URL               = '/admin/logout'
    USER_MANAGE_EMAILS_URL        = '/admin/manage-emails'
    USER_REGISTER_URL             = '/admin/invite'
    USER_RESEND_CONFIRM_EMAIL_URL = '/admin/resend-confirm-email'    
    USER_RESET_PASSWORD_URL       = '/admin/reset-password/<token>'

    USER_AFTER_REGISTER_ENDPOINT = 'invite_sent'
    USER_AFTER_CONFIRM_ENDPOINT = 'user.change_password'

    # Flask-WTF settings
    RECAPTCHA_PUBLIC_KEY = '6LcmKQcTAAAAAC8Gy-On5cNSfIvLu6TNCEMXBErq'
    RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY',  'not so secret')

    # Celery
    CELERY_BROKER_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL') or 'redis://localhost:6379'
    CELERY_REDIS_MAX_CONNECTIONS = 5

    # Cache
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379'

    # Raygun
    RAYGUN_APIKEY = os.environ.get('RAYGUN_APIKEY') or 'debug'
    GEOCODE_APIKEY = os.environ.get('GEOCODE_APIKEY')

app = Flask(__name__)
app.config.from_object(__name__+'.ConfigClass')

Compress(app)           # Initialize Flask-Compress
db = SQLAlchemy(app) 	# Initialize Flask-SQLAlchemy
mail = Mail(app)		# Initialize Flask-Mail

if not app.debug:
    flask_raygun.Provider(app, app.config['RAYGUN_APIKEY']).attach()

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

cache = Cache(
    app,
    config={
        'CACHE_TYPE': app.config['CACHE_TYPE'],
        'CACHE_REDIS_URL': app.config['CACHE_REDIS_URL'],
    }
)

from app import views, models, forms, tasks
from forms import InviteForm
from app.models import User
from app.views import *

db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
user_manager = UserManager(                     # Initialize Flask-User
    db_adapter,
    app,
    register_form=InviteForm,
    register_view_function=invite
)