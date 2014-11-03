from app import app, db
from models import Address
from flask import render_template

@app.route('/')
def index():
    return "Hello World!"

@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('login.html')