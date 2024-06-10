from flask import Blueprint, render_template
from flask_app.models import User
from flask_app import db
from flask_app.helper.sign_up_helper import SignUpForm # type: ignore

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    #input_data = request.form 
    return render_template('login.html')

@auth.route('/logout')
def logout():
    return "<h2>Logout<h1>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        new_user = User(user_name = form.user_name.data, 
                        email = form.email.data,
                        password = form.password.data,
                        phone  =form.password.data,
                        role = "user")
        print ("The neeeeew User is : ", new_user)
        try:
            db.session.add(new_user)
            db.session.commit()
            print("new user is created.")
        except Exception as e:
            db.session.rollback()
            print (f"Failed to create a user because : {e}")
            print("Failed Ya Youssef")

    else: 
       print ("IT is Get Ya Youssef")    
    return render_template('sign_up.html', form=form)
