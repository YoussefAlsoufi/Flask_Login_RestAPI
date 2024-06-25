from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_app.models import User
from flask_app import db, bcrypt, login_manager
from flask_app.helper.sign_up_helper import SignUpForm # type: ignore
from flask_app.helper.login_helper import LoginForm
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

#retrieves the user instance from db regarding to his Id.
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = LoginForm()
    print ("Login Process started !")
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        print ("The Login user is : ",user)
        print ("The hashed Pass: ", user.password)
        if user:
            if (bcrypt.check_password_hash(user.password, form.password.data)):
                login_user(user, remember=True)
                flash('Login successful!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('views.home'))
            else:
                flash('Login unsuccessful. Please check email and password.', 'danger')
        else:
            flash('Please Sign up first', 'danger')
            return redirect(url_for('sign_up.html'))
    else:
        print ("Login isn't Valid ")   
        print ("Erorors IS:  ", form.errors)    
    return render_template('login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        new_user = User(user_name = form.user_name.data, 
                        email = form.email.data,
                        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
                        phone  =form.phone.data,
                        role = "user")
        print ("The neeeeew User is : ", new_user)
        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Your account has been created successfully!', 'success')
            print("new user is created.")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            print (f"Failed to create a user because : {e}")
 
    return render_template('sign_up.html', form=form)
