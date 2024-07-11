from flask import Blueprint, redirect, url_for, request, flash
from flask import render_template
from flask_login import login_required, current_user, confirm_login
from flask_app import db
import logging

from flask_app.helper.update_roles_form import UpdateUserRoleForm
from flask_app.helper.update_roles_helper import get_updates, flash_updates, apply_updates
from flask_app.models import User
update_role = Blueprint('update_role', __name__)
user_list_url = 'update_role.users_list'

@update_role.route('/users_list', methods=['GET'])
@login_required
def users_list():
    if current_user.role == "admin" or current_user.role == "super-admin":
        users = User.query.all()
        form = UpdateUserRoleForm()  # Instantiate the form
        return render_template('users_list.html', users=users, form=form)
    
    flash("Access to user list is restricted to admins only", "info")
    return redirect(url_for('home_bp.home'))

@update_role.route('/users_list/update', methods=['POST'])
@login_required
def update_user_role():
    if current_user.role != "super-admin":
        flash("Access to update roles only for super admins", "info")
        logging.debug("User is not super-admin, redirected with flash message")
        return redirect(url_for(user_list_url))

    form = UpdateUserRoleForm()  # Instantiate the form with POST data
    if form.validate_on_submit():
        roles = request.form  # Adjust this to retrieve form data as needed
        users = User.query.all()
        updates = get_updates(users, roles)
        logging.debug(f"Updates: {updates}")
        apply_updates(updates)
        flash_updates(updates)
        logging.debug("Updates applied, redirecting with flash message")
        return redirect(url_for(user_list_url))
    
    # If form validation fails, or if it's a GET request, render the users list again
    logging.debug("Form validation failed or GET request, re-rendering users list")
    users = User.query.all()
    return render_template('users_list.html', users=users, form=form)

@update_role.route('/users_list/delete', methods=['POST'])
@login_required
def delete_user():
    if current_user.id == 5:  # Only allow super admin to delete users
        user_id = int(request.form.get('user_id'))
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash(f"User {user.user_name} deleted successfully.", 'success')
    else:
        flash("Access to delete users only for super admins.", 'info')

    return redirect(url_for('update_role.users_list'))