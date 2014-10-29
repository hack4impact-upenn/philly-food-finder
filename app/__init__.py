from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models
from app.models import User
from flask_user import SQLAlchemyAdapter, UserManager

db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
user_manager = UserManager(db_adapter, app)     # Initialize Flask-User