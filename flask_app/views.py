from flask import Blueprint, redirect, url_for, request, flash
from flask import render_template
from flask_login import login_required, current_user, confirm_login, fresh_login_required
from . import db, bcrypt
from flask_app.helper.edit_personal_info_helper import EditPersonalInfo
from flask_app.helper.update_user_role_helper import UpdateUserRoleForm
from flask_app.models import User
views = Blueprint('views', __name__)



@views.route('/')
@login_required
def home():
    print ("The current user is authenticated : ",current_user.is_authenticated)
    print (current_user)
    return render_template('home.html')

@views.route('/edit_personal_info', methods=['POST', 'GET'])
@fresh_login_required
@login_required
def edit_personal_info():
    form = EditPersonalInfo()
    print("The Updated process strarted !")
    if form.validate_on_submit():
            # Process the form data
            current_user.email = form.email.data if form.email.data is not None else current_user.email
            current_user.user_name = form.user_name.data if form.user_name.data is not None else current_user.user_name
            current_user.phone = form.phone.data if form.phone.data is not None else current_user.phone
            current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') if form.password.data else current_user.password
            # but in signForm password is required 
            try :  
                db.session.commit()
                flash('Your information has been updated!', 'success')
                return redirect(url_for('views.edit_personal_info'))
            except Exception as e:
                db.session.rollback()
                flash('Failed to save changes.', 'error')
                print(f"Failed Updating because : {e}")
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.user_name.data = current_user.user_name
        form.phone.data = current_user.phone
    else :
        print ("something bad is happenning !") 
    return render_template('edit_personal_info.html',  form=form)

def get_updates(users, roles):
    updates = []
    for user in users:
        user_id = str(user.id)
        role_key = f'roles[{user_id}]'
        if role_key in roles:
            new_role = roles[role_key]
            if new_role != user.role:
                updates.append((user, new_role))
    return updates
def apply_updates(updates):
    for user, new_role in updates:
        user.role = new_role
    db.session.commit()

def flash_updates(updates):
    if updates:
        for user, new_role in updates:
            flash(f' You updated Role of User ID {user.id} to {new_role}', 'success')
        flash('Roles updated successfully.', 'success')
    else:
        flash('No roles were updated.', 'info')

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