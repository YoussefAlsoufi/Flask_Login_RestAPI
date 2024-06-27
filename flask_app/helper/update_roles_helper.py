from flask import flash
from flask_app import db

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

def flash_updates(updates):
    if updates:
        for user, new_role in updates:
            flash(f' You updated Role of User ID {user.id} to {new_role}', 'success')
        flash('Roles updated successfully.', 'success')
    else:
        flash('No roles were updated.', 'info')

def apply_updates(updates):
    for user, new_role in updates:
        user.role = new_role
    db.session.commit()        