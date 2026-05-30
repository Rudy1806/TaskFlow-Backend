from flask import Blueprint, jsonify, request

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.extensions import db
from app.models.user import User

user_bp = Blueprint(
    "users",
    __name__
)


@user_bp.route("", methods=["GET"])
@jwt_required()
def get_users():

    users = User.query.all()

    return jsonify({
        "success": True,
        "data": [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
            for user in users
        ]
    })


@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    return jsonify({
        "success": True,
        "data": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at
        }
    })


@user_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    data = request.get_json()

    user.name = data.get(
        "name",
        user.name
    )

    user.email = data.get(
        "email",
        user.email
    )

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Profile updated"
    })