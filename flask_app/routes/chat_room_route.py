from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_app.helper.chat_room_form import ChatRoomform, LiveChatRoom
from flask_app.helper.chat_room_helper import generate_unique_code, rooms
from flask_login import current_user, login_required
from flask_app import socketio
from flask_socketio import join_room, leave_room, send

chat_room = Blueprint('chat_room', __name__)
chat_room_template = 'chat_room_home.html'
chat_room_live = 'chat_room.get_live_chat'

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
            
            return redirect(url_for(chat_room_live, code= code))

        elif create:

            room_code = generate_unique_code()
            rooms[room_code] = {"members":0, "messages":[]}

            generated_url = url_for(chat_room_live, code=room_code, _external=True)
            print("Generated URL:", generated_url)

            return redirect(url_for(chat_room_live, code = room_code))
    

    return render_template('chat_room_home.html', form=form)


@chat_room.route('/live_chat',methods = ['POST','GET'])
@login_required
def get_live_chat():
    form = LiveChatRoom()
    room_code = request.args.get('code')
    if not current_user.is_authenticated:
        return redirect (url_for('auth.login'))
    
    if current_user.role not in ("admin", "super-admin"): 
        return redirect(url_for('home_bp.home'))
    
    print (f"from live chat , the code is :{room_code}")
    print (f"from live chat, the rooms are {rooms}")
    if not room_code or room_code not in rooms:
        flash("Invalid or missing room code.", 'danger')
        return redirect(url_for('chat_room.get_chat_room'))
 
    return render_template('chat_room_live.html', form=form, room_code = room_code)


@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join')
def on_join(data):
    room = data.get('room')
    print(f"Socket.IO - Join request: Room code is {room}")
    print(f"Current rooms: {rooms}")
    if not room or room not in rooms:
        print(f'Invalid or missing room code: {room}')
        return  # Handle invalid or missing room code gracefully
    join_room(room)
    send(f'{current_user.user_name} has entered the room.', to=room)
    print(f'{current_user.user_name} joined room: {room}')

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    send(f'{current_user.user_name} has left the room.', to=room)
    print(f'{current_user.user_name} left room: {room}')
    
@socketio.on('send_message')
def handle_send_message(data):
    room = data['room']
    message = data['text']
    user = current_user.user_name
    rooms[room]['messages'].append({'user': user, 'text': message})
    send({'user': user, 'text': message}, to=room)
    print(f'Message from {user}: {message} in room: {room}')