from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO

db = SQLAlchemy()

migrate = Migrate()

ma = Marshmallow()

jwt = JWTManager()

socketio = SocketIO(
    cors_allowed_origins="*",
    async_mode="eventlet"
)