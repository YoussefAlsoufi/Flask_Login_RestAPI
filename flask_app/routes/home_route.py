from flask import Blueprint ,render_template
from flask_login import login_required, current_user

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/')
@login_required
def home():
    print ("The current user is authenticated : ",current_user.is_authenticated)
    print (current_user)
    return render_template('home.html')