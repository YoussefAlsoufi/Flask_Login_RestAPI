from flask import Blueprint, redirect, url_for, request, flash
from flask import render_template
from flask_login import login_required, current_user, confirm_login, fresh_login_required
from . import db, bcrypt

from flask_app.helper.update_roles_form import UpdateUserRoleForm
from flask_app.helper.update_roles_helper import get_updates, flash_updates, apply_updates
from flask_app.models import User
views = Blueprint('views', __name__)





@views.route('/users_list', methods=['GET', 'POST'])
@login_required
def users_list():
    users = User.query.all()
    form = UpdateUserRoleForm()

    if request.method == 'POST':
        if current_user.id == 10:
            roles = request.form
            print("roles form : ",roles)
            updates = get_updates(users, roles)
            apply_updates(updates)
            flash_updates(updates)
            return redirect(url_for('views.users_list'))
        else :
            flash("Access to update roles only for super admins", "info")
    return render_template('users_list.html', users=users, form=form)