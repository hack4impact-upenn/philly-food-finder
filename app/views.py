from app import app, db
from models import Address, FoodResource, TimeSlot, User
from forms import RequestNewFoodResourceForm
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask_user import login_required
from flask_user.views import _endpoint_url
from flask_login import current_user, login_user, logout_user

@app.route('/')
def index():
    return "Hello World!"

@app.route('/new_food_resource', methods = ['GET', 'POST'])
def add_resource():
    form = RequestNewFoodResourceForm(request.form)
    days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", 
        "Friday", "Saturday"]
    if request.method == 'POST' and form.validate():
        return "Hello World!"
    return render_template('add_resource.html', form=form)

@app.route('/admin')
@login_required
def admin():
    resources = FoodResource.query.all()
    resources_info = [
        ["farmers-markets", "Farmers' Markets"], 
        ["food-cupboards", "Food Cupboards"], 
        ["meals-on-wheels", "Meals On Wheels"], 
        ["share-host-sites", "SHARE Host Sites"], 
        ["soup-kitchens", "Soup Kitchens"],
        ["wic-offices", "WIC Offices"]]
    return render_template('admin.html', resources=resources, 
        resources_info=resources_info)

@login_required
def invite():
    """ Display registration form and create new User."""
    user_manager =  app.user_manager
    db_adapter = user_manager.db_adapter

    next = request.args.get('next', _endpoint_url(user_manager.after_login_endpoint))
    reg_next = request.args.get('reg_next', _endpoint_url(user_manager.after_register_endpoint))

    # Initialize form
    login_form = user_manager.login_form()                      # for login_or_register.html
    register_form = user_manager.register_form(request.form)    # for register.html
    if request.method!='POST':
        login_form.next.data     = register_form.next.data     = next
        login_form.reg_next.data = register_form.reg_next.data = reg_next

    # Process valid POST
    if request.method=='POST' and register_form.validate():

        # Create a User object using Form fields that have a corresponding User field
        User = db_adapter.UserClass
        user_class_fields = User.__dict__
        user_fields = {}

        # Create a UserEmail object using Form fields that have a corresponding UserEmail field
        if db_adapter.UserEmailClass:
            UserEmail = db_adapter.UserEmailClass
            user_email_class_fields = UserEmail.__dict__
            user_email_fields = {}

        # Create a UserAuth object using Form fields that have a corresponding UserAuth field
        if db_adapter.UserAuthClass:
            UserAuth = db_adapter.UserAuthClass
            user_auth_class_fields = UserAuth.__dict__
            user_auth_fields = {}

        # Enable user account
        if db_adapter.UserProfileClass:
            if hasattr(db_adapter.UserProfileClass, 'active'):
                user_auth_fields['active'] = True
            elif hasattr(db_adapter.UserProfileClass, 'is_enabled'):
                user_auth_fields['is_enabled'] = True
            else:
                user_auth_fields['is_active'] = True
        else:
            if hasattr(db_adapter.UserClass, 'active'):
                user_fields['active'] = True
            elif hasattr(db_adapter.UserClass, 'is_enabled'):
                user_fields['is_enabled'] = True
            else:
                user_fields['is_active'] = True

        # For all form fields
        for field_name, field_value in register_form.data.items():
            # Hash password field
            if field_name=='password':
                hashed_password = user_manager.hash_password(field_value)
                if db_adapter.UserAuthClass:
                    user_auth_fields['password'] = hashed_password
                else:
                    user_fields['password'] = hashed_password
            # Store corresponding Form fields into the User object and/or UserProfile object
            else:
                if field_name in user_class_fields:
                    user_fields[field_name] = field_value
                if db_adapter.UserEmailClass:
                    if field_name in user_email_class_fields:
                        user_email_fields[field_name] = field_value
                if db_adapter.UserAuthClass:
                    if field_name in user_auth_class_fields:
                        user_auth_fields[field_name] = field_value

        # Creates temporary password
        if db_adapter.UserAuthClass:
                    user_auth_fields['password'] = hashed_password
                else:
                    user_fields['password'] = hashed_password

        # Add User record using named arguments 'user_fields'
        user = db_adapter.add_object(User, **user_fields)
        if db_adapter.UserProfileClass:
            user_profile = user

        # Add UserEmail record using named arguments 'user_email_fields'
        if db_adapter.UserEmailClass:
            user_email = db_adapter.add_object(UserEmail,
                    user=user,
                    is_primary=True,
                    **user_email_fields)
        else:
            user_email = None

        # Add UserAuth record using named arguments 'user_auth_fields'
        if db_adapter.UserAuthClass:
            user_auth = db_adapter.add_object(UserAuth, **user_auth_fields)
            if db_adapter.UserProfileClass:
                user = user_auth
            else:
                user.user_auth = user_auth

        db_adapter.commit()

        # Send 'registered' email and delete new User object if send fails
        if user_manager.send_registered_email:
            try:
                # Send 'registered' email
                _send_registered_email(user, user_email)
            except Exception as e:
                # delete new User object if send  fails
                db_adapter.delete_object(user)
                db_adapter.commit()
                raise e

        # Send user_registered signal
        signals.user_registered.send(app._get_current_object(), user=user)

        # Redirect if USER_ENABLE_CONFIRM_EMAIL is set
        if user_manager.enable_confirm_email:
            next = request.args.get('next', _endpoint_url(user_manager.after_register_endpoint))
            return redirect(next)

        # Auto-login after register or redirect to login page
        next = request.args.get('next', _endpoint_url(user_manager.after_confirm_endpoint))
        if user_manager.auto_login_after_register:
            return _do_login_user(user, reg_next)                     # auto-login
        else:
            return redirect(url_for('user.login')+'?next='+reg_next)  # redirect to login page

    # Process GET or invalid POST
    return render_template(user_manager.register_template,
            form=register_form,
            login_form=login_form,
            register_form=register_form)

@app.route('/_admin')
def get_food_resource_data():
    names = FoodResource.query.all()
    return jsonify(names=[i.serialize_name_only() for i in names])
