from app import app, db
from models import Address
<<<<<<< HEAD
from flask import render_template
=======
from forms import RequestNewFoodResourceForm
from flask import render_template, flash, redirect, session, url_for, request, g
>>>>>>> 4ec4491d79ed9c83c4e5014489c1966a55054fd6

@app.route('/')
def index():
    return "Hello World!"

<<<<<<< HEAD
@app.route('/map')
def map():
    return render_template('staticmap.html')

=======
@app.route('/new_food_resource', methods=['GET', 'POST'])
def register():
    form = RequestNewFoodResourceForm(request.form)
    if request.method == 'POST' and form.validate():
        # user = User(form.username.data, form.email.data,
        #             form.password.data)
        # db_session.add(user)
        # flash('Thanks for registering')
        # return redirect(url_for('login'))
        return "Hello World!"
    return render_template('add_resource.html', form=form)
>>>>>>> 4ec4491d79ed9c83c4e5014489c1966a55054fd6
