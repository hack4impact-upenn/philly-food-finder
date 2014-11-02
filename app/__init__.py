from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.scss import Scss
from flask.ext.bcrypt import Bcrypt
import os
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
Scss(app)
bcrypt = Bcrypt(app)

from app import views, models, forms
from app.models import User
from flask_user import SQLAlchemyAdapter, UserManager

db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
user_manager = UserManager(db_adapter, app)     # Initialize Flask-User
