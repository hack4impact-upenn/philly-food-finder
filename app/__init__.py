from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models

