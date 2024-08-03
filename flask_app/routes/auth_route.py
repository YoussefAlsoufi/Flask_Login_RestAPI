from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_app.models import User
from flask_app import db, bcrypt, login_manager, gmail_client
from flask_app.helper.sign_up_helper import SignUpForm # type: ignore
from flask_app.helper.login_helper import LoginForm
from flask_login import login_user, login_required, logout_user, current_user
from flask_app.config_gmail import email_config

auth = Blueprint('auth', __name__)
login_endpoint = 'auth.login'
#retrieves the user instance from db regarding to his Id.
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print("Login Process started!")
    
    if form.validate_on_submit():
        user = get_user_by_email(form.email.data)
        print("The Login user is:", user)
        
        if user:
            if not handle_user_verification(user):
                return redirect(url_for(login_endpoint))
            
            if handle_user_authentication(user, form.password.data):
                return redirect_after_login()
            else:
                flash('Login unsuccessful. Please check email and password.', 'danger')
        else:
            flash('Please Sign up first', 'danger')
            return redirect(url_for('auth.signup'))
    else:
        print("Login isn't Valid")
        print("Errors are:", form.errors)
    
    return render_template('login.html', form=form)

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def handle_user_verification(user):
    if not user.is_verified:
        flash('Please verify your email address before logging in.', 'danger')
        return False
    return True

def handle_user_authentication(user, password):
    if bcrypt.check_password_hash(user.password, password):
        login_user(user, remember=True)
        flash('Login successful!', 'success')
        return True
    return False

def redirect_after_login():
    next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('home_bp.home'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for(login_endpoint))

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        verification_token = gmail_client.generate_verification_token(form.email.data.lower())
        new_user = User(user_name = form.user_name.data, 
                        email = form.email.data.lower(),
                        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
                        phone  =form.phone.data,
                        role = "user",
                        verification_token = verification_token)
        print ("The neeeeew User is : ", new_user)

        try:
            db.session.add(new_user)
            db.session.commit()
            service = email_config()
            if service:
                verification_link = url_for('email_token.verify_email', token=verification_token, _external=True)
                message = gmail_client.create_verification_email(form.email.data.lower(), verification_link)
                gmail_client.send_message(service, "me", message)
                flash('Your account has been created successfully!, Please verify your account.', 'success')
                print("new user is created.")
            #login_user(new_user, remember=True)
            
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to create a user because : {e}', 'danger')
            print (f"Failed to create a user because : {e}")
    else:
        print("From th Form, the errors : ", form.errors)
    return render_template('sign_up.html', form=form)
