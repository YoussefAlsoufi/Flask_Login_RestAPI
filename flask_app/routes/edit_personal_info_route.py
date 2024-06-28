from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, fresh_login_required, current_user
from flask_app import db, bcrypt
from flask_app.helper.edit_personal_info_helper import EditPersonalInfo

edit_personal_info_bp = Blueprint('edit_personal_info_bp', __name__)

@edit_personal_info_bp.route('/edit_personal_info', methods=['POST', 'GET'])
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
                return redirect(url_for('edit_personal_info_bp.edit_personal_info'))
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
