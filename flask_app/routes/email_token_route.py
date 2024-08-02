from flask import Blueprint, flash, redirect, url_for
from flask_app.gmail_client import confirm_verification_token
from flask_app.models import User
from flask_app import db

email_token = Blueprint('verify_email', __name__)

@email_token.route('/verify/<token>')
def verify_email(token):
    try:
        email = confirm_verification_token(token)
    except:
        flash('The verification link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.signup'))
    
    user = User.query.filter_by(email=email).first_or_404()
    if user.is_verified:
        flash('Account already verified. Please login.', 'success')
    else:
        user.is_verified = True
        user.verification_token = None
        db.session.commit()
        flash('Your account has been verified! You can now login.', 'success')
    return redirect(url_for('auth.login'))