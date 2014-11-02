from app import app, db
from models import Address
from flask import render_template

@app.route('/')
def index():
    return "Hello World!"

@app.route('/map')
def map():
    return render_template('staticmap.html')

