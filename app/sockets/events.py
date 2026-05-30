from flask_socketio import emit, join_room, leave_room

from app.extensions import socketio


@socketio.on("join_room")
def handle_join(data):
    room = data.get("room")

    join_room(room)

    emit(
        "joined",
        {
            "room": room
        },
        room=room
    )


@socketio.on("leave_room")
def handle_leave(data):
    room = data.get("room")

    leave_room(room)

    emit(
        "left",
        {
            "room": room
        },
        room=room
    )