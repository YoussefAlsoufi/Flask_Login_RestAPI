from flask import Blueprint, flash, redirect, url_for
from flask_app.gmail_client import confirm_verification_token
from flask_app.models import User
from flask_app import db
from itsdangerous import BadSignature, SignatureExpired

email_token = Blueprint('email_token', __name__)
signup_route = 'auth.signup'
@email_token.route('/verify/<token>')
def verify_email(token):
        
    email = confirm_verification_token(token)
    if email == 'expired':
        flash('The verification link has expired.', 'danger')
        return redirect(url_for(signup_route))
    elif email == 'invalid':
        flash('The verification link is invalid.', 'danger')
        return redirect(url_for(signup_route))
    elif email == 'error':
        flash('An unexpected error occurred during verification. Please try again later.', 'danger')
        return redirect(url_for(signup_route))
    
    user = User.query.filter_by(email=email).first_or_404()
    if user.is_verified:
        flash('Account already verified. Please login.', 'success')
    else:
        user.is_verified = True
        user.verification_token = None
        db.session.commit()
        flash('Your account has been verified! You can now login.', 'success')
    return redirect(url_for('auth.login'))