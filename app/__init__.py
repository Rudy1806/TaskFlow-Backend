from flask import Flask
from flask_cors import CORS

from app.config import Config

from app.extensions import (
    db,
    migrate,
    ma,
    jwt,
    socketio
)

from app.routes.health import health_bp
from app.routes.auth import auth_bp
from app.routes.task import task_bp
from app.routes.dashboard import dashboard_bp
from app.routes.notification import notification_bp
from app.routes.user import user_bp

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)
    print("FRONTEND_URL =", app.config["FRONTEND_URL"])
    CORS(
    app,
    resources={r"/*": {"origins": "*"}}
)

    db.init_app(app)

    migrate.init_app(
        app,
        db
    )

    ma.init_app(app)

    jwt.init_app(app)
    from flask import jsonify

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print("INVALID TOKEN:", error)
        return jsonify({"msg": error}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        print("MISSING TOKEN:", error)
        return jsonify({"msg": error}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        print("TOKEN EXPIRED")
        return jsonify({"msg": "Token expired"}), 401

    socketio.init_app(
        app,
        cors_allowed_origins="*"
    )
    
    from app.models import (
    User,
    Task,
    Comment,
    Notification,
    ActivityLog
    )
    app.register_blueprint(
        health_bp,
        url_prefix="/api"
    )

    app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth"
    )

    app.register_blueprint(
    task_bp,
    url_prefix="/api/tasks"
    )

    app.register_blueprint(
    dashboard_bp,
    url_prefix="/api/dashboard"
    )

    app.register_blueprint(
        notification_bp,
        url_prefix="/api/notifications"
    )
    app.register_blueprint(
    user_bp,
    url_prefix="/api/users"
    )

    return app