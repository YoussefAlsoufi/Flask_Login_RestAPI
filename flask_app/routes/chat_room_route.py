from mailbox import Message
from flask import Blueprint, jsonify, render_template, request, flash, url_for, redirect
from flask_app.helper.chat_room_form import ChatRoomform, LiveChatRoom
from flask_app.helper.chat_room_helper import generate_unique_code, rooms
from flask_login import current_user, login_required
from flask_app import socketio
from flask_socketio import join_room, leave_room, send

chat_room = Blueprint('chat_room', __name__)
chat_room_template = 'chat_room_home.html'
chat_room_live = 'chat_room.get_live_chat'
user_info = {}

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
    
    if room_code not in rooms:
        # Emit an event to handle leaving the room
        socketio.emit('leave', {'room': room_code})
        redirect(url_for("chat_room.get_chat_room"))
    
    print (f"from live chat , the code is :{room_code}")
    print (f"from live chat, the rooms are {rooms}")
    if not room_code or room_code not in rooms:
        flash("Invalid or missing room code.", 'danger')
        return redirect(url_for('chat_room.get_chat_room'))
 
    return render_template('chat_room_live.html', form=form, room_code = room_code, current_user= current_user)

# Adjust how messages are fetched and sent to the client
@chat_room.route('/get_messages', methods=['GET'])
def get_messages():
    room_code = request.args.get('room_code')
    # Example: Fetch messages for the room from the database
    messages = Message.query.filter_by(room=room_code).order_by(Message.timestamp.desc()).limit(50).all()
    return jsonify([msg.serialize() for msg in messages])    

@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('join')
def on_join(data):

    room = data.get('room')
    print(f"Socket.IO - Join request: Room code is {room}")
    print(f"Current rooms: {rooms}")
    if not room or room not in rooms:
        print(f'Invalid or missing room code: {room}')
        return  # Handle invalid or missing room code gracefully
    join_room(room)
    rooms[room]["members"] += 1
    user = current_user.user_name
    user_info[request.sid] = {"user":user, "room":room}
    send({'user': user, 'text': "has entered the room."}, to=room)
    print(f'{current_user.user_name} joined room: {room}')
    print(f"User_info : {user_info}")


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    sid = request.sid
    user_sid = user_info.pop(sid, None)
    if user_sid:
        room = user_sid['room']
        user = user_sid['user']
        leave_room(room)
        print (f"the rooms after discnnect are : {rooms}")
        send({'user': user, 'text': "has left the room"}, to=room)
        print(f'{user} left room: {room}')

'''
        if room in rooms :
            rooms[room]["members"] -= 1
            if rooms[room]['members'] == 0:
                del rooms[room]'''

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    user = current_user.user_name
    message= "has lift the room."
    send({'user': user, 'text': message}, to=room)
    print(f'{current_user.user_name} left room: {room}')
    
@socketio.on('send_message')
def handle_send_message(data):
    room = data['room']
    message = data['text']
    user = current_user.user_name
    rooms[room]['messages'].append({'user': user, 'text': message})
    send({'user': user, 'text': message}, to=room)
    print(f'Message from {user}: {message} in room: {room}')


