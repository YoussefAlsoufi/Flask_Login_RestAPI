from flask import Blueprint, redirect, url_for, request, flash
from flask import render_template
from flask_login import login_required, current_user, confirm_login
from flask_app import db

from flask_app.helper.update_roles_form import UpdateUserRoleForm
from flask_app.helper.update_roles_helper import get_updates, flash_updates, apply_updates
from flask_app.models import User
update_role = Blueprint('update_role', __name__)


@update_role.route('/users_list', methods=['GET'])
@login_required
def users_list():
    users = User.query.all()
    form = UpdateUserRoleForm()  # Instantiate the form
    return render_template('users_list.html', users=users, form=form)

@update_role.route('/users_list/update', methods=['POST'])
@login_required
def update_user_role():
    if current_user.id != 4:
        flash("Access to update roles only for super admins", "info")
        return redirect(url_for('update_role_bp.users_list'))

    form = UpdateUserRoleForm()  # Instantiate the form with POST data
    if form.validate_on_submit():
        roles = request.form  # Adjust this to retrieve form data as needed
        users = User.query.all()
        updates = get_updates(users, roles)
        apply_updates(updates)
        flash_updates(updates)

        return redirect(url_for('update_role.users_list'))
    
    # If form validation fails, or if it's a GET request, render the users list again
    users = User.query.all()
    return render_template('users_list.html', users=users, form=form)

@update_role.route('/users_list/delete', methods=['POST'])
@login_required
def delete_user():
    if current_user.id == 4:  # Only allow super admin to delete users
        user_id = int(request.form.get('user_id'))
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash(f"User {user.user_name} deleted successfully.", 'success')
    else:
        flash("Access to delete users only for super admins.", 'info')

    return redirect(url_for('update_role.users_list'))