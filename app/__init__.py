from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
<<<<<<< HEAD
from flask.ext.scss import Scss
=======
from flask.ext.bcrypt import Bcrypt
>>>>>>> e6991dcdbee50a52f91d094d8b0a23a13f450626
import os
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
<<<<<<< HEAD
Scss(app)

from app import views, models, forms
=======
bcrypt = Bcrypt(app)

from app import views, models
from app.models import User
from flask_user import SQLAlchemyAdapter, UserManager
>>>>>>> e6991dcdbee50a52f91d094d8b0a23a13f450626

db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
user_manager = UserManager(db_adapter, app)     # Initialize Flask-User
