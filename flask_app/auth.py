from flask import Blueprint, render_template, request
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
        print("Success")
    return render_template('sign_up.html', form=form)
