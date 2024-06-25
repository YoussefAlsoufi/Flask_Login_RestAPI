from flask import Blueprint, redirect, url_for
from flask import render_template
from flask_login import login_required, current_user
views = Blueprint('views', __name__)


@login_required
@views.route('/')

def home():
    if current_user.is_authenticated:
        return render_template('home.html')
    else:
        return redirect(url_for('auth.login'))