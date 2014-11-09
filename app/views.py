from app import app, db
from models import Address, User
from forms import RequestNewFoodResourceForm, LoginForm
from flask import render_template, flash, redirect, session, url_for, request, g

@app.route('/')
def index():
    return "Hello World!"

@app.route('/new_food_resource', methods = ['GET', 'POST'])
def add_resource():
    form = RequestNewFoodResourceForm(request.form)
    if request.method == 'POST' and form.validate():
        return "Hello World!"
    return render_template('add_resource.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        u = User.query.filter_by(username = form.username.data).first()
        if(u):
        	if(u.verify_password(candidate = form.password.data)):
        		print 'verified!'
        	else:
        		print 'password is wrong!'
        else:
        	print 'failed to login!'
    return render_template('login.html', form=form)