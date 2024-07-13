from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_app.helper.chat_room_form import ChatRoomform, LiveChatRoom
from flask_app.helper.chat_room_helper import generate_unique_code, rooms
from flask_login import current_user, login_required

chat_room = Blueprint('chat_room', __name__)
chat_room_template = 'chat_room_home.html'
chat_room_live = 'chat_room_live.html'

@chat_room.route('/chat_room', methods=['POST','GET'])
@login_required
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
                flash("The Room you want to join doesn't exist, please check the room code.", "danger")
                return render_template(chat_room_template, form=form)
            
            return redirect(url_for('chat_room.get_live_chat'))

        elif create:

            room_code = generate_unique_code()
            rooms[room_code] = {"members":0, "messages":[]}

            return redirect(url_for('chat_room.get_live_chat', code = room_code))
    

    return render_template(chat_room_template, form=form)


@chat_room.route('/live_chat',methods = ['POST','GET'])
@login_required
def get_live_chat():
    form = LiveChatRoom()
    if not current_user.is_authenticated:
        return redirect (url_for('auth.login'))
    if current_user.role not in ("admin", "super-admin"): 
        return redirect(url_for('home_bp.home'))

    room_code = request.args.get('code')
    return render_template(chat_room_live, form=form, room_code = room_code)
    
