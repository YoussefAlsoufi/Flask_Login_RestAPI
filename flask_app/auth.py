from flask import Blueprint, render_template, redirect, url_for, flash
from flask_app.models import User
from flask_app import db, bcrypt
from flask_app.helper.sign_up_helper import SignUpForm # type: ignore
from flask_app.helper.login_helper import LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print ("Login Process started !")
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        print ("The Login user is : ",user)
        print ("The hashed Pass: ", user.password)
        if user:
            if (bcrypt.check_password_hash(user.password, form.password.data)):
                flash('Login successful!', 'success')
                return redirect(url_for('views.home'))
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
def logout():
    return "<h2>Logout<h1>"

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
            flash('Your account has been created successfully!', 'success')
            print("new user is created.")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            print (f"Failed to create a user because : {e}")
 
    return render_template('sign_up.html', form=form)
