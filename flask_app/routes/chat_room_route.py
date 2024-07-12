from flask import Blueprint, render_template

chat_room = Blueprint('chat_room', __name__)

@chat_room.route('/chat_room', methods=['POST','GET'])
def get_chat_room():
    return render_template('chat_room.html')