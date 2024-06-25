from flask import Blueprint, redirect, url_for
from flask import render_template
from flask_login import login_required, current_user
views = Blueprint('views', __name__)



@views.route('/')
@login_required
def home():
    return render_template('home.html')
