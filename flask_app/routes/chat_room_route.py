from flask import Blueprint, render_template, request, flash
from flask_app.helper.chat_room_form import ChatRoomform
from flask_app.helper.chat_room_helper import generate_unique_code, rooms
from flask_login import current_user

chat_room = Blueprint('chat_room', __name__)
chat_room_template = 'chat_room.html'

@chat_room.route('/chat_room', methods=['POST','GET'])
def get_chat_room():
    form = ChatRoomform()
    if form.validate_on_submit:
        join = request.form.get("join", False)
        create = request.form.get("create", False)
        code = form.code.data

        if join:
            print ("the rooms : ",rooms)
            if not code :
                flash ("Enter the room code to join.", 'danger')
                return render_template(chat_room_template, form=form)
            elif code not in rooms:
                flash("The Room you want to join doesn't exist, please check the code.", "danger")
                return render_template(chat_room_template, form=form)
            
            return render_template(chat_room_template, form=form)

        elif create:

            room_code = generate_unique_code()
            rooms[room_code] = {"members":0, "messages":[]}

            return f"Creating room with name: {current_user.user_name}"
        
        session["room"] = room_code
        session["name"] = current_user.user_name
        
    return render_template(chat_room_template)