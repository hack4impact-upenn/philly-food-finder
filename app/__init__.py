from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.scss import Scss
import os
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
Scss(app)

from app import views, models, forms

